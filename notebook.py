from pages import *
import os
import base64


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

    def addPatternPage(self, patternUnit, **kwargs):
        props = self.__dict__.copy()
        props.update(kwargs)
        page = PatternPage(patternUnit=patternUnit, **props)
        self.pages.append(page)
        return page

    def addChecklistPage(self, **kwargs):
        props = self.__dict__.copy()
        props.update(kwargs)
        page = ChecklistPage(**props)
        self.pages.append(page)

    def removeLastPage(self):
        self.pages = self.pages[:-1]

    def saveSvgs(self, Dir=''):
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

    def toHTML(self, Dir='', previewMargin=False, skipSvgs=False):
        if not skipSvgs:
            self.saveSvgs(Dir=Dir)

        _direction = "rtl" if self.rtl else "ltr"
        pageOneMargin = 'right' if self.rtl else 'left'

        htmlTxt = f'<html>\n<head>\n<style>\nhtml,body{{margin:0;padding:0;direction:{_direction};}}\nbody{{display:flex;flex-wrap:wrap;}}\n</style>\n</head>\n<body>\n'

        for p in range(len(self.pages)):
            name = f'p{p:03}'
            path = "/".join(['pages', f"{name}.svg"])

            styleTxt = ''
            if p == 0 and previewMargin:
                styleTxt += f'style="margin-{pageOneMargin}:{self.pages[p].svgWidth}mm;"'

            htmlTxt += f'<img src="{path}" {styleTxt} >\n'

        htmlTxt += '</body>\n</html>'

        with open(os.path.join(self.mainDirectory(Dir), 'index.html'), "w") as f:
            f.write(htmlTxt)

    def toPrintHTML(self, Dir='', loopPaper=5):
        self.saveSvgs(Dir=Dir)

        _direction = "rtl" if self.rtl else "ltr"
        htmlTxt = f'<html>\n<head>\n<style>\nhtml,body{{margin:0;padding:0;direction:{_direction};}}\nbody{{display:flex;flex-wrap:wrap;}}\n</style>\n</head>\n<body>\n'

        for d in range(0, len(self.pages)-1, loopPaper*4):
            for i in range(0, loopPaper*2, 2):
                for p in [d+loopPaper*4-i-1, d+i, d+i+1, d+loopPaper*4-i-2]:
                    name = f'p{p:03}'
                    path = "/".join(['pages', f"{name}.svg"])
                    htmlTxt += f'<img src="{path}" >\n'

        htmlTxt += '</body>\n</html>'

        with open(os.path.join(self.mainDirectory(Dir), 'print.html'), "w") as f:
            f.write(htmlTxt)

        self.toHTML(Dir=Dir, previewMargin=True, skipSvgs=True)

    def previewSvg(self, pageLeft=None, pageRight=None, Dir='', padding=20, radius=10, previewScl=4, save=False):
        scl = self.scale * previewScl
        w = self.pages[-1].svgWidth
        h = self.pages[-1].svgHeight

        jeld = 1

        name = f"preview-{'e' if pageLeft is None else pageLeft}-{'e' if pageRight is None else pageRight}"

        _previewSvg = Svg(
            name,
            (self.width+padding)*2*scl,
            (self.height+padding*2)*scl,
        )

        _previewSvg.addDefs(
            '<linearGradient id="leftG" x1="0" x2="1" y1="0" y2="0">'
            '<stop offset="80%" stop-color="black" stop-opacity="0" />'
            '<stop offset="100%" stop-color="black" stop-opacity=".03" />'
            '</linearGradient>'
        )
        _previewSvg.addDefs(
            '<linearGradient id="rightG" x1="0" x2="1" y1="0" y2="0">'
            '<stop offset="0%" stop-color="black" stop-opacity=".2" />'
            '<stop offset="1%   " stop-color="black" stop-opacity=".1" />'
            '<stop offset="3%" stop-color="black" stop-opacity=".03" />'
            '<stop offset="80%" stop-color="black" stop-opacity="0" />'
            '</linearGradient>'
        )

        _previewSvg.addObjectText(
            '<mask id="paperLeft" mask-type="luminance">'
            f'<rect rx="{radius}" x="{padding}" y="{padding}" width="{self.width}" height="{self.height}" fill="white" transform="scale({scl})" />'
            f'<rect  x={padding+self.width-radius} y={padding} width={radius} height={radius} fill="white" transform="scale({scl})" />'
            f'<rect  x={padding+self.width-radius} y={padding+self.height-radius} width={radius} height={radius} fill="white" transform="scale({scl})" />'
            '</mask>'
        )

        _previewSvg.addObjectText(
            '<mask id="paperRight" mask-type="luminance">'
            f'<rect rx="{radius}" x="{padding+self.width}" y="{padding}" width="{self.width}" height="{self.height}" fill="white" transform="scale({scl})" />'
            f'<rect  x={padding+self.width} y={padding} width={radius} height={radius} fill="white" transform="scale({scl})" />'
            f'<rect  x={padding+self.width} y={padding+self.height-radius} width={radius} height={radius} fill="white" transform="scale({scl})" />'
            '</mask>'
        )

        _previewSvg.addObjectText(
            '<mask id="coverLeft" mask-type="luminance">'
            f'<rect rx="{radius+jeld}" x="{padding-jeld}" y="{padding-jeld}" width="{self.width+jeld}" height="{self.height+2*jeld}" fill="white" transform="scale({scl})" />'
            f'<rect rx="{jeld}" x={padding+self.width-2*radius} y={padding-jeld} width={2*radius} height={2*radius} fill="white" transform="scale({scl})" />'
            f'<rect  rx="{jeld}"  x={padding+self.width-2*radius} y={padding+self.height+jeld-2*radius} width={2*radius} height={2*radius} fill="white" transform="scale({scl})" />'
            '</mask>'
        )

        _previewSvg.addObjectText(
            '<mask id="coverRight" mask-type="luminance">'
            f'<rect rx="{radius+jeld}" x="{padding+self.width}" y="{padding-jeld}" width="{self.width+jeld}" height="{self.height+2*jeld}" fill="white" transform="scale({scl})" />'
            f'<rect rx="{jeld}"  x={padding+self.width} y={padding-jeld} width={2*radius} height={2*radius} fill="white" transform="scale({scl})" />'
            f'<rect rx="{jeld}"  x={padding+self.width} y={padding+self.height+jeld-2*radius} width={2*radius} height={2*radius} fill="white" transform="scale({scl})" />'
            '</mask>'
        )
        _previewSvg.addRect(
            x=0, y=0, w="100%", h="100%", fill="white"
        )

        _previewSvg.addRect(
            x=0, y=0, w="100%", h="100%", fill="#b58a69",
            mask="url(#coverLeft)"
        )
        _previewSvg.addRect(
            x=0, y=0, w="100%", h="100%", fill="#b58a69",
            mask="url(#coverRight)"
        )
        if pageLeft is not None:
            leftSvg: Svg = self.pages[pageLeft].page['left']
            base64_svg = base64.b64encode(leftSvg.text().encode('utf-8')).decode('utf-8')  # noqa

            path = "/".join(['pages', f"p{pageLeft:03}.svg"])
            base64_path = f"data:image/svg+xml;base64,{base64_svg}"
            _x = (padding-self.margin["outside"])*scl
            _y = (padding-self.margin["top"])*scl
            _w = w*scl
            _h = h*scl

            _previewSvg.addDefs(
                '<filter id="pageLEFT">'
                f'<feImage x="{_x}" y="{_y}" width="{_w}" height="{_h}" href="{base64_path}" result="pageL" />'
                '<feBlend in="SourceGraphic" in2="pageL" mode="multiply" />'
                '</filter>'
            )

            _previewSvg.addRect(
                x=0, y=0, w="100%", h="100%", fill="#eeeee6",
                filter="url(#pageLEFT)", mask="url(#paperLeft)",
            )

            _previewSvg.addRect(
                x=0, y=0, w="50%", h="100%", fill="url(#leftG)",
                mask="url(#paperLeft)"
            )

        if pageRight is not None:
            rightSvg = self.pages[pageRight].page['right']
            base64_svg = base64.b64encode(rightSvg.text().encode('utf-8')).decode('utf-8')  # noqa

            path = "/".join(['pages', f"p{pageRight:03}.svg"])
            base64_path = f"data:image/svg+xml;base64,{base64_svg}"

            _x = (self.width+padding-self.margin["inside"])*scl
            _y = (padding-self.margin["top"])*scl
            _w = w*scl
            _h = h*scl

            _previewSvg.addDefs(
                '<filter id="pageRIGHT">'
                f'<feImage x="{_x}" y="{_y}" width="{_w}" height="{_h}" href="{base64_path}" result="pageR" />'
                '<feBlend in="SourceGraphic" in2="pageR" mode="multiply" />'
                '</filter>'
            )

            _previewSvg.addRect(
                x=0, y=0, w="100%", h="100%", fill="#eeeee6",
                filter="url(#pageRIGHT)", mask="url(#paperRight)"
            )

            _previewSvg.addRect(
                x="50%", y=0, w="50%", h="100%", fill="url(#rightG)",
                mask="url(#paperRight)"
            )

        if save:
            _previewSvg.save(self.mainDirectory(Dir))

        return _previewSvg.text()

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
