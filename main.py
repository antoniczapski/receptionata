# TODO: this is a workaround, requires `pip install pysqlite3-binary`
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# -------------------------------------------------------------------

import argparse
import pathlib

import bs4
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders.html_bs import BSHTMLLoader
from langchain_community.document_loaders.pdf import PDFMinerLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


if __name__ == "__main__":
    load_dotenv()
    THIS_FILE_DIR = pathlib.Path(__file__).parent
    DATA_DIR = THIS_FILE_DIR / "data"
    CHROMA_PERSISTENCE_DIR = THIS_FILE_DIR / "chroma"

    argparser = argparse.ArgumentParser()
    argparser.add_argument("query", type=str)
    args = argparser.parse_args()
    
    query = args.query

    # text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    #     model_name="gpt-3.5-turbo",
    #     chunk_size=1000,
    #     chunk_overlap=200,
    # )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
    )

    documents = []
    for pdf in map(str, DATA_DIR.glob("*.pdf")):
        documents.extend(PDFMinerLoader(pdf).load())
    for html in DATA_DIR.glob("*.html"):
        loader = BSHTMLLoader(
            html,
            bs_kwargs=dict(
                features="html.parser",
                parse_only=bs4.SoupStrainer("article")
            ),
        )
        documents.extend(loader.load())

    documents = text_splitter.split_documents(documents)

    chroma = Chroma(
        collection_name="documents",
        embedding_function=OpenAIEmbeddings(),
        persist_directory=str(CHROMA_PERSISTENCE_DIR),
    )
    # chroma.add_documents(documents)

    relevant_documents = chroma.similarity_search_with_score(query)

    print("----------------------------------------------------------------------------------------------------")
    for relevant_document, score in relevant_documents:
        print(f"[{relevant_document.metadata["source"]}]\n\n")
        print(relevant_document.page_content)
        print("----------------------------------------------------------------------------------------------------")
