from aaaSvg import Svg
from replaceText import perNo, arbNo


class Page():
    def __init__(self, name='Untitle-Page', **kwargs) -> None:
        # general
        self.name = name
        self.width = kwargs.get('width', 148)
        self.height = kwargs.get('height', 210)
        self.scale = kwargs.get('scale', 2.83465)

        # margin and padding
        self.margin = kwargs.get(
            'margin',
            {'top': 5, 'outside': 5, 'bottom': 5, 'inside': 0}
        )
        if isinstance(self.margin, list):
            nameList = ['top', 'outside', 'bottom', 'inside']
            self.margin = dict(zip(nameList, self.margin))

        # colors
        self.bgColor = kwargs.get('bgColor', 'none')

        # SVG
        self.svgWidth = self.width + \
            self.margin['outside'] + self.margin['inside']
        self.svgHeight = self.height + \
            self.margin['top'] + self.margin['bottom']

        # info on page
        self.guide = kwargs.get('guide', False)

    @property
    def page(self):
        self.pages = {}
        self.makePages()
        return self.pages

    def makePages(self):
        for loc in ['right', 'left']:
            self.definePage(loc)
            self.drawGuide(loc)

    def definePage(self, loc):
        self.pages[loc] = Svg(
            self.name+'-'+loc, self.svgWidth*self.scale, self.svgHeight*self.scale)

        self.pages[loc].addStyle(
            'bg',
            f'fill:{self.bgColor};'
            'stroke:none;'
        )

        self.pages[loc].addRect(
            0,
            0,
            self.width+self.margin['outside'] + self.margin['inside'],
            self.height+self.margin['top'] + self.margin['bottom'],
            class_='bg',
            transform=f'scale({self.scale})'
        )

    def drawGuide(self, loc):
        if not self.guide:
            return

        _dir = {
            'right': ['inside', 'outside'],
            'left': ['outside', 'inside']
        }

        self.pages[loc].addRect(
            self.margin[_dir[loc][0]],
            self.margin['top'],
            self.width,
            self.height,
            stroke='#0ff',
            fill='none',
            style='stroke-width:0.25;',
            transform=f'scale({self.scale})'
        )


class LinePage(Page):
    def __init__(self, name='Untitle-LinePage', **kwargs) -> None:
        super().__init__(name, **kwargs)

        # margin and padding
        self.padding = kwargs.get(
            'padding',
            {'top': 32, 'outside': 0, 'bottom': 10, 'inside': 0}
        )
        if isinstance(self.padding, list):
            nameList = ['top', 'outside', 'bottom', 'inside']
            self.padding = dict(zip(nameList, self.padding))

        # line and dot peroperty
        self.lineHeight = kwargs.get('lineHeight', 6)
        self.lineWidth = kwargs.get('lineWidth', 0.05)

        # colors
        self.lineColor = kwargs.get('lineColor', '#555')

    @property
    def page(self):
        self.pages = {}
        self.makePages()
        return self.pages

    def makePages(self):
        for loc in ['right', 'left']:
            self.definePage(loc)
            self.drawlines(loc)
            self.drawGuide(loc)

    def drawlines(self, loc):
        self.pages[loc].addStyle(
            'line',
            'fill:none;'
            f'stroke:{self.lineColor};'
            f'stroke-width:{self.lineWidth};'
        )
        xLeft, xRight = self.xloc(loc)
        y = self.margin['top'] + self.padding['top']
        while y <= self.svgHeight - self.margin['bottom'] - self.padding['bottom']:
            self.pages[loc].addLine(
                xLeft, y, xRight, y,
                transform=f'scale({self.scale})',
                class_='line'
            )
            y += self.lineHeight

    def xloc(self, loc, space=None):
        _dir = {
            'right': ['inside', 'outside'],
            'left': ['outside', 'inside']
        }
        if space:
            xLeftSpace = self.padding[_dir[loc][0]] + \
                self.margin[_dir[loc][0]]+space
            xRightSpace = self.svgWidth - \
                (self.padding[_dir[loc][1]]+self.margin[_dir[loc][1]]+space)
            return (xLeftSpace, xRightSpace)
        else:
            xLeft = 0 if self.padding[_dir[loc][0]] == 0 else self.padding[_dir[loc][0]] + \
                self.margin[_dir[loc][0]]
            xRight = self.svgWidth
            xRight -= 0 if self.padding[_dir[loc][1]] == 0 else self.padding[_dir[loc][1]] + \
                self.margin[_dir[loc][1]]
            return (xLeft, xRight)


class DotPage(Page):
    def __init__(self, name='Untitle-DotPage', **kwargs) -> None:
        super().__init__(name, **kwargs)


class WeekPage(LinePage):
    def __init__(self, weekKeys, name='Untitle-WeekPage', **kwargs) -> None:
        super().__init__(name, **kwargs)

        self.dataJson = kwargs.get('dataJson', 'left')
        self.weekKeys = weekKeys

        self.layout = kwargs.get('layout', 'left')
        self.daysHeight = kwargs.get('daysHeight', 4)
        self.lineShiftDown = kwargs.get('lineShiftDown', 0)

        # font style
        self.fontHeightScl = kwargs.get('fontHeightScl', 0.66)
        self.fontFamily = kwargs.get('fontFamily', 'Anjoman')
        self.fontWeight = kwargs.get('fontWeight', {})
        self.fontSize = kwargs.get('fontSize', {})

        # colors
        self.primaryColor = kwargs.get('primaryColor', '#000')
        self.secondColor = kwargs.get('secondColor', '#ddd')

        # Data show
        self.calendarOrder = kwargs.get('calendarOrder', ['sh', 'wc', 'ic'])
        self.showEvents = kwargs.get('showEvents', True)
        self.showWeekdays = kwargs.get('showWeekdays', False)
        self.showFullCalendar = kwargs.get('showFullCalendar', False)
        self.weekend = kwargs.get('weekend', 0)

    @property
    def page(self):
        self.pages = {}
        self.makePages()
        return self.pages

    def makePages(self):
        for loc in ['right', 'left']:
            self.definePage(loc)
            self.drawlines(loc)
            self.addFirstCal(loc)
            self.addSecondCal(loc)
            self.addthirdCal(loc)
            self.addEventOfDays(loc)
            self.drawGuide(loc)

    def drawlines(self, loc):
        self.pages[loc].addStyle(
            'line',
            'fill:none;'
            f'stroke:{self.lineColor};'
            f'stroke-width:{self.lineWidth};'
        )

        xLeft, xRight = self.xloc(loc)
        space = self.lineHeight*self.daysHeight
        xLeftSpace, xRightSpace = self.xloc(loc, space)

        self.daysY = []
        y = self.margin['top'] + self.padding['top']
        lineNo = 0
        while y <= self.svgHeight - self.margin['bottom'] - self.padding['bottom']:
            if lineNo < self.lineShiftDown:
                xl, xr = xLeft, xRight
            elif lineNo % self.daysHeight == self.lineShiftDown % self.lineHeight:
                self.daysY.append(y)
                xl, xr = xLeft, xRight
            else:
                if self.layout == 'left':
                    xl, xr = xLeftSpace, xRight
                else:
                    xl, xr = xLeft, xRightSpace

            self.pages[loc].addLine(
                xl, y, xr, y,
                transform=f'scale({self.scale})',
                class_='line'
            )
            y += self.lineHeight
            lineNo += 1

    def addFirstCal(self, loc):
        calID = self.calendarOrder[0]

        self.pages[loc].addStyle(
            'firstCal',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("firstCal","")}";'
            f'font-size:{self.fontSize.get("firstCal", self.lineHeight * self.daysHeight * 2)/self.scale}px;'
            'text-anchor:middle;'
        )
        self.pages[loc].addStyle(
            'holiday',
            f'fill:{self.secondColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("holiday","")}";'
            f'font-size:{self.fontSize.get("holiday", self.lineHeight * self.daysHeight * 2)/self.scale}px;'
            'text-anchor:middle;'
        )
        self.pages[loc].addStyle(
            'firstCalWeekdays',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("firstCalWeekdays","")}";'
            f'font-size:{self.fontSize.get("firstCalWeekdays", 8)/self.scale}px;'
            'text-anchor:middle;'
        )
        self.pages[loc].addStyle(
            'firstCalWeekdaysHoliday',
            f'fill:{self.secondColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("firstCalWeekdaysHoliday","")}";'
            f'font-size:{self.fontSize.get("firstCalWeekdaysHoliday", 8)/self.scale}px;'
            'text-anchor:middle;'
        )

        space = self.lineHeight * self.daysHeight * 0.55
        xLeftSpace, xRightSpace = self.xloc(loc, space)

        x = xLeftSpace if self.layout == 'left' else xRightSpace
        for i in range(len(self.weekKeys)):
            dayKey = self.weekKeys[i]

            # y location
            dayH = self.fontHeightScl * \
                self.fontSize.get("firstCal", self.lineHeight *
                                  self.daysHeight * 2)/self.scale
            weekdayH = self.fontSize.get("firstCalWeekdays", 8)/self.scale

            if self.showWeekdays:
                yNo = (self.daysY[i]+self.daysY[i+1])/2 + dayH/2-weekdayH/2-0.5
                yWeekday = yNo + weekdayH + 1
            else:
                yNo = (self.daysY[i]+self.daysY[i+1])/2 + dayH/2
                yWeekday = 0

            # holiday style
            holiday = False
            for e in self.dataJson[dayKey]['event']['values']:
                if e["dayoff"] == True:
                    holiday = True
            if i > 6-self.weekend:
                holiday = True

            # text of cal
            textCal = self.dataJson[dayKey][calID]['date'][2]
            if calID == 'sh':
                textCal = perNo(textCal)
            elif calID == 'ic':
                textCal = arbNo(textCal)

            textWeekday = self.dataJson[dayKey][calID]['weekday']

            if isinstance(textWeekday, list):
                textWeekday = textWeekday[1]

            self.pages[loc].addText(
                x,
                yNo,
                textCal,
                transform=f'scale({self.scale})',
                class_='holiday' if holiday else 'firstCal'
            )

            if self.showWeekdays:
                self.pages[loc].addText(
                    x,
                    yWeekday,
                    textWeekday,
                    transform=f'scale({self.scale})',
                    class_='firstCalWeekdaysHoliday' if holiday else 'firstCalWeekdays'
                )

    def addSecondCal(self, loc):
        pass

    def addthirdCal(self, loc):
        pass

    def addEventOfDays(self, loc):
        pass
