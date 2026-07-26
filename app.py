import streamlit as st

from rag import (
    load_vector_db,
    search_chunks,
    generate_answer,
)

# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="Health Transformation Knowledge Assistant",
    page_icon="🏥",
    layout="wide"
)

# ---------------------------------------
# Custom Styling
# ---------------------------------------

st.markdown("""
<style>

/* Main Page */
.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    padding-left:4rem;
    padding-right:4rem;
}

/* Title */
.main-title{
    font-size:52px;
    font-weight:800;
    color:#163A5F;
    margin-bottom:5px;
}

/* Subtitle */
.subtitle{
    font-size:20px;
    color:#555;
    margin-bottom:25px;
}

/* Labels */
label{
    font-size:18px !important;
    font-weight:600 !important;
}

/* Input Box */
.stTextInput input{
    font-size:18px !important;
    padding:15px !important;
    border-radius:10px !important;
}

/* Button */
.stButton>button{
    width:100%;
    height:55px;
    font-size:18px;
    font-weight:700;
    border-radius:12px;
}

/* Section Titles */
.section-title{
    font-size:30px;
    font-weight:700;
    color:#163A5F;
    margin-top:20px;
    margin-bottom:10px;
}

/* Answer Box */
.answer-box{
    background:#F4F8FB;
    padding:22px;
    border-radius:12px;
    border-left:6px solid #1976D2;
    font-size:18px;
    line-height:1.8;
}

/* Expanders */
.streamlit-expanderHeader{
    font-size:17px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# Load Existing Vector DB
# ---------------------------------------

@st.cache_resource
def load_rag():
    return load_vector_db()

collection = load_rag()

# ---------------------------------------
# Header
# ---------------------------------------

st.markdown("""
<div class="main-title">
🏥 Health Transformation Knowledge Assistant
</div>

<div class="subtitle">
Explore India's Health Transformation initiatives through AI-powered semantic search using Retrieval-Augmented Generation (RAG).
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------
# Question Input
# ---------------------------------------

question = st.text_input(
    "🔍 Enter your question",
    placeholder="Example: What is PM-JAY?"
)

# ---------------------------------------
# Search
# ---------------------------------------

if st.button("🔍 Generate Answer"):

    if question.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Searching the knowledge base..."):

        results = search_chunks(collection, question)

        retrieved_docs = results["documents"][0]
        retrieved_metadata = results["metadatas"][0]

        answer = generate_answer(question, retrieved_docs)

    st.markdown(
        '<div class="section-title">🤖 Answer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
<div class="answer-box">
{answer}
</div>
""",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="section-title">📚 Supporting Evidence</div>',
        unsafe_allow_html=True
    )

    for meta, doc in zip(retrieved_metadata, retrieved_docs):

        clean_doc = doc.split("\n\n", 1)[1] if "\n\n" in doc else doc

        with st.expander(f"📄 {meta['display_title']}"):
            st.write(clean_doc)

    