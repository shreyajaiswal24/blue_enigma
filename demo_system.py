#!/usr/bin/env python3
# Demo the hybrid system without OpenAI chat
import json
from typing import List
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from neo4j import GraphDatabase
import config

# Config
EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
TOP_K = 5

# Initialize clients
pc = Pinecone(api_key=config.PINECONE_API_KEY)
index = pc.Index(config.PINECONE_INDEX_NAME)

# Connect to Neo4j
driver = GraphDatabase.driver(
    config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
)

def embed_text(text: str) -> List[float]:
    """Get embedding for a text string using Hugging Face."""
    return EMBED_MODEL.encode([text])[0].tolist()

def pinecone_query(query_text: str, top_k=TOP_K):
    """Query Pinecone index using embedding."""
    vec = embed_text(query_text)
    res = index.query(
        vector=vec,
        top_k=top_k,
        include_metadata=True,
        include_values=False
    )
    return res["matches"]

def fetch_graph_context(node_ids: List[str]):
    """Fetch neighboring nodes from Neo4j."""
    facts = []
    with driver.session() as session:
        for nid in node_ids:
            q = (
                "MATCH (n:Entity {id:$nid})-[r]-(m:Entity) "
                "RETURN type(r) AS rel, labels(m) AS labels, m.id AS id, "
                "m.name AS name, m.type AS type, m.description AS description "
                "LIMIT 5"
            )
            recs = session.run(q, nid=nid)
            for r in recs:
                facts.append({
                    "source": nid,
                    "rel": r["rel"],
                    "target_id": r["id"],
                    "target_name": r["name"],
                    "target_desc": (r["description"] or "")[:200],
                })
    return facts

def demo_query(query_text: str):
    """Demo a query showing both vector and graph results."""
    print(f"🔍 Query: {query_text}")
    print("=" * 60)
    
    # Get vector search results
    matches = pinecone_query(query_text, top_k=TOP_K)
    print(f"\n📊 Vector Search Results (Top {len(matches)}):")
    for i, m in enumerate(matches, 1):
        meta = m["metadata"]
        score = m.get("score", 0)
        print(f"{i}. {meta.get('name', 'Unknown')} ({meta.get('type', 'Unknown')})")
        print(f"   ID: {m['id']} | Score: {score:.3f}")
        print(f"   Location: {meta.get('city', 'Unknown')}")
        print()
    
    # Get graph relationships
    match_ids = [m["id"] for m in matches]
    graph_facts = fetch_graph_context(match_ids)
    
    print(f"🔗 Graph Relationships ({len(graph_facts)} found):")
    for fact in graph_facts[:10]:  # Show top 10
        print(f"• {fact['source']} -[{fact['rel']}]-> {fact['target_name']}")
        if fact['target_desc']:
            print(f"  {fact['target_desc'][:100]}...")
        print()
    
    print("✅ Demo complete!")
    return matches, graph_facts

# Run demo queries
print("🏮 Vietnam Travel Assistant Demo")
print("Using FREE Hugging Face embeddings + Neo4j + Pinecone")
print("=" * 60)

queries = [
    "What are the best places to visit in Hanoi?",
    "Beach destinations in Vietnam",
    "Cultural attractions in Ho Chi Minh City"
]

for i, query in enumerate(queries, 1):
    print(f"\n🔸 Demo {i}/3")
    demo_query(query)
    print("-" * 60)

driver.close()
print("\n🎉 All demos complete! The hybrid system is working perfectly!")