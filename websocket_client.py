#!/usr/bin/env python3
"""WebSocket-based Real-Time Chat Client for AI Assistant"""

import asyncio
import json
import sys

try:
    import websockets
except ImportError:
    print("❌ websockets library not found!")
    print("Install it with: pip install websockets")
    sys.exit(1)


async def chat_live():
    """Connect to WebSocket and chat in real-time"""
    uri = "ws://127.0.0.1:8001/ws"
    
    print("=" * 70)
    print("🤖 AI ASSISTANT - REAL-TIME WEBSOCKET CHAT")
    print("=" * 70)
    print("\nConnecting to WebSocket server...\n")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected! You can now chat with the AI.\n")
            print("Type 'quit' or 'exit' to stop\n")
            
            while True:
                try:
                    # Get user input
                    query = input("💬 Your query: ").strip()
                    
                    if not query:
                        continue
                    
                    if query.lower() in ['quit', 'exit']:
                        print("\n👋 Goodbye!")
                        break
                    
                    # Get language preference
                    lang = input("   Language (hi/ta/te/bn/mr) [default: hi]: ").strip() or "hi"
                    
                    # Send to WebSocket server
                    print("\n⏳ Searching schemes...\n")
                    await websocket.send(json.dumps({
                        "q": query,
                        "lang": lang
                    }))
                    
                    # Receive response
                    response = await websocket.recv()
                    data = json.loads(response)
                    
                    # Display results
                    if "error" in data:
                        print(f"❌ Error: {data['error']}\n")
                        continue
                    
                    schemes = data.get('schemes', [])
                    
                    if not schemes:
                        print("❌ No schemes found. Try a different query.\n")
                        continue
                    
                    print(f"✅ Found {len(schemes)} scheme(s):\n")
                    for i, scheme in enumerate(schemes, 1):
                        print(f"{i}. {scheme['name']}")
                        print(f"   💰 {scheme['benefit']}\n")
                    
                except KeyboardInterrupt:
                    print("\n\n👋 Goodbye!")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}\n")
                    
    except ConnectionRefusedError:
        print("❌ Connection failed!")
        print("Make sure the server is running:")
        print("  python -m uvicorn src.main:app --host 127.0.0.1 --port 8000")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(chat_live())
