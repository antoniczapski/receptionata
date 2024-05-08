import argparse

from dotenv import load_dotenv

from chroma import get_chroma_client


if __name__ == "__main__":
    load_dotenv()  # TODO: temporary, remove once backend containerized

    argparser = argparse.ArgumentParser()
    argparser.add_argument("query", type=str)
    args = argparser.parse_args()
    
    query = args.query

    chroma = get_chroma_client()

    relevant_documents = chroma.similarity_search_with_score(query)

    print("----------------------------------------------------------------------------------------------------")
    for relevant_document, score in relevant_documents:
        print(f"[{relevant_document.metadata["source"]}]\n\n")
        print(relevant_document.page_content)
        print("----------------------------------------------------------------------------------------------------")
