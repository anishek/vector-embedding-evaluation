from src.file_management import FileReader
import chardet


def test_single_file_read():
    reader = FileReader("./test/resources/test/", 1)
    file_location, content = reader.read_next()
    assert file_location in [
        "./test/resources/test/1.txt",
        "./test/resources/test/2.txt",
    ]
    assert content in ["a file 1", "a file 2"]
    assert reader.read_next() == (None, None)


def test_multiple_files_read():
    reader = FileReader("./test/resources/test/", 2)
    number_of_files_read = 0
    while True:
        file_location, content = reader.read_next()
        if file_location == None or content == None:
            break
        number_of_files_read += 1
        assert file_location in [
            "./test/resources/test/1.txt",
            "./test/resources/test/2.txt",
        ]
        assert content in ["a file 1", "a file 2"]
    assert number_of_files_read == 2


def test_successufully_read_if_available_files_less_than_requested():
    reader = FileReader("./test/resources/test/", 4)
    number_of_files_read = 0
    while True:
        file_location, content = reader.read_next()
        if file_location == None or content == None:
            break
        number_of_files_read += 1
        assert file_location in [
            "./test/resources/test/1.txt",
            "./test/resources/test/2.txt",
        ]
        assert content in ["a file 1", "a file 2"]
    assert number_of_files_read == 2
