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
            if self.showEvents:
                self.addEventOfDays(loc)
            self.addMonthandWeek(loc)
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

    def addOtherCal(self, loc, order):
        if order == 'secondCal':
            calID = self.calendarOrder[1]
            downH = 0.5
        elif order == 'thirdCal':
            calID = self.calendarOrder[2]
            downH = 1.5

        try:
            self.pages[loc].addStyle(
                order,
                f'fill:{self.primaryColor};'
                f'stroke:None;'
                f'font-family:"{self.fontFamily} {self.fontWeight.get(order,"")}";'
                f'font-size:{self.fontSize.get(order, 8)/self.scale}px;'
                f'text-anchor:{"start" if self.layout=="left" else "end"};'
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
            'text-anchor:end;'
        )

        for i in range(len(self.weekKeys)):
            dayKey = self.weekKeys[i]
            events = self.dataJson[dayKey]['event']['values']

            eventList = list(map(lambda e: e['occasion'], events))
            eventList = list(
                map(lambda x: x if len(x) < 120 else '', eventList))
            eventText = self.divider.join(eventList)
            eventText2 = ''
            l = 875 / self.fontSize['events']
            if len(eventText) > l:
                i = 1
                while (len(self.divider.join(eventList[-i:])) < l and i < len(eventList)):
                    eventText2 = self.divider.join(eventList[:-i])
                    eventText = self.divider.join(eventList[-i:])
                    i += 1

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
                eventText,
                transform=f'scale({self.scale})',
                class_='events',
            )
            self.pages[loc].addText(
                xRightSpace,
                y2,
                eventText2,
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
