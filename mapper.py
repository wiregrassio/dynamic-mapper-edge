#!/usr/bin/env python

import json

def set_nested_value(data, path, value):
    keys = path.split('.')
    for key in keys[:-1]:
        data = data.setdefault(key, {})
    data[keys[-1]] = value

# Open and read the JSON file into a string
with open('mapping.json', 'r') as f:
    template_string = f.read()

template = json.loads(template_string)

for mapping in template:
    print (mapping)

exit()

print (mapping)

path = "target.kafka_TemperatureMeasurement.processTemp.value"
new_value = 42

set_nested_value(mapping, path, new_value)

print (mapping)

exit()
# Convert the mapping dictionary to a JSON string
mapping_json = json.dumps(mapping, indent=4)



# Write the JSON string to a file
with open('filtered_mapping.json', 'w') as file:
    file.write(mapping_json)