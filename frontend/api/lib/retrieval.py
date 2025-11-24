"""
Retrieval module for querying ChromaDB
"""

import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict


EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class Retriever:
    def __init__(self, chroma_path: str = "./chroma_db"):
        self.chroma_path = chroma_path
        self.client = chromadb.PersistentClient(path=chroma_path)
        self.collection = None
        self.embedding_model = None

    def initialize(self):
        """Initialize embedding model and connect to ChromaDB"""
        print("Initializing retrieval system...")

        # Load embedding model
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

        # Get collection
        try:
            self.collection = self.client.get_collection("sierra_knowledge")
            count = self.collection.count()
            print(f"Connected to collection with {count} documents")

            if count == 0:
                print("Warning: Collection is empty. Run ingestion first.")
        except Exception as e:
            print(f"Error: Could not find collection. Run ingestion first.")
            print(f"Exception: {e}")
            raise e

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve top-k most relevant chunks for a query"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()

        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        # Format results
        retrieved_docs = []

        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                doc = {
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                }
                retrieved_docs.append(doc)

        return retrieved_docs

    def format_context(self, docs: List[Dict]) -> str:
        """Format retrieved documents into context string for Claude"""
        if not docs:
            return "No relevant information found."

        context_parts = []

        for i, doc in enumerate(docs, 1):
            title = doc['metadata'].get('title', 'Unknown')
            url = doc['metadata'].get('url', '')
            content = doc['content']

            context_parts.append(
                f"[Source {i}: {title}]\n"
                f"URL: {url}\n"
                f"{content}"
            )

        return "\n\n---\n\n".join(context_parts)

    def get_unique_sources(self, docs: List[Dict]) -> List[str]:
        """Extract unique source URLs from retrieved documents"""
        sources = set()
        for doc in docs:
            url = doc['metadata'].get('url', '')
            if url:
                sources.add(url)
        return list(sources)


# Test the retriever
if __name__ == "__main__":
    retriever = Retriever()
    retriever.initialize()

    # Test query
    test_query = "What are Sierra's core values?"
    print(f"\n🔍 Test query: {test_query}\n")

    docs = retriever.retrieve(test_query, top_k=3)

    print(f"Retrieved {len(docs)} documents:\n")
    for i, doc in enumerate(docs, 1):
        print(f"Document {i}:")
        print(f"  Title: {doc['metadata']['title']}")
        print(f"  URL: {doc['metadata']['url']}")
        print(f"  Content preview: {doc['content'][:150]}...")
        print()
