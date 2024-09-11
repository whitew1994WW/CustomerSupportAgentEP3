from chromadb import PersistentClient, EmbeddingFunction, Embeddings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from typing import List
import json


MODEL_NAME = 'dunzhang/stella_en_1.5B_v5'
DB_PATH = './.chroma_db'
FAQ_FILE_PATH= './FAQ.json'
INVENTORY_FILE_PATH = './inventory.json'

class Product:
    def __init__(self, name: str, id: str, description: str, type: str, price: float, quantity: int):
        self.name = name
        self.id = id
        self.description = description
        self.type = type
        self.price = price
        self.quantity = quantity

class QuestionAnswerPairs:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer

class CustomEmbeddingClass(EmbeddingFunction):
    def __init__(self, model_name):
        self.embedding_model = HuggingFaceEmbedding(model_name=MODEL_NAME)

    def __call__(self, input_texts: List[str]) -> Embeddings:
        return [self.embedding_model.get_text_embedding(text) for text in input_texts]



class FlowerShopVectorStore:
    def __init__(self):
        db = PersistentClient(path=DB_PATH)

        custom_embedding_function = CustomEmbeddingClass(MODEL_NAME)

        self.faq_collection = db.get_or_create_collection(name='FAQ', embedding_function=custom_embedding_function)
        self.inventory_collection = db.get_or_create_collection(name='Inventory', embedding_function=custom_embedding_function)

        if self.faq_collection.count() == 0:
            self._load_faq_collection(FAQ_FILE_PATH)

        if self.inventory_collection.count() == 0:
            self._load_inventory_collection(INVENTORY_FILE_PATH)

    def _load_faq_collection(self, faq_file_path: str):
        with open(faq_file_path, 'r') as f:
            faqs = json.load(f)

        self.faq_collection.add(
            documents=[faq['question'] for faq in faqs] + [faq['answer'] for faq in faqs],
            ids=[str(i) for i in range(0, 2*len(faqs))],
            metadatas = faqs + faqs
        )

    def _load_inventory_collection(self, inventory_file_path: str):
        with open(inventory_file_path, 'r') as f:
            inventories = json.load(f)

        self.inventory_collection.add(
            documents=[inventory['description'] for inventory in inventories],
            ids=[str(i) for i in range(0, len(inventories))],
            metadatas = inventories
        )

    def query_faqs(self, query: str): 
        return self.faq_collection.query(query_texts=[query], n_results=5)
    
    def query_inventories(self, query: str):
        return self.inventory_collection.query(query_texts=[query], n_results=5)
