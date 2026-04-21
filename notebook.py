from pages import *
import os


class Notebook():
    def __init__(self, **kwargs) -> None:
        # general
        self.name = kwargs.get('name', 'Untitle-Notebook')
        self.saveFolderName = f'output-{self.name}'

        self.rtl = kwargs.get('rtl', True)
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
            lst = ['top', 'outside', 'bottom', 'inside']
            self.margin = dict(zip(lst, self.margin))

        self.padding = kwargs.get(
            'padding',
            {'top': 32, 'outside': 0, 'bottom': 10, 'inside': 0}
        )
        if isinstance(self.padding, list):
            lst = ['top', 'outside', 'bottom', 'inside']
            self.padding = dict(zip(lst, self.padding))

        # line and dot peroperty
        self.lineHeight = kwargs.get('lineHeight', 6)
        self.lineWidth = kwargs.get('lineWidth', 0.05)

        # colors
        self.bgColor = kwargs.get('bgColor', 'none')
        self.lineColor = kwargs.get('lineColor', '#999')

        # pages
        self.pages = kwargs.get('pages', [])

        # info on page
        self.guide = kwargs.get('guide', False)

    def mainDirectory(self, Dir):
        return os.path.join(Dir, self.saveFolderName)

    def pagesDirectory(self, Dir):
        return os.path.join(
            self.mainDirectory(Dir), 'pages')

    def addEmptyPage(self, **kwargs):
        props = self.__dict__.copy()
        props.update(kwargs)
        page = Page(**props)
        self.pages.append(page)

    def addLinePage(self, **kwargs):
        props = self.__dict__.copy()
        props.update(kwargs)
        page = LinePage(**props)
        self.pages.append(page)

    def addLinePageWithTitle(self, **kwargs):
        props = self.__dict__.copy()
        props.update(kwargs)
        page = LinePageWithTitle(**props)
        self.pages.append(page)

    def addSquarePage(self, **kwargs):
        props = self.__dict__.copy()
        props.update(kwargs)
        page = SquarePage(**props)
        self.pages.append(page)

    def addDotPage(self, **kwargs):
        props = self.__dict__.copy()
        props.update(kwargs)
        page = DotPage(**props)
        self.pages.append(page)

    def addChecklistPage(self, **kwargs):
        props = self.__dict__.copy()
        props.update(kwargs)
        page = ChecklistPage(**props)
        self.pages.append(page)

    def removeLastPage(self):
        self.pages = self.pages[:-1]

    def toHTML(self, Dir='', previewMargin=False):

        if not os.path.exists(self.mainDirectory(Dir)):
            os.mkdir(self.mainDirectory(Dir))

        if not os.path.exists(self.pagesDirectory(Dir)):
            os.mkdir(self.pagesDirectory(Dir))

        _direction = "rtl" if self.rtl else "ltr"
        htmlTxt = f'<html>\n<head>\n<style>\nhtml,body{{margin:0;padding:0;direction:{_direction};}}\nbody{{display:flex;flex-wrap:wrap;}}\n</style>\n</head>\n<body>\n'
        for i in range(len(self.pages)):
            if i % 2 == 0 ^ self.rtl:
                pageDir = 'right'
                pageOneMargin = 'left'
            else:
                pageDir = 'left'
                pageOneMargin = 'right'
            print(
                f'#{i+1:>3}: {str(self.pages[i].__class__)[8:-2].split(".")[-1]}({pageDir[:1]})')

            svg: Svg = self.pages[i].page[pageDir]
            svg.name = f'p{i:03}'
            svg.save(
                self.pagesDirectory(Dir),
                width=f'{self.pages[i].svgWidth}mm',
                height=f'{self.pages[i].svgHeight}mm'
            )
            path = "/".join(['pages', f"{svg.name}.svg"])

            styleTxt = ''
            if i == 0 and previewMargin:
                styleTxt += f'style="margin-{pageOneMargin}:{self.pages[i].svgWidth}mm;"'

            htmlTxt += f'<img src="{path}" {styleTxt} >\n'

        htmlTxt += '</body>\n</html>'

        with open(os.path.join(self.mainDirectory(Dir), 'index.html'), "w") as f:
            f.write(htmlTxt)

    def toPrintHTML(self, Dir='', loopPaper=5):
        if not os.path.exists(self.mainDirectory(Dir)):
            os.mkdir(self.mainDirectory(Dir))

        if not os.path.exists(self.pagesDirectory(Dir)):
            os.mkdir(self.pagesDirectory(Dir))

        _direction = "rtl" if self.rtl else "ltr"
        htmlTxt = f'<html>\n<head>\n<style>\nhtml,body{{margin:0;padding:0;direction:{_direction};}}\nbody{{display:flex;flex-wrap:wrap;}}\n</style>\n</head>\n<body>\n'

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
                self.pagesDirectory(Dir),
                width=f'{self.pages[i].svgWidth}mm',
                height=f'{self.pages[i].svgHeight}mm'
            )

        for d in range(0, len(self.pages)-1, loopPaper*4):
            for i in range(0, loopPaper*2, 2):
                for p in [d+loopPaper*4-i-1, d+i, d+i+1, d+loopPaper*4-i-2]:
                    name = f'p{p:03}'
                    path = "/".join(['pages', f"{name}.svg"])
                    htmlTxt += f'<img src="{path}" >\n'

        htmlTxt += '</body>\n</html>'

        with open(os.path.join(self.mainDirectory(Dir), 'index.html'), "w") as f:
            f.write(htmlTxt)

    def toPDF(self, Dir='', removeSvgs=True, removePdfs=True):
        try:
            if not os.path.exists(self.mainDirectory(Dir)):
                os.mkdir(self.mainDirectory(Dir))

            if not os.path.exists(self.pagesDirectory(Dir)):
                os.mkdir(self.pagesDirectory(Dir))

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
                    self.pagesDirectory(Dir),
                    width=f'{self.pages[i].svgWidth}mm',
                    height=f'{self.pages[i].svgHeight}mm'
                )

                fpath = os.path.join(self.pagesDirectory(Dir), svg.name)
                os.system(
                    f'inkscape "{fpath}.svg" --export-filename="{fpath}.pdf"')
                if removeSvgs:
                    os.system(f'rm "{fpath}.svg"')

            os.chdir(f"{self.pagesDirectory(Dir)}")

            os.system(f'pdfunite *.pdf ../cal.pdf')

            if removePdfs:
                os.chdir(f"{self.mainDirectory(Dir)}")
                os.system(f'rm -r pages')

            os.chdir(os.path.dirname(os.path.realpath(__file__)))
        except:
            print('"inkscape" and "pdfunite" requirement for use toPDF function.')

    def toPrintPDF(self, Dir='', loopPaper=5, removeSvgs=True, removePdfs=True):
        self.toPDF(Dir, removeSvgs=removeSvgs, removePdfs=False)

        if loopPaper > 0:
            names = []
            for d in range(0, len(self.pages)-1, loopPaper*4):
                for i in range(0, loopPaper*2, 2):
                    for p in [d+loopPaper*4-i-1, d+i, d+i+1, d+loopPaper*4-i-2]:
                        names.append(f'p{p:03}.pdf')

            os.chdir(f"{self.pagesDirectory(Dir)}")
            name = " ".join(names)
            os.system(f'pdfunite {name} ../cal-print.pdf')
            os.chdir(os.path.dirname(os.path.realpath(__file__)))

        if removePdfs:
            os.chdir(f"{self.mainDirectory(Dir)}")
            os.system(f'rm -r pages')
            os.chdir(os.path.dirname(os.path.realpath(__file__)))

            print('pdfs removed')
