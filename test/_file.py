import file, pygame, os
from error import category

class create:

    def setup() -> None:
        pass

    def call_text() -> None:
        file.create([file.path.playground+"test_text"+file.ext.text], "Hello, world!")
    def call_data() -> None:
        file.create([file.path.playground+"test_data"+file.ext.data], {"Hello":"world!"})
    def call_log() -> None:
        file.create([file.path.playground+"test_log"+file.ext.log], "[DEBUG]: Hello, world!")
    def call_image() -> None:
        file.create([file.path.playground+"test_image"+file.ext.image], pygame.surface.Surface((20,20)))
    
    def access_text() -> None:
        assert file.files[file.path.playground+"test_text"+file.ext.text] == "Hello, world!"
    def access_data() -> None:
        assert file.files[file.path.playground+"test_data"+file.ext.data] == {"Hello":"world!"}
    def access_log() -> None:
        assert file.files[file.path.playground+"test_log"+file.ext.log] == "[DEBUG]: Hello, world!"
    def access_image() -> None:
        assert file.files[file.path.playground+"test_image"+file.ext.image].get_size() == (20,20)
    
    def modify_text() -> None:
        file.files[file.path.playground+"test_text"+file.ext.text] = "Hello"
    def modify_data() -> None:
        file.files[file.path.playground+"test_data"+file.ext.data] = {"Hello":""}
    def modify_log() -> None:
        file.files[file.path.playground+"test_log"+file.ext.log] = "[DEBUG]: Hello"
    def modify_image() -> None:
        file.files[file.path.playground+"test_image"+file.ext.image] = pygame.surface.Surface((10,10))

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

    def setup() -> None:
        create.call_text()
        create.call_data()
        create.call_log()
        create.call_image()
        
    def call_text() -> None:
        file.duplicate(file.path.playground+"test_text"+file.ext.text, [file.path.playground+"test_text2"+file.ext.text])
    def call_data() -> None:
        file.duplicate(file.path.playground+"test_data"+file.ext.data, [file.path.playground+"test_data2"+file.ext.data])
    def call_log() -> None:    
        file.duplicate(file.path.playground+"test_log"+file.ext.log, [file.path.playground+"test_log2"+file.ext.log])
    def call_image() -> None:    
        file.duplicate(file.path.playground+"test_image"+file.ext.image, [file.path.playground+"test_image2"+file.ext.image])

    def access_text() -> None:
        assert file.files[file.path.playground+"test_text"+file.ext.text] == file.files[file.path.playground+"test_text2"+file.ext.text]
    def access_data() -> None:
        assert file.files[file.path.playground+"test_data"+file.ext.data] == file.files[file.path.playground+"test_data2"+file.ext.data]
    def access_log() -> None:
        assert file.files[file.path.playground+"test_log"+file.ext.log] == file.files[file.path.playground+"test_log2"+file.ext.log]
    def access_image() -> None:
        assert file.files[file.path.playground+"test_image2"+file.ext.image].get_size() == (20,20)

    def nofile() -> None:
        assert file.duplicate(file.path.playground+"unknown_file"+file.ext.text, [file.path.playground+"other_unknown_file"+file.ext.text]) == category.not_found
        assert file.path.playground+"unknown_file"+file.ext.text not in file.files
        assert file.path.playground+"other_unknown_file"+file.ext.text not in file.files
        
    def truecopy_text() -> None:
        file.files[file.path.playground+"test_text2"+file.ext.text] = "Hello"
        assert file.files[file.path.playground+"test_text"+file.ext.text] != file.files[file.path.playground+"test_text2"+file.ext.text]
    def truecopy_data() -> None:
        file.files[file.path.playground+"test_data2"+file.ext.data]["Hello"] = ""
        assert file.files[file.path.playground+"test_data"+file.ext.data] != file.files[file.path.playground+"test_data2"+file.ext.data]
    def truecopy_log() -> None:
        file.files[file.path.playground+"test_log2"+file.ext.log] = "Hello"
        assert file.files[file.path.playground+"test_log"+file.ext.log] != file.files[file.path.playground+"test_log2"+file.ext.log]
    def truecopy_image() -> None:
        assert file.files[file.path.playground+"test_image"+file.ext.image] != file.files[file.path.playground+"test_image2"+file.ext.image]

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

    def setup() -> None:
        create.call_text()
        create.call_data()
        create.call_log()
        create.call_image()
    
    def call() -> None:
        file.close([file.path.playground+"test_text"+file.ext.text,
                    file.path.playground+"test_data"+file.ext.data,
                    file.path.playground+"test_log"+file.ext.log,
                    file.path.playground+"test_image"+file.ext.image])

    def noaccess_text() -> None:
        assert file.path.playground+"test_text"+file.ext.text not in file.files
    def noaccess_data() -> None:
        assert file.path.playground+"test_data"+file.ext.data not in file.files
    def noaccess_log() -> None:
        assert file.path.playground+"test_log"+file.ext.log not in file.files
    def noaccess_image() -> None:
        assert file.path.playground+"test_image"+file.ext.image not in file.files

    def nofile() -> None:
        assert file.close([file.path.playground+"unknown_file"+file.ext.text]) == [category.already_done]

    tests = {
        "Call":call,
        "Notaccess": {
            "Text":noaccess_text,
            "Data":noaccess_data,
            "Log":noaccess_log,
            "image":noaccess_image
        },
        "Nofile":nofile
    }

class write:

    def setup() -> None:
        create.call_text()
        create.call_data()
        create.call_log()
        create.call_image()
        file.create([file.path.playground+"test_text"+".unknown"], "Hello, world!")

        for item in os.listdir(file.path.playground):
            os.remove(file.path.playground+item)

    def call() -> None:
        file.write([file.path.playground+"test_text"+file.ext.text,
                    file.path.playground+"test_data"+file.ext.data,
                    file.path.playground+"test_log"+file.ext.log,
                    file.path.playground+"test_image"+file.ext.image])
        
    def access_text() -> None:
        assert os.path.exists(file.path.playground+"test_text"+file.ext.text)
    def access_data() -> None:
        assert os.path.exists(file.path.playground+"test_data"+file.ext.data)
    def access_log() -> None:
        assert os.path.exists(file.path.playground+"test_log"+file.ext.log)
    def access_image() -> None:
        assert os.path.exists(file.path.playground+"test_image"+file.ext.image)

    def nofile() -> None:
        assert file.write([file.path.playground+"unknown_file"+file.ext.text]) == [category.not_found]
        assert os.path.exists(file.path.playground+"unknown_file"+file.ext.text) == False

    def noext() -> None:
        assert file.write([file.path.playground+"test_text"+".unknown"]) == [category.unsupported]
        assert os.path.exists(file.path.playground+"test_text"+".unknown") == False

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

    def setup() -> None:
        create.call_text()
        create.call_data()
        create.call_log()
        create.call_image()
        write.call()
        open(f"{file.path.playground+"test_text"+".unknown"}", "w")
        file.files = {}

    def call() -> None:
        file.read([file.path.playground+"test_text"+file.ext.text,
                    file.path.playground+"test_data"+file.ext.data,
                    file.path.playground+"test_log"+file.ext.log,
                    file.path.playground+"test_image"+file.ext.image])
        
    def access_text() -> None:
        assert file.files[file.path.playground+"test_text"+file.ext.text] == "Hello, world!"
    def access_data() -> None:
        assert file.files[file.path.playground+"test_data"+file.ext.data] == {"Hello":"world!"}
    def access_log() -> None:
        assert file.files[file.path.playground+"test_log"+file.ext.log] == "[DEBUG]: Hello, world!"
    def access_image() -> None:
        assert file.files[file.path.playground+"test_image"+file.ext.image].get_size() == (20,20)

    def nofile() -> None:
        assert file.read([file.path.playground+"unknown_file"+file.ext.text]) == [category.not_found]
        assert file.path.playground+"unknown_file"+file.ext.text not in file.files

    def noext() -> None:
        assert file.read([file.path.playground+"unknown_file"+".unknown"]) == [category.unsupported]
        assert file.path.playground+"unknown_file"+file.ext.text not in file.files

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

    def setup() -> None:
        create.call_text()
        create.call_data()
        create.call_log()
        create.call_image()
        write.call()
        
    def call() -> None:
        file.delete([file.path.playground+"test_text"+file.ext.text,
                    file.path.playground+"test_data"+file.ext.data,
                    file.path.playground+"test_log"+file.ext.log,
                    file.path.playground+"test_image"+file.ext.image])
        
    def noaccess_text() -> None:
        assert os.path.exists(file.path.playground+"test_text"+file.ext.text) == False
    def noaccess_data() -> None:
        assert os.path.exists(file.path.playground+"test_data"+file.ext.data) == False
    def noaccess_log() -> None:
        assert os.path.exists(file.path.playground+"test_log"+file.ext.log) == False
    def noaccess_image() -> None:
        assert os.path.exists(file.path.playground+"test_image"+file.ext.image) == False

    def nofile() -> None:
        assert file.delete([file.path.playground+"unknown_file"+file.ext.text]) == [category.not_found]

    tests = {
        "Call":call,
        "Noaccess": {
            "Text": noaccess_text,
            "Data": noaccess_data,
            "Log": noaccess_log,
            "Image": noaccess_image
        },
        "Nofile":nofile
    }

class ask:

    filelist = None
    
    def setup() -> None:
        create.call_text()
        create.call_data()
        create.call_log()
        create.call_image()
        write.call()
        file.files = {}

    def call() -> None:
        ask.filelist = file.ask([file.path.playground+"test_text"+file.ext.text,
                             file.path.playground+"test_data"+file.ext.data,
                             file.path.playground+"test_log"+file.ext.log,
                             file.path.playground+"test_image"+file.ext.image])
        
    def access_text() -> None:
        assert ask.filelist[0] == "Hello, world!"
    def access_data() -> None:
        assert ask.filelist[1] == {"Hello":"world!"}
    def access_log() -> None:
        assert ask.filelist[2] == "[DEBUG]: Hello, world!"
    def access_image() -> None:
        assert ask.filelist[3].get_size() == (20,20)

    def reaccess_text() -> None:
        assert file.files[file.path.playground+"test_text"+file.ext.text] == "Hello, world!"
    def reaccess_data() -> None:
        assert file.files[file.path.playground+"test_data"+file.ext.data] == {"Hello":"world!"}
    def reaccess_log() -> None:
        assert file.files[file.path.playground+"test_log"+file.ext.log] == "[DEBUG]: Hello, world!"
    def reaccess_image() -> None:
        assert file.files[file.path.playground+"test_image"+file.ext.image].get_size() == (20,20)

    def nofile() -> None:
        assert file.ask([file.path.playground+"unknown"+file.ext.text]) == [category.not_found]

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
        "Nofile":nofile
    }

class directory:

    def setup() -> None:
        pass

    def call() -> None:
        file.directory([file.path.playground])

    def alreadyexist() -> None:
        assert file.directory([file.path.playground]) == [category.already_done]

    tests = {
        "Call":call,
        "Alreadyexist":alreadyexist
    }

class find:

    def setup() -> None:
        directory.call()

    def call() -> None:
        file.directory([file.path.playground])

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