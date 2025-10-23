#!/usr/bin/env python3
# Fix Neo4j connection issues
from neo4j import GraphDatabase
import config
import time

def test_and_fix_neo4j():
    print("🔧 Testing and fixing Neo4j connection...")
    
    try:
        # Create new driver with better configuration
        driver = GraphDatabase.driver(
            config.NEO4J_URI, 
            auth=(config.NEO4J_USER, config.NEO4J_PASSWORD),
            max_connection_lifetime=3600,  # 1 hour
            max_connection_pool_size=50,
            connection_acquisition_timeout=60,
            encrypted=True,
            trust="TRUST_SYSTEM_CA_SIGNED_CERTIFICATES"
        )
        
        # Test connection
        with driver.session() as session:
            result = session.run("RETURN 'Connection successful!' as message")
            record = result.single()
            print(f"✅ {record['message']}")
            
            # Check node count
            result = session.run("MATCH (n:Entity) RETURN count(n) as count")
            count = result.single()["count"]
            print(f"✅ Found {count} nodes in database")
        
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def reset_neo4j_driver():
    """Update app.py with better Neo4j configuration"""
    print("🔧 Updating Neo4j driver configuration...")
    
    # Read current app.py
    with open('/home/shreya_24/Blue Enigma/app.py', 'r') as f:
        content = f.read()
    
    # Replace the driver initialization
    old_driver = 'driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))'
    
    new_driver = '''driver = GraphDatabase.driver(
    config.NEO4J_URI, 
    auth=(config.NEO4J_USER, config.NEO4J_PASSWORD),
    max_connection_lifetime=3600,
    max_connection_pool_size=10,
    connection_acquisition_timeout=60,
    encrypted=True
)'''
    
    if old_driver in content:
        content = content.replace(old_driver, new_driver)
        
        with open('/home/shreya_24/Blue Enigma/app.py', 'w') as f:
            f.write(content)
        
        print("✅ Updated app.py with better Neo4j configuration")
        return True
    else:
        print("⚠️ Driver config not found in expected format")
        return False

if __name__ == "__main__":
    print("🛠️ Neo4j Connection Fix Tool")
    print("=" * 40)
    
    # Test current connection
    if test_and_fix_neo4j():
        print("\n✅ Neo4j connection is working!")
    else:
        print("\n❌ Connection still failing")
        print("💡 Try these solutions:")
        print("1. Check if your Neo4j AuraDB instance is running")
        print("2. Verify the connection URI is correct")
        print("3. Check if your Neo4j password has expired")
        print("4. Go to https://console.neo4j.io/ and restart your instance")
    
    # Update driver config
    reset_neo4j_driver()
    
    print("\n🔄 Please restart your Flask app:")
    print("   Ctrl+C to stop current app")
    print("   Then run: python3 app.py")