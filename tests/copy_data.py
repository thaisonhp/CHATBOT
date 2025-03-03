from chromadb import PersistentClient

client = PersistentClient(path="./chroma_db")

client.delete_collection("langchain")

