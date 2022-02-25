from pages import *
from notebook import Notebook
import json


class Calendar(Notebook):
    def __init__(self, dataJsonPath, **kwargs) -> None:
        super().__init__(**kwargs)
        # general
        self.name = kwargs.get('name', 'Untitle-Calendar')
        self.dataJsonPath = dataJsonPath
        self.readDataJson()

        # design
        self.layout = kwargs.get('layout', 'left')
        self.daysHeight = kwargs.get('daysHeight', 4)

        # Data show
        self.calendarOrder = kwargs.get('layout', ['sh', 'wc', 'ic'])
        self.showEvents = kwargs.get('showEvents', True)
        self.showWeekdays = kwargs.get('showWeekdays', False)
        self.showFullCalendar = kwargs.get('showFullCalendar', False)

        # font style
        self.fontFamily = kwargs.get('fontFamily', 'Anjoman')

        # colors
        self.primaryColor = kwargs.get('primaryColor', '#000')
        self.secondColor = kwargs.get('secondColor', '#ddd')

    def readDataJson(self):
        try:
            with open(self.dataJsonPath) as f:
                self.dataJson = json.load(f)
        except:
            print('JSON file is not exist.')
            exit()

    def addWeekPage(self, i):
        page = WeekPage(**self.__dict__)
        self.pages.append(page)
