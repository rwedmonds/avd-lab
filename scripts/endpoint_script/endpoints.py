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

import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(searchpath="./"))
template = env.get_template("./endpoints.j2")  # Jinja template to be applied

DATA_DIR = "./data_files"
ENDPOINT_FILES_DIR = "./endpoint_files"

for filename in os.listdir(DATA_DIR):  # Iterate over all .csv files
    in_file = os.path.join(DATA_DIR, filename)  # Complete path to file
    df = pd.read_csv(in_file)  # Load in_file as pandas dataframe
    out_file = f"{ENDPOINT_FILES_DIR}/{os.path.splitext(filename)[0]}.yml"
    if os.path.exists(out_file):
        os.remove(out_file)  # Delete file if it exists
    endpoints_dict = {}
    for index, row in df.iterrows():
        ENDPOINT_NAME = row["Endpoint Name"]
        ENDPOINT_PORT1 = row["Endpoint Port 1"]
        ENDPOINT_PORT2 = row["Endpoint Port 2"]
        ENDPOINT_PORT3 = row["Endpoint Port 3"]
        ENDPOINT_PORT4 = row["Endpoint Port 4"]
        SWITCH1_PORT1 = str(row["Switch1 Port 1"]
                            ).capitalize().replace(" ", "")
        SWITCH2_PORT1 = str(row["Switch2 Port 1"]
                            ).capitalize().replace(" ", "")
        SWITCH1_PORT2 = str(row["Switch1 Port 2"]
                            ).capitalize().replace(" ", "")
        SWITCH2_PORT2 = str(row["Switch2 Port 2"]
                            ).capitalize().replace(" ", "")
        SWITCH1 = row["Switch 1"]
        SWITCH2 = row["Switch 2"]
        port_profile = row["Port Profile"]

        # If server is already in endpoints_dict, append these fields
        if ENDPOINT_NAME in endpoints_dict:
            endpoints_dict[ENDPOINT_NAME].append(SWITCH1_PORT1)
            endpoints_dict[ENDPOINT_NAME].append(SWITCH2_PORT1)
            endpoints_dict[ENDPOINT_NAME].append(SWITCH1_PORT2)
            endpoints_dict[ENDPOINT_NAME].append(SWITCH2_PORT2)
            endpoints_dict[ENDPOINT_NAME].append(ENDPOINT_PORT1)
            endpoints_dict[ENDPOINT_NAME].append(ENDPOINT_PORT2)
            endpoints_dict[ENDPOINT_NAME].append(ENDPOINT_PORT3)
            endpoints_dict[ENDPOINT_NAME].append(ENDPOINT_PORT4)
        else:
            endpoints_dict[ENDPOINT_NAME] = [
                ENDPOINT_NAME, ENDPOINT_PORT1, ENDPOINT_PORT2, ENDPOINT_PORT3,
                ENDPOINT_PORT4, SWITCH1_PORT1, SWITCH2_PORT1, SWITCH1_PORT2,
                SWITCH2_PORT2, SWITCH1, SWITCH2, port_profile
            ]

    # This is where we apply the Jinja template
    for item, values in endpoints_dict.items():
        print(item, values)
        ENDPOINT_NAME = item
        ENDPOINT_PORT1 = str(values[1])
        ENDPOINT_PORT2 = str(values[2])
        ENDPOINT_PORT3 = str(values[3])
        ENDPOINT_PORT4 = str(values[4])
        SWITCH1_PORT1 = str(values[5])
        SWITCH2_PORT1 = str(values[6])
        SWITCH1_PORT2 = str(values[7])
        SWITCH2_PORT2 = str(values[8])
        SWITCH1 = values[9]
        SWITCH2 = values[10]
        port_profile = values[11]

        with open(out_file, "a", encoding="utf-8") as f:
            output = template.render(
                endpoint_name=ENDPOINT_NAME, endpoint_port1=ENDPOINT_PORT1,
                endpoint_port2=ENDPOINT_PORT2, endpoint_port3=ENDPOINT_PORT3,
                endpoint_port4=ENDPOINT_PORT4, switch1_port1=SWITCH1_PORT1,
                switch2_port1=SWITCH2_PORT1, switch1_port2=SWITCH1_PORT2,
                switch2_port2=SWITCH2_PORT2, switch1=SWITCH1, switch2=SWITCH2,
                port_profile=port_profile
            )

            f.write(output)
