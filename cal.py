from pages import *
from notebook import Notebook


class Calendar(Notebook):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # general
        self.name = kwargs.get('name', 'Untitle-Calendar')

    def addWeekPage(self):
        page = WeekPage()
        self.pages.append(page)
