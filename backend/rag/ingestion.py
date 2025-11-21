"""
Document ingestion pipeline
Processes scraped content, chunks it, generates embeddings, and stores in ChromaDB
"""

import json
from typing import List, Dict
from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import hashlib
import re
import unicodedata
from typing import List
import nltk
from nltk.tokenize import sent_tokenize

# Configuration
CHUNK_SIZE = 800
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class DocumentIngestion:
    def __init__(self, chroma_path: str = "./chroma_db"):
        self.chroma_path = chroma_path
        self.client = chromadb.PersistentClient(path=chroma_path)
        self.collection = None
        self.embedding_model = None

    def initialize(self):
        """Initialize embedding model and ChromaDB collection"""
        print("Initializing ingestion pipeline...")

        # Load embedding model
        print(f"Loading embedding model: {EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

        # Get or create collection
        try:
            self.collection = self.client.get_collection("sierra_knowledge")
            print(f"Found existing collection with {self.collection.count()} documents")
        except:
            self.collection = self.client.create_collection(
                name="sierra_knowledge",
                metadata={"description": "Sierra AI knowledge base"}
            )
            print("Created new collection: sierra_knowledge")

    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 200


    def clean_text_for_rag(self, text: str) -> str:
        text = unicodedata.normalize("NFKC", text)

        text = text.replace("\r\n", "\n").replace("\r", "\n")

        cleaned_lines = []
        for line in text.split("\n"):
            stripped = line.strip()
            if not stripped:
                continue
            if len(stripped) < 4 and not re.search(r"[A-Za-z0-9]", stripped):
                continue
            cleaned_lines.append(stripped)

        text = " ".join(cleaned_lines)

        text = re.sub(r"\s+", " ", text).strip()

        return text


    def chunk_text(self, text: str) -> List[str]:
        
        if not text or not text.strip():
            return []

        text = self.clean_text_for_rag(text)

        sentences = sent_tokenize(text)

        chunks: List[str] = []
        current_chunk_sentences: List[str] = []
        current_len = 0

        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue

            sent_len = len(sent) + 2

            if current_len + sent_len > CHUNK_SIZE:
                if current_chunk_sentences:
                    chunk_text = " ".join(current_chunk_sentences).strip()
                    chunks.append(chunk_text)

                    words = chunk_text.split()

                    approx_words_overlap = max(1, int(CHUNK_OVERLAP / 5))
                    overlap_words = words[-approx_words_overlap:]

                    current_chunk_sentences = [" ".join(overlap_words), sent]
                    current_len = len(" ".join(current_chunk_sentences))
                else:
                    current_chunk_sentences = [sent]
                    current_len = sent_len
            else:
                current_chunk_sentences.append(sent)
                current_len += sent_len

        if current_chunk_sentences:
            chunk_text = " ".join(current_chunk_sentences).strip()
            chunks.append(chunk_text)

        chunks = [c for c in chunks if len(c) > 50]

        return chunks


    def generate_id(self, text: str, metadata: dict) -> str:
        content = f"{metadata['url']}:{text[:100]}"
        return hashlib.md5(content.encode()).hexdigest()

    def ingest_document(self, doc: Dict[str, str]) -> int:
        url = doc['url']
        title = doc['title']
        content = doc['content']

        chunks = self.chunk_text(content)

        if not chunks:
            return 0

        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for i, chunk in enumerate(chunks):
            chunk_id = self.generate_id(chunk, {'url': url, 'index': i})
            ids.append(chunk_id)
            documents.append(chunk)
            metadatas.append({
                'url': url,
                'title': title,
                'chunk_index': i,
                'total_chunks': len(chunks)
            })

        # Generate embeddings
        embeddings = self.embedding_model.encode(documents).tolist()

        # Add to ChromaDB
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

        return len(chunks)

    def ingest_all(self, scraped_content_path: str = "./data/scraped_content.json"):
        
        """Ingest all scraped documents"""
        print(f"Loading scraped content from {scraped_content_path}")

        with open(scraped_content_path, 'r', encoding='utf-8') as f:
            documents = json.load(f)

        print(f"Found {len(documents)} documents to ingest\n")

        total_chunks = 0

        for i, doc in enumerate(documents, 1):
            print(f"[{i}/{len(documents)}] Processing: {doc['title'][:50]}...")
            chunks_added = self.ingest_document(doc)
            total_chunks += chunks_added
            print(f"Added {chunks_added} chunks")

        print(f"\nIngestion complete!")
        print(f"Total documents: {len(documents)}")
        print(f"Total chunks: {total_chunks}")
        print(f"Collection size: {self.collection.count()}")

    def clear_collection(self):
        """Clear all data from the collection"""
        print("Clearing existing collection...")
        self.client.delete_collection("sierra_knowledge")
        self.collection = self.client.create_collection(
            name="sierra_knowledge",
            metadata={"description": "Sierra AI knowledge base"}
        )
        print("Collection cleared")


def main():
    """Run the ingestion pipeline"""
    ingestion = DocumentIngestion()
    ingestion.initialize()

    # ingestion.clear_collection()

    ingestion.ingest_all()


if __name__ == "__main__":
    main()
