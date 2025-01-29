import file
from args import path, ext

def creation_data() -> None|str:
    file.create([path.test+"test_file2"+ext.data], {})
    return file.files[path.test+"test_file2"+ext.data] == {}

def creation_text() -> None|str:
    file.create([path.test+"test_file1"+ext.text], "Hello, world!")
    return file.files[path.test+"test_file1"+ext.text] == "Hello, world!"

tests = [
    creation_data,
    creation_text
    ]