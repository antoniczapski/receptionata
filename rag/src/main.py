import argparse

from config import get_config
from chroma import get_chroma_client


if __name__ == "__main__":
    chroma_client = get_chroma_client(get_config())

    argparser = argparse.ArgumentParser()
    argparser.add_argument("query", type=str)
    args = argparser.parse_args()

    query = args.query

    print(chroma_client.similarity_search_with_score(query))
