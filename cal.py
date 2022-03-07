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
        self.startWeekday = kwargs.get('startWeekday', 'Sat')
        self.weekend = kwargs.get('weekend', 0)
        self.divider = kwargs.get('divider', ' / ')
        self.sentence = kwargs.get('sentence', [])
        self.personalEvents = kwargs.get('personalEvents', {})

        # design
        self.layout = kwargs.get('layout', 'left')
        self.daysHeight = kwargs.get('daysHeight', 4)
        self.lineShiftDown = kwargs.get('lineShiftDown', 0)
        self.iconSize = kwargs.get('iconSize', self.lineHeight*0.8)

        # Data show
        self.calendarOrder = kwargs.get('calendarOrder', ['sh', 'wc', 'ic'])
        self.showEvents = kwargs.get('showEvents', True)
        self.showWeekdays = kwargs.get('showWeekdays', False)
        self.showFullCalendar = kwargs.get('showFullCalendar', False)
        self.showWeekNo = kwargs.get('showWeekNo', True)
        self.showTime = kwargs.get('showTime', False)

        # font style
        self.fontHeightScl = kwargs.get('fontHeightScl', 0.67)
        self.fontFamily = kwargs.get('fontFamily', 'Anjoman')

        fontWeight = kwargs.get('fontWeight', {})
        defaultFontWeight = {
            'firstCal': 'Thin',
            'holiday': 'Thin',
            'firstCalWeekdays': 'ExtraLight',
            'firstCalWeekdaysHoliday': 'ExtraLight',
            'secondCal': 'Thin',
            'holidaysPage': 'Thin',
            'holidaysPageNo': 'Medium',
            'thirdCal': 'Thin',
            'monthAndWeek': 'Light',
            'events': 'ExtraLight',
            'time': 'Regular',
            'firstPageTitle': 'Thin',
            'turnOfYear':  'Thin',
            'firstPageOther': 'Light',
            'name': 'Black',
            'sentence': 'Light',
            'onePageYear': 'Light',
            'onePageYearHolidays': 'Medium',
            'onePageYearMonth': 'Black',
            'personalEvents': 'ExtraLight'
        }
        self.fontWeight = {}
        for k, v in defaultFontWeight.items():
            self.fontWeight[k] = fontWeight.get(k, v)

        fontSize = kwargs.get('fontSize', {})
        defaultFontSize = {
            'firstCal':  self.lineHeight * self.daysHeight * 2,
            'holiday':  self.lineHeight * self.daysHeight * 2,
            'firstCalWeekdays': 7,
            'firstCalWeekdaysHoliday': 7,
            'secondCal': 7,
            'holidaysPage': 7,
            'holidaysPageNo': 7,
            'thirdCal': 7,
            'monthAndWeek': 7,
            'time': 5,
            'events': 5,
            'firstPageTitle':  self.lineHeight * self.daysHeight * 4,
            'turnOfYear':  7,
            'firstPageOther': 9,
            'name': 9,
            'sentence': 9,
            'onePageYear': 7,
            'onePageYearHolidays': 7,
            'onePageYearMonth': 7,
            'personalEvents': 6
        }
        self.fontSize = {}
        for k, v in defaultFontSize.items():
            self.fontSize[k] = fontSize.get(k, v)

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

    def weekKeys(self, weekNo):
        key = list(self.dataJson.keys())
        for dayNo in range(7):
            if self.dataJson[key[dayNo]]['wc']['weekday'][0] == self.startWeekday:
                key = key[dayNo:]
                break

        return key[(weekNo-1)*7:weekNo*7]

    def addWeekPage(self, weekNo):
        page = WeekPage(weekNo, self.weekKeys(weekNo), **self.__dict__)
        self.pages.append(page)

    def addFirstPage(self):
        page = FirstPage(**self.__dict__)
        self.pages.append(page)

    def addHolidaysPage(self, **kwargs):
        page = HolidaysPage(**self.__dict__, **kwargs)
        self.pages.append(page)
