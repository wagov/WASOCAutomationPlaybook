import json
import os
import urllib.parse

# Change to repo rules being deployed from
REPO = 'WASOCAutomationPlaybook/TaskAutomations'
DEPLOY_TO_AZURE = '[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/'
DEPLOY_BASE_URL = ''

rule_list = []
deploy_list = []
table_head = []
table_head.append("| **Rule Name** | **Deploy Rule** |")
table_head.append("|-|-|")

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
        encoded_url = urllib.parse.quote_plus(unencoded_url)
        final_url = f'{DEPLOY_TO_AZURE}{encoded_url})'
        
        deploy_list.append(f"| {rule_name} | {final_url} |")
        
with open('deploy.md', 'w') as f:
    # Sort the list before writing to file
    sorted_list = table_head + sorted(deploy_list)
    for line in sorted_list:
        f.write(f'{line}\n')
