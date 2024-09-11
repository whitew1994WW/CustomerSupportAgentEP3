import streamlit as st
from vector_store import FlowerShopVectorStore
from chatbot import app
from langchain_core.messages import AIMessage, HumanMessage


st.set_page_config(layout='wide', page_title='Flower Shop Chatbot', page_icon='💐')

if 'message_history' not in st.session_state:
    st.session_state.message_history = [AIMessage(content="Hiya, Im the flower shop chatbot. How can I help?")]

left_col, main_col, right_col = st.columns([1, 2, 1])

# 1. Buttons for chat - Clear Button

with left_col:
    if st.button('Clear Chat'):
        st.session_state.message_history = []


# 2. Chat history and input
with main_col:
    user_input = st.chat_input("Type here...")

    if user_input:
        st.session_state.message_history.append(HumanMessage(content=user_input))

        response = app.invoke({
            'messages': st.session_state.message_history
        })

        st.session_state.message_history = response['messages']

    for i in range(1, len(st.session_state.message_history) + 1):
        this_message = st.session_state.message_history[-i]
        if isinstance(this_message, AIMessage):
            message_box = st.chat_message('assistant')
        else:
            message_box = st.chat_message('user')
        message_box.markdown(this_message.content)
# 3. State variables
