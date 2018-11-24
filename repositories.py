from models import JSONStore, TaskSchema


class DataRepo:
    def __init__(self, json_file):
        self.json_source = JSONStore(json_file)
        self.data_schema = TaskSchema()

    def get_records(self):
        if len(self.json_source.data) == 0:
            return []
        return self.data_schema.load(self.json_source.data, many=True)

    def validate_fields(self, fields):
        return self.data_schema.load(fields, partial=True)

    def add_record(self, data):
        record_obj = self.data_schema.load(data)
        self.json_source.data.append(self.data_schema.dump(record_obj))
        self.json_source.save()
        return record_obj

    def save_changes(self, updated_collection):
        self.json_source.data = self.data_schema.dump(updated_collection, many=True)
        self.json_source.save()

    def save_data(self):
        pass
