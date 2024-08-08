import streamlit as st
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def sentence_(source_sentence,sentences):
    
    # Add source sentence to the list of sentences to process all at once
    all_sentences = [source_sentence] + sentences

    # Load model from Hugging Face Hub
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

    # Tokenize sentences
    encoded_input = tokenizer(all_sentences, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Perform pooling
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embeddings
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

    # Separate the source sentence embedding from the rest
    source_embedding = sentence_embeddings[0]
    comparison_embeddings = sentence_embeddings[1:]

    # Compute cosine similarities
    cosine_similarities = F.cosine_similarity(source_embedding.unsqueeze(0), comparison_embeddings)

    print("Cosine similarities with the source sentence:")
    for i, similarity in enumerate(cosine_similarities):
        values=f"Sentence: '{sentences[i]}', Similarity: {similarity.item()}"
        #st.text_area('',values)

    output_text = f"Source Sentence: '{source_sentence}',  is very Similar to : '{sentences[cosine_similarities.argmax()]}'"
    st.text_area('',output_text)

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

st.title("Sentence Similarity")
url='https://tse1.mm.bing.net/th?id=OIP.tE7I47hhyuaoIJB5l1MyrwHaER&pid=Api&P=0&h=180'
st.image(url,width=500)
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
    sentence_(main_sentence,sentence)
