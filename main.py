import openai
import os
from sentence_transformers import SentenceTransformer

BASE_FOLDER = os.environ.get("BASE_FOLDER", "./")


class FileReader:
    def __init__(self, base_folder_name=BASE_FOLDER, max_files_to_read=1):
        if os.path.isdir(base_folder_name):
            self.folder_name = base_folder_name
        else:
            raise ValueError("Folder does not exist")
        self.max_files_to_read = max_files_to_read
        self.current_files_read = 0
        self.files_to_read = []
        for dir_path, dirs, files in os.walk(base_folder_name):
            for file in files:
                self.current_files_read += 1
                if self.current_files_read > self.max_files_to_read:
                    break
                self.files_to_read.append(os.path.join(dir_path, file))
        self.files_iter = iter(self.files_to_read)

    def read_next(self):
        try:
            with open(next(self.files_iter), "r", encoding="utf-8") as current_file:
                return current_file.read()
        except StopIteration:
            return None


def openai_embedding(text):
    openai.embeddings.create(
        model="text-embedding-ada-002", input=text.replace("\n", " ")
    )
    embedding = response["data"][0]["embedding"]
    return embedding


# based on https://huggingface.co/intfloat/multilingual-e5-large-instruct
# from leaderboard at https://huggingface.co/spaces/mteb/leaderboard
def e5_large_embedding(text):
    model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")
    # to get the max token length that the model can process used
    # print("Max:", model.max_seq_length)  # Output: 512
    return model.encode(text)
    # similarities = model.similarity(embeddings, embeddings)
    # print(similarities.shape)


def main():
    reader = FileReader()
    print(reader.files_to_read)
    while (content := reader.read_next()) is not None:
        embedding = e5_large_embedding(content)
        print(embedding)

    print("Hello from vector-embedding-evaluation!")


if __name__ == "__main__":
    main()
