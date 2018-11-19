import json
from marshmallow import Schema, fields, post_dump, post_load


class JSONStore:
    def __init__(self, json_file="tasks.json"):
        self.json_file = json_file

        try:
            with open(self.json_file, 'r') as data_file:
                self.data = json.load(data_file)
        except FileNotFoundError:
            self.data = []

    def add(self, record):
        self.data.append(record)
        with open(self.json_file, 'w') as data_file:
            json.dump(self.data, data_file)


class Task:
    def __init__(self, date, title, time_spent, notes):
        self.date = date
        self.title = title
        self.time_spent = time_spent
        self.notes = notes

    def __repr__(self):
        return '<Task(title={self.title!r})>'.format(self=self)


class TaskSchema(Schema):
    def __init__(self):
        self.json_store = JSONStore()
        super().__init__()
    date = fields.DateTime(format="%d/%m/%Y", required=True)
    title = fields.Str(required=True)
    time_spent = fields.Int(required=True)
    notes = fields.Str()

    @post_load
    def make_task(self, data):
        return Task(**data)

    @post_dump
    def save_task(self, data):
        self.json_store.add(data)
