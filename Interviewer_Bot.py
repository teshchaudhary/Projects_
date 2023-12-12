import streamlit as st
from streamlit_lottie import st_lottie
from langchain.llms import OpenAIChat, HuggingFaceHub
import webbrowser
import requests
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import warnings
warnings.filterwarnings('ignore')

load_dotenv()

class ITInterviewerChatbot:
    def __init__(self):
        self.vector_store = None

    def initialize_session_state(self):
        if "chat_sessions" not in st.session_state:
            st.session_state.chat_sessions = {}

        if "active_session" not in st.session_state:
            self.new_chat_session()

    def new_chat_session(self):
        chat_number = len(st.session_state.chat_sessions) + 1
        identifier = f"Chat - {chat_number}"
        st.session_state.chat_sessions[identifier] = []
        st.session_state.active_session = identifier
        self.greet_user()

    def open_external_link(self, url):
        webbrowser.open_new_tab(url)

    def process_user_input(self, user_input, prompt):
        llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.5, "max_length": 512})
        chain = LLMChain(llm=llm, prompt=prompt)

        return chain.run(user_input)

    def load_lottie_animation(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            return "Connection Failed"
        return r.json()

    def greet_user(self):
        st.session_state.chat_sessions[st.session_state.active_session].append(
            {"role": "assistant", "content": "Hello! I'm your IT Interviewer. How can I help you today?"})

    def run(self):
        self.initialize_session_state()

        st.markdown("<h1 style='font-size:40px;'>Interview-Buddy</h1>", unsafe_allow_html=True)

        if "active_session" in st.session_state:
            if st.session_state.active_session is None:
                st.markdown("<h1 style='font-size:50px;'>Chat Exited</h1>", unsafe_allow_html=True)
                st.markdown("<h1 style='font-size:40px;'>Click on new Chat button to start a new conversation</h1>",
                            unsafe_allow_html=True)
            else:
                for message in st.session_state.chat_sessions[st.session_state.active_session]:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                user_input = st.chat_input("Reply:")

                if user_input:
                    demo_template = '''
                    You are a Professional Interviewer designed to take short interviewes of user.
                    Remember these things in whole session:
                        Do not ask user more than one question in one go.
                        If user is not able to give any answer to the questions you asked, just move to next question.
                        Do not give solution of questions in middle of interview.

                    You will take interview in following manner:
                        After user's introduction ask him his domain/topic in which he wants to give interview.
                        After user give a domain, You will ask questions in given manner:
                            After user tells a domain ask first theory questions related to the domain he gave.
                            After he give answer of 1st question ask another question related to the domain he gave.
                            After he give answer of previous question ask another question related to the domain he gave.
                            After he give answer of previous question ask another question related to the domain he gave.


                    Things to do at end of whole session:
                        After user give response to all questions, at the end of whole interview give answers
                        to the user of the questions you aksed one by one and also give feedback to user performance 
                        in interview.
                        At the end of interview You can provide personalized advice on how he can improve in his domain only if he perform very bad. 

                    In whichever language user ask question reply in same language.
                    For example if user's language is hinglish. reply in hinglish.
                    '''


                    prompt = PromptTemplate(
                        template=demo_template
                    )

                    advice = self.process_user_input(user_input, prompt)
                    st.session_state.chat_sessions[st.session_state.active_session].append(
                        {"role": "user", "content": user_input})

                    with st.chat_message("user"):
                        st.markdown(user_input)

                    with st.chat_message("assistant"):
                        st.markdown(advice)

                    st.session_state.chat_sessions[st.session_state.active_session].append(
                        {"role": "assistant", "content": advice})
        else:
            st.markdown("<h1 style='font-size:50px;'>Chat Exited</h1>", unsafe_allow_html=True)
            st.markdown("<h1 style='font-size:40px;'>Click on new Chat button to start a new conversation</h1>", unsafe_allow_html=True)


if __name__ == "__main__":
    app = ITInterviewerChatbot()
    app.run()
