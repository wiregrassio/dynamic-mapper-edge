#!/usr/bin/env python

import json, random, subprocess
from datetime import datetime

# Read the template from the JSON file
with open('template.json', 'r') as f:
    template = json.loads(f.read())[0]

# sample message
message = {
    'id': 'Postman',
    'type': 'temperature',
    'value': random.randint(0, 100),
    'time': str(datetime.now().isoformat())
}

# Convert message and template to JSON strings
message_json = json.dumps(message)
template_json = json.dumps(template)

# Call the mapper.py script with the message and template as arguments
result = subprocess.run(
    ['python', 'mapper.py', '--message', message_json, '--pretty'], 
    capture_output=True, 
    text=True
)

print("return code: ", result.returncode)
print("stdout: ", result.stdout)
print("stderr: ", result.stderr)