"""Views for task management
"""


class View:
    """View base class.

    Args:
        layout (str): Text to display for current view.
        choices (:obj:`dict` of :obj:`str`): User choices for current view.
        prompt (str): Prompt styling for user input.

    Attributes:
        prompt (str): User input prompt prefix.
    """
    def __init__(self, layout, choices, prompt):
        self._layout = layout
        self.choices = choices
        self.prompt = prompt

    def handle_choice(self, choice):
        """Ensure choice exists in choices dict.

        Args:
            choice (str): User's choice selection.

        Returns:
            choice (str): User's choice selection if valid.
            error (str): Error message for invalid choice.
        """
        if choice not in self.choices:
            error = "Invalid Choice please choose from {}".format(", ".join(self.choices))
            return error
        return choice

    def render_layout(self):
        """Applies available choices to view layout.

        Returns:
            Formatted string (str)
        """
        return self._layout.format(*sorted(self.choices))

    def present_view(self, error: str = None):
        """Prints view layout to screen and prompts for input.

        Args:
            error (str): Errors to present to user, if any

        Returns:
            user_input (str)
        """
        if error:
            print("\n** {} **\n".format(error))
        print(self.render_layout())
        user_input = self.handle_choice(input(self.prompt).lower())
        while user_input.startswith("Invalid"):
            print(user_input)
            user_input = self.handle_choice(input(self.prompt).lower())
        return user_input


class MainView(View):
    """Base application view.

    Args: choices (:obj:`dict` of :obj:`str`): User choices for current view.

    Attributes:
        prompt (str): User input prompt prefix.
    """
    def __init__(self, choices):
        self._layout = """WORKLOG
        What would you like to do?
        {}) Add new entry
        {}) Search existing entries
        {}) Quit program"""

        self.choices = choices

        self.prompt = "Choice> "
        super().__init__(self._layout, self.choices, self.prompt)


class NewTaskView(View):
    """View presented when adding a new task."""
    def __init__(self):
        self._layout = """NEW TASK
        """

    def present_view(self, confirmation=False, error=None):
        """Prints formatted view to user.

        Args:
            confirmation (bool): Switch for confirmation dialog.
            error: (:obj:`Exception`): Validation errors.

        Returns:
            task (dict): New task data.
            None: From confirmation dialog.
        """
        if confirmation:
            input("The entry has been added.  Press Enter to continue")
            return
        if error:
            print(
                "\n** ERROR **\n{}\n\nPlease try again".format(
                    "\n".join(f"{k}: {' '.join(v)}" for k, v in error.messages.items())
                )
            )
        print(self._layout)
        task = {
            "date": input("Enter date (DD/MM/YYYY): "),
            "title": input("Task Title: "),
            "time_spent": input("Time spent (rounded minutes): "),
            "notes": input("Notes (Optional): "),
        }
        return task


class SearchView(View):
    """Menu of search methods.

    Args:
        choices (:obj:`dict`): Key mappings for layout.
    """
    def __init__(self, choices):
        self._layout = """SEARCH
        Choose your search method:
        {}) Exact Date
        {}) Range of Dates
        {}) Exact Text Search
        {}) Regex Pattern
        {}) Return to menu"""

        self.choices = choices

        self.prompt = "Search Method> "
        super().__init__(self._layout, self.choices, self.prompt)

    def exact_date(self):
        """Collects input intended for a fixed date search.

        Returns:
            date_string (str): User inputted date.

        """
        print("Exact Date Search")
        date_string = input("Enter a date in the format DD/MM/YYYY> ")
        return date_string

    def date_range(self):
        """Collects input intended for a date range search.

        Returns:
            (start_date, end_date) (str, str): User inputted date range.
        """
        start_date = input("Enter a start date in the format DD/MM/YYYY> ")
        end_date = input("Enter an end date in the format DD/MM/YYYY> ")
        return start_date, end_date

    def exact_match(self):
        """Collects input intended for a fixed text search.

        Returns:
            text_to_match (str): User inputted text string.
        """
        text_to_match = input("Enter the text to search for> ")
        return text_to_match

    def regex_pattern(self):
        """Collects input intended for a regular expression search.

        Returns:
            regex_to_match (str): User inputted string.
        """
        regex_to_match = input("Enter the regex pattern you'd like to use> ")
        return regex_to_match


class ResultView(View):
    """Displays search results and prompts for user input.

    Args:
        result (:obj:`list` of :obj:`Task`): Result from successful search query.
    """
    def __init__(self, result):
        self.result = result
        self._layout = """RESULT
        Date: {2.date:%d/%m/%Y}
        Title: {2.title}
        Time Spent: {2.time_spent}
        Notes: {2.notes}
        
        Result {0} of {1}"""
        self.page = 0

        self._options = {
            "n": self.next_item,
            "p": self.prev_item,
            "e": self.edit_item,
            "d": self.delete_item,
            "r": self.go_back,
        }

        if len(self.result) > 1:
            self.prompt = (
                "[N]ext, [P]revious, [E]dit, [D]elete, [R]eturn to search menu> "
            )
        else:
            self.prompt = "[E]dit, [D]elete, [R]eturn to search menu> "
        super().__init__(self._layout, self._options, self.prompt)

    def present_view(self):
        """Print formatted view to screen and collect next user input

        Returns:
            :obj:`method`: Adjusts pagination and re-presents view.
            :obj:`Task`: If "e" or "d" chosen, returns Task to be mutated.
        """
        print(self.render_layout(self.page, self.result[self.page]))
        user_input = self.handle_choice(input(self.prompt).lower())
        while user_input.startswith("Invalid"):
            print(user_input)
            user_input = self.handle_choice(input(self.prompt).lower())
        return self._options[user_input]()

    def render_layout(self, page, task):
        """Pass pagination information and task to layout.

        Args:
            page (int): Current index position of Task list.
            task (:obj:`Task`): Current task to be viewed.

        Returns:
            _layout (str): Formatted layout string.
        """
        return self._layout.format(page + 1, len(self.result), task)

    def next_item(self):
        """Advance result view one page.

        Returns:
            present_view (:obj:`str`) Updated page view and user input.
        """
        if self.page + 1 > len(self.result) - 1:
            self.page = 0
        else:
            self.page += 1
        return self.present_view()

    def prev_item(self):
        """Reverse result view one page.

        Returns:
            present_view (:obj:`str`) Updated page view and user input.
        """
        if self.page - 1 < 0:
            self.page = len(self.result) - 1
        else:
            self.page -= 1
        return self.present_view()

    def edit_item(self):
        """Request task edit.

        Returns:
            (str, :obj:`Task`): Choice and task to edit.
        """
        return "e", self.result[self.page]

    def delete_item(self):
        """Request task deletion.

        Returns:
            (str, :obj:`Task`): Choice and task to delete.
        """
        return "d", self.result[self.page]

    def go_back(self):
        return None, None


class EditView(View):
    """Present view of editable items and prompt for choice.

    Args:
        task (:obj:`Task`): Specific task to modify.
    """
    def __init__(self, task):
        self.task = task
        self._layout = """EDIT
        {0}) Date: {5.date:%d/%m/%Y}
        {1}) Title: {5.title}
        {2}) Time Spent: {5.time_spent}
        {3}) Notes: {5.notes}
        {4}) Back to results"""

        self._options = {
            "a": self.edit_date,
            "b": self.edit_title,
            "c": self.edit_time,
            "d": self.edit_notes,
            "e": self.go_back,
        }

        self.prompt = "Choose the item to edit> "

        super().__init__(self._layout, self._options, self.prompt)

    def present_view(self, error=None):
        """Print view and prompt for input.

        Args:
            error (:obj:`ValidationError`): Schema validation exception.

        Returns:
            (str): User inputted choice.
        """
        if error:
            print(
                "\n** ERROR **\n{}\n\nPlease try again".format(
                    "\n".join(f"{k}: {' '.join(v)}" for k, v in error.messages.items())
                )
            )
        print(self.render_layout())
        user_input = self.handle_choice(input(self.prompt).lower())
        while user_input.startswith("Invalid"):
            print(user_input)
            user_input = self.handle_choice(input(self.prompt).lower())
        return self._options[user_input]()

    def render_layout(self):
        """Format layout string for presentation.

        Returns:
            _layout (str): Formatted view output.

        """
        return self._layout.format(*self._options.keys(), self.task)

    def edit_date(self):
        """Collect new date.

        Returns:
            (:obj:`dict` of {`str`:`str`}): Updated field content.
        """
        new_date = input("Enter the new date (DD/MM/YYYY): ")
        return {'field': 'date', 'content': new_date}

    def edit_title(self):
        """Collect new title.

        Returns:
           (:obj:`dict` of {`str`:`str`}): Updated field content.
        """
        new_title = input("Enter your new title: ")
        return {'field': 'title', 'content': new_title}

    def edit_time(self):
        """Collect new time_spent.

        Returns:
            (:obj:`dict` of {`str`:`str`}): Updated field content.
        """
        new_time = input("Enter new time in rounded minutes: ")
        return {'field': 'time_spent', 'content': new_time}

    def edit_notes(self):
        """Collect new notes.

        Returns:
            (:obj:`dict` of {`str`:`str`}): Updated field content.
        """
        new_notes = input("Enter your updated notes: ")
        return {'field': 'notes', 'content': new_notes}

    def go_back(self):
        return None
