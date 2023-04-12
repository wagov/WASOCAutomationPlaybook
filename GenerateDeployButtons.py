import json
import os
import urllib.parse

# Change to repo rules being deployed from
REPO = 'WASOCAutomationPlaybook/TaskAutomations'
DEPLOY_TO_AZURE = '[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/'
DEPLOY_BASE_URL = ''

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
        unencoded_url = f'https://raw.githubusercontent.com/wagov/{file_location}'
        encoded_url = urllib.parse.quote(unencoded_url)
        final_url = f'{DEPLOY_TO_AZURE}{encoded_url})'
        print(final_url)
        
        deploy_list.append(f"| {rule_name} | {final_url} |")
        
with open('deploy.md', 'w') as f:
    for line in deploy_list:
        f.write(f'{line}\n')
