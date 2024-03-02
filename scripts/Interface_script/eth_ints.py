"""
This script reads .json files containing Ethernet and Port-Channel interfaces,
creates a folder with the device name inventory/host_vars, and creates a
corresponding YAML file in the format <devicename>.yml. It creates a separate
array for each type of interface and lists the interfaces of that type under
that array.
"""

import os
import json
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(searchpath="./"),
                  trim_blocks=True, lstrip_blocks=True)
# ------------------------------------------------------- #
# Ethernet interface template
# ------------------------------------------------------- #
ethernet_template = env.get_template("./mgmt_eth_ints.j2")
# ------------------------------------------------------- #
# Port-Channel interface template
# ------------------------------------------------------- #
port_channel_template = env.get_template("./mgmt_pc_ints.j2")

DATA_DIR = "./data_files"

for filename in os.listdir(DATA_DIR):  # Iterate over all .json files
    in_file = os.path.join(DATA_DIR, filename)  # Complete path to file
    # ------------------------------------------------------- #
    # Create directory in host_vars with device name as the
    # directory name
    # ------------------------------------------------------- #
    output_dir = f"../../inventory/host_vars/{os.path.splitext(filename)[0]}"
    # ------------------------------------------------------- #
    # Create the directory if it doesn't already exist
    # ------------------------------------------------------- #
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    out_file = f"{output_dir}/{os.path.splitext(filename)[0]}.yml"
    # ------------------------------------------------------- #
    # Delete existing file
    # ------------------------------------------------------- #
    if os.path.exists(out_file):
        os.remove(out_file)  # Delete file if it exists

    # ------------------------------------------------------- #
    # Write the Port-Channel interface header before looping
    # through json file
    # ------------------------------------------------------- #
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("""custom_structured_configuration_prefix: [mgmt_]

# Port-Channel Interfaces
mgmt_port_channel_interfaces:
""")

    # ------------------------------------------------------- #
    # Write the Port-Channel interfaces to the output file
    # ------------------------------------------------------- #
    with open(in_file, encoding="utf-8") as f:
        port_channels = json.load(f)
        for port_channel in port_channels["port_channel_interfaces"]:
            name = port_channel["interface"]
            description = port_channel["description"]
            mode = port_channel["mode"]
            allowed_vlans = port_channel["allowed_vlans"]

            with open(out_file, "a", encoding="utf-8") as f:
                output = port_channel_template.render(name=name,
                                                      description=description,
                                                      mode=mode,
                                                      allowed_vlans=allowed_vlans)
                f.write(output)

    # ------------------------------------------------------- #
    # Write the Ethernet interface header prior to looping
    # through json file
    # ------------------------------------------------------- #
    with open(out_file, "a", encoding="utf-8") as f:
        f.write("""# Switched Interfaces
mgmt_ethernet_interfaces:
""")

    # ------------------------------------------------------- #
    # Write the Ethernet interfaces to the output file
    # ------------------------------------------------------- #
    with open(in_file, encoding="utf-8") as f:
        interface_list = json.load(f)
        for interface in interface_list["ethernet_interfaces"]:
            name = interface["interface"]
            description = interface["description"]
            mode = interface["mode"]
            shutdown = interface["shutdown"]
            access_vlan = interface["access_vlan"]
            channel_group = interface["channel_group"]
            channel_mode = interface["channel_mode"]

            with open(out_file, "a", encoding="utf-8") as f:
                output = ethernet_template.render(name=name,
                                                  description=description,
                                                  mode=mode,
                                                  shutdown=shutdown,
                                                  access_vlan=access_vlan,
                                                  channel_group=channel_group,
                                                  channel_mode=channel_mode)
                f.write(output)
