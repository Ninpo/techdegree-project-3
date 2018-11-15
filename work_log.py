from views import MainView


def main():
    view = MainView()
    while view is not False:
        print(view.render_layout())
        view = view.handle_choice(input(view.prompt).lower())


if __name__ == "__main__":
    main()
