"""
Takes as input a CSV file with a large number of hosts and IP addresses and
generates Ansible inventory entries in YAML format for use in Ansible playbooks
"""
import os
import csv
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(searchpath="./"))
template = env.get_template("./inventory.j2") # Jinja template to be applied

DATA_DIR = "./data_files"
ENDPOINT_FILES_DIR = "./inventory_files"
IN_FILE = f"{DATA_DIR}/inventory.csv"
OUT_FILE = f"{ENDPOINT_FILES_DIR}/inventory.yml"

with open(IN_FILE, "r", encoding="utf-8")as f:
    if os.path.exists(OUT_FILE):
        os.remove(OUT_FILE) # Delete file if it exists
    data = csv.reader(f, delimiter=",")
    with open(OUT_FILE, "a", encoding="utf-8") as f:
        f.write("  hosts:\n")
    for row in data:
        switch = row[0]
        mgmt_ip = row[1]

        with open(OUT_FILE, "a", encoding="utf-8") as f:
            output = template.render(switch=switch, mgmt_ip=mgmt_ip)

            f.write(output)
