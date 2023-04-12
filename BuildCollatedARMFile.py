# Should be run in the directory above the repo folder.

import json
import os

TEMPLATE_FILE = 'template.json'
OUTPUT_FILE = 'CollatedDeployment.json'
REPO = 'WASOCAutomationPlaybook/TaskAutomations' # Change to WAGOV [repo/folder] the rules are being deployed from

# Load the template file
template = []
with open(TEMPLATE_FILE, 'r') as f:
    template = json.load(f)

# Create a list of the automations that will be added to the template folder
# by iterating through the `REPO` folder. This enforces a strict naming convention
# where each folder name has an identical name to the file inside, with the file
# having a `.json` extension. The script will fail if the naming convention isn't
# followed
rule_list = []
for folder in os.listdir(REPO):
    # simple check to exclude files
    if not (folder.endswith('.json') or folder.endswith('.md') or folder.startswith('.')):
        rule_list.append(f'{folder}/{folder}.json')

# Iterate over each rule discovered in the previous step and load the contents
# into a `json` object.
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
