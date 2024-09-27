# Q&A Chatbot
from langchain_community.llms import OpenAI
import streamlit as st
import os

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env


# Function to load OpenAI model and get a response from it
def get_openai_response(question):
    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="text-davinci-003", temperature=0.5)
    response = llm(question)
    return response

# Initialize our Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Langchain Application")

# Input field for user question
input = st.text_input("Input: ", key="input")

# Debug: Print the API key to check if it's loaded (remove in production)
st.write("API Key Loaded:", os.getenv("OPENAI_API_KEY") is not None)

# Submit button
submit = st.button("Ask the question")

# If the ask button is clicked
if submit:
    if input:
        response = get_openai_response(input)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please enter a question.")
