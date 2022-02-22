from aaaSvg import Svg


class Page():
    def __init__(self, name='Untitle-Page', **kwargs) -> None:
        # general
        self.name = name
        self.width = kwargs.get('width', 148)
        self.height = kwargs.get('height', 210)
        self.scale = kwargs.get('scale', 2.83465)

        # margin and padding
        nameList = ['top', 'outside', 'bottom', 'inside']
        margin = kwargs.get('margin', [5, 5, 5, 0])

        self.margin = dict(zip(nameList, margin))

        # colors
        self.bgColor = kwargs.get('bgColor', 'none')

    # pages
    def right(self):
        self.both()
        self.pages['right'].addStyle(
            'bg',
            f'fill:{self.bgColor};'
            'stroke:none;'
        )
        self.pages['right'].addRect(
            self.margin['inside'],
            self.margin['top'],
            self.width,
            self.height,
            class_='bg',
            transorm=f'scale({self.scale})'
        )

        self.pages['right'].text

    def left(self):
        self.both()
        self.pages['left'].addStyle(
            'bg',
            f'fill:{self.bgColor};'
            'stroke:none;'
        )
        self.pages['left'].addRect(
            self.margin['outside'],
            self.margin['top'],
            self.width,
            self.height,
            class_='bg',
            transorm=f'scale({self.scale})'
        )

    def both(self):
        svgWidth = self.width + self.margin['outside'] + self.margin['inside']
        svgHeight = self.height + self.margin['top'] + self.margin['bottom']
        self.pages = {
            'right': Svg(self.name+'-r', svgWidth, svgHeight),
            'left': Svg(self.name+'-l', svgWidth, svgHeight)
        }


class LinePage(Page):
    def __init__(self, name='Untitle-LinePage', **kwargs) -> None:
        super().__init__(name, **kwargs)


class DotPage(Page):
    def __init__(self, name='Untitle-DotPage', **kwargs) -> None:
        super().__init__(name, **kwargs)


class WeekPage(LinePage):
    def __init__(self, name='Untitle-WeekPage', **kwargs) -> None:
        super().__init__(name, **kwargs)
