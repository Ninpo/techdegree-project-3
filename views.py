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
        print("Add New")

    def search_existing(self):
        return SearchView(self)

    def quit(self):
        return False


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
        date_string = input("Enter a date in the format DD/MM/YY> ")
        test_data = [{'date': date_string, 'title': "A Title", 'time_spent': 104, 'notes': "This is a note"}]
        return ResultView(test_data, self)

    def date_range(self):
        print("Date range search")

    def exact_match(self):
        print("Exact Match Search")

    def regex_pattern(self):
        print("Regex pattern search")


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

