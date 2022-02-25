from aaaSvg import Svg


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
            {'top': 32, 'outside': 0, 'bottom': 0, 'inside': 0}
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
    def __init__(self, name='Untitle-WeekPage', **kwargs) -> None:
        super().__init__(name, **kwargs)

        self.layout = kwargs.get('layout', 'left')
        self.daysHeight = kwargs.get('daysHeight', 4)

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
        pass

    def addFirstCal(self, loc):
        pass

    def addSecondCal(self, loc):
        pass

    def addthirdCal(self, loc):
        pass

    def addEventOfDays(self, loc):
        pass
