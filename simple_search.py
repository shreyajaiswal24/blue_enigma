#!/usr/bin/env python3
# Simple search without OpenAI chat - just shows results
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from neo4j import GraphDatabase
import config

# Initialize
model = SentenceTransformer('all-MiniLM-L6-v2')
pc = Pinecone(api_key=config.PINECONE_API_KEY)
index = pc.Index(config.PINECONE_INDEX_NAME)
driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))

def search_vietnam(query):
    print(f"🔍 Searching: {query}")
    print("=" * 50)
    
    # Get embeddings and search
    vec = model.encode([query])[0].tolist()
    results = index.query(vector=vec, top_k=5, include_metadata=True)
    
    print("🏖️ **SEARCH RESULTS:**")
    for i, match in enumerate(results["matches"], 1):
        meta = match["metadata"]
        score = match.get("score", 0)
        print(f"{i}. **{meta.get('name', 'Unknown')}** ({meta.get('type', 'Unknown')})")
        print(f"   📍 Location: {meta.get('city', 'Unknown')}")
        print(f"   ⭐ Relevance: {score:.3f}")
        print()
    
    # Get graph connections
    node_ids = [m["id"] for m in results["matches"]]
    with driver.session() as session:
        for nid in node_ids[:3]:  # Check top 3
            q = "MATCH (n:Entity {id:$nid})-[r]-(m:Entity) RETURN m.name AS name, type(r) AS rel LIMIT 3"
            connections = session.run(q, nid=nid)
            for conn in connections:
                print(f"🔗 Connected to: {conn['name']} ({conn['rel']})")
    
    print("\n✅ Search complete!")

def interactive_search():
    print("🏮 **Vietnam Travel Search** (No OpenAI needed)")
    print("Type your travel questions. Type 'exit' to quit.")
    
    while True:
        query = input("\n❓ Your question: ").strip()
        if not query or query.lower() in ("exit", "quit"):
            break
        search_vietnam(query)
        print("-" * 60)

if __name__ == "__main__":
    interactive_search()
    driver.close()