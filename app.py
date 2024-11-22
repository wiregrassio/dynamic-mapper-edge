#!/usr/bin/env python

import json, jsonata, argparse

api_topics = {
    'MEASUREMENT': 'c8y/measurement/measurements/create',
    'EVENT': 'c8y/event/events/create',
    'ALARM': 'c8y/alarm/alarms/create'
}

class TemplateValidationError(Exception):
    pass

class SubstitutionError(Exception):
    pass

#takes dot notation path and sets value in nested dictionary
def set_nested_value(data, path, value):
    keys = path.split('.')
    for key in keys[:-1]:
        data = data.setdefault(key, {})
    data[keys[-1]] = value

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--message', type=str, required=True, help='The message in JSON format')
    parser.add_argument('--pretty', action='store_true', help='Pretty Print flag') #used by debugger
    args = parser.parse_args()

    inbound_message = json.loads(args.message)
    with open('template.json', 'r') as f:
        template = json.loads(f.read())[0]

    # Validate Template
    if template['direction'] != 'INBOUND':
        raise TemplateValidationError('This Mapper Only Accepts Inbound Templates')
    
    elif template['mappingType'] != 'JSON':
        raise TemplateValidationError('This Mapper Only Accepts JSON Mappings')

    #Load Template
    outbound_message = json.loads(template['target']) 
    topic = template['subscriptionTopic'] #not currently implimented
    substitutions = template['substitutions']

    for sub in substitutions:
        query = jsonata.Jsonata(sub['pathSource'])
        result = query.evaluate(inbound_message)

        if result == None:
            raise SubstitutionError(f'"{sub["pathSource"]}" Field Not Found in Message')
        else:
            set_nested_value(outbound_message, sub['pathTarget'], result) 

    # Remove the "source" key from outbound_message as thin-edge doesn't use it
    outbound_message.pop('source', None)

    payload = {
        'message': outbound_message,
        'topic': api_topics[template['targetAPI']]
    }

    if args.pretty: 
        print(json.dumps(payload, indent=2))
    
    else: 
        print(json.dumps(payload))

    exit(0)