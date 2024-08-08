
import requests
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv('SECRET_KEY')
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {secret_key}"}

def output (values,sentence,main_sentence):
    index_output=values.index(max(values))
    exit=f"Souce Sentence: '{main_sentence}',  is very Similar To: '{sentence[index_output]}'"
    st.text_area("",exit)
    
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	output(response.json(),sentence,main_sentence)


# making dictonary
def dictonary(source_sentence,sentence):
    dicton={}
    inner={}
    inner["source_sentence"]=source_sentence
    inner["sentences"]=sentence
    dicton["inputs"]=inner
    query(dicton)


# background 
st.markdown(f"""
<style>
    /* Set the background image for the entire app */
    .stApp {{
        background-color:#C0C0C0;
        background-size: 1300px;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    
    </style>
""", unsafe_allow_html=True)

    
st.title(" Sentence Similarity ")
url='https://tse1.mm.bing.net/th?id=OIP.tE7I47hhyuaoIJB5l1MyrwHaER&pid=Api&P=0&h=180'
st.image(url,width=700)
main_sentence=st.text_input("Please enter the Source Sentence")
sentence=[]
st.write("Sentences to compare to")
sentence1=st.text_input("Please Enter sentence 1")
sentence2=st.text_input("Please Enter sentence 2")
sentence3=st.text_input("Please Enter sentence 3")
sentence.append(sentence1)
sentence.append(sentence2)
sentence.append(sentence3)
if st.button("Find The Similarity"):
    dictonary(main_sentence,sentence)
