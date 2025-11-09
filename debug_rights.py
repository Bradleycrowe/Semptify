from learning_adapter import LearningAdapter

adapter = LearningAdapter({
    'location': 'Minneapolis, MN',
    'issue_type': 'maintenance',
    'stage': 'HAVING_TROUBLE'
})

print(f"Location: {adapter.location}")
print(f"Issue type: {adapter.issue_type}")
print(f"Stage: {adapter.stage}")

dashboard = adapter.build_dashboard()
json_data = dashboard.to_json()

for comp in json_data['components']:
    if comp['component']['type'] == 'RightsComponent':
        print(f"\nRights component:")
        print(f"Content: {comp['component']['content']}")
        print(f"HTML contains 'Maintenance': {'Maintenance' in comp['component']['html']}")
        print(f"HTML contains 'maintenance': {'maintenance' in comp['component']['html']}")
        print(f"HTML contains 'Repair': {'Repair' in comp['component']['html']}")
        print(f"\nFirst 800 chars of HTML:")
        print(comp['component']['html'][:800])
