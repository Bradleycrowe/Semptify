from Semptify import app
client = app.test_client()
# Get tasks
resp_tasks = client.get('/maintenance/tasks')
print('TASKS status', resp_tasks.status_code)
print('TASKS json', resp_tasks.json)
# Run all maintenance tasks
resp_run = client.post('/maintenance/run')
print('RUN status', resp_run.status_code)
print('RUN keys', list(resp_run.json.keys()))
# Fetch status
resp_status = client.get('/maintenance/status')
print('STATUS status', resp_status.status_code)
print('STATUS json keys', list(resp_status.json.keys()))
