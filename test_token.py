import urllib.request
import json

base_url = "https://department-store-management.vercel.app/api"

print("Logging in...")
req = urllib.request.Request(f"{base_url}/login", data=json.dumps({"username":"admin", "password":"password"}).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        token = data.get('token')
        print(f"Token: {token[:10]}...")
        
        print("Testing protected route...")
        req2 = urllib.request.Request(f"{base_url}/admin/stats", headers={'Authorization': f'Bearer {token}'})
        with urllib.request.urlopen(req2) as resp2:
            print(f"Status: {resp2.status}")
except urllib.error.HTTPError as e:
    print(f"Error {e.code}: {e.read().decode()}")
