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
    'width': 160,
    'name': 'UntitleCalendar',
    'fontFamily': 'vazirmatn',
    'sentence': [
        'Lorem ipsum dolor sit amet,',
        'consectetur adipiscing elit,',
        'sed do eiusmod tempor incididunt'
    ],
    'padding': [25, 0, 9, 0],
    'lineHeight': 5,
    'daysHeight': 5,
    'showWeekdays': False,
    'weekend': [6],
    'secondColor': '#f00',
    'personalEvents': {
        '1405-10-30': {'icon': 'fire'},
        '1405-10-30': {'icon': 'fire'},
        '1405-10-18': {'icon': 'plane'},
        '1405-10-16': {'icon': 'ship'},
        '1405-8-25': {'icon': 'internet'},
        '1405-8-24': {'icon': 'hand'},
        '1405-10-7': {'icon': 'hand'},
        '1405-4-24': {'icon': 'hand'},
        '1405-12-23': {'icon': 'pi'},
        '1405-11-25': {'icon': 'heart'},
    }
}

newBook = Calendar('data.json',
                   startDate='1405-1-1',
                   ** previewProperty,
                   **example
                   )

newBook.addFirstPage(years=['1405', '2026 - 2027', '1448 - 1447'],
                     turnOfYear=['جمعه ۲۹ اسفند ۱۴۰۴', 'ساعت ۱۸:۱۵:۵۹'])

newBook.addLinePage()
newBook.addChecklistPage(title='اهداف سال ۱۴۰۵',
                         pattern='01', checkboxscale=0.6)

newBook.addOneYearPage(year=1405,  title='سال ۱۴۰۵')
newBook.addHolidaysPage(year=1405, title='تعطیلات رسمی ۱۴۰۵')

for i in range(53):
    newBook.addLinePage()
    newBook.addWeekPage(i+1)

newBook.addLinePage()
newBook.toHTML(rootPath)
