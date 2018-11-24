from models import JSONStore, TaskSchema


class DataRepo:
    """Repository for application data queries.

    Args:
        json_file (str): File name of JSON object.

    """

    def __init__(self, json_file):
        self.json_source = JSONStore(json_file)
        self.data_schema = TaskSchema()

    def get_records(self):
        """Load and validate on disk JSON data then deserialise.

        Returns:
            :obj:`list` of :obj:`Task`: Task object(s) representing each available Task record.

        """
        return self.data_schema.load(self.json_source.data, many=True)

    def validate_fields(self, fields):
        """Validate an incomplete list of field values for edits.

        Args:
            fields (dict): Field and data to validate.

        Returns:
            :obj:`dict`: If valid, {field: content}
        """
        return self.data_schema.load(fields, partial=True)

    def add_record(self, data):
        """Create new Task record and save to disk.

        Args:
            data (dict): {field: content} task data for serialisation and object mapping.

        Returns:
            :obj:`Task`: New Task object for added task.
        """
        record_obj = self.data_schema.load(data)
        self.json_source.data.append(self.data_schema.dump(record_obj))
        self.json_source.save()
        return record_obj

    def save_changes(self, updated_collection):
        """Flush data changes to disk.

        Args:
            updated_collection (:obj:`list` of :obj:`Task`): Task controller's task list for serialisation.

        Notes:
            Serialises Task objects to list of dicts in JSON object's data attribute.
            Serialises to JSON on disk.
        """
        self.json_source.data = self.data_schema.dump(updated_collection, many=True)
        self.json_source.save()
