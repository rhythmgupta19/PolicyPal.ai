import asyncio
import json
import websockets

async def test():
    async with websockets.connect('ws://127.0.0.1:8000/ws') as ws:
        # Send a query
        await ws.send(json.dumps({'q': 'health insurance', 'lang': 'hi'}))
        
        # Receive response
        response = await ws.recv()
        data = json.loads(response)
        
        print('✅ WebSocket Test Successful!')
        print(f'Found {len(data.get("schemes", []))} schemes:')
        for scheme in data.get('schemes', []):
            print(f'  • {scheme["name"]}: {scheme["benefit"]}')

asyncio.run(test())
