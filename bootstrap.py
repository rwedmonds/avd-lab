#!/usr/bin/env python

"""
CVP ZTP BootStrap Script logic (this script)

1) Immediately clean up and remove any files that could prevent ZTP from
	starting if a failure were to occur.
2) Start dead lock timer. If timer expires script will exit (node reload)
3) Configure EOS
		-Enable eAPI
		-Add temporary CVP user
		-Generate random password for CVP user and store in memory
		-Try to disable Copp
4) Upgrade to default image if we are running an invalid image
5) Upgrade the TerminAttr.swix on the device and enable TerminAttr to connect
to ingest
5) Send CVP user password to CVP server and continue to do so periodically
	file exist, wait for a few seconds (to permit any copy to complete and for
	the outstanding eAPI request to be successful) then copy the file to
	'/mnt/flash/startup-config' and exit the script. This should result in
	the reload of the switch and the startup-config being applied.
7) If any error occurs then exit the script causing the switch to reload and
	for the ZTP process to start over.
CVP Server logic (CVP server expectations)
1) Connect and discover the device
2) Once the switch is running valid version, write the
	switch configuration within a CLI config session, then run 'copy
	session-config flash:cvp-config'. The node will reload.
"""

import logging
import logging.handlers
import os
import random
import string
import subprocess
import time
import thread
import re
import socket
import json
import tempfile
import base64
from distutils.version import LooseVersion
import requests

NO_IP_ADDR_MSG = "Unable to obtain node IP address(s)"

try:
	# squelch annoying warnings
	requests.packages.urllib3.disable_warnings()
except AttributeError:
	pass  # not applicable to older versions of requests

logger = None
def setupLogger():
	global logger
	logger = logging.getLogger("bootstrap")
	logger.setLevel(logging.DEBUG)
	try:
		handler = logging.handlers.SysLogHandler(address='/dev/log')
		logger.addHandler(handler)
	except socket.error:
		print("error setting up logger")
		logger = None

def log(msg):
	""" Print message to terminal and log if logging is up"""
	print(msg)
	if logger:
		logger.critical(msg)

class DeviceStatus(object):
	def __init__(self, statusMsg):
		self.serialNumber = ""
		self.systemMacAddress = ""
		self.modelName = ""
		self.hardwareRevision = ""
		self.version = "4.20.11M"
		self.statusMsg = statusMsg

class CliManager(object):
	FAST_CLI_BINARY = "/usr/bin/FastCli"
	def __init__(self):
		self.fastCliBinary = CliManager.FAST_CLI_BINARY
		self.confidenceCheck()

	def confidenceCheck(self):
		assert os.path.isfile(self.fastCliBinary), "FastCli Binary Not Found"

	def runCommands(self, cmdList):
		cmdOutput = ""
		rc = 0
		errMsg = ""
		try:
			cmds = "\n".join(cmdList)
			cmdOutput = subprocess.check_output(
				"echo -e '" + cmds + "' | " + self.fastCliBinary, shell=True, stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError as e:
			rc = e.returncode
			errMsg = e.output
			log("running commands %s errMsg %s" % (cmds, errMsg))
			return (rc, errMsg)

		if cmdOutput:
			for line in cmdOutput.split('\n'):
				if line.startswith('%'):
					errMsg = cmdOutput
					log("running commands %s errMsg %s" % (cmds, errMsg))
					return(1, errMsg)
		return (0, cmdOutput)

class Status(object):
	NOT_READY = 0
	INIT_FAILED = 1
	SANITY_CHECK_FAILED = 2
	BASE_CONFIG_FAILED = 3
	IMAGE_UPGRADE_FAILED = 4
	IMAGE_UPGRADE_INPROGRESS = 5
	TERMINATTR_UPGRADE_FAILED = 6
	TERMINATTR_UPGRADE_SKIPPED = 7
	TERMINATTR_UPGRADE_SUCCESS = 8
	CONFIG_FAILED = 9
	SUCCESS = 10
	CONFIG_REQUEST_SUCCESS = 11

	statusMsgDict = {
		NOT_READY: "not ready",
		INIT_FAILED:"initialization failed",
		SANITY_CHECK_FAILED:"sanity check failed",
		BASE_CONFIG_FAILED:"setting up base EOS configuration failed",
		IMAGE_UPGRADE_FAILED:"upgrading to cvp default EOS image failed",
		IMAGE_UPGRADE_INPROGRESS:"upgrading to cvp default EOS image",
		TERMINATTR_UPGRADE_SKIPPED:("EOS running newer version of terminAttr than default" +
			      "terminAttr version"),
		TERMINATTR_UPGRADE_FAILED:"failed to upgrade terminattr to default cvp version",
		CONFIG_FAILED:"failed in applying EOS configuration on the box",
		SUCCESS:"bootstrap script completed successfully",
		CONFIG_REQUEST_SUCCESS:"Successfully requested CVP for config",
	}

	def __init__(self):
		self.val = Status.NOT_READY
		self.msg = None

	def setValue(self, v, customMsg=None):
		self.val = v
		self.msg = Status.statusMsgDict.get(self.val)
		if customMsg:
			self.msg += ", %s" % customMsg
		log("status code=%s msg=%s" % (self.val, self.msg))

	def getValue(self):
		return self.val

class ImageUpgrade(object):
	# pylint: disable=too-many-instance-attributes
	# pylint: disable=too-many-arguments
	TERMINATTR_BINARY = "/usr/bin/TerminAttr"
	EPOCH_FILE = '/etc/hwepoch.json'
	FLASH_DIR = '/mnt/flash'
	BOOTFILE_PATH = "/mnt/flash/boot-config"

	def __init__(self, cvpIP, status, proto, cliManager, isOnPrem, nginxCertFile,
		caPath, keyPath, certsPath, sanIpsProvided, dnsName):
		self.status = status
		self.cliManager = cliManager
		self.flashDir = ImageUpgrade.FLASH_DIR
		self.bootfilePath = ImageUpgrade.BOOTFILE_PATH
		self.epochFile = ImageUpgrade.EPOCH_FILE
		self.terminAttrBinary = ImageUpgrade.TERMINATTR_BINARY
		self.instEpoch = "2"
		self.imageSz = self.toMB("931.9 MB")
		self.imageName = "EOS-4.25.4M.swi"
		self.isOnPrem = isOnPrem
		self.nginxCertFile = nginxCertFile
		self.caPath = caPath
		self.clientKeyPath = keyPath
		self.clientCertificatePath = certsPath
		imageResourcePath =  "/api/v1/files/CVPImages/"
		if isOnPrem:
			imageResourcePath = "/cvpservice/image/getImagebyId/"
		cvpNameOrig = dnsName if isOnPrem and not sanIpsProvided else cvpIP
		self.imageUrl = proto + "://" + cvpNameOrig + imageResourcePath + self.imageName
		self.dlImages = []

	def toMB(self, imgSize):
		if "MB" in imgSize:
			return float(imgSize.strip("MB"))
		elif "GB" in imgSize:
			return (0.1 + float(imgSize.strip("GB"))) * 1024
		else:
			return float(imgSize)

	def getFlashDiskUsage(self):
		diskUsageOutput = subprocess.check_output(["df", "-m", self.flashDir])
		diskUsageOutput = diskUsageOutput.split('\n')
		return diskUsageOutput

	def run(self):
		if self.imageName.endswith(".swi"):
			self.upgradeEOSImage()
			if self.status.getValue() == Status.IMAGE_UPGRADE_INPROGRESS:
				log("Image upgrade in progress. Waiting to reboot..")
				while True:
					time.sleep(1)
		else:
			if not self.isTerminAttrVersionValid():
				self.upgradeTerminAttr()
			else:
				log("TerminAttr version is valid. Skipping upgrade")
				self.status.setValue(Status.TERMINATTR_UPGRADE_SKIPPED, "current version is valid")

	def cleanUp(self):
		if not self.dlImages:
			return

		files = " ".join(self.dlImages)
		# try cleaning up the downloaded swi/swix images from flash
		clCmdList = ["enable", "bash bash -c \"rm -f %s\"" % files]
		r, err = self.cliManager.runCommands(clCmdList)
		if r:
			self.status.setValue(Status.IMAGE_UPGRADE_FAILED, err)
			return

	def checkHwEpochCompliant(self):
		log("check hw epoch compliance")
		if os.path.exists(self.epochFile):
			with open(self.epochFile) as f:
				hwEpochData = json.load(f)
				switchEpoch = hwEpochData["hwEpoch"].values()[0]
				log("hw epoch %s new eos epoch %s" % (switchEpoch, self.instEpoch))
				return float(switchEpoch) <= float(self.instEpoch)
		return True

	def maybeCleanupFlash(self):
		# cleanup non boot swi files
		if self.isSpaceAvailable():
			log("free space available..nothing to do")
			return

		log("cleaning up flash")
		# default to EOS.swi
		bootImagePath = self.flashDir + "/EOS.swi"
		with open(self.bootfilePath) as f:
			for line in f:
				line = line.strip()
				key, val = line.split('=')
				if key == "SWI":
					valArr = val.split(":")
					if((len(valArr) != 2) or (valArr[0].lower() != "flash")):
						return
					bootImagePath = self.flashDir + valArr[1]

		# find swi files in flash directory
		swiFileList = []
		try:
			findOutput = subprocess.check_output(["find", self.flashDir, "-name", "*.swi"])
			swiFileList = findOutput.split('\n')
		except subprocess.CalledProcessError:
			return

		for fn in swiFileList:
			if fn != bootImagePath:
				try:
					log("deleting %s" % fn)
					os.remove(fn)
				except OSError as e:
					log("failed deleting %s error: %s" %
						                   (fn, e.strerror))
				if self.isSpaceAvailable():
					log("free space available..nothing to do")
					return
			else:
				log("preserving %s" % fn)
		return

	def isSpaceAvailable(self, ):
		log("check space available")
		freeSz = 0.0
		try:
			diskUsageOutput = self.getFlashDiskUsage()
			#  output
			#Filesystem     1M-blocks  Used Available Use% Mounted on
			#/dev/sda1           1906  1391       515  74% /mnt/flash
			if len(diskUsageOutput) < 2:
				log("disk usage output unexpected %s" % diskUsageOutput)
				# attempt installing anyways
				return False

			diskUsageOutputArr = diskUsageOutput[1].split()
			if len(diskUsageOutputArr) < 6:
				log("disk usage output unexpected %s" % diskUsageOutputArr)
				# attempt installing anyways
				return False

			freeSz = float(diskUsageOutputArr[3])
		except subprocess.CalledProcessError as e:
			log("df Command Failed " + str(e))
			# attempt installing anyways
			return False

		log("freeSz : %f imageSz :%f" % (freeSz, self.imageSz))
		return freeSz > self.imageSz

	def isTerminAttrPresent(self):
		return os.path.isfile(self.terminAttrBinary)

	@staticmethod
	def getStandbyModule(moduleInfo):
		supModules = []
		for moduleVal in moduleInfo["modules"].values():
			if "supervisor" in moduleVal["typeDescription"].lower():
				supModules.append(moduleVal)
		if len(supModules) < 2:
			log("found less than 2 supervisors")
			return None

		if supModules[0].get('status') == 'active':
			return supModules[1]
		return supModules[0]

	def maybeUpgradeTerminAttrOnPeerSup(self):
		maxPeerPowerUpWaitAttempts = 600
		numWaitAttempts = 0
		while True:
			cmdList = ["enable", "show module | json"]
			rc, cmdOutput = self.cliManager.runCommands(cmdList)
			if rc != 0 or not cmdOutput:
				log("error getting module information %r" % repr(cmdOutput))
				return

			moduleOutput = json.loads(cmdOutput)
			if not moduleOutput.get('redundancyMode') == 'active':
				log("script not running on active")
				return

			standbyModule = self.getStandbyModule(moduleOutput)
			if not standbyModule:
				log("standby module not found")
				return

			standbyStatus = standbyModule.get('status')
			if standbyStatus == 'standby':
				log("standby supervisor is up")
				break
			else:
				log("waiting for standby supervisor to power up %s" % standbyStatus)
				numWaitAttempts += 1

			if numWaitAttempts > maxPeerPowerUpWaitAttempts:
				log("exceeded max time for supervisor to power up")
				return

			time.sleep(1)

		log("installing TerminAttr on peer supervisor")
		numInstallAttempts = 0
		maxInstallAttempts = 5

		while True:
			print("standby module found")
			cmdList = ["enable",
				"session peer-supervisor copy flash:/%s extension:" % self.imageName,
				"session peer-supervisor copy installed-extensions boot-extensions"]
			rc, errMsg = self.cliManager.runCommands(cmdList)
			if rc != 0:
				log("failed to install TerminAttr on standby %s" % errMsg)
				numInstallAttempts += 1
				if numInstallAttempts > maxInstallAttempts:
					log("exceeded max extension installation attempt on peer")
					return
			else:
				log("installed TerminAttr extension on standby successfully")
				return

	def downloadImage(self):
		'''Downloads image to /mnt/flash'''
		wgetCmd = "wget %s -P /mnt/flash" % self.imageUrl
		if self.isOnPrem:
			wgetCmd = "{wgetCmd} --ca-certificate={caCert}".format(
					wgetCmd=wgetCmd, caCert=self.nginxCertFile)
		else:
			wgetCmd = "{} --ca-certificate={} --certificate={} --private-key={}".format(
				wgetCmd, self.caPath, self.clientCertificatePath, self.clientKeyPath)
		dwnlCmdList = ["enable", "bash bash -c \"%s\"" % wgetCmd]
		return self.cliManager.runCommands(dwnlCmdList)

	def upgradeTerminAttr(self):
		log("upgrading TerminAttr")
		self.maybeCleanupFlash()

		# try cleaning up the TerminAttr image from flash
		self.dlImages.append('/mnt/flash/' + self.imageName)

		# download the TerminAttr image first to flash
		r, err = self.downloadImage()
		if r:
			self.status.setValue(Status.IMAGE_UPGRADE_FAILED, err)
			return

		self.maybeUpgradeTerminAttrOnPeerSup()

		cmdList = ["enable",
			"copy flash:/%s extension:" % self.imageName,
			"extension %s" % self.imageName,
			"copy installed-extensions boot-extensions"]
		rc, errMsg = self.cliManager.runCommands(cmdList)
		if rc:
			if self.isTerminAttrPresent():
				self.status.setValue(Status.TERMINATTR_UPGRADE_SKIPPED, " err=%s" % errMsg)
			else:
				self.status.setValue(Status.TERMINATTR_UPGRADE_FAILED, " err=%s" % errMsg)
		else:
			self.status.setValue(Status.TERMINATTR_UPGRADE_SUCCESS)

	@staticmethod
	def getTerminAttrVersion():
		try:
			currVersionOutput = subprocess.check_output(['rpm', '-q', 'TerminAttr-core',
				'--queryformat', '%{VERSION}-%{RELEASE}'])
			return currVersionOutput
		except subprocess.CalledProcessError as e:
			msg = "rpm -q TerminAttr-core --queryformat %{VERSION}-%{RELEASE}"
			log("Error running {}. Aborting. Error: {}".format(msg, str(e)))
			return None

	def isTerminAttrVersionValid(self):
		currVersion = self.getTerminAttrVersion()
		if not currVersion:
			return False
		return LooseVersion(currVersion) >= LooseVersion("v1.11.1-1")

	def upgradeEOSImage(self,):
		log("upgrading Default Eos Image")
		self.maybeCleanupFlash()

		if not self.checkHwEpochCompliant():
			self.status.setValue(Status.IMAGE_UPGRADE_FAILED, "epoch check failed")
			return

		# try cleaning up the EOS image from flash
		self.dlImages.append('/mnt/flash/' + self.imageName)

		# Download image on flash
		r, err = self.downloadImage()
		if r:
			self.status.setValue(Status.IMAGE_UPGRADE_FAILED, err)
			return

		cmdList = ["enable", "install source flash:/%s" % self.imageName]
		rc, errMsg = self.cliManager.runCommands(cmdList)
		if rc:
			self.status.setValue(Status.IMAGE_UPGRADE_FAILED, errMsg)
			return

		self.status.setValue(Status.IMAGE_UPGRADE_INPROGRESS)
		for reloadToken in ["reload all now", "reload now"]:
			rc, errMsg = self.cliManager.runCommands(["enable", reloadToken])
			if rc == 0:
				break
			log("reload command failed %s" % errMsg)
		return

class BootstrapManager(object):
	# pylint: disable=too-many-instance-attributes
	# pylint: disable=too-many-arguments
	CVP_USER = "cvptemp"
	CVP_NOTIFY_INTVL = 60
	CVP_POLL_INTVL = 2
	CVP_CONFIG_PATH = "/mnt/flash/cvp-config"
	STARTUP_CONFIG_PATH = "/mnt/flash/startup-config"
	ZTP_CONFIG_PATH = "/mnt/flash/zerotouch-config"
	PASSWD_PATH = "/var/local/.bootstrap_password"
	LOCALHOST = "127.0.0.1"
	INTERNAL1_1 = "127.1.0.1"
	INTERNAL2_1 = "127.1.0.2"

	def __init__(self):
		self.passwdPath = BootstrapManager.PASSWD_PATH
		self.startupConfigPath = BootstrapManager.STARTUP_CONFIG_PATH
		self.cvpConfigPath = BootstrapManager.CVP_CONFIG_PATH
		self.ztpConfigPath = BootstrapManager.ZTP_CONFIG_PATH
		self.bootstrapLogger = None
		self.keepRunning = True
		self.exitCode = 0
		self.hostname = None
		self.ipAddrs = []
		# Do not try to resolve these IPs to obtain a hostname in case the DHCP
		# server doesn't provide one. In case the DHCP server doesn't provide a
		# resolvable IP, we set the hostname to 'sw-<IP>' and have the customers
		# rely on that.
		# INTERNAL[1|2]_1: On a modular switch with redundant supervisors, this would be
		# the IP of the internal interface on one of the supervisors. /etc/hosts always
		# contains a DNS entry for these IPs and they get resolved to 'supervisor1' and
		# 'supervisor2' respectively.
		self.ipNoResolve = (BootstrapManager.LOCALHOST, BootstrapManager.INTERNAL1_1,
				BootstrapManager.INTERNAL2_1)
		self.status = Status()
		self.statusMsg = None
		self.cliManager = None
		self.tempDir = tempfile.mkdtemp()
		self.nginxcertfile = os.path.join(self.tempDir, "cvp.crt")
		self.runcurl = os.path.join(self.tempDir, "curlOutput")
		self.isOnPrem = None
		self.nginxCertificate = None
		self.cvAddr = None
		self.cvAuth = None
		self.cvIps = None
		self.switchSerialNumber = None
		self.sanIpsProvided = None
		self.dnsName = None
		self.setTemplateParams()
		self.caPath = None
		self.clientKeyPath = None
		self.clientCertificatePath = None
		self.cvpIp = self.chooseCvpIP( self.cvIps )
		self.cvpBootstrapUrl = "https://" + self.cvpIp + "/ztp/bootstrap"
		self.cvpUrl = "https://" + self.cvpIp + "/cvpservice/services/ztp/config"
		if self.isOnPrem and not self.sanIpsProvided:
			self.cvpBootstrapUrl = "https://" + self.dnsName + "/ztp/bootstrap"
			self.cvpUrl = "https://" + self.dnsName + "/cvpservice/services/ztp/config"
		self.cvpUser = BootstrapManager.CVP_USER
		self.cvpUserPassword = None
		self.configPollInterval = BootstrapManager.CVP_POLL_INTVL
		self.cvpNotifyInterval = BootstrapManager.CVP_NOTIFY_INTVL
		self.setCvpUserPasswd()
		# get a handle to cliManager
		try:
			self.cliManager = CliManager()
		except AssertionError as e:
			self.status.setValue(Status.SANITY_CHECK_FAILED, str(e))
			self.fatalExit()

		if self.isOnPrem:
			self.saveNginxCertToFile()
		else:
			self.populateCertificateDetails()

		self.checkCvpConfigPath()

		log("cvIps = %s" % self.cvIps)
		log("cvpNotifyIntvl = %d" % self.cvpNotifyInterval)
		log("configPollIntvl = %d" % self.configPollInterval)
		log("cvpUrl = %s" % self.cvpUrl)
		log("cvpUser = %s" % self.cvpUser)
		log("cvAddr = %s" % self.cvAddr)
		log("cvAuth = %s" % self.cvAuth)

	def checkCvpConfigPath(self):
		persistDir = os.path.dirname(BootstrapManager.CVP_CONFIG_PATH)
		if not os.path.exists(persistDir):
			self.status.setValue(Status.SANITY_CHECK_FAILED,
				"dir %s does not exist" % persistDir)
			self.fatalExit()


	def setTemplateParams(self):
		self.isOnPrem = "true" == "true"
		self.nginxCertificate = "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURNVENDQWhtZ0F3SUJBZ0lKQU1VRDQ1UCt2YlgzTUEwR0NTcUdTSWIzRFFFQkN3VUFNQll4RkRBU0JnTlYKQkFNTUMzTmxiR1l1YzJsbmJtVmtNQjRYRFRJeU1EY3lOVEUzTXpNeU4xb1hEVEl6TURjeU5URTNNek15TjFvdwpGakVVTUJJR0ExVUVBd3dMYzJWc1ppNXphV2R1WldRd2dnRWlNQTBHQ1NxR1NJYjNEUUVCQVFVQUE0SUJEd0F3CmdnRUtBb0lCQVFESzFRNGR6MmxDT1JHNTNWWUM2eFVWeEJaNytrYXhmR3dOMnM0amF1a3ZtdERtZjlad0xDMXgKbmc5VlVxU3AzcmhmUjNxc3h6em11b3d4bURneUcvMUR3VlFIeElzN2F3VG5ITWhyOWRncHRDNjUrZzljUTY5ZQo0b1VBQ1grVkhOWUp5NXU0dEs1L254NjI2c3NLanMvKzhSNVh3cUQwUnY4bkhWTnBsK3FWbXNKUno5aU9JRjA4CkJKZHRCVENLVE15N1B3aGY4d2djY1JmRHVpWXBMY3Z1bGEyeVJLRnBlTWY3RDNaNmdRRDNQNnRMUzhPa2ExZjYKNURMdmQxWTVUR1ZPaW9kWndJWGJtL3pMQnJBbDJGU3ZUd2x3SjVxNjRXQi9YUEpZTWVPWVpwUTIvQ3pFaGJMdgpYb3pjR1U5ejlOOXhCeWoyVm9UblVDMXc5cGdRSjZBWkFnTUJBQUdqZ1lFd2Z6QUpCZ05WSFJNRUFqQUFNQXNHCkExVWREd1FFQXdJQzVEQVRCZ05WSFNVRUREQUtCZ2dyQmdFRkJRY0RBVEJRQmdOVkhSRUVTVEJIZ2dOamRuQ0MKRDJOMmNDNXpiR0ZqYTJWeUxtVjJaWUlOTVRreUxqRTJPQzR5TlRVdU5ZY0V3S2ovQllJSmJHOWpZV3hvYjNOMApnZ2t4TWpjdU1DNHdMakdIQkg4QUFBRXdEUVlKS29aSWh2Y05BUUVMQlFBRGdnRUJBRnN3bGdKUEFCWFJmcTZ5CnI1dXNLbVYzaGh0WHExWVNtZ1RPL1ZCVllFU3JiN2taRVVaV3FUNG9ZTlpTbm9Mbkw4N1RBYVM4dzR1L0Y0VWoKZEl1WFVJa0RGUGFDaFhGN0d4QWp4b3ZTejlBSjJscXBiT1NpelorK2gweFc4SmNBaTBocEl0ZlFOMitXQXppaQp1YUl0T3dMeGZodElOYWZZY1dscjVtVnAyWnBlK3JSb05aMUQ1R3R0VDh5bXo5TS9SZXRJaFN5YVlIMmtJdWdRCldVUE9lNnpJMmRURUxKYmh3WUc4eXJZalRPVXNWRW1MOUMyMHJRemMwTm1La2tBZkU2U2s5ZGo2ekd2bGZvQjcKK0tFWDZhZnZ4WUpiQjhFWXZSS0VkdVN6VkZpVzJhQjNweElTODhOSVRSZTZhTVhNVVBWbU9nWkVCbU5sWjNXQQo0eFdCdWs4PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg=="
		self.cvAddr = "192.168.255.5:9910"
		self.cvAuth = "token,/tmp/token"
		self.cvIps = "192.168.255.5"
		self.switchSerialNumber = ""
		self.sanIpsProvided = "true" == "true"
		self.dnsName = ""

	# Oslo supports minimum TerminAttr version 1.11.0. And 1.14.0 introduces
	# -certsconfig option that allows getting certs path from TerminAttr.
	# For Oslo to support ZTP onboarding on CVaaS using certs, we will have to
	# hard code certs path here if TerminAttr version is >= 1.11.0 and <1.14.0.
	def isTaSupportedOnOsloUnsupportedCertsConfig(self):
		currVersion = ImageUpgrade.getTerminAttrVersion()
		if not currVersion:
			return False
		return LooseVersion(currVersion) >= LooseVersion("v1.11.0") and \
			LooseVersion(currVersion) < LooseVersion("v1.14.0")


	def populateCertificateDetails(self):
		cmdList = ["enable", "bash bash -c \"/usr/bin/TerminAttr -cvaddr={} -cvauth={} -certsconfig\"".format(self.cvAddr, self.cvAuth)]
		rc, out = self.cliManager.runCommands(cmdList)
		if rc != 0:
			if self.isTaSupportedOnOsloUnsupportedCertsConfig():
				self.clientCertificatePath = "/persist/secure/ssl/terminattr/primary/certs/client.crt"
				self.clientKeyPath = "/persist/secure/ssl/terminattr/primary/keys/client.key"
			else:
				log("Failed to get certs details")
				self.fatalExit()
		else:
			certsConfig = json.loads(out)
			if certsConfig.has_key(self.cvAddr):
				if certsConfig[self.cvAddr].has_key("caFile"):
					self.caPath = certsConfig[self.cvAddr]["caFile"]
				if certsConfig[self.cvAddr].has_key("certFile"):
					self.clientCertificatePath = certsConfig[self.cvAddr]["certFile"]
				if certsConfig[self.cvAddr].has_key("keyFile"):
					self.clientKeyPath = certsConfig[self.cvAddr]["keyFile"]

		log("clientCertificatePath = %s" % self.clientCertificatePath)
		log("clientKeyPath = %s" % self.clientKeyPath)
		log("caPath = %s" % self.caPath)


	def chooseCvpIP(self, cvIPs):
		cvIps = cvIPs.split(",")
		for cvIp in cvIps:
			if self.netcatable(cvIp):
				return cvIp
		# In case no ip is reachable return the first one
		# and let the script fail at later step.
		log("No CV nodes responding. Defaulting to %s" % cvIps[0])
		return cvIps[0]

	def netcatable(self, ip):
		command = ['nc', "-zv", ip]
		return subprocess.call(command) == 0

	@staticmethod
	def getEosVersion():
		currVersionOutput = subprocess.check_output(['rpm', '-q', 'Eos',
			'--queryformat', '%{VERSION}-%{RELEASE}'])
		return currVersionOutput

	def setCvpUserPasswd(self, ):
		# We continue to use the same randomly generated password for a device
		# until it is rebooted. This prevents weird race conditions on the CVP
		# side where we attempt to access the device just as ZTP decides to
		# restart its process and change the password that the device is using.
		if os.path.exists(self.passwdPath):
			with open(self.passwdPath) as f:
				self.cvpUserPassword = f.read()
		else:
			# Generate a new random password and stash it away
			self.cvpUserPassword = str(''.join(random.choice(
				string.ascii_uppercase +
				string.ascii_lowercase +
				string.digits) for _ in range(16)))
			with open(BootstrapManager.PASSWD_PATH, 'w') as f:
				f.write(self.cvpUserPassword)

	def getIpAddresses(self):
		output, _error = subprocess.Popen(["ip", "address", "show"],
			stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
		return output

	def resolve(self, ip):
		return socket.getnameinfo((ip, 0), 0)

	def setIpAddressAndHostname(self,):
		output = self.getIpAddresses()
		for line in output.split("\n"):
			if 'inet' in line:
				match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
				if match:
					ipAddr = match.group()
					if ipAddr not in self.ipNoResolve:
						self.ipAddrs.append(ipAddr)

		if not self.ipAddrs:
			self.status.setValue(Status.INIT_FAILED, NO_IP_ADDR_MSG)
			self.fatalExit()

		goodHostName = None
		cmdList = ["enable", "show hostname | json"]
		rc, cmdOutput = self.cliManager.runCommands(cmdList)
		if rc != 0 or not cmdOutput:
			log("no existing hostname from DHCP")
		else:
			j = json.loads(cmdOutput)
			if "hostname" in j and j["hostname"] != "localhost":
				goodHostName = j["hostname"]

		if not goodHostName:
			log(self.ipAddrs)
			for ip in self.ipAddrs:
				# if a valid name entry; h = fqdn else h = ip
				h = None
				try:
					h, _ = self.resolve(ip)
				except:  # pylint: disable=W0702
					log("Could not resolve ip %s to a host name" % ip)
				# getnameinfo() might return 'localhost' on EOS >= 4.25.1
				# if there's no DNS server
				if h and ip != h and h != "localhost":
					goodHostName = h.split('.')[0]
					break

		if not goodHostName:
			goodHostName = "sw-%s" % self.ipAddrs[0]
		self.hostname = goodHostName
		log("hostname %s ipAddrs %s" % (self.hostname, self.ipAddrs))

	# Meant to be used by tests
	def resetIpAddressAndHostname(self):
		self.hostname = None
		self.ipAddrs = []

	def deleteFile(self, path):
		if os.path.isfile(path):
			try:
				os.remove(path)
			except os.error:
				log("Cannot remove {}. You can delete it manually.".format(path))

	def cleanUp(self,):
		log("Removing temporary files")
		self.deleteFile(self.cvpConfigPath)
		self.deleteFile(self.ztpConfigPath)

	def fatalExit(self,):
		log("BootStrap failed, exiting script (switch will reload)")
		self.postZTPErrorStatus()
		time.sleep(10)
		self.cleanUp()
		# If this method is called from a thread then a call to 'exit' will not
		# cause the main thread to exit. Setting global run flag to false.
		self.exitCode = -1
		self.keepRunning = False
		self.cleanUpTempFiles()
		exit(self.exitCode)

	def addBaseConfig(self,):
		log("Applying Base EOS configuration")
		cmdList = ["enable", "configure",
			"username {user} privilege 15 secret {passwd}".format(
				user=self.cvpUser, passwd=self.cvpUserPassword),
			"hostname {hostname}".format(hostname=self.hostname)]
		rc, errMsg = self.cliManager.runCommands(cmdList)
		if rc:
			self.status.setValue(Status.BASE_CONFIG_FAILED, errMsg)
			self.fatalExit()

	def runCommandsTemplates(self, templateList):
		for templateV in templateList:
			configName, cmds, abortOnFail = templateV
			rc, errMsg = self.cliManager.runCommands(cmds)
			if rc:
				errMsg = configName + "Config Failed, errMsg: " + errMsg
				self.status.setValue(Status.CONFIG_FAILED, errMsg)
				if abortOnFail:
					self.fatalExit()

	def runConfigChecker(self,):
		def waitForConfig():
			"""
			Notify CVP server that system is in need of configuration and provide
			CVP server with relevant data. And at the same time:
			Poll file system for cvp-config. This file should be created by CVP
			server issuing the command "copy session-config cvp-config" from within
			a config session over eAPI. After the file is created, wait a few
			seconds for eAPI request from CVP to fully complete before
			copying the file to /mnt/flash/startup-config and exiting.
			"""
			counter = 0
			while self.keepRunning:
				if self.status.getValue() != Status.CONFIG_REQUEST_SUCCESS:
					log("Sending request to " + self.cvpUrl + " [" + str(counter) + "]")
					self.sendZTPConfigRequest()
				if os.path.exists(self.cvpConfigPath):
					log("cvp-config found, writing to startup-config")
					rc = subprocess.call(["mv", self.cvpConfigPath, self.startupConfigPath])
					if rc != 0:
						errMsg = "config move to /mnt/flash returned error code " + str(rc)
						self.status.setValue(Status.CONFIG_FAILED, errMsg)
						self.fatalExit()
					else:
						self.status.setValue(Status.SUCCESS)
						self.cleanExit()

				counter += 1
				time.sleep(self.configPollInterval)

		thread.start_new_thread(waitForConfig, ())

	def executeCurl(self, url, payload):
		contentTypeStr = '"Content-Type:application/json"'
		with open(self.runcurl, 'w') as f:
			cmdStr = "curl -H {contentType} -X POST {postUrl} -d '{data}'".format(
						contentType=contentTypeStr, postUrl=url, data=json.dumps(payload))
			if self.isOnPrem:
				cmdStr = "{curlCmd} --cacert {caCertPath}".format(curlCmd=cmdStr,
						   caCertPath=self.nginxcertfile)
				if not self.sanIpsProvided:
					cmdStr = "{curlCmd} --resolve {dnsName}:{port}:{ipAddr}".format(curlCmd=cmdStr,
					dnsName=self.dnsName, port=443, ipAddr=self.cvpIp)
			else:
				caCert = "--cacert {}".format(self.caPath) if self.caPath else ""
				cmdStr = "{curlCmd} {caCert} --cert {clientCertPath} --key {clientKeyPath}".format(
						curlCmd=cmdStr, caCert=caCert, clientCertPath=self.clientCertificatePath,
						clientKeyPath=self.clientKeyPath)
			f.write(cmdStr)
		cmdList = [ 'enable', 'bash bash -c "bash %s"' % self.runcurl]
		r, errMsg = self.cliManager.runCommands(cmdList)
		return (r, errMsg)

	def cleanUpTempFiles(self,):
		# delete the cvp.crt file
		self.deleteFile(self.nginxcertfile)
		self.deleteFile(self.runcurl)

	def postZTPErrorStatus(self,):
		""" Send HTTP notices to the CVP server in the form of HTTP request
            with the temporary CVP user information encoded
		"""
		log("posting ztp error status")
		deviceStatus = DeviceStatus(self.status.msg)
		payload = deviceStatus.__dict__
		r, errMsg = self.executeCurl(self.cvpBootstrapUrl, payload)
		if r != 0:
			log("Error posting ztp error status: %s" % errMsg)

	def sendZTPConfigRequest(self,):
		""" Send HTTP notices to the CVP server in the form of HTTP request
            with the temporary CVP user information encoded
		"""
		ipStringList = ",".join(self.ipAddrs)
		payload = {'password': self.cvpUserPassword,
					  'ipStringList': ipStringList,
					  'deviceID': self.switchSerialNumber}
		r, errMsg = self.executeCurl(self.cvpUrl, payload)
		if r != 0:
			log("Error sending ztp config request: %s" % errMsg)
			return
		self.status.setValue(Status.CONFIG_REQUEST_SUCCESS)

	def cleanExit(self,):
		self.cleanUp()
		self.keepRunning = False

	def saveNginxCertToFile(self):
		# write the nginx certificate to a file to be passed to requests
		try:
			decodedCert = base64.b64decode(self.nginxCertificate)
			certFile = open(self.nginxcertfile, "w")
			certFile.write(decodedCert)
		except IOError as e:
			log("Cannot open {} error : {}".format(self.nginxcertfile, str(e)))
		finally:
			certFile.close()

	def startTerminAttr(self):
		# starts the terminattr
		cvAuth = self.cvAuth
		if not self.isOnPrem:
			# we've already exchanged the token, use the client certs now.
			cvAuth = "certs,{},{}".format(self.clientCertificatePath, self.clientKeyPath)
			if self.caPath:
				cvAuth = "{},{}".format(cvAuth, self.caPath)
		cmds = ["enable",
			"configure",
			"daemon TerminAttr",
			"exec /usr/bin/TerminAttr -cvaddr={cvAddr} -cvcompression=gzip -taillogs -cvauth={cvAuth} -smashexcludes=ale,flexCounter,hardware,kni,pulse,strata -ingestexclude=/Sysdb/cell/1/agent,/Sysdb/cell/2/agent".format(cvAddr=self.cvAddr,cvAuth=cvAuth),
			"no shutdown",
			"end"]
		rc, outOrErr = self.cliManager.runCommands(cmds)
		if rc:
			errMsg = "Failed to start TerminAttr, errMsg: " + outOrErr
			self.status.setValue(Status.CONFIG_FAILED, errMsg)
			self.fatalExit()

	def run(self,):
		proto = 'http'
		self.cleanUp()
		self.setIpAddressAndHostname()
		self.addBaseConfig()

		self.runCommandsTemplates([('''EapiConfig''', ['enable', 'configure', 'management api http-commands', 'protocol https', 'no shut', 'wait-for-warmup Capi', 'end'], True), ('''DisableThrottlingConfig''', ['enable', 'configure', 'control-plane', 'no service-policy input copp-system-policy', 'end'], False), ('''MaxSessionsConfig''', ['enable', 'configure', 'service configuration session max pending 10', 'end'], False), ('''SetClockConfig''', ['enable', 'clock set 04:22:29 2022-12-26'], False), ]) # pylint: disable=line-too-long

		currVersion = self.getEosVersion()
		if LooseVersion(currVersion) >= LooseVersion("4.17"):
			proto = 'https'
		imageUpgrade = ImageUpgrade(self.cvpIp, self.status, proto, self.cliManager,
						self.isOnPrem, self.nginxcertfile, self.caPath, self.clientKeyPath,
						self.clientCertificatePath, self.sanIpsProvided, self.dnsName)
		imageUpgrade.run()

		self.runCommandsTemplates([])

		# start terminAttr
		if self.isOnPrem:
			SaveEnrollToken( certEnabled=True, token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhc2V0SUQiOjMsImV4cCI6MTY3MjAyOTE0OSwia2lkIjoiMDMzZWViMWY0YTAzYWYzNSIsIm5iZiI6MTY3MjAyODU0OX0.kK-6cskUX29XGPeWL08Y3MgR5eaXrSzailE5u7aNE_kU_eZd_uwSn5f6VAvbYgTM52gl3qbgQC5v6GQCIVMUfw1s9N-9ALP-25G_Tmko7Vn3lgYlGcQ2bLTfAd2uFs0hMRxU_U9Y10o-sPvBzb-U_jKq1X7218ovR0f2Qlh11xfqDnoZZIMCP5nL2CBorFKylNNOPSPyi_c-1rrBFWcV_1BIzBHDuudOp18YicC_J6VBUO_f-GgvhlNlmZFV0voRuFXIRcPj4pevFLvgNJaVcmY0A_ibAFsYz9snpVOQNX26xi6BNg_q0xvHkJJeB6BH2oiRfHDGeQvFg6C2fk7RiU-iTJaOp9wuo31F8lc5QUPCt317_kvlcR08_2gfv6q0THHuIqhlNaqmls3hvM8a7s05nIfS__AN_wKhXlM4MsPIOKjjuBAuqb0jaxe22MgbuwbMlCMHJjMJ-Nlzxp-RAqI7kROI3UAzLeOHWYyoCupZt1KURoPtEVjy97wAyhUr9FOpILTVEqWa0s7SLIizwDc5K1_buK5PFrHIMske-_1dwXu0owmQsuAAY8dRM-K6nsjq51iTZiucV9eBao5cNv0LFJUlu8jpIH5NPrGt9kMGiSJdhFr3UdWcfrfT8ZgUgpsnMsiszJ_i_w5KVMQbuzcaVWS_G7Q135OH7tiYCW4", # pylint: disable=line-too-long
						     tokenFile="/tmp/token" )
		self.startTerminAttr()

		# clean up any downloaded EOS/TerminAttr images
		imageUpgrade.cleanUp()
		# wait for the config change
		self.runConfigChecker()

		log("waiting for Eos configuration")
		while True:
			if not self.keepRunning:
				exit(self.exitCode)
			time.sleep(1)

		self.cleanUpTempFiles()

def SaveEnrollToken( certEnabled, token, tokenFile ):
	""" If the certificate setting is enabled, saves an enrollment token in
        a token file.
	"""
	if not certEnabled:
		return
	with open( tokenFile, "w+" ) as f:
		f.write( token )



if __name__ == "__main__":
	setupLogger()
	BootstrapManager().run()
