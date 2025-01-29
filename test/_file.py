import file, pygame
from args import path, ext

class create:
    @staticmethod
    def working() -> None|bool:
        file.create([path.test+"test_text"+ext.text], "Hello, world!")
        file.create([path.test+"test_data"+ext.data], {"Hello":"world!"})
        file.create([path.test+"test_log"+ext.log], "[DEBUG]: Hello, world!")
        file.create([path.test+"test_image"+ext.image], pygame.surface.Surface((20,20)))
    
    @staticmethod
    def accessible() -> None|bool:
        assert file.files[path.test+"test_text"+ext.text] == "Hello, world!"
        assert file.files[path.test+"test_data"+ext.data] == {"Hello":"world!"}
        assert file.files[path.test+"test_log"+ext.log] == "[DEBUG]: Hello, world!"
        assert file.files[path.test+"test_image"+ext.image].get_size() == (20,20)
    
    @staticmethod
    def modifiable() -> None|bool:
        file.files[path.test+"test_text"+ext.text] = "Hello"
        file.files[path.test+"test_data"+ext.data] = {"Hello":""}
        file.files[path.test+"test_log"+ext.log] = "[DEBUG]: Hello"
        file.files[path.test+"test_image"+ext.image] = pygame.surface.Surface((10,10))

    tests = [
        working,
        accessible,
        modifiable
    ]

class duplicate:
    @staticmethod
    def setup() -> None|bool:
        try:
            file.files[path.test+"test_text"+ext.text] = "Hello, world!"
            file.files[path.test+"test_data"+ext.data] = {"Hello":"world!"}
            file.files[path.test+"test_log"+ext.log] = "[DEBUG]: Hello, world!"
            file.files[path.test+"test_image"+ext.image] = pygame.surface.Surface((20,20))
        except Exception:
            assert False
        
    @staticmethod
    def working() -> None|bool:
        file.duplicate(path.test+"test_text"+ext.text, [path.test+"test_text2"+ext.text])
        file.duplicate(path.test+"test_data"+ext.data, [path.test+"test_data2"+ext.data])
        file.duplicate(path.test+"test_log"+ext.log, [path.test+"test_log2"+ext.log])
        file.duplicate(path.test+"test_image"+ext.image, [path.test+"test_image2"+ext.image])

    @staticmethod
    def accessible() -> None|bool:
        assert file.files[path.test+"test_text"+ext.text] == file.files[path.test+"test_text2"+ext.text]
        assert file.files[path.test+"test_data"+ext.data] == file.files[path.test+"test_data2"+ext.data]
        assert file.files[path.test+"test_log"+ext.log] == file.files[path.test+"test_log2"+ext.log]
        assert file.files[path.test+"test_image2"+ext.image].get_size() == (20,20)
    
    @staticmethod
    def truecopy() -> None|bool:
        file.files[path.test+"test_text2"+ext.text] = "Hello"
        assert file.files[path.test+"test_text"+ext.text] != file.files[path.test+"test_text2"+ext.text]
        file.files[path.test+"test_data2"+ext.data]["Hello"] = ""
        assert file.files[path.test+"test_data"+ext.data] != file.files[path.test+"test_data2"+ext.data]
        file.files[path.test+"test_log2"+ext.log] = "Hello"
        assert file.files[path.test+"test_log"+ext.log] != file.files[path.test+"test_log2"+ext.log]
        assert file.files[path.test+"test_image"+ext.image] != file.files[path.test+"test_image2"+ext.image]

    tests = [
        setup,
        working,
        accessible,
        truecopy
    ]

class close:
    @staticmethod
    def setup() -> None|bool:
        try:
            file.files[path.test+"test_text"+ext.text] = "Hello, world!"
            file.files[path.test+"test_data"+ext.data] = {"Hello":"world!"}
            file.files[path.test+"test_log"+ext.log] = "[DEBUG]: Hello, world!"
            file.files[path.test+"test_image"+ext.image] = pygame.surface.Surface((20,20))
        except Exception:
            assert False
    
    @staticmethod
    def working() -> None|bool:
        file.close([path.test+"test_text"+ext.text])
        file.close([path.test+"test_data"+ext.data])
        file.close([path.test+"test_log"+ext.log])
        file.close([path.test+"test_image"+ext.image])

    @staticmethod
    def notaccessible() -> None|bool:
        assert path.test+"test_text"+ext.text not in file.files
        assert path.test+"test_data"+ext.data not in file.files
        assert path.test+"test_log"+ext.log not in file.files
        assert path.test+"test_image"+ext.image not in file.files

    tests = [
        setup,
        working,
        notaccessible
    ]