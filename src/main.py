from dotenv import load_dotenv

# loading local configurations in env variables
load_dotenv()

from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from file_management import FileReader
from db_manager import PostgresManager
import asyncio
from concurrent.futures import ProcessPoolExecutor


# based on https://huggingface.co/intfloat/multilingual-e5-large-instruct
# from leaderboard at https://huggingface.co/spaces/mteb/leaderboard
async def e5_large_embedding(input_data, read_from_location):
    model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")
    # to get the max token length that the model can process used
    print("Max:", model.max_seq_length)  # Output: 512
    embeddings_to_add = []
    chunked_texts = recursive_chunking(input_data, model.max_seq_length)
    print("chunked_texts ", len(chunked_texts))
    with ProcessPoolExecutor() as executor:
        tasks = [
            get_embeddings_async(chunked_text, executor)
            for chunked_text in chunked_texts
        ]
        results = await asyncio.gather(*tasks)
        for result in results:
            text, embedding = result
            embeddings_to_add.append(
                {
                    "location": read_from_location,
                    "embedding": embedding,
                    "text_content": text,
                }
            )
    pg_manager = PostgresManager()
    print("embeddings found : ", len(embeddings_to_add))
    pg_manager.insert_embeddings_batch(embeddings_to_add)


async def get_embeddings_async(text, executor):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, get_embeddings_sync, text)


def get_embeddings_sync(text):
    model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")
    return text, model.encode(text)


# chunk_size reflects the number of characters that a chunk has, tokens is what the llm model is limited on hence
#  it is better to figure out how to split the text so as to create as many tokens for vectorization
def recursive_chunking(text, chunk_size=512):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=0,
        length_function=len,
    )
    texts = text_splitter.split_text(text)
    print("Chunks: ", len(texts))
    return texts


def main():
    reader = FileReader()
    read_from_location, content = reader.read_next()
    asyncio.run(e5_large_embedding(content, read_from_location))


if __name__ == "__main__":
    main()
