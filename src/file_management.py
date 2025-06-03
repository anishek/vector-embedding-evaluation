import os
import chardet

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

    def file_encoding(self, file_path):
        with open(file_path, "rb") as f:
            result = chardet.detect(f.read())
        return result["encoding"]

    def read_next(self):
        try:
            read_from_location = next(self.files_iter)
            fe = self.file_encoding(read_from_location)
            with open(read_from_location, "r", encoding=fe) as current_file:
                return read_from_location, current_file.read()
        except StopIteration:
            return None, None
