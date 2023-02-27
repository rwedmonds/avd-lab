#!/usr/bin/python
# Copyright (c) 2021 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the COPYING file.

import subprocess
import os
import json
import sys
import requests
import Cell
import urlparse


##############  USER INPUT  ##############
# Note: If you are saving the file on windows, please make sure to use linux (LF) as newline.
# By default, windows uses (CR LF), you need to convert the newline char to linux (LF).

# address for CVaaS, usually just "www.arista.io"
CVADDR = "www.cv-staging.corp.arista.io"

# enrollment token to be copied from CVaaS Device Registration page
ENROLLMENT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhc2V0SUQiOjEzNTUsImV4cCI6MTY3NDYxNjUyNSwia2lkIjoiZTY5NTI3NmEyNmUyMmFlNiIsIm5iZiI6MTY3MjAyNDUyNSwicmVlbnJvbGxEZXZpY2VzIjpbIioiXX0.dy0Vy-fEkjrBAftf7N1Yry2BRenUYsS17qQsDOjwW0Z_rNUriqCEzZZUecRKOeSCOrRHd7X1FRNxA8p-fQx7EpsK4yc1umaMdvtqPgA-T4JdkRwJDBfmfNHyX7etGALg5Kjea6CY-1bz1cFXOEedVornKXpPj01fuzgO1jTe7MY8tLinNVLp_Oh8IAp8inF4CbU6BBynEM7kCva_n2S8aIQSqdbkuZLnTwBZgJMYa8PxShUmECN5MoDS62qOZNRcLVL3AZlMC91AU_JGohz2NYh6mzQL4YCwpwMX0A7OqIdZSZbRcvX4N2VrgoqK8ZcPEnbAWVjOp75ROMg9lPWebsXCq4bhUGlHVRuTcSAf3wN3NXvMbbemERW-QR6wWlpXjfwd6Oe1GsZMOmhwZucd9bs5db66OuMqMg-VMTXvaGyC1zc0y7rQ13KOMlemsrCmSQcq9ehmyFV_45JeCgTiG-GUh1QaXqerBYf40Re97L6GVbqR5O-M1qjXiu8X0YCU4-oeivkbGHzcBVRsGcOwtdOKv4bf1IlkVsWyi0frrlxRUyFaumoYNIP-vFLj9IvvpRlLm25OD0exRczzu3Yp5EQfuMbXxBMqxVOBm9X6wyrcNlNqPqmJI5yJ4qf3RPVv86PcLq_72N6y0Ft1VbJnD_OgZKxsLJNZPqNZWIpGeTQ"

# Add proxy url if device is behind proxy server, leave it as an empty string otherwise
CVPROXY = ""

# EOSURL is an optional parameter, which needs to be added only if the EOS version
# is <4.24, in which case, SysDbHelperUtils is not present on the device.
# This needs to be a http URL pointing to a SWI image on the local network.
EOSURL = ""


##############  CONSTANTS  ##############
SECURE_HTTPS_PORT = "443"
SECURE_TOKEN = "token-secure"
INGEST_PORT = "9910"
INGEST_TOKEN = "token"
TOKEN_FILE_PATH = "/tmp/token.tok"
BOOT_SCRIPT_PATH = "/tmp/bootstrap-script"
REDIRECTOR_PATH = "api/v3/services/arista.redirector.v1.AssignmentService/GetOne"


##############  HELPER FUNCTIONS  ##############
proxies = { "https" : CVPROXY, "http" : CVPROXY }


def get_value_from_file( filename, key ):
    """Given a filepath and a key, get_value_from_file searches for key=VALUE in it
and returns the found value without any whitespaces. In case no key specified,
gives the first string in the first line of the file."""
    if not key:
        with open( filename, "r", encoding="utf-8" ) as in_file:
            return in_file.readline().split()[ 0 ]
    else:
        with open( filename, "r", encoding="utf-8" ) as in_file:
            lines = in_file.readlines()
            for line in lines:
                if key in line :
                    return line.split( "=" )[ 1 ].rstrip( "\n" )
    return None


def try_image_upgrade( error_message ):
    """Attempt to upgrade EOS if version is not new enough"""
    # Raise import error if EOSURL is empty
    if EOSURL == "":
        print( "Specify EOSURL for EOS version upgrade" )
        raise( error_message )
    subprocess.call( [ "mv", "/mnt/flash/EOS.swi", "/mnt/flash/EOS.swi.bak" ] )
    try:
        cmd = f"wget {EOSURL} -O /mnt/flash/EOS.swi; sudo ip netns exec default /usr/bin/FastCli \
            -p15 -G -A -c $'configure\nboot system flash:/EOS.swi'"
        subprocess.check_output( cmd, shell=True, stderr=subprocess.STDOUT )
    except subprocess.CalledProcessError as err:
        # If the link to EOSURL specified is incorrect, then revert back to the older version
        subprocess.call( [ "mv", "/mnt/flash/EOS.swi.bak", "/mnt/flash/EOS.swi" ] )
        print( err.output )
        raise( err )
    subprocess.call( [ "rm", "/mnt/flash/EOS.swi.bak" ] )
    subprocess.call( [ "reboot" ] )


##############  SysdbHelperUtils IMPORT HANDLING  ##############
# SysdbHelperUtils library is not present in most EOS versions <4.24. Thus in such a
# case, we locally upgrade the EOS version and reboot the  device. After the upgrade,
# EOS version of device must be upgraded and import for SysdbHelperUtils will not fail.
try:
    from SysdbHelperUtils import SysdbPathHelper
except ImportError as e:
    try_image_upgrade( e )


##############  MAIN SCRIPT  ##############
class BootstrapManager( object ):
    """Class for managing the bootstrap process"""
    # def __init__( self ):
    #     super( BootstrapManager, self ).__init__()

    def get_bootstrap_url( self, url ):
        "Get the URL for the bootstrap file"
        pass


##################################################################################
# step 1: get client certificate using the enrollment token
##################################################################################
    def get_client_certificates( self ):
        with open( TOKEN_FILE_PATH, "w", encoding="utf-8" ) as token_file:
            token_file.write( ENROLLMENT_TOKEN )

        # A timeout of 60 seconds is used with TerminAttr commands since in most
        # versions of TerminAttr, the command execution does not finish if a wrong
        # flag is specified leading to the catch block being never executed
        cmd = "timeout 60s "
        cmd += "/usr/bin/TerminAttr"
        cmd += " -cvauth " + self.token_type + "," + TOKEN_FILE_PATH
        cmd += " -cvaddr " + self.enroll_addr
        cmd += " -enrollonly"

        # Use CVPROXY only when it is specified, this is to ensure that if we are on
        # older version of EOS that doesn't support cvporxy flag, the script won't fail
        if CVPROXY != "":
            cmd += " -CVPROXY=" + CVPROXY

        try:
            subprocess.check_output( cmd, shell=True, stderr=subprocess.STDOUT )
        except subprocess.CalledProcessError as process_error:
            # If the above subprocess call times out, it means that -CVPROXY
            # flag is not present in the Terminattr version running on that device
            # Hence we have to do an image upgrade in this case.
            if e.returncode == 124: # timeout
                try_image_upgrade( process_error )
        else:
            print( process_error.output )
            raise process_error

        print( "step 1 done, exchanged enrollment token for client certificates" )


##################################################################################
# Step 2: get the path of stored client certificate
##################################################################################
    def get_certificate_paths( self ):
        # Timeout added for TerminAttr
        cmd = "timeout 60s "
        cmd += "/usr/bin/TerminAttr"
        cmd += " -cvaddr " + self.enroll_addr
        cmd += " -certsconfig"

        try:
            response = subprocess.check_output( cmd, shell=True, stderr=subprocess.STDOUT )
            json_response = json.loads( response )
            self.certificate = str( json_response[ self.enroll_addr ][ 'certFile' ] )
            self.key = str( json_response[ self.enroll_addr ][ 'keyFile' ] )
        except subprocess.CalledProcessError:
            base_path = "/persist/secure/ssl/terminattr/primary/"
            self.certificate = base_path + "certs/client.crt"
            self.key = base_path + "keys/client.key"

        print( "step 2 done, obtained client certificates location from TA" )
        print( "ceriticate location: " + self.certificate )
        print( "key location: " + self.key )


##################################################################################
# step 3 get bootstrap script using the certificates
##################################################################################
    def check_with_redirector( self, serialNum ):
        if not self.redirector_url:
            return

        try:
            payload = '{"key": {"system_id": "%s"}}' % serialNum
            response = requests.post( self.redirector_url.geturl(), data=payload,
                cert=( self.certificate, self.key ), proxies=proxies, timeout=30 )
            response.raise_for_status()
            clusters = response.json()[ 0 ][ "value" ][ "clusters" ][ "values" ]
            assignment = clusters [ 0 ][ "hosts" ][ "values" ][ 0 ]
            self.bootstrap_url = self.get_bootstrap_url( assignment )
        except Exception as exception:
            print(f"error talking to redirector: {exception}")
            print( "no assignment found from redirector" )

    def get_bootstrap_script( self ):
        # setting Sysdb access variables
        sysname = os.environ.get( "SYSNAME", "ar" )
        path_helper = SysdbPathHelper( sysname )

        # sysdb paths accessed
        cell_id = str( Cell.cellId() )
        mib_status = path_helper.getEntity( "hardware/entmib" )
        tmp_status = path_helper.getEntity( "cell/" + cell_id + "/hardware/tpm/status" )

        # setting header information
        headers = {}
        headers[ 'X-Arista-SystemMAC' ] = mib_status.systemMacAddr
        headers[ 'X-Arista-ModelName' ] = mib_status.root.modelName
        headers[ 'X-Arista-HardwareVersion' ] = mib_status.root.hardwareRev
        headers[ 'X-Arista-Serial' ] = mib_status.root.serialNum

        headers[ 'X-Arista-TpmApi' ] = tmp_status.tpmVersion
        headers[ 'X-Arista-TpmFwVersion' ] = tmp_status.firmwareVersion
        headers[ 'X-Arista-SecureZtp' ] = str( tmp_status.boardValidated )

        headers[ 'X-Arista-SoftwareVersion' ] = get_value_from_file(
                "/etc/swi-version", "SWI_VERSION" )
        headers[ 'X-Arista-Architecture' ] = get_value_from_file( "/etc/arch", "" )

        # get the URL to the right cluster
        self.check_with_redirector( mib_status.root.serialNum )

        # making the request and writing to file
        response = requests.get( self.bootstrap_url.geturl(), headers=headers,
                cert=( self.certificate, self.key ), proxies=proxies, timeout=15 )
        response.raise_for_status()
        with open( BOOT_SCRIPT_PATH, "w", encoding="utf-8" ) as f:
            f.write( response.text )

        print( "step 3.1 done, bootstrap script fetched and stored on disk" )

    # execute the obtained bootstrap file
    def execute_bootstrap( self ):
        cmd = "python " + BOOT_SCRIPT_PATH
        os.environ['CVPROXY'] = CVPROXY
        try:
            subprocess.check_output( cmd, shell=True, stderr=subprocess.STDOUT,
                                    env=os.environ )
        except subprocess.CalledProcessError as process_error:
            print( process_error.output )
            raise process_error
        print( "step 3.2 done, executing the fetched bootstrap script" )

    def run( self ):
        self.get_client_certificates()
        self.get_certificate_paths()
        self.get_bootstrap_script()
        self.execute_bootstrap()


class CloudBootstrapManager( BootstrapManager ):
    def __init__( self ):
        super( CloudBootstrapManager, self ).__init__()

        self.bootstrap_url = self.get_bootstrap_url( CVADDR )
        self.redirector_url = self.bootstrap_url._replace( path=REDIRECTOR_PATH )
        self.token_type = SECURE_TOKEN
        self.enroll_addr = self.bootstrap_url.netloc + ":" + SECURE_HTTPS_PORT
        self.enroll_addr = self.enroll_addr.replace( "www", "apiserver" )

    def get_bootstrap_url( self, addr ):
        addr = addr.replace( "apiserver", "www" )
        addr_url = urlparse.urlparse( addr )
        if addr_url.netloc == "":
            addr_url = addr_url._replace( path="", netloc=addr_url.path )
        if addr_url.path == "":
            addr_url = addr_url._replace( path="/ztp/bootstrap" )
        if addr_url.scheme == "":
            addr_url = addr_url._replace( scheme="https" )
        return addr_url


class OnPremBootstrapManager( BootstrapManager ):
    def __init__( self ):
        super( OnPremBootstrapManager, self ).__init__()

        self.bootstrap_url = self.get_bootstrap_url( CVADDR )
        self.redirector_url = None
        self.token_type = INGEST_TOKEN
        self.enroll_addr = self.bootstrap_url.netloc + ":" + INGEST_PORT

    def get_bootstrap_url( self, addr ):
        addr_url = urlparse.urlparse( addr )
        if addr_url.netloc == "":
            addr_url = addr_url._replace( path="", netloc=addr_url.path )
        if addr_url.path == "":
            addr_url = addr_url._replace( path="/ztp/bootstrap" )
        if addr_url.scheme == "":
            addr_url = addr_url._replace( scheme="http" )
        return addr_url


if __name__ == "__main__":
    # check inputs
    if CVADDR == "":
        sys.exit( "error: address to CVP missing" )
    if ENROLLMENT_TOKEN == "":
        sys.exit( "error: enrollment token missing" )

    # check whether it is cloud or on prem
    if CVADDR.find( "arista.io" ) != -1 :
        bm = CloudBootstrapManager()
    else:
        bm = OnPremBootstrapManager()

    # run the script
    bm.run()
