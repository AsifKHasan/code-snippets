f = open('messages.json')
d = json.load(f)

# conversations is a list
d = d['conversations']

g_names = ['ActiveNetwork', 'Datacenter&Infrastructure', 'HR&Admin__HR', 'SoftwareServices', 'TEAM360°']
groups = [{'group': g['displayName'], 'messages': g['MessageList']} for g in d if g['displayName'] in g_names]

f = open('skype-messages.json', 'w')
f.write(json.dumps(groups, sort_keys=False, indent=4))

for g in d:
    print(g['displayName'])

c = d[0]
c.keys()
# dict_keys(['id', 'displayName', 'version', 'properties', 'threadProperties', 'MessageList'])
c['id']
c['displayName']
c['version']
c['properties']
c['threadProperties']

# MessageList is a list
ml = c['MessageList']

m = ml[0]
