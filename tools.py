from langchain_core.tools import tool
from typing import List, Dict
from vector_store import FlowerShopVectorStore

vector_store = FlowerShopVectorStore()


@tool
def query_knowledge_base(query: str) -> List[Dict[str, str]]:
    """
    Looks up information in a knowledge base to help with answering customer questions and getting information on business processes.

    Args:
        query (str): Question to ask the knowledge base

    Return:
        List[Dict[str, str]]: Potentially relevant question and answer pairs from the knowledge base
    """
    return vector_store.query_faqs(query=query)



@tool
def search_for_product_reccommendations(description: str):
    """
    Looks up information in a knowledge base to help with product recommendation for customers. For example:

    "Boquets suitable for birthdays, maybe with red flowers"
    "A large boquet for a wedding"
    "A cheap boquet with wildflowers"

    Args:
        query (str): Description of product features

    Return:
        List[Dict[str, str]]: Potentially relevant products
    """
    return vector_store.query_inventories(query=description)