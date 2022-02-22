from pages import *
from notebook import *


class Calendar(Notebook):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def addWeekPage(self):
        page = WeekPage()
        self.pages.append(page)
