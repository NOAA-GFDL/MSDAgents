from __future__ import annotations

import logging

from shared.client import Client, MilvusRetriever

# Suppress gRPC debug logs (too_many_pings warnings)
logging.getLogger("grpc").setLevel(logging.WARNING)

import re
from pathlib import Path
from typing import Any

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from pymilvus import MilvusClient

from shared.chatbot import RAGChatbot


LLM_MODEL = "llama3.2"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
MILVUS_DB_PATH = Path("/home/Ryan.Mulhall/msdagents/fms-chatbot/local_storage/fms_milvus.db")
COLLECTION_NAME = "FMS"
TOP_K = 15
MAX_CANDIDATES = 2000

SYSTEM_MESSAGE = (
  "FMS is the Flexible Modeling System, a Fortran library used for scientific computing in climate simulations. "
  "You are an FMS coding assistant to answer questions about FMS routines and modules. "
  "Only answer questions using the retrieved context. "
  "If context is insufficient, say you do not have enough information from the indexed FMS docs. "
  "Ensure that any code examples you provide are valid Fortran code. "
  "FMS contains many interfaces to provide generic interfaces to different data types, "
  "which should be used instead of calling their routines directly. "
  "If a routine belongs to a generic interface, provide the name of the generic interface in your answer first. "
  "\n\nContext:\n{context}"
)


client = Client(COLLECTION_NAME)
retriever = MilvusRetriever(client)

chatbot = RAGChatbot(
    retriever=retriever,
    system_message=SYSTEM_MESSAGE,
    model_name=LLM_MODEL,
)

while True:
    user_question = input("\nYou: ").strip()
    if user_question.lower() in {"quit", "exit", "q"}:
        print("Bye.")
        break

    response, docs_and_scores, context = chatbot.ask(user_question)
    print(f"\nAssistant: {response}")
    print(f"source: {[doc['sourcefile'] for doc in docs_and_scores]}")
    print("\n\n")
