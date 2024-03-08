"""
Build configs from yaml files
"""

import os
# import subprocess
import difflib
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result
import pyavd


def build_config(task: Task, eos_designs, avd_facts):
    """
    Build configs
    """
    structured_config = pyavd.get_device_structured_config(
        task.host.name, eos_designs[task.host.name], avd_facts=avd_facts)
    config = pyavd.get_device_config(structured_config)

    task.host.data["designed-config"] = config
    return Result(host=task.host)


def pull_config(task: Task):
    """
    Pull configs
    """
    with open(f'inventory/intended/configs/{task.host.name}.cfg', "r",
              encoding="utf-8") as f:
        task.host.data["running-config"] = f.read()
    return Result(host=task.host)


def diff_config(task: Task):
    """
    Diff configs
    """
    changed = False
    diff = ""
    for line in difflib.unified_diff(task.host.data["running-config"].split("\n"), task.host.data["designed-config"].split("\n"), fromfile='running-config', tofile='designed-config', lineterm=''):
        diff += f'{line}\n'
        changed = True
    return Result(host=task.host, diff=diff, changed=changed)


def deploy_config(task: Task):
    """
    Deploy configs
    """
    with open(f'inventory/intended/configs/{task.host.name}.cfg', "w",
              encoding="utf-8") as f:
        f.write(task.host.data["designed-config"])
    return Result(host=task.host, changed=True)


def config_management(task: Task, eos_designs, avd_facts):
    """
    Manage configs
    """
    task.run(task=build_config, eos_designs=eos_designs, avd_facts=avd_facts)

    # task.run(task=pull_config)
    # result = task.run(task=diff_config)[0]
    # if result.changed:
    task.run(task=deploy_config)


def run():
    """Build configs"""
    # Initialize Nornir object from config_file
    nr = InitNornir(config_file="../inventory/config.yml")

    eos_designs = {}

    for hostname in nr.inventory.hosts:
        host = nr.inventory.hosts[hostname]

        # Using .dict() or .data was not getting the group variables
        data = host.items()
        res = {}
        for (k, v) in data:
            res[k] = v

        eos_designs[hostname] = res

    # Validate input and convert types as needed
    failures = False
    for host in eos_designs:
        hostvars = eos_designs[host]

        results = pyavd.validate_inputs(hostvars)
        if results.failed:
            for result in results.validation_errors:
                print(result)
            failures = True
    if failures:
        exit(1)

    # Generate facts
    avd_facts = pyavd.get_avd_facts(eos_designs)

    output = nr.run(task=config_management,
                    eos_designs=eos_designs, avd_facts=avd_facts)
    print_result(output)


run()
os.remove("nornir.log")

# docs = input("\n\nRun Ansible playbook to generate documentation (y/n)? ")
# if docs.lower() == "y":
#     subprocess.Popen('ansible-playbook playbooks/avd_lab_generate_docs.yml --tags build', shell=True)
