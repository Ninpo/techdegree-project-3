"""CLI Task Logger

Author: Alex Boag-Munroe"""

from json.decoder import JSONDecodeError
from controllers import TaskController
from repositories import DataRepo


def main():
    """App initialisation.
    """
    json_file = "tasks.json"
    try:
        data_interface = DataRepo(json_file)
    except JSONDecodeError as err:
        print("Invalid JSON file {} detected.".format(json_file))
        print("JSON error: {}".format(err))
        return
    task_app = TaskController(data_interface)
    task_app.start()


if __name__ == "__main__":
    main()
