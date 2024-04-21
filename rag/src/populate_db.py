import pathlib

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.html_bs import BSHTMLLoader

from config import get_config
from chroma import get_chroma_client

DATA_DIR_PATH = pathlib.Path(__file__).parent.parent / "data"


if __name__ == "__main__":
    chroma_client = get_chroma_client(get_config())

    documents = []
    # TODO: maybe use DirectoryLoader
    for html_filename in DATA_DIR_PATH.glob("*.html"):
        documents.extend(BSHTMLLoader(html_filename).load_and_split())
    for pdf_filename in DATA_DIR_PATH.glob("*.pdf"):
        documents.extend(PyPDFLoader(str(pdf_filename)).load_and_split())

    chroma_client.add_documents(documents)
