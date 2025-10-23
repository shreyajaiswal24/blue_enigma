# Demo Configuration for Blue Enigma Vietnam Travel Assistant
# This is a demo config with mock values for running the application without real APIs

NEO4J_URI = "neo4j://localhost:7687"  # Mock URI for demo
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"  # Mock password for demo

OPENAI_API_KEY = "sk-demo-key-for-video"  # Mock API key for demo

PINECONE_API_KEY = "demo-pinecone-key"  # Mock API key for demo
PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = "vietnam-travel"
PINECONE_VECTOR_DIM = 384        # For sentence-transformers all-MiniLM-L6-v2 model