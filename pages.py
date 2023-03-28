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
        )

        for x in [self.margin[_dir[loc][0]], self.width+self.margin[_dir[loc][0]]]:
            y1 = self.margin['top']-self.trimMarkMargin
            y2 = self.height + self.margin['top'] + self.trimMarkMargin

            self.pages[loc].addLine(
                x, y1 - self.trimMark, x, y1,
                class_='trimMark',
                transform=f'scale({self.scale})'
            )
            self.pages[loc].addLine(
                x, y2, x, y2 + self.trimMark,
                class_='trimMark',
                transform=f'scale({self.scale})'
            )

        for y in [self.margin['top'], self.height+self.margin['top']]:
            x1 = self.margin[_dir[loc][0]]-self.trimMarkMargin
            x2 = self.width + self.margin[_dir[loc][0]] + self.trimMarkMargin

            self.pages[loc].addLine(
                x1 - self.trimMark, y, x1, y,
                class_='trimMark',
                transform=f'scale({self.scale})'
            )
            end = self.width + self.margin['inside'] + self.margin['outside']
            self.pages[loc].addLine(
                x2, y, x2 + self.trimMark, y,
                class_='trimMark',
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

    def xloc(self, loc, space=None, margin=False):
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
        elif margin:
            xLeft = self.margin[_dir[loc][0]] if self.padding[_dir[loc][0]] == 0 else self.padding[_dir[loc][0]] + \
                self.margin[_dir[loc][0]]
            xRight = self.svgWidth
            xRight -= self.margin[_dir[loc][1]] if self.padding[_dir[loc][1]] == 0 else self.padding[_dir[loc][1]] + \
                self.margin[_dir[loc][1]]
            return (xLeft, xRight)
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

        self.daysJson = kwargs.get('daysJson', '')
        self.eventJson = kwargs.get('eventJson', '')
        self.calNamesJson = kwargs.get('calNamesJson', '')

        self.weekKeys = weekKeys
        self.weekNo = weekNo
        self.divider = kwargs.get('divider', ' / ')
        self.personalEvents = kwargs.get('personalEvents', {})

        self.layout = kwargs.get('layout', 'left')
        self.daysHeight = kwargs.get('daysHeight', 4)
        self.lineShiftDown = kwargs.get('lineShiftDown', 0)
        self.weekend = kwargs.get('weekend', 0)
        self.iconSize = kwargs.get('iconSize', self.lineHeight*0.8)

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
            self.addPersonalEvents(loc)
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
                sh = self.daysJson[dayKey][calID]
                month = self.calNamesJson[calID]['month'][str(sh[1])]

                textCal = f"{sh[2]} {month} {sh[0]}"
            elif calID == 'wc':
                wc = self.daysJson[dayKey][calID]
                month = self.calNamesJson[calID]['month'][str(wc[1])]

                textCal = f"{month} {wc[2]}, {wc[0]}"
            elif calID == 'ic':
                ic = self.daysJson[dayKey][calID]
                month = self.calNamesJson[calID]['month'][str(ic[1])]

                textCal = f"{ic[2]} {month} {ic[0]}"
        else:
            cal = self.daysJson[dayKey][calID]
            textCal = str(cal[2])

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

            todaySh = self.daysJson[dayKey]["sh"]
            todayIc = self.daysJson[dayKey]["ic"]
            todayWc = self.daysJson[dayKey]["wc"]

            events = []
            events += self.eventJson.get(
                f"sh-{todaySh[1]}-{todaySh[2]}", [])
            events += self.eventJson.get(
                f"ic-{todayIc[1]}-{todayIc[2]}", [])
            events += self.eventJson.get(
                f"wc-{todayWc[1]}-{todayWc[2]}", [])

            for e in events:
                if e["dayoff"] == True:
                    holiday = True
            if i > 6-self.weekend:
                holiday = True

            # text of cal
            textCal = self.calendarText(calID, dayKey)

            wd = str(self.daysJson[dayKey]['weekday'])
            textWeekday = self.calNamesJson[calID]['weekday'][wd]

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

    def addPersonalEvents(self, loc):
        iconPath = {
            'cake': 'M 0.863 0.7952 h -0.0572 v -0.2761 a 0.0759 0.0759 90 0 0 -0.0758 -0.0757 h -0.1861 v -0.1089 a 0.0279 0.0279 90 0 0 -0.0279 -0.0279 h -0.004 v -0.0359 a 0.012 0.012 90 0 0 -0.024 0 v 0.0359 h -0.004 a 0.0279 0.0279 90 0 0 -0.0279 0.0279 v 0.1089 h -0.1961 a 0.0759 0.0759 90 0 0 -0.0758 0.0757 v 0.2761 h -0.0472 a 0.012 0.012 90 1 0 0 0.024 h 0.0069 l 0.0069 0.0241 a 0.0456 0.0456 90 0 0 0.042 0.0317 h 0.6144 a 0.0456 0.0456 90 0 0 0.042 -0.0317 l 0.0069 -0.0241 h 0.0069 a 0.012 0.012 90 1 0 0 -0.024 z m -0.383 -0.4607 a 0.0041 0.0041 90 0 1 0.0039 -0.004 h 0.032 a 0.0041 0.0041 90 0 1 0.0039 0.004 v 0.1089 h -0.0398 z m -0.22 0.1328 h 0.47 a 0.052 0.052 90 0 1 0.0519 0.0518 v 0.0368 a 0.0835 0.0835 90 0 0 -0.0456 0.0229 a 0.0579 0.0579 90 0 1 -0.0843 0 a 0.0816 0.0816 90 0 0 -0.115 0 a 0.0579 0.0579 90 0 1 -0.0843 0 a 0.0816 0.0816 90 0 0 -0.115 0 a 0.0789 0.0789 90 0 1 -0.0224 0.0149 a 0.012 0.012 90 0 0 -0.0078 0.0112 v 0.0818 a 0.012 0.012 90 1 1 -0.0239 0 v -0.0814 a 0.0119 0.0119 90 0 0 -0.0077 -0.0116 a 0.0762 0.0762 90 0 1 -0.0224 -0.0149 a 0.0838 0.0838 90 0 0 -0.0456 -0.0229 v -0.0368 a 0.052 0.052 90 0 1 0.0521 -0.0518 z m -0.0521 0.1127 a 0.0637 0.0637 90 0 1 0.03 0.017 a 0.1173 0.1173 90 0 0 0.0221 0.0156 v 0.0741 a 0.0359 0.0359 90 1 0 0.0718 0 v -0.0741 a 0.12 0.12 90 0 0 0.0216 -0.0155 a 0.058 0.058 90 0 1 0.0842 0 a 0.0815 0.0815 90 0 0 0.1151 0 a 0.058 0.058 90 0 1 0.0842 0 a 0.0815 0.0815 90 0 0 0.1151 0 a 0.0635 0.0635 90 0 1 0.03 -0.017 v 0.2151 h -0.5741 v -0.2152 z m 0.6183 0.2567 a 0.022 0.022 90 0 1 -0.019 0.0144 h -0.6144 a 0.022 0.022 90 0 1 -0.019 -0.0144 l -0.005 -0.0175 h 0.6624 z m -0.383 -0.5632 a 0.0759 0.0759 90 0 1 -0.0193 -0.0506 c 0 -0.0387 0.0293 -0.0785 0.0713 -0.0969 a 0.0123 0.0123 90 0 1 0.01 0 c 0.042 0.0184 0.0713 0.0582 0.0713 0.0969 a 0.0759 0.0759 90 0 1 -0.0193 0.0506 a 0.012 0.012 90 0 1 -0.0179 -0.016 a 0.0516 0.0516 90 0 0 0.0133 -0.0346 c 0 -0.0281 -0.0212 -0.0573 -0.0522 -0.0727 c -0.031 0.0154 -0.0522 0.0446 -0.0522 0.0727 a 0.0516 0.0516 90 0 0 0.0133 0.0346 a 0.012 0.012 90 0 1 -0.001 0.0169 a 0.0117 0.0117 90 0 1 -0.008 0.0031 a 0.0121 0.0121 90 0 1 -0.0093 -0.004 z',
            'fire': 'M 0.7417 0.4956 c -0.0152 -0.07 -0.0284 -0.13 -0.0023 -0.1848 a 0.0131 0.0131 90 0 0 -0.0142 -0.0185 c -0.0031 0.0006 -0.0731 0.0148 -0.1179 0.1137 a 0.3755 0.3755 90 0 1 -0.0464 -0.075 a 0.3172 0.3172 90 0 1 -0.0181 -0.231 a 0.0131 0.0131 90 0 0 -0.0173 -0.0159 a 0.2216 0.2216 90 0 0 -0.0738 0.0538 c -0.0324 0.0353 -0.0693 0.0979 -0.0612 0.196 a 0.7242 0.7242 90 0 1 0.0018 0.1137 a 0.2248 0.2248 90 0 0 -0.0426 -0.08 a 0.2146 0.2146 90 0 0 -0.0525 -0.0466 a 0.0131 0.0131 90 0 0 -0.0193 0.0138 c 0.0159 0.0857 0 0.1343 -0.0165 0.1859 a 0.3962 0.3962 90 0 0 -0.025 0.1318 a 0.2636 0.2636 90 0 0 0.5272 0 a 0.728 0.728 90 0 0 -0.0219 -0.1569 z m -0.1445 0.3744 a 0.1238 0.1238 90 0 0 0.0272 -0.0775 a 0.4686 0.4686 90 0 0 -0.05 -0.2077 a 0.4 0.4 90 0 0 -0.0506 -0.0793 a 0.013 0.013 90 0 0 -0.02 0.0172 a 0.4449 0.4449 90 0 1 0.0942 0.27 a 0.0984 0.0984 90 0 1 -0.098 0.0979 c -0.0563 0 -0.0983 -0.0519 -0.0983 -0.0983 a 0.13 0.13 90 0 1 0.01 -0.0509 a 0.013 0.013 90 1 0 -0.0242 -0.01 a 0.1546 0.1546 90 0 0 -0.0118 0.06 a 0.1239 0.1239 90 0 0 0.03 0.0788 a 0.238 0.238 90 0 1 -0.1433 -0.218 a 0.37 0.37 90 0 1 0.0237 -0.1238 c 0.0149 -0.046 0.03 -0.0933 0.0221 -0.1667 a 0.2005 0.2005 90 0 1 0.0673 0.1513 a 0.0131 0.0131 90 0 0 0.0079 0.012 a 0.0129 0.0129 90 0 0 0.0141 -0.0025 c 0.0053 -0.005 0.0315 -0.0378 0.0189 -0.1915 c -0.0058 -0.0708 0.0122 -0.13 0.0537 -0.1754 a 0.2119 0.2119 90 0 1 0.04 -0.0343 a 0.35 0.35 90 0 0 0.0269 0.22 a 0.366 0.366 90 0 0 0.0651 0.0987 a 0.0131 0.0131 90 0 0 0.012 0.0036 a 0.0135 0.0135 90 0 0 0.01 -0.0082 c 0.0239 -0.0638 0.0584 -0.0933 0.0815 -0.1067 c -0.0156 0.0539 -0.0026 0.1118 0.0106 0.1725 a 0.6965 0.6965 90 0 1 0.0213 0.1519 a 0.2381 0.2381 90 0 1 -0.1403 0.2169 z m -0.0831 -0.2714 a 0.0131 0.0131 90 0 0 -0.0156 0.01 a 0.1453 0.1453 90 0 1 -0.013 0.0362 c -0.0269 -0.0315 -0.052 -0.0325 -0.0551 -0.0325 a 0.0131 0.0131 90 0 0 -0.013 0.0131 a 0.1725 0.1725 90 0 1 -0.0074 0.0517 a 0.0131 0.0131 90 0 0 0.0087 0.0163 a 0.0126 0.0126 90 0 0 0.0038 0.0006 a 0.013 0.013 90 0 0 0.0125 -0.0093 a 0.189 0.189 90 0 0 0.0076 -0.0421 l 0.0008 0 a 0.0921 0.0921 90 0 1 0.0316 0.0313 a 0.0133 0.0133 90 0 0 0.01 0.0057 a 0.0129 0.0129 90 0 0 0.0105 -0.0038 c 0.002 -0.0019 0.0193 -0.02 0.0286 -0.062 a 0.013 0.013 90 0 0 -0.01 -0.0152 z',
            'hand': 'M 0.7231 0.1888 a 0.0839 0.0839 90 0 0 -0.0468 -0.0231 v -0.0141 a 0.0642 0.0642 90 0 0 -0.1158 -0.0384 a 0.0639 0.0639 90 0 0 -0.1029 0 a 0.064 0.064 90 0 0 -0.11 0.0117 a 0.0582 0.0582 90 0 0 -0.0966 0.0437 v 0.0764 a 0.0562 0.0562 90 0 0 0.0008 0.0092 l 0.0048 0.1591 a 0.1378 0.1378 90 0 0 0.022 0.0707 l 0.057 0.0879 a 0.0171 0.0171 90 0 1 0.0027 0.0093 v 0.024 h -0.037 a 0.0332 0.0332 90 0 0 -0.0331 0.0331 v 0.039 a 0.033 0.033 90 0 0 0.0318 0.0327 l -0.015 0.1591 a 0.0427 0.0427 90 0 0 0.0426 0.0469 h 0.324 a 0.0427 0.0427 90 0 0 0.0426 -0.0469 l -0.015 -0.1591 a 0.033 0.033 90 0 0 0.0319 -0.033 v -0.039 a 0.0332 0.0332 90 0 0 -0.0331 -0.0331 h -0.0407 v -0.0449 a 0.0182 0.0182 90 0 1 0.0021 -0.0082 l 0.09 -0.165 a 0.1567 0.1567 90 0 0 0.019 -0.0746 v -0.063 a 0.0839 0.0839 90 0 0 -0.0253 -0.0604 z m -0.1111 -0.0759 a 0.0387 0.0387 90 0 1 0.0386 0.0387 v 0.0134 l -0.0772 0.0018 v -0.0152 a 0.0387 0.0387 90 0 1 0.0386 -0.0387 z m -0.1029 0 a 0.0387 0.0387 90 0 1 0.0386 0.0387 v 0.0157 l -0.0077 0 a 0.0587 0.0587 90 0 0 -0.057 0.0583 v 0.015 a 0.05 0.05 90 0 0 0.01 0.0317 a 0.0426 0.0426 90 0 1 -0.0228 -0.0376 v -0.0831 a 0.0387 0.0387 90 0 1 0.0389 -0.0387 z m -0.1415 0.0387 a 0.0386 0.0386 90 1 1 0.0772 0 v 0.0833 a 0.0386 0.0386 90 0 1 -0.0772 0 v -0.0833 z m -0.0583 -0.0155 a 0.0326 0.0326 90 0 1 0.0326 0.0325 v 0.0764 a 0.0325 0.0325 90 0 1 -0.0643 0.0068 l -0.0008 -0.0246 v -0.0586 a 0.0326 0.0326 90 0 1 0.0325 -0.0325 z m 0.355 0.7489 a 0.017 0.017 90 0 1 -0.0127 0.0056 h -0.3238 a 0.017 0.017 90 0 1 -0.017 -0.0188 l 0.0152 -0.1618 h 0.3274 l 0.0153 0.1614 a 0.0172 0.0172 90 0 1 -0.0044 0.0136 z m 0.0211 -0.2467 v 0.039 a 0.0074 0.0074 90 0 1 -0.0074 0.0074 h -0.3766 a 0.0074 0.0074 90 0 1 -0.0074 -0.0074 v -0.039 a 0.0074 0.0074 90 0 1 0.0074 -0.0074 h 0.3766 a 0.0074 0.0074 90 0 1 0.0074 0.0074 z m 0.0374 -0.3263 a 0.1306 0.1306 90 0 1 -0.0159 0.0623 l -0.09 0.165 a 0.0423 0.0423 90 0 0 -0.0053 0.02 v 0.0454 h -0.2475 v -0.024 a 0.0425 0.0425 90 0 0 -0.0068 -0.0232 l -0.0573 -0.0875 a 0.1118 0.1118 90 0 1 -0.0179 -0.0574 l -0.0036 -0.1181 a 0.058 0.058 90 0 0 0.079 -0.0174 a 0.064 0.064 90 0 0 0.1 -0.0038 a 0.0642 0.0642 90 0 0 0.0515 0.0259 h 0.07 a 0.0315 0.0315 90 0 1 0.03 0.0215 c -0.0358 0.0452 -0.071 0.0928 -0.0406 0.18 a 0.0128 0.0128 90 1 0 0.0242 -0.0085 c -0.0265 -0.0757 0.0041 -0.1142 0.0394 -0.1588 l 0.001 -0.0012 a 0.0127 0.0127 90 0 0 0.0026 -0.01 a 0.057 0.057 90 0 0 -0.0566 -0.0482 h -0.0377 a 0.0326 0.0326 90 0 1 -0.0326 -0.0327 v -0.015 a 0.0328 0.0328 90 0 1 0.0319 -0.0326 l 0.1221 -0.0027 a 0.0587 0.0587 90 0 1 0.06 0.0587 z',
            'heart': 'M 0.5 0.8749 a 0.0145 0.0145 90 0 1 -0.01 -0.0042 l -0.3254 -0.3252 a 0.2394 0.2394 90 0 1 0.3313 -0.3455 l 0.0041 0.0038 l 0.0041 -0.0038 a 0.2394 0.2394 90 0 1 0.3313 0.3455 l -0.3254 0.3252 a 0.0145 0.0145 90 0 1 -0.01 0.0042 z m -0.1662 -0.7091 a 0.21 0.21 90 0 0 -0.1488 0.3593 l 0.315 0.3149 l 0.3151 -0.315 a 0.2105 0.2105 90 1 0 -0.2978 -0.2976 l -0.0808 0.0808 a 0.0144 0.0144 90 1 1 -0.02 -0.02 l 0.0635 -0.0639 l -0.005 -0.0043 a 0.21 0.21 90 0 0 -0.1412 -0.0542 z m 0.399 0.0633 a 0.0144 0.0144 90 0 0 -0.0086 -0.0185 a 0.1728 0.1728 90 0 0 -0.06 -0.0106 a 0.0144 0.0144 90 1 0 0 0.0288 a 0.1428 0.1428 90 0 1 0.05 0.0088 a 0.0157 0.0157 90 0 0 0.0051 0.0009 a 0.0145 0.0145 90 0 0 0.0135 -0.0094 z m 0.1052 0.1444 a 0.1737 0.1737 90 0 0 -0.0411 -0.1121 a 0.0144 0.0144 90 1 0 -0.022 0.0186 a 0.1448 0.1448 90 0 1 0.0342 0.0935 a 0.0145 0.0145 90 0 0 0.0289 0 z m -0.3471 0.3838 a 0.0145 0.0145 90 0 0 0 -0.02 l -0.0285 -0.0285 a 0.0145 0.0145 90 0 0 -0.02 0 a 0.0142 0.0142 90 0 0 -0.0042 0.01 a 0.0147 0.0147 90 0 0 0.0042 0.01 l 0.0285 0.0285 a 0.0146 0.0146 90 0 0 0.01 0.0042 a 0.0143 0.0143 90 0 0 0.01 -0.0042 z m -0.0755 -0.0754 a 0.0143 0.0143 90 0 0 0 -0.02 l -0.1076 -0.108 a 0.0141 0.0141 90 0 0 -0.02 0 a 0.0142 0.0142 90 0 0 0 0.02 l 0.1073 0.108 a 0.0143 0.0143 90 0 0 0.01 0.0042 a 0.0147 0.0147 90 0 0 0.0103 -0.0042 z',
            'internet': 'M 0.7 0.5 a 0.2 0.2 90 1 0 0.2 0.2 a 0.2 0.2 90 0 0 -0.2 -0.2 z m 0 0.0253 a 0.173 0.173 90 0 1 0.1136 0.0432 l -0.245 0.245 a 0.173 0.173 90 0 1 -0.0433 -0.1135 a 0.1749 0.1749 90 0 1 0.1747 -0.1747 z m 0 0.3492 a 0.1733 0.1733 90 0 1 -0.1136 -0.0431 l 0.245 -0.2451 a 0.1737 0.1737 90 0 1 -0.1314 0.2882 z m -0.2 0 c -0.0716 0 -0.1347 -0.098 -0.1614 -0.2334 h 0.12 a 0.0126 0.0126 90 0 0 0.0125 -0.0122 h 0 a 0.0125 0.0125 90 0 0 -0.0125 -0.013 h -0.1243 a 0.7426 0.7426 90 0 1 0 -0.2318 h 0.3314 c 0.0029 0.018 0.0055 0.05 0.0068 0.0679 a 0.0126 0.0126 90 0 0 0.0139 0.0116 h 0 a 0.0127 0.0127 90 0 0 0.0115 -0.0136 c -0.0013 -0.0172 -0.0037 -0.0485 -0.0064 -0.066 h 0.1645 a 0.3731 0.3731 90 0 1 0.0185 0.116 c 0 0.0064 -0.0008 0.016 -0.0015 0.0237 a 0.013 0.013 90 0 0 0.0113 0.0142 h 0 a 0.0129 0.0129 90 0 0 0.0147 -0.0121 c 0.001 -0.0069 0.001 -0.0158 0.001 -0.0258 a 0.4 0.4 90 1 0 -0.4 0.4 c 0.0128 0 0.03 -0.0015 0.0429 -0.0026 a 0.0129 0.0129 90 0 0 0.0113 -0.016 l 0 -0.001 a 0.0131 0.0131 90 0 0 -0.0157 -0.01 a 0.1743 0.1743 90 0 1 -0.0385 0.0041 z m 0.3467 -0.5156 h -0.16 c -0.019 -0.1 -0.0573 -0.1811 -0.1061 -0.2244 a 0.3758 0.3758 90 0 1 0.2661 0.2244 z m -0.3467 -0.2334 c 0.0716 0 0.1347 0.098 0.1613 0.2334 h -0.3227 c 0.0267 -0.1354 0.0898 -0.2334 0.1614 -0.2334 z m -0.081 0.009 c -0.049 0.0433 -0.0871 0.1242 -0.1061 0.2244 h -0.16 a 0.3758 0.3758 90 0 1 0.2661 -0.2244 z m -0.2935 0.3655 a 0.3731 0.3731 90 0 1 0.0185 -0.1159 h 0.1645 a 0.7853 0.7853 90 0 0 0 0.2318 h -0.1645 a 0.3731 0.3731 90 0 1 -0.0185 -0.1159 z m 0.0278 0.1411 h 0.16 c 0.019 0.1 0.0573 0.1812 0.1061 0.2244 a 0.3758 0.3758 90 0 1 -0.2661 -0.2244 z',
            'pi': 'M 0.279 0.7746 a 0.0177 0.0177 90 0 1 -0.0111 -0.0314 c 0.0672 -0.0537 0.0835 -0.0948 0.1255 -0.475 h -0.0634 a 0.1192 0.1192 90 0 0 -0.103 0.06 l -0.0149 0.0259 a 0.0177 0.0177 90 1 1 -0.0306 -0.0176 l 0.0153 -0.0265 a 0.1546 0.1546 90 0 1 0.1332 -0.0771 h 0.4728 a 0.0177 0.0177 90 0 1 0 0.0353 h -0.3739 c -0.042 0.3808 -0.0584 0.4382 -0.1389 0.5025 a 0.0178 0.0178 90 0 1 -0.011 0.0039 z m 0.3576 -0.0119 a 0.05 0.05 90 0 1 -0.0389 -0.0184 c -0.0367 -0.043 -0.0362 -0.1671 0.0014 -0.4022 a 0.0175 0.0175 90 0 1 0.02 -0.0147 a 0.0178 0.0178 90 0 1 0.0146 0.02 c -0.043 0.2677 -0.0289 0.351 -0.0094 0.3738 a 0.0147 0.0147 90 0 0 0.012 0.0059 c 0.024 0 0.0529 -0.0353 0.0719 -0.0878 a 0.0177 0.0177 90 1 1 0.0332 0.012 c -0.0249 0.0699 -0.0642 0.1114 -0.1048 0.1114 z',
            'plane': 'M 0.7894 0.5306 a 0.0124 0.0124 90 0 1 0.0035 0.0086 a 0.0117 0.0117 90 0 1 -0.0035 0.0085 l -0.01 0.01 a 0.0124 0.0124 90 0 1 -0.0172 0 a 0.0122 0.0122 90 0 1 -0.0036 -0.0086 a 0.012 0.012 90 0 1 0.0036 -0.0086 l 0.01 -0.01 a 0.0122 0.0122 90 0 1 0.0173 0 z m -0.0583 0.0461 a 0.0119 0.0119 90 0 0 -0.0086 0.0035 l -0.05 0.05 a 0.0123 0.0123 90 0 0 0 0.0172 a 0.0124 0.0124 90 0 0 0.0172 0 l 0.05 -0.05 a 0.0115 0.0115 90 0 0 0.0036 -0.0086 a 0.0121 0.0121 90 0 0 -0.0121 -0.0121 z m -0.2711 -0.3702 a 0.012 0.012 90 0 0 -0.0086 0.0036 l -0.01 0.01 a 0.0121 0.0121 90 0 0 -0.0035 0.0086 a 0.0119 0.0119 90 0 0 0.0035 0.0086 a 0.0126 0.0126 90 0 0 0.0173 0 l 0.01 -0.01 a 0.0121 0.0121 90 0 0 0 -0.0172 a 0.0122 0.0122 90 0 0 -0.0087 -0.0036 z m 0.4051 0.3949 a 0.012 0.012 90 0 0 -0.0086 -0.0036 a 0.0122 0.0122 90 0 0 -0.0086 0.0036 l -0.0832 0.0832 a 0.0121 0.0121 90 0 0 0 0.0172 a 0.0125 0.0125 90 0 0 0.0172 0 l 0.0832 -0.0832 a 0.0122 0.0122 90 0 0 0.0036 -0.0086 a 0.0119 0.0119 90 0 0 -0.0036 -0.0086 z m -0.4545 -0.3452 a 0.0122 0.0122 90 0 0 -0.0086 0.0036 l -0.05 0.05 a 0.0117 0.0117 90 0 0 -0.0035 0.0085 a 0.0122 0.0122 90 0 0 0.0035 0.0087 a 0.0126 0.0126 90 0 0 0.0172 0 l 0.05 -0.05 a 0.0122 0.0122 90 0 0 -0.0086 -0.0208 z m -0.0206 -0.1254 a 0.0119 0.0119 90 0 0 -0.0086 0.0035 l -0.0832 0.0832 a 0.0123 0.0123 90 0 0 0 0.0172 a 0.0119 0.0119 90 0 0 0.0086 0.0036 a 0.0122 0.0122 90 0 0 0.0086 -0.0036 l 0.0832 -0.0832 a 0.012 0.012 90 0 0 0.0036 -0.0086 a 0.0122 0.0122 90 0 0 -0.0036 -0.0086 a 0.0119 0.0119 90 0 0 -0.0086 -0.0035 z m 0.485 0.22 a 0.0119 0.0119 90 0 1 -0.005 0.0109 l -0.05 0.04 a 0.0117 0.0117 90 0 1 -0.0073 0.0028 l -0.0983 -0.0237 l 0 0.0008 a 0.4044 0.4044 90 0 1 -0.0544 0.0711 l -0.1257 0.13 l -0.0009 0.0009 l 0.03 0.0361 l 0.2426 0.141 c 0.0052 0.0046 0.0062 0.0075 0.0063 0.0106 a 0.0124 0.0124 90 0 1 -0.0058 0.0105 l -0.035 0.0215 a 0.1093 0.1093 90 0 1 -0.0574 0.0167 a 0.0871 0.0871 90 0 1 -0.032 -0.0059 l -0.266 -0.1041 l -0.0008 0 l -0.08 0.08 l -0.0383 0.0388 c -0.0292 0.0291 -0.0625 0.0452 -0.0936 0.0452 a 0.0656 0.0656 90 0 1 -0.0474 -0.0182 l -0.0123 -0.0124 c -0.0319 -0.0319 -0.0211 -0.0929 0.0246 -0.1387 l 0.12 -0.1154 l 0.0007 -0.0006 l -0.1039 -0.2713 a 0.1019 0.1019 90 0 1 0.011 -0.0894 l 0.0215 -0.035 a 0.0124 0.0124 90 0 1 0.01 -0.0058 a 0.0126 0.0126 90 0 1 0.0085 0.0033 l 0.1424 0.2445 l 0.0315 0.0317 l 0.1368 -0.126 a 0.282 0.282 90 0 1 0.07 -0.0509 l 0.0009 -0.0005 l -0.0218 -0.0986 a 0.0122 0.0122 90 0 1 0.0029 -0.0107 l 0.04 -0.0495 a 0.0121 0.0121 90 0 1 0.0093 -0.0045 a 0.0135 0.0135 90 0 1 0.0087 0.0034 l 0.0607 0.1134 l 0.0006 0.0011 l 0.0339 -0.0119 a 0.0532 0.0532 90 0 1 0.006 -0.0005 a 0.01 0.01 90 0 1 0.0082 0.0028 a 0.0121 0.0121 90 0 1 0.0024 0.0138 l -0.0133 0.0277 l -0.0005 0.0012 l 0.113 0.0643 c 0.0053 0.0043 0.0065 0.007 0.0067 0.0097 z m -0.2522 -0.1617 l 0.02 0.0843 l 0.0491 -0.0147 l 0.0015 -0.0005 l -0.0434 -0.0909 l -0.0038 -0.0073 l -0.023 0.0284 z m -0.316 0.3719 l 0.0008 0.0019 l 0.0836 -0.0729 l 0.0011 -0.001 l -0.0316 -0.0374 l -0.1318 -0.2265 l -0.0012 -0.002 l -0.0109 0.0176 h 0 a 0.0775 0.0775 90 0 0 -0.009 0.0678 z m -0.0631 0.28 l -0.0186 -0.0049 a 0.0851 0.0851 90 0 1 -0.0392 -0.0222 a 0.087 0.087 90 0 1 -0.0223 -0.0393 l -0.0049 -0.0185 l -0.0055 0.0183 c -0.0065 0.0218 -0.0037 0.0407 0.0077 0.0521 l 0.0124 0.0124 a 0.0413 0.0413 90 0 0 0.03 0.0111 a 0.0768 0.0768 90 0 0 0.022 -0.0035 z m 0.05 -0.0431 l -0.0109 -0.0012 a 0.09 0.09 90 0 1 -0.0543 -0.0251 a 0.0891 0.0891 90 0 1 -0.025 -0.0544 l -0.0012 -0.0109 l -0.0133 0.012 l 0 0 v 0 c -0.0082 0.0324 -0.003 0.06 0.0145 0.0773 a 0.0682 0.0682 90 0 0 0.05 0.0187 a 0.1111 0.1111 90 0 0 0.0252 -0.003 l 0.0016 0 z m 0.221 -0.1922 l -0.0011 -0.001 l -0.0766 0.08 l -0.0014 0.0015 l 0.2554 0.1054 a 0.061 0.061 90 0 0 0.0232 0.0043 a 0.0852 0.0852 90 0 0 0.0445 -0.0133 l 0.012 -0.0073 l -0.22 -0.1342 z m 0.2159 -0.3339 l 0.0013 -0.0031 l -0.0811 0.0326 a 0.2586 0.2586 90 0 0 -0.0869 0.0567 l -0.333 0.32 l 0 0 v 0 c -0.0075 0.0314 -0.0022 0.0582 0.0148 0.0752 a 0.0686 0.0686 90 0 0 0.05 0.0186 a 0.1091 0.1091 90 0 0 0.0227 -0.0018 h 0.0005 l 0.3232 -0.3343 a 0.2548 0.2548 90 0 0 0.0567 -0.0857 z m 0.1052 0.0865 l -0.0865 -0.0522 l -0.0052 -0.0028 l -0.02 0.0485 l 0 0.0014 l 0.0835 0.0253 l 0.0007 0 l 0.0258 -0.0185 z',
            'ship': 'M 0.3289 0.2983 h 0 a 0.0129 0.0129 90 0 1 -0.0129 0.0129 h -0.0006 a 0.0128 0.0128 90 0 1 -0.0128 -0.0129 h 0 a 0.0128 0.0128 90 0 1 0.0128 -0.0129 h 0.0006 a 0.0129 0.0129 90 0 1 0.0129 0.0129 z m 0.04 -0.0129 h -0.0006 a 0.0129 0.0129 90 0 0 -0.0129 0.0129 h 0 a 0.0129 0.0129 90 0 0 0.0129 0.0129 h 0.0006 a 0.0129 0.0129 90 0 0 0.0129 -0.0129 h 0 a 0.0129 0.0129 90 0 0 -0.0131 -0.0129 z m 0.0526 0 h -0.0006 a 0.0128 0.0128 90 0 0 -0.0128 0.0129 h 0 a 0.0128 0.0128 90 0 0 0.0128 0.0129 h 0.0006 a 0.0129 0.0129 90 0 0 0.0129 -0.0129 h 0 a 0.0129 0.0129 90 0 0 -0.0131 -0.0129 z m 0.0521 0.0258 h 0.0006 a 0.0128 0.0128 90 0 0 0.0128 -0.0129 h 0 a 0.0128 0.0128 90 0 0 -0.0128 -0.0129 h -0.0006 a 0.0129 0.0129 90 0 0 -0.0129 0.0129 h 0 a 0.0129 0.0129 90 0 0 0.0127 0.0129 z m 0.0526 0 h 0.0006 a 0.0129 0.0129 90 0 0 0.0132 -0.0129 h 0 a 0.0129 0.0129 90 0 0 -0.0129 -0.0129 h -0.0011 a 0.0128 0.0128 90 0 0 -0.0128 0.0129 h 0 a 0.0128 0.0128 90 0 0 0.0128 0.0129 z m 0.0527 0 h 0.0006 a 0.0128 0.0128 90 0 0 0.0128 -0.0129 h 0 a 0.0128 0.0128 90 0 0 -0.0128 -0.0129 h -0.0006 a 0.0129 0.0129 90 0 0 -0.0129 0.0129 h 0 a 0.0129 0.0129 90 0 0 0.0127 0.0129 z m 0.0526 0 h 0.0006 a 0.0129 0.0129 90 0 0 0.0129 -0.0129 h 0 a 0.0129 0.0129 90 0 0 -0.0129 -0.0129 h -0.0006 a 0.0129 0.0129 90 0 0 -0.0129 0.0129 h 0 a 0.0129 0.0129 90 0 0 0.0127 0.0129 z m 0.0527 0 h 0.0006 a 0.0128 0.0128 90 0 0 0.0128 -0.0129 h 0 a 0.0128 0.0128 90 0 0 -0.0128 -0.0129 h -0.0008 a 0.0129 0.0129 90 0 0 -0.0129 0.0129 h 0 a 0.0129 0.0129 90 0 0 0.0129 0.0129 z m 0.237 0.4345 h 0 a 0.0129 0.0129 90 0 1 -0.0129 0.0129 h -0.8166 a 0.0129 0.0129 90 0 1 -0.0129 -0.0129 h 0 a 0.0128 0.0128 90 0 1 0.0129 -0.0128 h 0.196 a 0.1841 0.1841 90 0 1 -0.09 -0.1582 v -0.087 a 0.0211 0.0211 90 0 1 0.0117 -0.019 l 0.0409 -0.02 v -0.2079 a 0.0212 0.0212 90 0 1 0.0211 -0.0208 h 0.11 v -0.0716 a 0.0212 0.0212 90 0 1 0.0212 -0.0212 h 0.1944 a 0.0212 0.0212 90 0 1 0.0212 0.0212 v 0.0716 h 0.11 a 0.0212 0.0212 90 0 1 0.0218 0.0208 v 0.2074 l 0.0409 0.02 a 0.0211 0.0211 90 0 1 0.0117 0.019 v 0.087 a 0.1841 0.1841 90 0 1 -0.09 0.1582 h 0.196 a 0.0128 0.0128 90 0 1 0.0126 0.0133 z m -0.5136 -0.5257 h 0.1848 v -0.067 h -0.1848 z m -0.1316 0.1312 h 0.1683 l 0.05 -0.025 a 0.0131 0.0131 90 0 1 0.0116 0 l 0.05 0.025 h 0.1681 v -0.1058 h -0.448 z m 0.3313 0.0258 l 0.1167 0.0584 v -0.0584 z m -0.3313 0.0584 l 0.1167 -0.0584 h -0.1167 z m -0.0527 0.0921 l 0.2709 -0.1355 a 0.0131 0.0131 90 0 1 0.0116 0 l 0.2709 0.1355 v -0.037 l -0.2767 -0.1383 l -0.2767 0.1383 z m 0.3952 0.2054 a 0.1584 0.1584 90 0 0 0.1582 -0.1582 v -0.0184 l -0.2767 -0.1383 l -0.2767 0.1383 v 0.0184 a 0.1584 0.1584 90 0 0 0.1582 0.1582 z m -0.3814 0.0526 h -0.04 a 0.0129 0.0129 90 0 0 -0.0129 0.0129 h 0 a 0.0129 0.0129 90 0 0 0.0129 0.0129 h 0.04 a 0.0128 0.0128 90 0 0 0.0129 -0.0129 h 0 a 0.0128 0.0128 90 0 0 -0.0129 -0.0129 z m 0.1447 0.04 h -0.1058 a 0.0129 0.0129 90 0 0 -0.0129 0.0129 h 0 a 0.0129 0.0129 90 0 0 0.0129 0.0129 h 0.1058 a 0.0129 0.0129 90 0 0 0.0129 -0.0129 h 0 a 0.0129 0.0129 90 0 0 -0.0129 -0.0134 z m -0.2369 0 h -0.0137 a 0.0129 0.0129 90 0 0 -0.0129 0.0129 h 0 a 0.0129 0.0129 90 0 0 0.0129 0.0129 h 0.0137 a 0.0129 0.0129 90 0 0 0.0129 -0.0129 h 0 a 0.0129 0.0129 90 0 0 -0.0129 -0.0134 z m 0.3685 -0.0263 h -0.0134 a 0.0128 0.0128 90 0 0 -0.0129 0.0128 h 0 a 0.0129 0.0129 90 0 0 0.0129 0.0125 h 0.0137 a 0.0129 0.0129 90 0 0 0.0129 -0.0129 h 0 a 0.0128 0.0128 90 0 0 -0.0132 -0.0129 z m 0.1317 0.0258 h -0.0928 a 0.0128 0.0128 90 0 0 -0.0123 0.0129 h 0 a 0.0128 0.0128 90 0 0 0.0128 0.0129 h 0.0928 a 0.0128 0.0128 90 0 0 0.0128 -0.0129 h 0 a 0.0128 0.0128 90 0 0 -0.0133 -0.0129 z m 0.0526 0.0263 h -0.0137 a 0.0129 0.0129 90 0 0 -0.0129 0.0129 h 0 a 0.0129 0.0129 90 0 0 0.0129 0.0129 h 0.0137 a 0.0129 0.0129 90 0 0 0.0129 -0.0129 h 0 a 0.0129 0.0129 90 0 0 -0.0129 -0.0129 z m 0.2106 -0.0526 h -0.1322 a 0.0128 0.0128 90 0 0 -0.0129 0.0128 h 0 a 0.0129 0.0129 90 0 0 0.0129 0.0129 h 0.1322 a 0.0129 0.0129 90 0 0 0.0129 -0.0129 h 0 a 0.0128 0.0128 90 0 0 -0.0129 -0.0128 z',
        }
        # print('addPersonalEvents(', loc, ')')
        startAnchor = self.layout == "left"
        self.pages[loc].addStyle(
            'personalEvents',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("personalEvents","Regular")}";'
            f'font-size:{self.fontSize.get("personalEvents", 7)/self.scale}px;'
            f'text-anchor:{"start" if startAnchor else "end"};'
            'direction:rtl;'
        )
        self.pages[loc].addStyle(
            'icon',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
        )
        for i in range(len(self.weekKeys)):
            dayKey = self.weekKeys[i]

            if dayKey not in self.personalEvents:
                # print(dayKey, self.personalEvents)
                continue

            # y location
            eventH = self.fontHeightScl * \
                self.fontSize.get("personalEvents", 7)/self.scale

            eventY = self.daysY[i]+self.lineHeight/2 + eventH/2
            eventIconY = self.daysY[i]+(self.lineHeight-self.iconSize)/2

            space = self.lineHeight+self.iconSize if self.layout == 'left' else self.lineHeight

            e = self.personalEvents[dayKey]
            if 'icon' in e:
                Txtspace = self.lineHeight+self.iconSize*1.2
            else:
                Txtspace = space

            xLeftSpace, xRightSpace = self.xloc(loc, space+0.5)
            xLeftSpaceTxt, xRightSpaceTxt = self.xloc(loc, Txtspace+0.5)

            if self.layout == 'left':
                if 'icon' in e:
                    self.pages[loc].addPathByD(
                        iconPath[e["icon"]],
                        transform=f'scale({self.scale}) translate({xRightSpace} {eventIconY}) scale({self.iconSize})',
                        class_='icon'
                    )
                if 'text' in e:
                    self.pages[loc].addText(
                        xRightSpaceTxt,
                        eventY,
                        perNo(e['text']),
                        transform=f'scale({self.scale})',
                        class_='personalEvents'
                    )
            else:
                if 'icon' in e:
                    self.pages[loc].addPathByD(
                        iconPath[e["icon"]],
                        x=xLeftSpace,
                        y=eventIconY,
                        w=self.iconSize,
                        h=self.iconSize,
                        transform=f'scale({self.scale})',
                        class_='icon'
                    )
                if 'text' in e:
                    self.pages[loc].addText(
                        xLeftSpaceTxt,
                        eventY,
                        perNo(e['text']),
                        transform=f'scale({self.scale})',
                        class_='personalEvents'
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
        xLeft, xRight = self.xloc(loc, margin=True)
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
                cal = self.daysJson[dayKey][calID]

                # x and y location
                calH = self.fontHeightScl * \
                    self.fontSize.get(order, 8)/self.scale
                y = self.daysY[i] + self.lineHeight * downH + calH/2
                space = self.lineHeight*self.daysHeight
                xLeftSpace, xRightSpace = self.xloc(loc, space+0.5)
                x = xLeftSpace if self.layout == "left" else xRightSpace

                isfull = self.showFullCalendar or cal[2] == 1 or i == 0
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
            'direction: rtl;'
        )

        for i in range(len(self.weekKeys)):
            dayKey = self.weekKeys[i]

            todaySh = self.daysJson[dayKey]["sh"]
            todayIc = self.daysJson[dayKey]["ic"]
            todayWc = self.daysJson[dayKey]["wc"]

            events = []
            events += self.eventJson.get(
                f"sh-{todaySh[1]}-{todaySh[2]}", [])
            events += self.eventJson.get(
                f"ic-{todayIc[1]}-{todayIc[2]}", [])
            events += self.eventJson.get(
                f"wc-{todayWc[1]}-{todayWc[2]}", [])

            textArea = self.width - \
                self.padding['inside']-self.padding['outside'] - \
                self.lineHeight*(1+self.daysHeight)
            l = int(7.2 * (textArea) / self.fontSize['events'])
            eventList = list(map(lambda e: e['occasion'], events))
            eventText = self.divider.join(eventList)
            et = []

            if len(eventText) > l:
                etTemp2 = eventText
                a = int(len(eventText) / l)+1
                for _ in range(a):
                    etTemp = etTemp2[(-1*l):]

                    if etTemp == etTemp2:
                        txt = etTemp
                    else:
                        txt = " ".join(etTemp.split(" ")[1:])
                    et.append(txt)
                    etTemp2 = etTemp2[:(-1*len(txt))]
            else:
                et.append(eventText)

            # x and y location
            space = self.lineHeight if self.layout == 'left' else self.daysHeight*self.lineHeight
            _, xRightSpace = self.xloc(loc, space+0.5)
            calH = self.fontHeightScl * \
                self.fontSize.get('events', 5)/self.scale

            for en in range(len(et)):
                y = self.daysY[i+1] - self.lineHeight * (en+0.5) + calH/2
                self.pages[loc].addText(
                    xRightSpace,
                    y,
                    perNo(et[en]),
                    transform=f'scale({self.scale})',
                    class_='events',
                )

    def addMonthandWeek(self, loc):
        self.pages[loc].addStyle(
            'monthAndWeek',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("monthAndWeek","")}";'
            f'font-size:{self.fontSize.get("monthAndWeek", 8)/self.scale}px;'
            f'text-anchor:{"end" if self.layout=="left" else "start"};'
            'direction: rtl;'
        )

        calID = self.calendarOrder[0]

        mn = str(self.daysJson[self.weekKeys[0]][calID][1])
        startMonth = self.calNamesJson[calID]['month'][mn]

        mn = str(self.daysJson[self.weekKeys[-1]][calID][1])
        endMonth = self.calNamesJson[calID]['month'][mn]

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
                y = self.margin['top'] + \
                    self.padding['top']+i*self.lineHeight-w/2
                self.pages[loc].addRect(
                    x-w,
                    y,
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
    def __init__(self, year=1401, shiftDownHolidays=1, title='تعطیلات رسمی ۱۴۰۱', name='Untitle-LinePage', **kwargs) -> None:
        super().__init__(title, name, **kwargs)
        self.daysJson = kwargs.get('daysJson', '')
        self.eventJson = kwargs.get('eventJson', '')
        self.calNamesJson = kwargs.get('calNamesJson', '')
        self.shiftDownHolidays = shiftDownHolidays
        self.holidays = []
        for day in self.daysJson.keys():
            if self.daysJson[day]['sh'][0] == year:
                todaySh = self.daysJson[day]["sh"]
                todayIc = self.daysJson[day]["ic"]
                todayWc = self.daysJson[day]["wc"]

                events = []
                events += self.eventJson.get(
                    f"sh-{todaySh[1]}-{todaySh[2]}", [])
                events += self.eventJson.get(
                    f"ic-{todayIc[1]}-{todayIc[2]}", [])
                events += self.eventJson.get(
                    f"wc-{todayWc[1]}-{todayWc[2]}", [])

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
            # monthName = self.daysJson[day]['sh']['monthName']
            month = str(self.daysJson[day]['sh'][1])
            monthName = self.calNamesJson['sh']['month'][month]
            dateDay = self.daysJson[day]['sh'][2]
            wd = str(self.daysJson[day]['weekday'])
            weekday = self.calNamesJson['sh']['weekday'][wd]

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
                perNo(dateDay),
                transform=f'scale({self.scale})',
                class_='holidayNo'
            )
            self.pages[loc].addText(
                x3,
                y,
                perNo(weekday),
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


class OneYearPage(LinePageWithTitle):
    def __init__(self, year=1402, title='سال ۱۴۰۲', name='Untitle-LinePage', **kwargs) -> None:
        super().__init__(title, name, **kwargs)
        self.daysJson = kwargs.get('daysJson', '')
        self.eventJson = kwargs.get('eventJson', '')
        self.calNamesJson = kwargs.get('calNamesJson', '')
        self.year = year
        self.startWeekday = kwargs.get('startWeekday', 'Sat')
        self.weekend = kwargs.get('weekend', 0)
        self.secondColor = kwargs.get('secondColor', '#ddd')

        self.holidays = []
        for day in self.daysJson.keys():
            if self.daysJson[day]['sh'][0] == year:
                todaySh = self.daysJson[day]["sh"]
                todayIc = self.daysJson[day]["ic"]
                todayWc = self.daysJson[day]["wc"]

                events = []
                events += self.eventJson.get(
                    f"sh-{todaySh[1]}-{todaySh[2]}", [])
                events += self.eventJson.get(
                    f"ic-{todayIc[1]}-{todayIc[2]}", [])
                events += self.eventJson.get(
                    f"wc-{todayWc[1]}-{todayWc[2]}", [])

                for e in events:
                    if e['dayoff'] == True:
                        self.holidays.append(day)
                        break

    def makePages(self):
        super().makePages()
        for loc in ['right', 'left']:
            self.addMonths(loc)

    def addMonths(self, loc):
        self.pages[loc].addStyle(
            'onePageYear',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("onePageYear","")}";'
            f'font-size:{self.fontSize.get("onePageYear", 7)/self.scale}px;'
            'text-anchor:middle;'
            'direction:rtl;'
        )
        self.pages[loc].addStyle(
            'onePageYearHolidays',
            f'fill:{self.secondColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("onePageYearHolidays","")}";'
            f'font-size:{self.fontSize.get("onePageYearHolidays", 7)/self.scale}px;'
            'text-anchor:middle;'
            'direction:rtl;'
        )
        self.pages[loc].addStyle(
            'onePageYearMonth',
            f'fill:{self.primaryColor};'
            f'stroke:None;'
            f'font-family:"{self.fontFamily} {self.fontWeight.get("onePageYearMonth","")}";'
            f'font-size:{self.fontSize.get("onePageYearMonth", 7)/self.scale}px;'
            'text-anchor:start;'
            'direction:rtl;'
        )
        xLeft, xRight = self.xloc(loc, 2*self.lineHeight)
        yTop = self.margin['top']+self.padding['top']
        yBottom = self.margin['top'] + self.height - self.padding['bottom']

        w = (((yBottom-yTop)/4)//self.lineHeight)*self.lineHeight

        weekDays = ['Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        weekShift = weekDays.index(self.startWeekday)
        weekDays = weekDays[weekShift:] + weekDays[:weekShift]

        calKeysDict = {}
        monthList = {}
        for date_ in self.daysJson:
            day = self.daysJson[date_]['sh']

            if day[0] == self.year:
                if day[2] == 1:
                    monthList[day[1]
                              ] = self.calNamesJson['sh']['month'][str(day[1])]
                    calKeysDict[day[1]] = [date_]
                else:
                    calKeysDict[day[1]].append(date_)

        for m in range(1, 13):
            j = (m-1)//3
            i = (m-1) % 3

            self.addMonth(
                loc,
                xLeft+(2-i)*(xRight-xLeft)/3,
                yTop+j*w+self.lineHeight,
                (xRight-xLeft)/3,
                w,
                monthList[m],
                calKeysDict[m],
                weekDays
            )

    def addMonth(self, loc, xLeft, yTop, w, h, monthName, days, weekDays):
        colWidth = self.lineHeight if self.lineHeight <= w/7 else w/7

        if self.lineHeight <= h/8:
            lineHeight = self.lineHeight
            self.pages[loc].addRect(
                xLeft+w-colWidth,
                yTop+1,
                colWidth,
                h-2-lineHeight,
                transform=f'scale({self.scale})',
                fill="white",
            )
        else:
            lineHeight = (h-self.lineHeight)/7
            self.pages[loc].addRect(
                xLeft, yTop+1, w, h-self.lineHeight-2,
                transform=f'scale({self.scale})',
                fill="white",
            )

        calH = self.fontHeightScl * \
            self.fontSize.get("onePageYear", 7)/self.scale

        a = 0
        for date_ in days:
            day = self.daysJson[date_]
            # b = weekDays.index(day['wc']['weekday'][0])
            wd = str(day['weekday'])
            b = weekDays.index(self.calNamesJson['wc']['weekday-short'][wd])

            x = xLeft + w - colWidth * (a + 1.5)
            y = yTop + lineHeight * (b + 0.5) + calH/2

            isHoliday = (date_ in self.holidays) or (b > 6-self.weekend)

            self.pages[loc].addText(
                x,
                y,
                perNo(day['sh'][2]),
                transform=f'scale({self.scale})',
                class_='onePageYearHolidays' if isHoliday else 'onePageYear'
            )
            a += 1 if b == 6 else 0

        monthH = self.fontHeightScl * \
            self.fontSize.get("onePageYear", 7)/self.scale

        self.pages[loc].addText(
            0,
            0,
            monthName,
            transform=f' scale({self.scale}) translate({xLeft+w-colWidth/2+monthH/2} {yTop+1}) rotate(-90)',
            class_='onePageYearMonth'
        )
