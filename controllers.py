import re
from marshmallow.exceptions import ValidationError
import pendulum
import views


class TaskController:
    def __init__(self, data_repo):
        self.data_repo = data_repo
        self.tasks = self.data_repo.get_records()

    def render_view(self, view, confirmation=False, error=None):
        if confirmation:
            return view.present_view(confirmation=confirmation)
        if error:
            return view.present_view(error=error)
        return view.present_view()

    def start(self):
        index_choices = {
            "a": self.add_new_task,
            "b": self.search_existing,
            "c": self.quit,
        }
        index_view = views.MainView(index_choices)
        user_choice = self.render_view(index_view)
        index_choices[user_choice]()

    def add_new_task(self):
        new_task_view = views.NewTaskView()
        new_task_success = False
        view_options = None
        while not new_task_success:
            if view_options:
                task = self.render_view(new_task_view, **view_options)
            else:
                task = self.render_view(new_task_view)
            try:
                self.tasks.append(self.data_repo.add_record(task))
                new_task_success = True
            except ValidationError as err:
                view_options = {"confirmation": False, "error": err}
                continue
            else:
                view_options = {"confirmation": True, "error": None}
                self.render_view(new_task_view, **view_options)
                return self.start()

    def search_existing(self):
        search_methods = {
            "a": self.date_search,
            "b": self.date_range_search,
            "c": self.text_search,
            "d": self.regex_search,
            "e": self.start,
        }
        search_view = views.SearchView(search_methods)
        user_choice = self.render_view(search_view)
        if user_choice == "e":
            return search_methods[user_choice]()
        else:
            search_result = search_methods[user_choice](search_view)
        while not search_result:
            user_choice = self.render_view(search_view, error="No results found")
            if user_choice == "e":
                return search_methods[user_choice]()
            search_result = search_methods[user_choice](search_view)
        editing = True
        while editing:
            editing = self.handle_search_results(search_result)
        self.search_existing()

    def handle_search_results(self, search_result):
        result_choices = {"e": self.edit_task, "d": self.delete_task}
        result_view = views.ResultView(search_result)
        result_action, task = self.render_view(result_view)
        if not result_action:
            return
        edit_confirmed = False
        action_result = result_choices[result_action](task)
        while not edit_confirmed:
            if not action_result:
                return False
            if isinstance(action_result, dict):
                action_result = self.edit_task(
                    action_result["task"], action_result["error"]
                )
                continue
            elif action_result in ("back"):
                return True
            else:
                edit_confirmed = True
        return edit_confirmed

    def date_search(self, view):
        date = view.exact_date()
        try:
            date_stamp = pendulum.from_format(date, "DD/MM/YYYY").timestamp()
        except ValueError as err:
            print("\n{}".format(err))
            return None
        result = [task for task in self.tasks if task.date.timestamp() == date_stamp]
        if result:
            return result
        return None

    def date_range_search(self, view):
        start_date, end_date = view.date_range()
        try:
            start_date_stamp = pendulum.from_format(
                start_date, "DD/MM/YYYY"
            ).timestamp()
            end_date_stamp = pendulum.from_format(end_date, "DD/MM/YYYY").timestamp()
            if start_date_stamp > end_date_stamp:
                raise ValueError("Start date must be earlier than end date!")
        except ValueError as err:
            print("\n{}".format(err))
            return None
        result = [
            task
            for task in self.tasks
            if start_date_stamp <= task.date.timestamp() <= end_date_stamp
        ]
        if result:
            return result
        return None

    def text_search(self, view):
        match_text = view.exact_match()
        result = [
            task
            for task in self.tasks
            if any(
                match_text.lower() in str(val).lower() for val in vars(task).values()
            )
        ]
        if result:
            return result
        return None

    def regex_search(self, view):
        regex_pattern = view.regex_pattern()
        try:
            pattern_match = re.compile(regex_pattern, re.IGNORECASE)
        except re.error:
            print("Invalid regex pattern entered, please check and try again.")
            return None
        else:
            result = [
                task
                for task in self.tasks
                if any(
                    pattern_match.findall(val)
                    for val in vars(task).values()
                    if isinstance(val, str)
                )
            ]
        if result:
            return result
        return None

    def edit_task(self, task, error=None):
        edit_view = views.EditView(task)
        task_changes = self.render_view(edit_view, error=error)
        while task_changes:
            if len(task_changes["content"]) == 0:
                task_changes["content"] = None
            try:
                valid_data = self.data_repo.validate_fields(
                    {task_changes["field"]: task_changes["content"]}
                )
            except ValidationError as err:
                error = err
                task_changes = self.render_view(edit_view, error=error)
                continue
            setattr(task, task_changes["field"], valid_data[task_changes["field"]])
            self.data_repo.save_changes(self.tasks)
            print("Task {} edited.".format(task_changes["field"]))
            task_changes = self.render_view(edit_view, error=error)
        return "back"

    def delete_task(self, task):
        for idx, cur_task in enumerate(self.tasks):
            if cur_task is task:
                del self.tasks[idx]
                self.data_repo.save_changes(self.tasks)
        print("\nDeleted.\n")
        return False

    def quit(self):
        exit()
