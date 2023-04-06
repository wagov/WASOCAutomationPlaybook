# Should be run in the directory above the repo folder.

import json
import os

TEMPLATE_FILE = 'template.json'
OUTPUT_FILE = 'CollatedDeployment.json'
REPO = 'WASOCAutomationPlaybook/TaskAutomations' # Change to WAGOV [repo/folder] the rules are being deployed from

template = []
with open(TEMPLATE_FILE, 'r') as f:
    template = json.load(f)

rule_list = []
for folder in os.listdir(REPO):
    # simple check to exclude files
    if not (folder.endswith('.json') or folder.endswith('.md') or folder.startswith('.')):
        rule_list.append(f'{folder}/{folder}.json')

for rule in rule_list:
    json_location = f'{REPO}/{rule}'
    with open(json_location, 'r') as f:
        contents = json.load(f)
        
    displayName = contents['variables']['automationRuleName']
    name = contents['variables']['automationRuleGuid']
    ruleId = contents['variables']['existingRuleId']
    propertyValues = f"[resourceId('Microsoft.OperationalInsights/workspaces/providers/alertRules',parameters('existingWorkspaceName'),'Microsoft.SecurityInsights','{ruleId}')]"

    resources = contents['resources'][0]

    resources['name'] = name
    resources['properties']['displayName'] = displayName
    resources['properties']['triggeringLogic']['conditions'][0]['conditionProperties']['propertyValues'][0] = propertyValues
    
    template['resources'].append(resources)

with open(OUTPUT_FILE, 'w') as f:
    f.writelines(json.dumps(template, indent=2))
