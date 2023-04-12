# Script should be run in the directory above the repo folder.

import json
import os
import urllib.parse

# Change to the [repo/folder] for the rules that are being deployed
REPO = 'WASOCAutomationPlaybook-main/TaskAutomations'
DEPLOY_BASE_URL = '[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https://raw.githubusercontent.com/wagov/'

rule_list = []
deploy_list = []
deploy_list.append("| **Rule Name** | **Deploy Rule** |")
deploy_list.append("|-|-|")

for folder in os.listdir(REPO):
    # simple check to exclude files
    if not (folder.endswith('.json') or folder.endswith('.md') or folder.startswith('.')):
        rule_list.append(f'{folder}/{folder}.json')
        
for rule in rule_list:
    file_location = f'{REPO}/{rule}'
    with open(file_location, 'r') as f:
        data = json.load(f)
        rule_name = data['variables']['automationRuleName']
        unencoded_url = f'{DEPLOY_BASE_URL}{file_location}'
        deploy_link = urllib.parse.quote(unencoded_url)
        deploy_list.append(f"| {rule_name} | {deploy_link} |")
        
with open('deploy.md', 'w') as f:
    for line in deploy_list:
        f.write(f'{line}\n')
