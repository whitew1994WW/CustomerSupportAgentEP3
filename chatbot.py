from langgraph.graph import StateGraph, MessagesState
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from tools import query_knowledge_base, search_for_product_reccommendations

import os


prompt = """#Purpose 

You are a customer service chatbot for a flower shop company. You can help the customer achieve the goals listed below.

#Goals

1. Answer questions the user might have relating to serivces offered
2. Recommend products to the user based on their preferences

#Tone

Helpful and friendly. Use gen-z emojis to keep things lighthearted. You MUST always include a funny flower related pun in every response."""

chat_template = ChatPromptTemplate.from_messages(
    [
        ('system', prompt),
        ('placeholder', "{messages}")
    ]
)

with open('./.env', 'r', encoding='utf-8') as f:
    for line in f:
        key, value = line.strip().split('=')
        os.environ[key] = value

tools = [query_knowledge_base, search_for_product_reccommendations]

llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=os.environ['OPENAI_API_KEY']
)

llm_with_prompt = chat_template | llm.bind_tools(tools)


def call_agent(message_state: MessagesState):
    
    response = llm_with_prompt.invoke(message_state)

    return {
        'messages': [response]
    }

def is_there_tool_calls(state: MessagesState):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return 'tool_node'
    else:
        return '__end__'


graph = StateGraph(MessagesState)

tool_node = ToolNode(tools)

graph.add_node('agent', call_agent)
graph.add_node('tool_node', tool_node)

graph.add_conditional_edges(
    "agent",
    is_there_tool_calls
)
graph.add_edge('tool_node', 'agent')

graph.set_entry_point('agent')

app = graph.compile()

