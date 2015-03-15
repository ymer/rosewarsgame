from controller import Controller
from view import View


if __name__ == '__main__':

    view = View()

    controller = Controller.from_replay('./replay/a.json')

    controller.run_game()