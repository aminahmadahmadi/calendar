from pages import *
import os


class Notebook():
    def __init__(self, **kwargs) -> None:
        # general
        self.name = kwargs.get('name', 'Untitle')
        self.rtl = kwargs.get('rtl', True)
        self.width = kwargs.get('width', 148)
        self.height = kwargs.get('height', 210)
        self.scale = kwargs.get('scale', 2.83465)

        # margin and padding
        self.margin = kwargs.get(
            'margin',
            {'top': 5, 'outside': 5, 'bottom': 5, 'inside': 0}
        )
        if isinstance(self.margin, list):
            lst = ['top', 'outside', 'bottom', 'inside']
            self.margin = dict(zip(lst, self.margin))

        self.padding = kwargs.get(
            'padding',
            {'top': 32, 'outside': 0, 'bottom': 0, 'inside': 0}
        )
        if isinstance(self.padding, list):
            lst = ['top', 'outside', 'bottom', 'inside']
            self.padding = dict(zip(lst, self.padding))

        # line and dot peroperty
        self.lineHeight = kwargs.get('lineHeight', 6)
        self.lineWidth = kwargs.get('lineWidth', 0.125)

        # colors
        self.bgColor = kwargs.get('bgColor', 'none')
        self.lineColor = kwargs.get('lineColor', '#555')

        # pages
        self.pages = kwargs.get('pages', [])

        # info on page
        self.guide = kwargs.get('guide', False)

    def addEmptyPage(self):
        page = Page(**self.__dict__)
        self.pages.append(page)

    def addLinePage(self):
        page = LinePage(**self.__dict__)
        self.pages.append(page)

    def addDotPage(self):
        page = DotPage(**self.__dict__)
        self.pages.append(page)

    def toHTML(self, Dir=''):
        if not os.path.exists('\\'.join([Dir, self.name])):
            os.mkdir('\\'.join([Dir, self.name]))

        if not os.path.exists('\\'.join([Dir, self.name, 'pages'])):
            os.mkdir('\\'.join([Dir, self.name, 'pages']))

        htmlTxt = '<html>\n<head>\n<style>\nhtml,body{margin:0;padding: 0;}\n</style>\n</head>\n<body>\n'
        for i in range(len(self.pages)):
            if i % 2 == 0 ^ self.rtl:
                pageDir = 'right'
            else:
                pageDir = 'left'
            print(
                f'#{i+1:>3}: {str(self.pages[i].__class__)[8:-2].split(".")[-1]}({pageDir[:1]})')

            svg = self.pages[i].page[pageDir]
            svg.name = f'p{i:03}'
            svg.save(
                "\\".join([Dir, self.name, 'pages']),
                width=f'{self.pages[i].svgWidth}mm',
                height=f'{self.pages[i].svgHeight}mm'
            )
            path = "\\".join(['pages', f"{svg.name}.svg"])
            htmlTxt += f'<img src="{path}">\n'

        htmlTxt += '</body>\n</html>'

        with open('\\'.join([Dir, self.name, 'index.html']), "w") as f:
            f.write(htmlTxt)

    def toPDF():
        pass
