#!/usr/bin/env python3
import requests
import json
import time

API_URL = "http://localhost:5000/api"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing API health...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        data = response.json()
        print(f"✅ Health: {data}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_stats():
    """Test stats endpoint"""
    print("\n📊 Testing stats endpoint...")
    try:
        response = requests.get(f"{API_URL}/stats", timeout=10)
        data = response.json()
        print(f"✅ Stats: {data}")
        return True
    except Exception as e:
        print(f"❌ Stats failed: {e}")
        return False

def test_search(query):
    """Test search endpoint"""
    print(f"\n🔍 Testing search: '{query}'")
    try:
        response = requests.post(
            f"{API_URL}/search", 
            json={"query": query},
            timeout=30
        )
        data = response.json()
        
        if data.get('success'):
            print(f"✅ Found {data['total_found']} results")
            for i, result in enumerate(data['results'][:3], 1):
                print(f"  {i}. {result['name']} ({result['type']}) - Score: {result['score']}")
            
            if data['connections']:
                print(f"  🔗 {len(data['connections'])} connections found")
        else:
            print(f"❌ Search failed: {data.get('error')}")
        
        return True
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return False

def main():
    print("🧪 Testing Blue Enigma Web API")
    print("=" * 50)
    
    # Wait for server to be ready
    print("⏳ Waiting for server...")
    time.sleep(3)
    
    # Test endpoints
    if not test_health():
        print("❌ Server not ready, exiting...")
        return
    
    test_stats()
    
    # Test searches
    queries = [
        "Best places in Hanoi",
        "Beach destinations Vietnam",
        "Cultural attractions Ho Chi Minh City"
    ]
    
    for query in queries:
        test_search(query)
    
    print("\n🎉 API testing complete!")
    print("\n🌐 Open your browser to: http://localhost:5000")
    print("   Try the beautiful web interface!")

if __name__ == "__main__":
    main()