from cal import Calendar
import os

rootPath = os.getcwd()

newBook = Calendar('cal1401.json',
                   name='cal-1401',
                   margin=[0, 0, 0, 0],
                   showWeekdays=True,
                   secondColor='#f00',
                   weekend=1,
                   startWeekday='Sat',
                   showFullCalendar=False
                   )


newBook.addLinePage()
for i in range(53):
    newBook.addLinePage()
    newBook.addWeekPage(i+1)

newBook.toHTML(rootPath)
