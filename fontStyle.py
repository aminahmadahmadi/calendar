
class FontStyle():
    def __init__(self, default, appendix=None, **kwargs) -> None:
        self.default = default
        self.appendix = appendix

        self.firstCal = kwargs.get('firstCal', None)  # noqa
        self.holiday = kwargs.get('holiday', None)  # noqa
        self.firstCalWeekdays = kwargs.get('firstCalWeekdays', None)  # noqa
        self.firstCalWeekdaysHoliday = kwargs.get('firstCalWeekdaysHoliday', None)  # noqa
        self.secondCal = kwargs.get('secondCal', None)  # noqa
        self.holidaysPage = kwargs.get('holidaysPage', None)  # noqa
        self.holidaysPageNo = kwargs.get('holidaysPageNo', None)  # noqa
        self.thirdCal = kwargs.get('thirdCal', None)  # noqa
        self.monthAndWeek = kwargs.get('monthAndWeek', None)  # noqa
        self.titleofpage = kwargs.get('titleofpage', self.monthAndWeek)  # noqa
        self.events = kwargs.get('events', None)  # noqa
        self.time = kwargs.get('time', None)  # noqa
        self.firstPageTitle = kwargs.get('firstPageTitle', None)  # noqa
        self.turnOfYear = kwargs.get('turnOfYear', None)  # noqa
        self.firstPageOther = kwargs.get('firstPageOther', None)  # noqa
        self.name = kwargs.get('name', None)  # noqa
        self.sentence = kwargs.get('sentence', None)  # noqa
        self.onePageYear = kwargs.get('onePageYear', None)  # noqa
        self.onePageYearHolidays = kwargs.get('onePageYearHolidays', None)  # noqa
        self.onePageYearMonth = kwargs.get('onePageYearMonth', None)  # noqa
        self.onePageMonth = kwargs.get('onePageMonth', None)  # noqa
        self.onePageMonthHolidays = kwargs.get('onePageMonthHolidays', None)  # noqa
        self.onePageMonthDays = kwargs.get('onePageMonthDays', None)  # noqa
        self.personalEvents = kwargs.get('personalEvents', None)  # noqa

    def update(self, fontStyleDict: dict = {}):
        for k, v in fontStyleDict.items():
            self.__dict__[k] = v

    def get(self, param: str):
        r = self.__dict__[param]
        r = r if r else self.default

        if self.appendix == None:
            return r

        app = self.appendix.__dict__.get(param, None)
        if type(app) == str:
            return ' '.join([r, app])
        else:
            return r


def addTextStyle(obj, loc, name, fill, stroke=None, anchor=None, direction=None):
    try:
        fontWeight = obj.fontWeight.get(name)  # noqa
        fontOtherCSS = obj.fontOtherCSS.get(name)
        fontFamily = obj.fontFamily.get(name)  # noqa
        backupFonts = obj.backupFonts.get(name)  # noqa
        fontSize = obj.fontSize.get(name) / obj.scale  # noqa
        textAnchor = '' if anchor is None else f'text-anchor:{anchor};'
        textDir = '' if direction is None else f'direction:{direction};'
        obj.pages[loc].addStyle(
            name,
            f'fill:{fill};'
            f'stroke:None;'
            f'font-family:"{fontFamily}",{backupFonts};'
            f'font-weight:{fontWeight};{fontOtherCSS}'
            f'font-size:{fontSize}px;'
            f'{textAnchor}{textDir}'
        )
    except:
        print(
            f'Error in addTextStyle({obj}, {loc}, {fill}, {stroke}, {anchor})')
