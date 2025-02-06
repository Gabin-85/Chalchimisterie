import file, pygame, os
from args import path, ext

class create:

    def setup() -> None|bool:
        pass

    def call_text() -> None|bool:
        file.create([path.playground+"test_text"+ext.text], "Hello, world!")
    def call_data() -> None|bool:
        file.create([path.playground+"test_data"+ext.data], {"Hello":"world!"})
    def call_log() -> None|bool:
        file.create([path.playground+"test_log"+ext.log], "[DEBUG]: Hello, world!")
    def call_image() -> None|bool:
        file.create([path.playground+"test_image"+ext.image], pygame.surface.Surface((20,20)))
    
    def access_text() -> None|bool:
        assert file.files[path.playground+"test_text"+ext.text] == "Hello, world!"
    def access_data() -> None|bool:
        assert file.files[path.playground+"test_data"+ext.data] == {"Hello":"world!"}
    def access_log() -> None|bool:
        assert file.files[path.playground+"test_log"+ext.log] == "[DEBUG]: Hello, world!"
    def access_image() -> None|bool:
        assert file.files[path.playground+"test_image"+ext.image].get_size() == (20,20)
    
    def modify_text() -> None|bool:
        file.files[path.playground+"test_text"+ext.text] = "Hello"
    def modify_data() -> None|bool:
        file.files[path.playground+"test_data"+ext.data] = {"Hello":""}
    def modify_log() -> None|bool:
        file.files[path.playground+"test_log"+ext.log] = "[DEBUG]: Hello"
    def modify_image() -> None|bool:
        file.files[path.playground+"test_image"+ext.image] = pygame.surface.Surface((10,10))

    tests = {
        "Call": {
            "Text":call_text,
            "Data":call_data,
            "Log":call_log,
            "Image":call_image},
        "Access": {
            "Text":access_text,
            "Data":access_data,
            "Log":access_log,
            "Image":access_image},
        "Modify":{
            "Text":modify_text,
            "Data":modify_data,
            "Log":modify_log,
            "Image":modify_image},
    }

class duplicate:

    def setup() -> None|bool:
        try:
            create.call_text()
            create.call_data()
            create.call_log()
            create.call_image()
        except Exception:
            assert False
        
    def call_text() -> None|bool:
        file.duplicate(path.playground+"test_text"+ext.text, [path.playground+"test_text2"+ext.text])
    def call_data() -> None|bool:
        file.duplicate(path.playground+"test_data"+ext.data, [path.playground+"test_data2"+ext.data])
    def call_log() -> None|bool:    
        file.duplicate(path.playground+"test_log"+ext.log, [path.playground+"test_log2"+ext.log])
    def call_image() -> None|bool:    
        file.duplicate(path.playground+"test_image"+ext.image, [path.playground+"test_image2"+ext.image])

    def access_text() -> None|bool:
        assert file.files[path.playground+"test_text"+ext.text] == file.files[path.playground+"test_text2"+ext.text]
    def access_data() -> None|bool:
        assert file.files[path.playground+"test_data"+ext.data] == file.files[path.playground+"test_data2"+ext.data]
    def access_log() -> None|bool:
        assert file.files[path.playground+"test_log"+ext.log] == file.files[path.playground+"test_log2"+ext.log]
    def access_image() -> None|bool:
        assert file.files[path.playground+"test_image2"+ext.image].get_size() == (20,20)

    def nofile() -> None|bool:
        file.duplicate(path.playground+"unknown_file"+ext.text, [path.playground+"other_unknown_file"+ext.text])
        assert path.playground+"unknown_file"+ext.text not in file.files
        assert path.playground+"other_unknown_file"+ext.text not in file.files
        
    def truecopy_text() -> None|bool:
        file.files[path.playground+"test_text2"+ext.text] = "Hello"
        assert file.files[path.playground+"test_text"+ext.text] != file.files[path.playground+"test_text2"+ext.text]
    def truecopy_data() -> None|bool:
        file.files[path.playground+"test_data2"+ext.data]["Hello"] = ""
        assert file.files[path.playground+"test_data"+ext.data] != file.files[path.playground+"test_data2"+ext.data]
    def truecopy_log() -> None|bool:
        file.files[path.playground+"test_log2"+ext.log] = "Hello"
        assert file.files[path.playground+"test_log"+ext.log] != file.files[path.playground+"test_log2"+ext.log]
    def truecopy_image() -> None|bool:
        assert file.files[path.playground+"test_image"+ext.image] != file.files[path.playground+"test_image2"+ext.image]

    tests = {
        "Call": {
            "Text":call_text,
            "Data":call_data,
            "Log":call_log,
            "Image":call_image},
        "Access": {
            "Text":access_text,
            "Data":access_data,
            "Log":access_log,
            "Image":access_image},
        "Nofile":nofile,
        "Truecopy": {
            "Text":truecopy_text,
            "Data":truecopy_data,
            "Log":truecopy_log,
            "Image":truecopy_image}
    }

class close:

    def setup() -> None|bool:
        try:
            create.call_text()
            create.call_data()
            create.call_log()
            create.call_image()
        except Exception:
            assert False
    
    def call() -> None|bool:
        file.close([path.playground+"test_text"+ext.text,
                    path.playground+"test_data"+ext.data,
                    path.playground+"test_log"+ext.log,
                    path.playground+"test_image"+ext.image])

    def noaccess_text() -> None|bool:
        assert path.playground+"test_text"+ext.text not in file.files
    def noaccess_data() -> None|bool:
        assert path.playground+"test_data"+ext.data not in file.files
    def noaccess_log() -> None|bool:
        assert path.playground+"test_log"+ext.log not in file.files
    def noaccess_image() -> None|bool:
        assert path.playground+"test_image"+ext.image not in file.files

    tests = {
        "Call":call,
        "Notaccess": {
            "Text":noaccess_text,
            "Data":noaccess_data,
            "Log":noaccess_log,
            "image":noaccess_image
        }
    }

class write:

    def setup() -> None|bool:
        try:
            create.call_text()
            create.call_data()
            create.call_log()
            create.call_image()

            for item in os.listdir(path.playground):
                os.remove(path.playground+item)
        
        except Exception:
            assert False

    def call() -> None|bool:
        file.write([path.playground+"test_text"+ext.text,
                    path.playground+"test_data"+ext.data,
                    path.playground+"test_log"+ext.log,
                    path.playground+"test_image"+ext.image])
        
    def access_text() -> None|bool:
        assert os.path.exists(path.playground+"test_text"+ext.text)
    def access_data() -> None|bool:
        assert os.path.exists(path.playground+"test_data"+ext.data)
    def access_log() -> None|bool:
        assert os.path.exists(path.playground+"test_log"+ext.log)
    def access_image() -> None|bool:
        assert os.path.exists(path.playground+"test_image"+ext.image)

    def nofile() -> None|bool:
        file.write([path.playground+"unknown_file"+ext.text])
        assert os.path.exists(path.playground+"unknown_file"+ext.text) == False

    def noext() -> None|bool:
        file.write([path.playground+"unknown_file"+".unknown"])
        assert os.path.exists(path.playground+"unknown_file"+ext.text) == False

    tests = {
        "Call":call,
        "Access": {
            "Text":access_text,
            "Data":access_data,
            "Log":access_log,
            "Image":access_image},
        "Nofile":nofile,
        "Noext":noext
    }

class read:

    def setup() -> None|bool:
        create.call_text()
        create.call_data()
        create.call_log()
        create.call_image()
        write.call()
        file.files = {}

    def call() -> None|bool:
        file.read([path.playground+"test_text"+ext.text,
                    path.playground+"test_data"+ext.data,
                    path.playground+"test_log"+ext.log,
                    path.playground+"test_image"+ext.image])
        
    def access_text() -> None|bool:
        assert file.files[path.playground+"test_text"+ext.text] == "Hello, world!"
    def access_data() -> None|bool:
        assert file.files[path.playground+"test_data"+ext.data] == {"Hello":"world!"}
    def access_log() -> None|bool:
        assert file.files[path.playground+"test_log"+ext.log] == "[DEBUG]: Hello, world!"
    def access_image() -> None|bool:
        assert file.files[path.playground+"test_image"+ext.image].get_size() == (20,20)

    def nofile() -> None|bool:
        file.read([path.playground+"unknown_file"+ext.text])
        assert path.playground+"unknown_file"+ext.text not in file.files

    def noext() -> None|bool:
        file.read([path.playground+"unknown_file"+".unknown"])
        assert path.playground+"unknown_file"+ext.text not in file.files

    tests = {
        "Call":call,
        "Access": {
            "Text": access_text,
            "Data": access_data,
            "Log": access_log,
            "Image": access_image},
        "Nofile":nofile,
        "Noext":noext
    }

class delete:

    def setup() -> None|bool:
        create.call_text()
        create.call_data()
        create.call_log()
        create.call_image()
        write.call()
        
    def call() -> None|bool:
        file.delete([path.playground+"test_text"+ext.text,
                    path.playground+"test_data"+ext.data,
                    path.playground+"test_log"+ext.log,
                    path.playground+"test_image"+ext.image])
        
    def noaccess_text() -> None|bool:
        assert os.path.exists(path.playground+"test_text"+ext.text) == False
    def noaccess_data() -> None|bool:
        assert os.path.exists(path.playground+"test_data"+ext.data) == False
    def noaccess_log() -> None|bool:
        assert os.path.exists(path.playground+"test_log"+ext.log) == False
    def noaccess_image() -> None|bool:
        assert os.path.exists(path.playground+"test_image"+ext.image) == False

    tests = {
        "Call":call,
        "Noaccess": {
            "Text": noaccess_text,
            "Data": noaccess_data,
            "Log": noaccess_log,
            "Image": noaccess_image
        }
    }

class ask:

    filelist = None
    
    def setup() -> None|bool:
        create.call_text()
        create.call_data()
        create.call_log()
        create.call_image()
        write.call()
        file.files = {}

    def call() -> None|bool:
        ask.filelist = file.ask([path.playground+"test_text"+ext.text,
                             path.playground+"test_data"+ext.data,
                             path.playground+"test_log"+ext.log,
                             path.playground+"test_image"+ext.image])
        
    def access_text() -> None|bool:
        assert ask.filelist[0] == "Hello, world!"
    def access_data() -> None|bool:
        assert ask.filelist[1] == {"Hello":"world!"}
    def access_log() -> None|bool:
        assert ask.filelist[2] == "[DEBUG]: Hello, world!"
    def access_image() -> None|bool:
        assert ask.filelist[3].get_size() == (20,20)

    def reaccess_text() -> None|bool:
        assert file.files[path.playground+"test_text"+ext.text] == "Hello, world!"
    def reaccess_data() -> None|bool:
        assert file.files[path.playground+"test_data"+ext.data] == {"Hello":"world!"}
    def reaccess_log() -> None|bool:
        assert file.files[path.playground+"test_log"+ext.log] == "[DEBUG]: Hello, world!"
    def reaccess_image() -> None|bool:
        assert file.files[path.playground+"test_image"+ext.image].get_size() == (20,20)

    tests = {
        "Call":call,
        "Access": {
            "Text":access_text,
            "Data":access_data,
            "Log":access_log,
            "Image":access_image},
        "Reaccess": {
            "Text":reaccess_text,
            "Data":reaccess_data,
            "Log":reaccess_log,
            "Image":reaccess_image},
    }

class directory:

    def setup() -> None|bool:
        pass

    def call() -> None|bool:
        file.directory([path.playground])

    tests = {
        "Call":call
    }

class find:

    def setup() -> None|bool:
        directory.call()

    def call() -> None|bool:
        file.directory([path.playground])

    tests = {
        "Call":call
    }

functions = [
    create,
    duplicate,
    close,
    write,
    read,
    delete,
    ask,
    directory,
    find
]