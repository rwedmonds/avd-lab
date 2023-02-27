"""
This script reads .csv files containing information about servers connected
to switches and writes the connected_endpoints YAML definitions for use in your
Ansible AVD files using a Jinja template. It searches for duplicate server
names and, if found, combines the entries into a single entry in a list of
dictionaries with all of information presented only once, as Ansible expects.
This is an example of a row of CSV data used to generate the Ansible output,
with the fields signifying, in order, the local switch port, server name,
server port1, server port2, port profile to be assigned, switch1 hostname,
and switch2 hostname:

Ethernet1/1,server01,eth4,eth2,nutanix,switch01,switch02

The following is an example output, which would be placed under the
servers key in a connected_endpoints file:

  server01:
    adapters:
      - endpoint_ports: [eth4, eth2, eth5, eth3]
        switch_ports: [Ethernet1/1, Ethernet3/1, Ethernet1/1, Ethernet3/1]
        switches: [switch01, switch01, switch02, switch02]
        profile: nutanix 
"""

import csv
import os
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(searchpath="./"))
template = env.get_template("./endpoints.j2") # Jinja template to be applied

DATA_DIR = "./data_files"
ENDPOINT_FILES_DIR = "./endpoint_files"

for filename in os.listdir(DATA_DIR): # Iterate over all .csv files
    in_file = os.path.join(DATA_DIR, filename) # Complete path to file
    out_file = f"{ENDPOINT_FILES_DIR}/{os.path.splitext(filename)[0]}.yml"
    if os.path.exists(out_file):
        os.remove(out_file) # Delete file if it exists
    endpoints_dict = {}
    with open(in_file, "r", encoding=str)as f:
        rows = csv.reader(f, delimiter=",")
        for port, description, remote_port1, remote_port2, port_profile,\
            switch1, switch2 in rows:
            # If server is already in endpoints_dict, append these fields
            if description in endpoints_dict:
                endpoints_dict[description].append(port)
                endpoints_dict[description].append(remote_port1)
                endpoints_dict[description].append(remote_port2)
            # Otherwise, create a new dictionary entry
            else:
                endpoints_dict[description] = [port, remote_port1, remote_port2,\
                port_profile, switch1, switch2]

    # This is where we apply the Jinja template
    for item, values in endpoints_dict.items():
        port1 = values[0]
        port2 = values[6]
        description = item
        remote_port1 = values[1]
        remote_port2 = values[2]
        remote_port3 = values[7]
        remote_port4 = values[8]
        port_profile = values[3]
        switch1 = values[4]
        switch2 = values[5]

        with open(out_file, "a", encoding=str) as f:
            output = template.render(port1=port1, port2=port2,\
            description=description, remote_port1=remote_port1,\
            remote_port2=remote_port2, remote_port3=remote_port3,\
            remote_port4=remote_port4, port_profile=port_profile,\
            switch1=switch1, switch2=switch2)

            f.write(output)