from pages import *


class Notebook():
    def __init__(self, **kwargs) -> None:
        # general
        self.name = kwargs.get('name', 'Untitle')
        self.rtl = kwargs.get('rtl', True)
        self.width = kwargs.get('width', 148)
        self.height = kwargs.get('height', 210)
        self.scale = kwargs.get('scale', 2.83465)

        # margin and padding
        nameList = ['top', 'outside', 'bottom', 'inside']
        margin = kwargs.get('margin', [5, 5, 5, 0])
        padding = kwargs.get('padding', [32, 0, 0, 0])

        self.margin = dict(zip(nameList, margin))
        self.padding = dict(zip(nameList, padding))

        # line and dot peroperty
        self.lineHeight = kwargs.get('lineHeight', 6)
        self.lineWidth = kwargs.get('lineWidth', 0.125)

        # colors
        self.bgColor = kwargs.get('bgColor', 'none')
        self.lineColor = kwargs.get('lineColor', '#000')

        # pages
        self.pages = kwargs.get('pages', [])

        # last page location

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
        htmlTxt = '<html>\n<head>\n<style>\nhtml,body{margin:0;padding: 0;}\n</style>\n</head>\n<body>'
        for page in self.pages:
            htmlTxt += f'{page.svgText}\n'
        htmlTxt += '</body>\n</html>'

        with open('\\'.join([Dir, f'{self.name}.html']), "w") as f:
            f.write(htmlTxt)

    def toPDF():
        pass
