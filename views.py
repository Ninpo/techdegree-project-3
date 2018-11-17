from controllers import add_new_task, Search, Modify


class View:
    def __init__(self, layout, options, prompt, back=None):
        self._layout = layout
        self._options = options
        self.prompt = prompt
        if back:
            self.back = back
        else:
            self.back = self

    def handle_choice(self, choice):
        if choice not in self._options:
            print("Invalid Choice please choose from {}".format(', '.join(self._options.keys())))
            return self

        return self._options[choice]()

    def render_layout(self):
        return self._layout.format(*sorted(self._options.keys()))

    def present_view(self):
        print(self.render_layout())
        self.handle_choice(input(self.prompt).lower())

    def go_back(self):
        return self.back


class MainView(View):
    def __init__(self):
        self._layout = """WORKLOG
        What would you like to do?
        {}) Add new entry
        {}) Search existing entries
        {}) Quit program"""

        self._options = {'a': self.add_new,
                         'b': self.search_existing,
                         'c': self.quit}
        self.prompt = "Choice> "
        super().__init__(self._layout, self._options, self.prompt)

    def add_new(self):
        add_new_task()

    def search_existing(self):
        Search()

    def quit(self):
        return False


class NewTaskView(View):
    def __init__(self):
        self._layout = """NEW TASK
        """

    def present_view(self):
        print(self._layout)
        task = {
            'date': input("Enter date (DD/MM/YYYY): "),
            'title': input("Task Title: "),
            'time_spent': input("Time spent (rounded minutes): "),
            'notes': input("Notes (Optional): ")
        }
        add_new_task(task)
        input("The entry has been added.  Press Enter to continue")
        return MainView().present_view()



class SearchView(View):
    def __init__(self, back=None):
        self.back = back
        self._layout = """SEARCH
        Choose your search method:
        {}) Exact Date
        {}) Range of Dates
        {}) Exact Search
        {}) Regex Pattern
        {}) Return to menu"""

        self._options = {'a': self.exact_date,
                         'b': self.date_range,
                         'c': self.exact_match,
                         'd': self.regex_pattern,
                         'e': self.go_back}
        self.prompt = "Search Method> "
        super().__init__(self._layout, self._options, self.prompt, self.back)

    def exact_date(self):
        print("Exact Date Search")
        date_string = input("Enter a date in the format DD/MM/YYYY> ")
        Search.date_search(date_string)

    def date_range(self):
        start_date = input("Enter a start date in the format DD/MM/YYYY> ")
        end_date = input("Enter an end date in the format DD/MM/YYYY> ")
        Search.date_search(start_date, end_date)

    def exact_match(self):
        text_to_match = input("Enter the text to search for> ")
        Search.text_search(text_to_match)

    def regex_pattern(self):
        regex_to_match = input("Enter the regex pattern you'd like to use> ")


class ResultView(View):
    def __init__(self, result, back=None):
        self.back = back
        self.result = result
        self._layout = """RESULT
        Date: {date}
        Title: {title}
        Time Spent: {time_spent}
        Notes: {notes}
        
        Result {} of {}"""

        self._options = {'n': self.next_item,
                         'p': self.prev_item,
                         'e': self.edit_item,
                         'd': self.delete_item,
                         'r': self.go_back}

        if len(result) > 1:
            self.prompt = "[N]ext, [P]revious, [E]dit, [D]elete, [R]eturn to search menu> "
        else:
            self.prompt = "[E]dit, [D]elete, [R]eturn to search menu> "
        super().__init__(self._layout, self._options, self.prompt, self.back)

    def render_layout(self):
        return self._layout.format("1", "1", **self.result[0])

    def next_item(self):
        pass

    def prev_item(self):
        pass

    def edit_item(self):
        return EditView(self.result[0], self)

    def delete_item(self):
        pass


class EditView(View):
    def __init__(self, task, back=None):
        self.back = back
        self.task = task
        self._layout = """EDIT
        {}) Date: {date}
        {}) Title: {title}
        {}) Time Spent: {time_spent}
        {}) Notes: {notes}
        {}) Back to results"""

        self._options = {'a': self.edit_date,
                         'b': self.edit_title,
                         'c': self.edit_time,
                         'd': self.edit_notes,
                         'e': self.go_back}

        self.prompt = "Choose the item to edit> "

        super().__init__(self._layout, self._options, self.prompt, self.back)

    def render_layout(self):
        return self._layout.format(*self._options.keys(), **self.task)

    def edit_date(self):
        pass

    def edit_title(self):
        pass

    def edit_time(self):
        pass

    def edit_notes(self):
        pass

