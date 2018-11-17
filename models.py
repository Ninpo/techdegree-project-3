import json


class JSONModel:
    def __init__(self, json_file="scratch.json"):
        self.json_file = json_file
        try:
            with open(self.json_file, 'r') as data_file:
                self.data = json.load(data_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.data = []

    def add(self, record):
        self.data.append(record)
        with open(self.json_file, 'w') as data_file:
            json.dump(self.data, data_file)


class Task(JSONModel):
    def __init__(self):
        super().__init__()

    def edit(self):
        pass

    def delete(self):
        pass

    def date_search(self):
        pass

    def text_search(self):
        pass

