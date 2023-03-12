from cal import Calendar
import os

rootPath = os.getcwd()

printProperty = {
    'margin': [19, 14, 19, 14],
    'trimMark': 5,
    'trimMarkMargin': 7,
}
previewProperty = {
    'margin': [0, 0, 0, 0],
    'trimMark': 5,
    'trimMarkMargin': 7,
}

example = {
    'width': 130,
    'name': 'UntitleCalendar',
    'sentence': [
        'Lorem ipsum dolor sit amet,',
        'consectetur adipiscing elit,',
        'sed do eiusmod tempor incididunt'
    ],
    'padding': [25, 0, 9, 0],
    'lineHeight': 5,
    'daysHeight': 5,
    'showWeekdays': True,
    'weekend': 1,
    'secondColor': '#f00',
    'personalEvents': {
        '1401-10-30': {'icon': 'fire'},
        '1401-10-18': {'icon': 'plane'},
        '1401-10-16': {'icon': 'ship'},
        '1401-08-25': {'icon': 'internet'},
        '1401-08-24': {'icon': 'hand'},
        '1401-10-07': {'icon': 'hand'},
        '1401-04-24': {'icon': 'hand'},
        '1401-12-23': {'icon': 'pi'},
        '1401-11-25': {'icon': 'heart'},
    }
}

newBook = Calendar('1402.json',
                   **previewProperty,
                   **example
                   )

newBook.addFirstPage()
newBook.addLinePage()
newBook.addChecklistPage(title='اهداف سال ۱۴۰۲',
                         pattern='01', checkboxscale=0.6)

newBook.addOneYearPage()
newBook.addHolidaysPage()

for i in range(53):
    newBook.addLinePage()
    newBook.addWeekPage(i+1)

newBook.addLinePage()
newBook.toHTML(rootPath)
