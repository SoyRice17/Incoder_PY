class IOManager:
    def __init__(self):
        pass

    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()
