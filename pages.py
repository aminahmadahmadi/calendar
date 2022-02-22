from re import T
from tkinter import Y
from aaaSvg import Svg


class Page():
    def __init__(self, name='Untitle-Page', **kwargs) -> None:
        # general
        self.name = name
        self.width = kwargs.get('width', 148)
        self.height = kwargs.get('height', 210)
        self.scale = kwargs.get('scale', 2.83465)

        self.svgWidth = self.width + \
            self.margin['outside'] + self.margin['inside']
        self.svgHeight = self.height + \
            self.margin['top'] + self.margin['bottom']

        # margin and padding
        nameList = ['top', 'outside', 'bottom', 'inside']
        margin = kwargs.get('margin', [5, 5, 5, 0])
        self.margin = dict(zip(nameList, margin))

        # colors
        self.bgColor = kwargs.get('bgColor', 'none')

    # pages
    def makePages(self):
        for loc in ['right', 'left']:
            self.definePage(loc)

    def definePage(self, loc):
        self.pages = {}
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
            self.width,
            self.height,
            class_='bg',
            transform=f'scale({self.scale})'
        )


class LinePage(Page):
    def __init__(self, name='Untitle-LinePage', **kwargs) -> None:
        super().__init__(name, **kwargs)

        # margin and padding
        nameList = ['top', 'outside', 'bottom', 'inside']
        padding = kwargs.get('padding', [32, 0, 0, 0])
        self.padding = dict(zip(nameList, padding))

        # line and dot peroperty
        self.lineHeight = kwargs.get('lineHeight', 6)
        self.lineWidth = kwargs.get('lineWidth', 0.05)

        # colors
        self.lineColor = kwargs.get('lineColor', '#000')

        # pages
        self.pages = {}

    def makePages(self):
        for loc in ['right', 'left']:
            self.definePage(loc)
            self.drawlines(loc)

    def drawlines(self, loc):
        self.svg.addStyle(
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

    def xloc(self, loc):
        dir = {
            'right': ['inside', 'outside'],
            'left': ['outside', 'inside']
        }
        xLeft = 0 if self.padding[dir[loc][0]] == 0 else self.padding[dir[loc][0]] + \
            self.margin[dir[loc][0]]
        xRight = self.svgWidth
        xRight -= 0 if self.padding[dir[loc][1]] == 0 else self.padding[dir[loc][1]] + \
            self.margin[dir[loc][1]]

        return (xLeft, xRight)


class DotPage(Page):
    def __init__(self, name='Untitle-DotPage', **kwargs) -> None:
        super().__init__(name, **kwargs)


class WeekPage(LinePage):
    def __init__(self, name='Untitle-WeekPage', **kwargs) -> None:
        super().__init__(name, **kwargs)
