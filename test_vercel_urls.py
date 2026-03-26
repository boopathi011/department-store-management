import urllib.request
import json

urls = [
    "https://department-store-management.vercel.app/api/products",
    "https://department-store-management-pd6dl0scu.vercel.app/api/products"
]

for url in urls:
    print(f"\nTesting {url} ...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            print(f"Status: {response.status}")
            data = response.read().decode('utf-8')
            try:
                parsed = json.loads(data)
                print(f"Response: JSON array of length {len(parsed)}" if isinstance(parsed, list) else f"Response: JSON object keys {list(parsed.keys())}")
            except Exception:
                print(f"Response (first 100 chars): {data[:100]}")
    except urllib.error.HTTPError as e:
        print(f"HTTPError Status: {e.code}")
        body = e.read().decode('utf-8')
        try:
            parsed = json.loads(body)
            print(f"Error JSON: {parsed}")
        except Exception:
            print(f"Error Body (first 100 chars): {body[:100]}")
    except Exception as e:
        print(f"Exception: {str(e)}")
