from pages import *
from notebook import Notebook
import json
from fontStyle import FontStyle


class Calendar(Notebook):
    def __init__(self, daysJsonPath, startDate, **kwargs) -> None:
        super().__init__(**kwargs)
        # general
        self.name = kwargs.get('name', 'Untitle-Calendar')
        self.daysJsonPath = daysJsonPath
        self.eventJsonPath = kwargs.get('eventJsonPath', 'events.json')
        self.eventFilter = kwargs.get('eventFilter', [])
        self.calNamesJsonPath = kwargs.get('calNamesJsonPath', 'calNames.json')
        self.readDaysJson()
        self.readEventJson()
        self.readCalNamesJson()
        self.startWeekday = kwargs.get('startWeekday', 'Sat')
        self.weekend = kwargs.get('weekend', [])
        self.divider = kwargs.get('divider', ' / ')
        self.sentence = kwargs.get('sentence', [])
        self.personalEvents = kwargs.get('personalEvents', {})
        self.startDate = startDate

        # design
        self.layout = kwargs.get('layout', 'left')
        self.daysHeight = kwargs.get('daysHeight', 4)
        self.lineShiftDown = kwargs.get('lineShiftDown', 0)
        self.iconScale = kwargs.get('iconScale', 0.8)
        self.moonScale = kwargs.get('moonScale', 0.6)

        # Data show
        self.calendarOrder = kwargs.get('calendarOrder', ['sh', 'wc', 'ic'])
        self.showEvents = kwargs.get('showEvents', True)
        self.showHolidays = kwargs.get('showHolidays', True)
        self.showWeekdays = kwargs.get('showWeekdays', False)
        self.showFullCalendar = kwargs.get('showFullCalendar', None)
        self.showWeekNo = kwargs.get('showWeekNo', True)
        self.showTimeline = kwargs.get('showTimeline', False)
        self.timelineStart = kwargs.get('timelineStart', 6)
        self.timelineEnd = kwargs.get('timelineEnd', 22)
        self.timelinePattern = kwargs.get('timelinePattern', '01')
        self.showMoon = kwargs.get('showMoon', True)
        self.showJustImpMoon = kwargs.get('showJustImpMoon', True)
        self.moonRotationDeg = kwargs.get('moonRotationDeg', 45)
        self.moonStyle = kwargs.get('moonStyle', 'stroke')

        # font style
        self.fontHeightScl = kwargs.get('fontHeightScl', 0.67)
        self.fontWidthScl = kwargs.get('fontWidthScl', 7.2)

        defaultFontWeight = {
            'default': 400,
            'firstCal': 100,
            'holiday': 100,
            'firstCalWeekdays': 200,
            'firstCalWeekdaysHoliday': 200,
            'secondCal': 100,
            'holidaysPage': 100,
            'holidaysPageNo': 500,
            'thirdCal': 100,
            'monthAndWeek': 300,
            'events': 200,
            'time': 400,
            'firstPageTitle': 100,
            'turnOfYear':  100,
            'firstPageOther': 300,
            'name': 800,
            'sentence': 300,
            'onePageYear': 300,
            'onePageYearHolidays': 500,
            'onePageYearMonth': 800,
            'onePageMonth': 800,
            'onePageMonthHolidays': 500,
            'onePageMonthDays': 400,
            'personalEvents': 200
        }
        fontWeight = kwargs.get('fontWeight', {})
        self.fontWeight = FontStyle(** defaultFontWeight)
        self.fontWeight.update(fontWeight)

        fontFamily = kwargs.get('fontFamily', 'Anjoman')
        if type(fontFamily) == str:
            fontFamily = {'default': fontFamily}
        self.fontFamily = FontStyle(** fontFamily, appendix=self.fontWeight)

        backupFonts = kwargs.get('backupFonts', 'vazirmatn')
        if type(backupFonts) == str:
            backupFonts = {'default': backupFonts}
        self.backupFonts = FontStyle(** backupFonts)

        defaultFontSize = {
            'default': 7,
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
            'onePageMonth': 7,
            'onePageMonthHolidays': 7,
            'onePageMonthDays': 7,
            'personalEvents': 6
        }
        fontSize = kwargs.get('fontSize', {})
        self.fontSize = FontStyle(** defaultFontSize)
        self.fontSize.update(fontSize)

        fontOtherCSS = kwargs.get('fontOtherCSS', {})
        defaultFontOtherCSS = {'default': ''}
        self.fontOtherCSS = FontStyle(** defaultFontOtherCSS)
        self.fontOtherCSS.update(fontOtherCSS)

        # colors
        self.primaryColor = kwargs.get('primaryColor', '#000')
        self.secondColor = kwargs.get('secondColor', '#ddd')

    def readDaysJson(self):
        try:
            with open(self.daysJsonPath) as f:
                self.daysJson = json.load(f)
        except:
            print('JSON file is not exist.')
            exit()

    def readEventJson(self):
        try:
            with open(self.eventJsonPath) as f:
                self.eventJson = json.load(f)
        except:
            print('JSON file is not exist.')
            exit()

    def readCalNamesJson(self):
        try:
            with open(self.calNamesJsonPath) as f:
                self.calNamesJson = json.load(f)
        except:
            print('JSON file is not exist.')
            exit()

    def weekKeys(self, weekNo):
        keys = list(self.daysJson.keys())

        for dayNo in range(10000):
            wd = str(self.daysJson[keys[dayNo]]['weekday'])
            if self.calNamesJson['wc']['weekday-short'][wd] == self.startWeekday and self.startDate in keys[dayNo:dayNo+7]:
                newkeys = keys[dayNo:]
                break
        return newkeys[(weekNo-1)*7:weekNo*7]

    def addWeekPage(self, weekNo, monthFilter=None, **kwargs):
        props = self.__dict__.copy()
        props.update(kwargs)
        page = WeekPage(
            weekNo, self.weekKeys(weekNo),
            monthFilter=monthFilter, **props
        )
        self.pages.append(page)

    def addFirstPage(self, years, turnOfYear, translateX=0, **kwargs):
        props = self.__dict__.copy()
        props.update(kwargs)
        page = FirstPage(years, turnOfYear, translateX=translateX, **props)
        self.pages.append(page)

    def addHolidaysPage(self, year, title, **kwargs):
        props = self.__dict__.copy()
        props.update(kwargs)
        page = HolidaysPage(year, title, **props)
        self.pages.append(page)

    def addOneYearPage(self, year, title='', **kwargs):
        props = self.__dict__.copy()
        props.update(kwargs)
        page = OneYearPage(year, title, **props)
        self.pages.append(page)

    def addOneMonthPage(self, month, year, **kwargs):
        props = self.__dict__.copy()
        props.update(kwargs)
        page = OneMonthPage(month=month, year=year, **props)
        self.pages.append(page)


if __name__ == '__main__':
    myCalendar = Calendar(
        daysJsonPath='data.json',
        startDate='1405-1-1',
        name="example"
    )

    for i in range(53):
        myCalendar.addWeekPage(i+1)

    myCalendar.toHTML()
