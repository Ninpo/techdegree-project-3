from marshmallow.exceptions import ValidationError
import pendulum
import models
import views


class TaskController:
    def __init__(self):
        self.data_store = models.JSONStore()

    def add_new_task(self, task=None):
        if task:
            try:
                new_task = models.TaskSchema().load(task)
            except ValidationError as err:
                print(err)
                return views.NewTaskView().present_view()
            else:
                models.TaskSchema().dump(new_task)
                return True
        return views.NewTaskView().present_view()

    def date_search(self, date, end_date=None):
        tasks = models.TaskSchema().load(self.data_store.data, many=True)
        date_stamp = pendulum.from_format(date, "DD/MM/YYYY").timestamp()
        if not end_date:
            result = [
                task
                for task in tasks
                if task.date.timestamp()
                == date_stamp
            ]
        else:
            end_date_stamp = pendulum.from_format(end_date, "DD/MM/YYYY").timestamp()
            result = [task for task in tasks if date_stamp <= task.date.timestamp() <= end_date_stamp]
        return views.ResultView(result).present_view()

    def text_search(self, match_text, regex=False):
        pass

    def edit_task(self, task):
        pass

    def delete_task(self, task):
        pass
