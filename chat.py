#!/usr/bin/env python3
"""Interactive chat interface for AI Assistant"""

import urllib.request
import urllib.parse
import json
import sys

def ask_scheme(query, lang="hi"):
    """Query the AI assistant"""
    try:
        encoded_q = urllib.parse.quote(query)
        url = f'http://127.0.0.1:8000/ask?q={encoded_q}&lang={lang}'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        return data
    except Exception as e:
        return {"error": str(e), "schemes": []}

def format_response(data):
    """Pretty print the response"""
    schemes = data.get('schemes', [])
    
    if not schemes:
        print("❌ No schemes found. Try a different query.\n")
        return
    
    print(f"\n✅ Found {len(schemes)} scheme(s):\n")
    for i, scheme in enumerate(schemes, 1):
        print(f"{i}. {scheme['name']}")
        print(f"   💰 {scheme['benefit']}\n")

def main():
    """Interactive chat loop"""
    print("=" * 70)
    print("🤖 AI ASSISTANT - INDIAN GOVERNMENT SCHEMES")
    print("=" * 70)
    print("\nAsk about government schemes (health, education, business, housing, etc.)")
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
            
            # Ask AI
            print("\n⏳ Searching schemes...")
            response = ask_scheme(query, lang)
            
            # Display results
            format_response(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()
