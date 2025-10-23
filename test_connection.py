#!/usr/bin/env python3
import config
from neo4j import GraphDatabase

print("Testing Neo4j connection...")
print(f"URI: {config.NEO4J_URI}")
print(f"User: {config.NEO4J_USER}")
print(f"Password: {'*' * len(config.NEO4J_PASSWORD)}")

try:
    driver = GraphDatabase.driver(
        config.NEO4J_URI, 
        auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
    )
    
    with driver.session() as session:
        result = session.run("RETURN 'Connection successful!' as message")
        record = result.single()
        print(f"✅ {record['message']}")
        
    driver.close()
    print("✅ Neo4j connection test passed!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nPlease verify:")
    print("1. Neo4j instance is running")
    print("2. Connection URI is correct")
    print("3. Username and password are correct")