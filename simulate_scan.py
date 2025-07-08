import requests

payload = {
    'tag': 'PART-001',
    'zone': 'Warehouse',
    'subzone': 'A1',
    'technician': 'Alice',
    'job_id': 'JOB-1001'
}

response = requests.post('http://127.0.0.1:5000/api/scan', json=payload)
print(response.json())