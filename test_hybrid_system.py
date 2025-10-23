#!/usr/bin/env python3
import config
from neo4j import GraphDatabase
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

print("🧪 Testing Hybrid System Components...")

# Test Neo4j
print("\n1️⃣ Testing Neo4j...")
try:
    driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))
    with driver.session() as session:
        result = session.run("MATCH (n:Entity) RETURN count(n) as count")
        count = result.single()["count"]
        print(f"✅ Neo4j: {count} nodes loaded")
    driver.close()
except Exception as e:
    print(f"❌ Neo4j error: {e}")

# Test Pinecone
print("\n2️⃣ Testing Pinecone...")
try:
    pc = Pinecone(api_key=config.PINECONE_API_KEY)
    index = pc.Index(config.PINECONE_INDEX_NAME)
    stats = index.describe_index_stats()
    print(f"✅ Pinecone: {stats.total_vector_count} vectors loaded")
except Exception as e:
    print(f"❌ Pinecone error: {e}")

# Test Embeddings
print("\n3️⃣ Testing Embeddings...")
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    test_embedding = model.encode(["Vietnam travel"])
    print(f"✅ Embeddings: {len(test_embedding[0])} dimensions")
except Exception as e:
    print(f"❌ Embeddings error: {e}")

print("\n🎉 System ready for testing!")