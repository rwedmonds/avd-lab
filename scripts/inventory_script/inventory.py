"""
Takes as input a CSV file with a large number of hosts and IP addresses and
generates Ansible inventory entries in YAML format for use in Ansible playbooks
"""

import csv
import os
from jinja2 import Template

# Ensure the output directory exists
os.makedirs("./inventory_files", exist_ok=True)

# Jinja template as a string
TEMPLATE_STR = """
    "{{ switch }}":
      ansible_host: "{{ mgmt_ip }}"
      {%- if is_deployed == false %}
      is_deployed: {{ is_deployed }}
      {%- endif %}
"""

# Create a Jinja Template instance
template = Template(TEMPLATE_STR)

# Initialize an empty string to hold all rendered templates
ALL_RENDERED = ""

# Path to the CSV file
CSV_FILE_PATH = "./data_files/inventory.csv"

# Read the CSV file
with open(CSV_FILE_PATH, mode='r', newline='', encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)

    # Render the template for each row in the CSV
    for row in reader:
        # Convert `is_deployed` from string to boolean
        row['is_deployed'] = row['is_deployed'].lower() in ['true', '1',
                                                            't', 'y', 'yes']
        ALL_RENDERED += template.render(row)

# Output file path
OUTPUT_FILE_PATH = "./inventory_files/inventory.yml"

# Write the rendered template to the output file
with open(OUTPUT_FILE_PATH, 'w', encoding="utf-8") as output_file:
    output_file.write(ALL_RENDERED)

print("Inventory CSV processed and saved to inventory.yml")
