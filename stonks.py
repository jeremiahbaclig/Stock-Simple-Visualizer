import requests
import PySimpleGUI as sg
import datetime


def get_stock(symbol, year, month, day, daily):
    API_KEY = 'YOUR_KEY'
    day_counter = int(day)
    week_open, week_high, week_low, week_close = 0, 0, 0, 0

    if daily:
        r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol.upper() +
                         '&apikey=' + API_KEY)
        result = r.json()
        try:
            weeks = result['Time Series (Daily)']
        except KeyError:
            return -1, -1, -1, -1

        weekday = datetime.date(year, int(month), int(day)).weekday()

        try:
            for data in range(5-int(weekday)):
                thisDay = weeks[str(year) + '-' + str(month) + '-' + str(day)]
                week_open += float(thisDay['1. open'])
                week_high += float(thisDay['2. high'])
                week_low += float(thisDay['3. low'])
                week_close += float(thisDay['4. close'])
                day_counter += 1

                return week_open, week_high, week_low, week_close
        except KeyError:
            return -1, -1, -1, -1

    else:
        r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=' + symbol.upper() +
                         '&apikey=' + API_KEY)
        result = r.json()
        weeks = result['Weekly Time Series']
        return week_open, week_high, week_low, week_close


def show_stock(symbol, year, month, day, flag):
    week_open, week_high, week_low, week_close = get_stock(symbol, year, month, day, flag)

    if (week_open or week_high or week_low or week_close) is -1:
        sg.Popup("ERROR: Invalid date entered.")

    OH_AVG = (week_open+week_high)/2
    CH_AVG = (week_close+week_high)/2
    OC_AVG = (week_open+week_close)/2
    OL_AVG = (week_open+week_low)/2
    CL_AVG = (week_close+week_low)/2

    stock_display = [[sg.Text(symbol.upper())],
                     [sg.Text('\t\tAverage weekly values (by day):\t')],
                     [sg.Text('OPEN:\t\t'), sg.Text(f'{week_open:.2f}'), sg.Text('\tOPEN+HIGH:\t\t'), sg.Text(f'{OH_AVG:.2f}')],
                     [sg.Text('HIGH:\t\t'), sg.Text(f'{week_high:.2f}'), sg.Text('\tCLOSE+HIGH:\t\t'), sg.Text(f'{CH_AVG:.2f}')],
                     [sg.Text('LOW:\t\t'), sg.Text(f'{week_low:.2f}'), sg.Text('\tOPEN+LOW:\t\t'), sg.Text(f'{OL_AVG:.2f}')],
                     [sg.Text('CLOSE:\t\t'), sg.Text(f'{week_close:.2f}'), sg.Text('\tCLOSE+LOW:\t\t'), sg.Text(f'{CL_AVG:.2f}')],
                     [sg.Text('')],
                     [sg.Text('\tOPEN+CLOSE (TRUE):\t\t'), sg.Text(f'{OC_AVG:.2f}')],
                     [sg.Button('Return')]]

    while True:
        window = sg.Window('STONKS', stock_display, no_titlebar=True, alpha_channel=.75, grab_anywhere=True)
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Return':
            window.close()
            break
    start()


def start():
    sg.theme('DarkBlue1')
    flag = True

    while True:
        layout = [[sg.Text("Stock symbol (ie. TSLA)"), sg.Input(key='SYMBOL')],
                  [sg.Text('Year (YYYY)\t'), sg.Input(key='YEAR')],
                  [sg.Text('Month (MM)\t'), sg.Input(key='MONTH')],
                  [sg.Text('Day (DD)\t\t'), sg.Input(key='DAY')],
                  [sg.Radio('Daily', "CHOOSE", default=False, key='DAILY'), sg.Radio('Weekly', "CHOOSE",
                                                                                     default=False, key='WEEKLY')],
                  [sg.Button('Enter'), sg.Button('Quit')]]

        window = sg.Window('ENTER', layout, no_titlebar=True, alpha_channel=.75, grab_anywhere=True)
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Quit':
            window.close()
            break

        try:
            symbol = values['SYMBOL']
            year = int(values['YEAR'])
            month = values['MONTH']
            day = values['DAY']
            weekday = datetime.date(year, int(month), int(day)).weekday()
        except ValueError:
            sg.Popup("ERROR: Please input all information correctly.")
        except OverflowError:
            sg.Popup("ERROR: Please input all information correctly.")

        try:
            if 5-int(weekday) <= 0:
                sg.Popup("ERROR: Day entered not within trading period (try a weekday?).")
        except UnboundLocalError:
            window.close()
            continue

        if event == 'Enter' or event == 'Daily' or event == 'Weekly':
            window.close()
            if values['DAILY'] is True:
                show_stock(symbol, year, month, day, flag)
                break
            else:
                flag = False
                show_stock(symbol, year, month, day, flag)
                break
        else:
            sg.Popup("ERROR: Select Daily or Weekly.")


if __name__ == '__main__':
    start()
