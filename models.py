import json
from marshmallow import Schema, fields, post_load


class JSONStore:
    """Interface to on disk JSON file.

    Args:
        json_file (str): Path to json data file.

    Attributes:
        data (list of :obj:`dict`): Deserialised JSON.
    """

    def __init__(self, json_file):
        self.json_file = json_file

        try:
            with open(self.json_file, "r") as data_file:
                self.data = json.load(data_file)
        except FileNotFoundError:
            self.data = []

    def save(self):
        """Flush data to disk.
        """
        with open(self.json_file, "w") as data_file:
            json.dump(self.data, data_file)


class Task:
    """Class representation of a single task.

    Args:
        date (:obj:`datetime.datetime`): Date of task.
        title (str): Task title.
        time_spent (int): Time in minutes.
        notes (str): Optional notes.

    Attributes:
        date (:obj:`datetime.datetime`): Date of task.
        title (str): Task title.
        time_spent (int): Time in minutes.
        notes (str): Optional notes.
    """

    def __init__(self, date, title, time_spent, notes):
        self.date = date
        self.title = title
        self.time_spent = time_spent
        self.notes = notes

    def __repr__(self):
        return "<Task(title={self.title!r})>".format(self=self)


class TaskSchema(Schema):
    """marshmallow Schema object to validate and (de)serialise task data.

    Returns:
        :obj:`Task`
        :obj:`list` of :obj:`Task`: Deserialised task data.
        :obj:`dict`: Validated partial fields for edits.
    """

    date = fields.DateTime(format="%d/%m/%Y", required=True)
    title = fields.Str(required=True)
    time_spent = fields.Int(required=True)
    notes = fields.Str()

    @post_load
    def make_task(self, data):
        """Return Task object(s) or partial validated dict.

        Args:
            data (:obj:`dict` or :obj:`list` of :obj:`dict`): Deserialised JSON data.

        Returns:
            (:obj:`Task` or :obj:`list` of :obj:`Task`) if a full task record or set of records is passed.
            (:obj:`dict`): Validated dictionary of partial data for validation purposes.
        """
        if not len(data.keys()) < 4:
            return Task(**data)
        return dict(**data)
