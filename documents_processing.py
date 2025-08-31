import os.path
import tempfile
import streamlit as st
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredFileLoader
)
from config import *
from collections import defaultdict
from langchain_huggingface import HuggingFaceEmbeddings
import torch
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever


def load_documents(file):
    """
    根据用户上传的不同类型的文件使用不同的加载器进行加载
    :param file: 用户上传的文件
    :return: 加载后的文档
    """
    file_extension = os.path.splitext(file.name)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
        tmp.write(file.getvalue())
        tmp_path = tmp.name

    try:
        if file_extension == '.pdf':
            loader = PyPDFLoader(tmp_path)
        elif file_extension == '.txt':
            loader = TextLoader(tmp_path)
        elif file_extension == '.docx':
            loader = Docx2txtLoader(tmp_path)
        else:
            loader = UnstructuredFileLoader(tmp_path)

        return loader.load()
    except Exception as e:
        st.error(f"Load the document unsuccessfully: {str(e)}")
        return []
    finally:
        os.unlink(tmp_path)


def process_documents(files):
    all_chunks = []
    doc_mapping = defaultdict(list)

    for file in files:
        if file.name in st.session_state.processed_files:
            continue

        with st.spinner(f"正在处理 {file.name}..."):
            documents = load_documents(file)

            if not documents:
                continue

            chunks = TEXT_SPLITER.split_documents(documents)

            for chunk in chunks:
                chunk.metadata['source_doc'] = file.name

            all_chunks.extend(chunks)
            doc_mapping[file.name] = chunks

            st.session_state.processed_files[file.name] = True

    if not all_chunks:
        return None

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    vector_db = Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PERSIST_DIR
    )

    texts = [doc.page_content for doc in all_chunks]
    metadatas = [doc.metadata for doc in all_chunks]
    keyword_retriever = BM25Retriever.from_texts(texts, metadatas=metadatas)

    return vector_db, keyword_retriever


