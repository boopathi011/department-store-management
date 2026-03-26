import urllib.request
import json
import random

base_url = "https://department-store-management.vercel.app/api"
test_user = f"tester_{random.randint(1000, 9999)}"

print(f"Registering {test_user}...")
req = urllib.request.Request(f"{base_url}/register", data=json.dumps({"username":test_user, "name": "Tester", "password":"password", "role":"user"}).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as resp:
        print("Register Status:", resp.status)
except urllib.error.HTTPError as e:
    print(f"Register Error 400: {e.read().decode()}")

print("Logging in...")
req = urllib.request.Request(f"{base_url}/login", data=json.dumps({"username":test_user, "password":"password"}).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        token = data.get('token')
        print(f"Token: {token[:10]}...")
        
        print("Testing protected route /user/stats...")
        req2 = urllib.request.Request(f"{base_url}/user/stats", headers={'Authorization': f'Bearer {token}'})
        try:
            with urllib.request.urlopen(req2) as resp2:
                print(f"Stats Status: {resp2.status}")
                print(resp2.read().decode()[:100])
        except urllib.error.HTTPError as e:
            print(f"Stats Error {e.code}: {e.read().decode()}")
except urllib.error.HTTPError as e:
    print(f"Login Error {e.code}: {e.read().decode()}")
