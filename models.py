import json


class JSONModel:
    def __init__(self, json_file):
        self.json_file = json_file
        try:
            with open(json_file, 'r') as data_file:
                self.data = json.load(data_file)
        except FileNotFoundError:
            self.data = []


class Task(JSONModel):
    def __init__(self):
        super().__init__()

    def add(self):
        pass

    def edit(self):
        pass

    def delete(self):
        pass

    def date_search(self):
        pass

    def text_search(self):
        pass

