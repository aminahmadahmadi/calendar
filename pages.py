from aaaSvg import Svg
from replaceText import perNo, arbNo


class Page():
    def __init__(self, name='Untitle-Page', **kwargs) -> None:
        # general
        self.name = name
        self.width = kwargs.get('width', 148)
        self.height = kwargs.get('height', 210)
        self.scale = kwargs.get('scale', 2.83465)

        # Trim Mark
        self.trimMarkMargin = kwargs.get('trimMarkMargin', 3)
        self.trimMark = kwargs.get('trimMark', 0)

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
            self.drawTrimMark(loc)

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

    def drawTrimMark(self, loc):
        if self.trimMark == 0:
            return

        _dir = {
            'right': ['inside', 'outside'],
            'left': ['outside', 'inside']
        }
        self.pages[loc].addStyle(
            'trimMark',
            'fill:none;'
            'stroke:#000;'
            'stroke-width:0.05;'
            f'transform:scale({self.scale});'
        )

        for x in [self.margin[_dir[loc][0]], self.width+self.margin[_dir[loc][0]]]:
            y1 = self.margin['top']-self.trimMarkMargin
            y2 = self.height + self.margin['top'] + self.trimMarkMargin

            self.pages[loc].addLine(
                x, y1 - self.trimMark, x, y1,
                class_='trimMark'
            )
            self.pages[loc].addLine(
                x, y2, x, y2 + self.trimMark,
                class_='trimMark'
            )

        for y in [self.margin['top'], self.height+self.margin['top']]:
            x1 = self.margin[_dir[loc][0]]-self.trimMarkMargin
            x2 = self.width + self.margin[_dir[loc][0]] + self.trimMarkMargin

            self.pages[loc].addLine(
                x1 - self.trimMark, y, x1, y,
                class_='trimMark'
            )
            end = self.width + self.margin['inside'] + self.margin['outside']
            self.pages[loc].addLine(
                x2, y, x2 + self.trimMark, y,
                class_='trimMark'
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
        self.lineColor = kwargs.get('lineColor', '#999')

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
            self.drawTrimMark(loc)

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
    def __init__(self, weekNo, weekKeys, name='Untitle-WeekPage', **kwargs) -> None:
        super().__init__(name, **kwargs)

        self.dataJson = kwargs.get('dataJson', 'left')
        self.weekKeys = weekKeys
        self.weekNo = weekNo
        self.divider = kwargs.get('divider', ' / ')

        self.layout = kwargs.get('layout', 'left')
        self.daysHeight = kwargs.get('daysHeight', 4)
        self.lineShiftDown = kwargs.get('lineShiftDown', 0)
        self.weekend = kwargs.get('weekend', 0)

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
        self.showWeekNo = kwargs.get('showWeekNo', True)
        self.showTime = kwargs.get('showTime', False)

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
            self.addThirdCal(loc)
            self.drawTime(loc)
            if self.showEvents:
                self.addEventOfDays(loc)
            self.addMonthandWeek(loc)
            self.drawGuide(loc)
            self.drawTrimMark(loc)

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
        while lineNo < self.daysHeight*7+1+self.lineShiftDown or y <= self.svgHeight - self.margin['bottom'] - self.padding['bottom']:
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

    def calendarText(self, calID, dayKey, full=False):
        if full:
            if calID == 'sh':
                sh = self.dataJson[dayKey][calID]
                textCal = f"{sh['date'][2]} {sh['monthName']} {sh['date'][0]}"
            elif calID == 'wc':
                wc = self.dataJson[dayKey][calID]
                textCal = f"{wc['monthName'][1]} {wc['date'][2]}, {wc['date'][0]}"
            elif calID == 'ic':
                ic = self.dataJson[dayKey][calID]
                textCal = f"{ic['date'][2]} {ic['monthName']} {ic['date'][0]}"
        else:
            cal = self.dataJson[dayKey][calID]
            textCal = str(cal['date'][2])

        if calID == 'sh':
            return perNo(textCal)
        elif calID == 'wc':
            return textCal
        elif calID == 'ic':
            return arbNo(textCal)

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
            textCal = self.calendarText(calID, dayKey)
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

    def drawTime(self, loc, pattern='01'):
        if not self.showTime:
            return

        self.pages[loc].addStyle(
            'time',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("time","")}";'
            f'font-size:{self.fontSize.get("time", 5)/self.scale}px;'
            'text-anchor:middle;'
        )
        xLeft, xRight = self.xloc(loc)
        space = self.lineHeight*self.daysHeight*1.75
        xLeftSpace, xRightSpace = self.xloc(loc, space)

        if self.layout == 'left':
            xl, xr = xLeftSpace, xRight
        else:
            xl, xr = xLeft, xRightSpace

        for y in self.daysY[:-1]:
            calH = self.fontHeightScl * \
                self.fontSize.get('time', 5)/self.scale

            y1 = y
            y2 = y1+1
            y3 = y2 + calH + 0.5

            for i in range(17):
                x = xl + (xr-xl)*i/17
                self.pages[loc].addLine(
                    x, y1, x, y2,
                    transform=f'scale({self.scale})',
                    class_='line'
                )
                if pattern[i % len(pattern)] == '1':
                    self.pages[loc].addText(
                        x,
                        y3,
                        perNo(i+6),
                        transform=f'scale({self.scale})',
                        class_='time',
                    )

    def addOtherCal(self, loc, order):
        if order == 'secondCal':
            calID = self.calendarOrder[1]
            downH = 0.5
        elif order == 'thirdCal':
            calID = self.calendarOrder[2]
            downH = 1.5

        try:
            startAnchor = (self.layout == "right") ^ (calID == "wc")
            self.pages[loc].addStyle(
                order,
                f'fill:{self.primaryColor};'
                f'stroke:None;'
                f'font-family:"{self.fontFamily} {self.fontWeight.get(order,"")}";'
                f'font-size:{self.fontSize.get(order, 8)/self.scale}px;'
                f'text-anchor:{"start" if startAnchor else "end"};'
                f'direction:{"ltr" if calID=="wc" else "rtl"};'
            )

            for i in range(len(self.weekKeys)):
                dayKey = self.weekKeys[i]
                cal = self.dataJson[dayKey][calID]

                # x and y location
                calH = self.fontHeightScl * \
                    self.fontSize.get(order, 8)/self.scale
                y = self.daysY[i] + self.lineHeight * downH + calH/2
                space = self.lineHeight*self.daysHeight
                xLeftSpace, xRightSpace = self.xloc(loc, space+0.5)
                x = xLeftSpace if self.layout == "left" else xRightSpace

                isfull = self.showFullCalendar or cal['date'][2] == 1 or i == 0
                self.pages[loc].addText(
                    x,
                    y,
                    self.calendarText(calID, dayKey, isfull),
                    transform=f'scale({self.scale})',
                    class_=order
                )
        except:
            pass

    def addSecondCal(self, loc):
        self.addOtherCal(loc, 'secondCal')

    def addThirdCal(self, loc):
        self.addOtherCal(loc, 'thirdCal')

    def addEventOfDays(self, loc):
        self.pages[loc].addStyle(
            'events',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("events","")}";'
            f'font-size:{self.fontSize.get("events", 5)/self.scale}px;'
            'text-anchor:start;'
            'direction: rtl'
        )

        for i in range(len(self.weekKeys)):
            dayKey = self.weekKeys[i]
            events = self.dataJson[dayKey]['event']['values']

            eventList = list(map(lambda e: e['occasion'], events))
            eventList = list(
                map(lambda x: x if len(x) < 120 else '', eventList))
            eventText = self.divider.join(eventList)
            eventText2 = ''
            textArea = self.width - \
                self.padding['inside']-self.padding['outside'] - \
                self.lineHeight*(1+self.daysHeight)
            l = 7.8 * (textArea) / self.fontSize['events']

            if len(eventText) > l:
                j = 1
                while (len(self.divider.join(eventList[-j:])) < l and j < len(eventList)):
                    eventText2 = self.divider.join(eventList[:-j])
                    eventText = self.divider.join(eventList[-j:])
                    j += 1

            # x and y location
            space = self.lineHeight if self.layout == 'left' else self.daysHeight*self.lineHeight
            _, xRightSpace = self.xloc(loc, space+0.5)
            calH = self.fontHeightScl * \
                self.fontSize.get('events', 5)/self.scale
            y1 = self.daysY[i+1] - self.lineHeight * 0.5 + calH/2
            y2 = self.daysY[i+1] - self.lineHeight * 1.5 + calH/2

            self.pages[loc].addText(
                xRightSpace,
                y1,
                perNo(eventText),
                transform=f'scale({self.scale})',
                class_='events',
            )
            self.pages[loc].addText(
                xRightSpace,
                y2,
                perNo(eventText2),
                transform=f'scale({self.scale})',
                class_='events',
            )
        pass

    def addMonthandWeek(self, loc):
        self.pages[loc].addStyle(
            'monthAndWeek',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("monthAndWeek","")}";'
            f'font-size:{self.fontSize.get("monthAndWeek", 8)/self.scale}px;'
            f'text-anchor:{"start" if self.layout=="left" else "end"};'
        )

        calID = self.calendarOrder[0]
        startMonth = self.dataJson[self.weekKeys[0]][calID]['monthName']
        endMonth = self.dataJson[self.weekKeys[-1]][calID]['monthName']
        if isinstance(startMonth, list):
            startMonth = startMonth[1]
            endMonth = endMonth[1]

        monthes = [startMonth] if startMonth == endMonth else [
            startMonth, endMonth]

        weekText = f'هفته {perNo(self.weekNo)}  {self.divider}  ' if self.showWeekNo else ''
        monthText = " و ".join(monthes)
        text = weekText+monthText

        # x and y location
        calH = self.fontHeightScl * \
            self.fontSize.get("monthAndWeek", 8)/self.scale
        y = self.daysY[0] - self.lineHeight * 0.5 + calH/2
        space = self.lineHeight*self.daysHeight
        xLeftSpace, xRightSpace = self.xloc(loc, space+0.5)
        x = xLeftSpace if self.layout == "left" else xRightSpace

        self.pages[loc].addText(
            x,
            y,
            text,
            transform=f'scale({self.scale})',
            class_='monthAndWeek'
        )


class LinePageWithTitle(LinePage):
    def __init__(self, title='', name='Untitle-LinePage', **kwargs) -> None:
        super().__init__(name, **kwargs)

        self.title = title

        # colors
        self.primaryColor = kwargs.get('primaryColor', '#000')

        # font style
        self.fontHeightScl = kwargs.get('fontHeightScl', 0.66)
        self.fontFamily = kwargs.get('fontFamily', 'Anjoman')
        self.fontWeight = kwargs.get('fontWeight', {})
        self.fontSize = kwargs.get('fontSize', {})

    def makePages(self):
        super().makePages()
        for loc in ['right', 'left']:
            self.addTitle(loc)

    def addTitle(self, loc):
        self.pages[loc].addStyle(
            'titleofpage',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("monthAndWeek","")}";'
            f'font-size:{self.fontSize.get("monthAndWeek", 8)/self.scale}px;'
            'text-anchor:start;'
            'direction:rtl;'
        )

        # x and y location
        calH = self.fontHeightScl * \
            self.fontSize.get("monthAndWeek", 8)/self.scale
        y = self.margin['top']+self.padding['top'] - \
            self.lineHeight * 0.5 + calH/2
        space = self.lineHeight*2
        xLeftSpace, xRightSpace = self.xloc(loc, space+0.5)
        x = xRightSpace

        self.pages[loc].addText(
            x,
            y,
            self.title,
            transform=f'scale({self.scale})',
            class_='titleofpage'
        )


class ChecklistPage(LinePageWithTitle):
    def __init__(self, title='', name='Untitle-LinePage', pattern='010', checkboxscale=0.6, **kwargs) -> None:
        super().__init__(title, name, **kwargs)

        self.pattern = pattern
        self.checkboxscale = checkboxscale

    def makePages(self):
        super().makePages()
        for loc in ['right', 'left']:
            self.addCheckBox(loc)

    def addCheckBox(self, loc):
        self.pages[loc].addStyle(
            'checkbox',
            'fill:white;'
            f'stroke:{self.lineColor};'
            f'stroke-width:{self.lineWidth};'
        )
        lines = (self.height-self.padding['top'] -
                 self.padding['bottom']) // self.lineHeight+1
        space = self.lineHeight*2
        xLeftSpace, xRightSpace = self.xloc(loc, space+0.5)
        x = xRightSpace
        w = self.lineHeight*self.checkboxscale
        for i in range(lines):
            if self.pattern[i % len(self.pattern)] == '1':
                self.pages[loc].addRect(
                    x-w,
                    self.padding['top']+i*self.lineHeight-w/2,
                    w,
                    w,
                    transform=f'scale({self.scale})',
                    class_='checkbox',
                )


class FirstPage(LinePage):
    def __init__(self, name='John Smith', sentence=[], years=['1401', '2022 - 2023', '1444 - 1443'], turnOfYear=['یک شنبه ۲۹ اسفندماه ۱۴۰۰', 'ساعت ۱۹:۰۳:۲۶'], **kwargs) -> None:
        super().__init__(name, **kwargs)

        self.sentence = sentence
        self.years = years
        self.turnOfYear = turnOfYear

        # colors
        self.primaryColor = kwargs.get('primaryColor', '#000')

        # font style
        self.fontHeightScl = kwargs.get('fontHeightScl', 0.66)
        self.fontFamily = kwargs.get('fontFamily', 'Anjoman')
        self.fontWeight = kwargs.get('fontWeight', {})
        self.fontSize = kwargs.get('fontSize', {})

        self.daysHeight = kwargs.get('daysHeight', 4)

    def makePages(self):
        for loc in ['right', 'left']:
            self.definePage(loc)
            self.addYears(loc)
            self.addNameSentence(loc)
            self.drawGuide(loc)
            self.drawTrimMark(loc)

    def addYears(self, loc):
        first, second, third = tuple(self.years)
        self.pages[loc].addStyle(
            'firstInfo',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("firstPageTitle","")}";'
            f'font-size:{self.fontSize.get("firstPageTitle", self.lineHeight*self.daysHeight*4)/self.scale}px;'
            f'text-anchor:{"start" if loc=="left" else "end"};'
        )
        self.pages[loc].addStyle(
            'secondInfo',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("firstPageOther","")}";'
            f'font-size:{self.fontSize.get("firstPageOther", 9)/self.scale}px;'
            f'text-anchor:{"start" if loc=="left" else "end"};'
        )
        self.pages[loc].addStyle(
            'turnOfYear',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("turnOfYear","")}";'
            f'font-size:{self.fontSize.get("turnOfYear", 7)/self.scale}px;'
            f'text-anchor:{"start" if loc=="right" else "end"};'
            'direction:rtl;'

        )

        space = self.lineHeight * self.daysHeight
        xLeftSpace, xRightSpace = self.xloc(loc, space)

        x = xLeftSpace if loc == 'left' else xRightSpace
        y = self.margin['top']+self.padding['top'] + \
            self.lineHeight*self.daysHeight*0.9

        self.pages[loc].addText(
            x-self.lineHeight * self.daysHeight / 7,
            y,
            perNo(first),
            transform=f'scale({self.scale})',
            class_='firstInfo'
        )
        self.pages[loc].addText(
            x,
            y+self.lineHeight*1.2,
            second,
            transform=f'scale({self.scale})',
            class_='secondInfo'
        )
        self.pages[loc].addText(
            x,
            y+self.lineHeight*2,
            arbNo(third),
            transform=f'scale({self.scale})',
            class_='secondInfo'
        )

        for i in range(len(self.turnOfYear)):
            self.pages[loc].addText(
                x,
                y+self.lineHeight*(5+0.1*self.fontSize.get("turnOfYear", 7)*i),
                perNo(self.turnOfYear[i]),
                transform=f'scale({self.scale})',
                class_='turnOfYear'
            )

    def addNameSentence(self, loc):
        self.pages[loc].addStyle(
            'name',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("name","")}";'
            f'font-size:{self.fontSize.get("name", 79)/self.scale}px;'
            f'text-anchor:{"start" if loc=="right" else "end"};'
            'direction:rtl;'
        )
        self.pages[loc].addStyle(
            'sentence',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("sentence","")}";'
            f'font-size:{self.fontSize.get("sentence", 9)/self.scale}px;'
            f'text-anchor:{"start" if loc=="right" else "end"};'
            'direction:rtl;'

        )

        space = self.lineHeight * self.daysHeight
        xLeftSpace, xRightSpace = self.xloc(loc, space)

        x = xLeftSpace if loc == 'left' else xRightSpace
        y = self.height + \
            self.margin['top'] - self.padding['bottom'] - \
            (len(self.sentence)+3)*self.lineHeight

        self.pages[loc].addText(
            x,
            y,
            perNo(self.name),
            transform=f'scale({self.scale})',
            class_='name'
        )

        y += self.lineHeight
        for line in self.sentence:
            y += self.lineHeight
            self.pages[loc].addText(
                x,
                y,
                perNo(line),
                transform=f'scale({self.scale})',
                class_='sentence'
            )


class HolidaysPage(LinePageWithTitle):
    def __init__(self, year=1401, shiftDownHolidays=2, title='تعطیلات رسمی ۱۴۰۱', name='Untitle-LinePage', **kwargs) -> None:
        super().__init__(title, name, **kwargs)
        self.dataJson = kwargs.get('dataJson', '')
        self.shiftDownHolidays = shiftDownHolidays
        self.holidays = []
        for day in self.dataJson.keys():
            dayYear = self.dataJson[day]['sh']['date'][0]
            if self.dataJson[day]['sh']['date'][0] == year:
                events = self.dataJson[day]['event']['values']
                for e in events:
                    if e['dayoff'] == True:
                        self.holidays.append((day, e['occasion']))
                        break

    def makePages(self):
        super().makePages()
        for loc in ['right', 'left']:
            self.addHolidays(loc)

    def addHolidays(self, loc):

        self.pages[loc].addStyle(
            'holiday',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("holidaysPage","")}";'
            f'font-size:{self.fontSize.get("holidaysPage", 7)/self.scale}px;'
            'text-anchor:start;'
            'direction:rtl;'
        )
        self.pages[loc].addStyle(
            'holiday',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("holidaysPage","")}";'
            f'font-size:{self.fontSize.get("holidaysPage", 7)/self.scale}px;'
            'text-anchor:start;'
            'direction:rtl;'
        )
        self.pages[loc].addStyle(
            'holidayNo',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("holidaysPageNo","")}";'
            f'font-size:{self.fontSize.get("holidaysPageNo", 7)/self.scale}px;'
            'text-anchor:middle;'
            'direction:rtl;'
        )

        calH = self.fontHeightScl * \
            self.fontSize.get("holidaysPage", 7)/self.scale
        y = self.margin['top']+self.padding['top'] + \
            self.lineHeight * (self.shiftDownHolidays+0.5) + calH/2

        _, x1 = self.xloc(loc, 2*self.lineHeight+0.5)
        _, x2 = self.xloc(loc, 5*self.lineHeight+0.5)
        _, x3 = self.xloc(loc, 6*self.lineHeight+0.5)
        _, x4 = self.xloc(loc, 9*self.lineHeight+0.5)

        lastMonth = ''
        for day, event in self.holidays:
            monthName = self.dataJson[day]['sh']['monthName']
            dateInfo = self.dataJson[day]['sh']

            # x and y location
            if monthName != lastMonth:
                self.pages[loc].addText(
                    x1,
                    y,
                    perNo(monthName),
                    transform=f'scale({self.scale})',
                    class_='holiday'
                )
                lastMonth = monthName
            self.pages[loc].addText(
                x2,
                y,
                perNo(dateInfo['date'][2]),
                transform=f'scale({self.scale})',
                class_='holidayNo'
            )
            self.pages[loc].addText(
                x3,
                y,
                perNo(dateInfo['weekday']),
                transform=f'scale({self.scale})',
                class_='holiday'
            )
            self.pages[loc].addText(
                x4,
                y,
                perNo(event),
                transform=f'scale({self.scale})',
                class_='holiday'
            )
            y += self.lineHeight
