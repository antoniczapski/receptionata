# TODO: this is a workaround, requires `pip install pysqlite3-binary`
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# -------------------------------------------------------------------

import chromadb
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_chroma import Chroma

from config import Config


def get_chroma_client(config: Config) -> Chroma:
    chroma_client = chromadb.HttpClient(
        host=config.chroma_hostname,
        port=config.chroma_port,
    )
    return Chroma(
        client=chroma_client,
        collection_name="documents",
        embedding_function=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    )
