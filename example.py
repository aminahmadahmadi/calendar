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
        '1403-10-30': {'icon': 'fire'},
        '1403-10-30': {'icon': 'fire'},
        '1403-10-18': {'icon': 'plane'},
        '1403-10-16': {'icon': 'ship'},
        '1403-8-25': {'icon': 'internet'},
        '1403-8-24': {'icon': 'hand'},
        '1403-10-7': {'icon': 'hand'},
        '1403-4-24': {'icon': 'hand'},
        '1403-12-23': {'icon': 'pi'},
        '1403-11-25': {'icon': 'heart'},
    }
}

newBook = Calendar('data.json',
                   startDate='1403-1-1',
                   ** previewProperty,
                   **example
                   )

newBook.addFirstPage(years=['1403', '2024 - 2025', '1446 - 1445'],
                     turnOfYear=['چهارشنبه ۱ فروردین ۱۴۰۳', 'ساعت ۰۶:۳۶:۲۶'])

newBook.addLinePage()
newBook.addChecklistPage(title='اهداف سال ۱۴۰۳',
                         pattern='01', checkboxscale=0.6)

newBook.addOneYearPage(year=1403)
newBook.addHolidaysPage(year=1403, title='تعطیلات رسمی ۱۴۰۳')

for i in range(53):
    newBook.addLinePage()
    newBook.addWeekPage(i+1)

newBook.addLinePage()
newBook.toHTML(rootPath)
