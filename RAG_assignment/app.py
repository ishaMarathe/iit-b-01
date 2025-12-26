import os
import streamlit as st
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chat_models import init_chat_model

DATA_DIR = "resumes"
DB_PATH = "chroma_db"

os.makedirs(DATA_DIR, exist_ok=True)

embedder = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = chromadb.Client(
    settings=chromadb.Settings(persist_directory=DB_PATH)
)

store = db.get_or_create_collection(name="resume_store")

def read_pdf(path):
    loader = PyPDFLoader(path)
    pages = loader.load()
    return "\n".join(p.page_content for p in pages)

def save_resume(name, text):
    rid = name.replace(".pdf", "")
    vec = embedder.embed_documents([text])[0]
    store.add(
        ids=[rid],
        documents=[text],
        embeddings=[vec],
        metadatas=[{"file": name}]
    )

def upload(file):
    path = os.path.join(DATA_DIR, file.name)
    with open(path, "wb") as f:
        f.write(file.getbuffer())
    text = read_pdf(path)
    save_resume(file.name, text)

def load_folder():
    for name in os.listdir(DATA_DIR):
        if name.endswith(".pdf"):
            rid = name.replace(".pdf", "")
            found = store.get(ids=[rid])
            if not found["ids"]:
                text = read_pdf(os.path.join(DATA_DIR, name))
                save_resume(name, text)

def find(query, top_k):
    qvec = embedder.embed_query(query)
    return store.query(query_embeddings=[qvec], n_results=top_k)

def remove(rid):
    store.delete(ids=[rid])

model = init_chat_model(
    model="google/gemma-3n-e4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy-key"
)

st.title("Resume shortlisting system")

if st.button("Load resumes"):
    load_folder()
    st.success("Resumes loaded")

file = st.file_uploader("Upload resume (PDF)", type=["pdf"])
if file:
    upload(file)
    st.success("Resume saved")

query = st.text_area("Enter Question")
top_k = st.slider("Top results", 1, 10, 3)

if st.button("Search"):
    if query.strip():
        out = find(query, top_k)
        if not out["ids"]:
            st.warning("No results")
        else:
            st.subheader("Results")
            for i in range(len(out["ids"][0])):
                rid = out["ids"][0][i]
                text = out["documents"][0][i]

                prompt = f"""
                    You are reviewing a resume for a job.

                    Use only the resume text.
                    Do not guess or add information.

                    Job Description:
                    {query}

                    Resume:
                    {text}

                    Briefly explain why this resume fits or does not fit.
                """
                ans = model.invoke(prompt)

                st.write(f"Rank {i+1}: {rid}")
                st.write(ans.content)
                st.write("-----")
    else:
        st.error("Enter Question first")

st.header("Stored Resumes")
data = store.get()

if data["ids"]:
    for rid in data["ids"]:
        a, b = st.columns([4, 1])
        a.write(rid)
        if b.button("Delete", key=f"rm_{rid}"):
            remove(rid)
            st.warning(f"Deleted {rid}")
else:
    st.info("No resumes found")
