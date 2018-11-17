import models
import views
import pendulum


def validate_new_task(task):
    pass


def add_new_task(task=None):
    if task:
        validate_new_task(task)
        create_task = models.Task()
        create_task.add(task)
    else:
        return views.NewTaskView().present_view()


class Search:
    def __init__(self):
        pass

    def date_search(self, date, end_date=None):
        pass

    def text_search(self, match_text, regex=False):
        pass


class Modify:
    def __init__(self):
        pass

    def edit_task(self, task):
        pass

    def delete_task(self, task):
        pass
