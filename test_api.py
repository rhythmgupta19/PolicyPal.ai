import urllib.request
import urllib.parse
import json

queries = [
    'health insurance',
    'education',
    'business loan',
    'housing'
]

for q in queries:
    encoded_q = urllib.parse.quote(q)
    url = f'http://127.0.0.1:8000/ask?q={encoded_q}&lang=hi'
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        print(f'\nQuery: {q}')
        print('=' * 60)
        schemes = data.get('schemes', [])
        if schemes:
            for s in schemes:
                print(f'  {s["name"]} - {s["benefit"]}')
        else:
            print('  No schemes found')
    except Exception as e:
        print(f'Error for "{q}": {e}')
