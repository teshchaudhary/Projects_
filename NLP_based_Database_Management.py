import streamlit as st
from sqlalchemy import create_engine
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAIChat
from langchain.agents.agent_types import AgentType
from streamlit_extras.add_vertical_space import add_vertical_space
import os
from dotenv import load_dotenv

st.header("SQL - AI")

with st.sidebar:
    st.title('SQL - AI')
    st.markdown('''
    ## These are some Links
    - [GitHub Repository](https://github.com/teshchaudhary/SQL-AI)     
    - [GitHub](https://github.com/teshchaudhary)
    - [LinkedIn](https://www.linkedin.com/in/tesh-chaudhary/)
    ''')
    add_vertical_space(5)
    st.write('Made by Tesh Chaudhary')

def connect_to_database():
    try:
        connection = create_engine("mysql+mysqlconnector://root:Tesh@localhost/classicmodels")
        return connection
    except Exception as err:
        st.error(f"Error: {err}")
        return None

connection = connect_to_database()

if connection:
    load_dotenv()
    st.success("Connection Successful")
    # Creating an SQLDatabase object for structured interaction with the database
    database = SQLDatabase(connection)

    # Initialize the OpenAI model
    llm = OpenAIChat(model_name='gpt-3.5-turbo')

    # Create an SQLDatabaseToolkit
    toolkit = SQLDatabaseToolkit(db = database, llm = llm)

    # Initialize the SQL agent
    agent_executor = create_sql_agent(
        llm = llm,
        toolkit = toolkit,
        verbose = True,
        agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Input a natural language query
    prompt = st.text_input('What do you want to know?')

    # Handle user input and display results
    if st.button('Run'):
        if prompt:
            # Store user query in chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})

            # Get assistant's response
            final = agent_executor.run(prompt)

            # Store assistant's response in chat history
            st.session_state.chat_history.append({"role": "assistant", "content": final})

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.text("User: " + message["content"])
        elif message["role"] == "assistant":
            st.text("Assistant: " + message["content"])

else:
    st.error("Failed to connect to the database")

if st.button("Reconnect"):
    connection = connect_to_database()
