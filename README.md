# Stock-Simple-Visualizer

Prototype of a stock analysis application. Pulls from the *Alpha Vantage API* and utilizes *PySimpleGUI* to receive user input. Continuously 
takes user input from given stock symbol, date, and outputs based on daily (averaged throughout the week) or weekly data. 
In this simple version, basic error handling is considered for incorrect dates, symbols, or overflow. API key required to use.

![](media/stonks_prototype2.gif)
![image](https://user-images.githubusercontent.com/55364674/121823802-7c162c80-cc75-11eb-9333-bee661d1001e.png)

For future updates (TO-DO):
- [ ] Additional error handling for more situations.
- [x] Display graph data (Matplotlib and Pandas).
- [ ] Interactive calculator from Open, Close, Low, High.
- [ ] Choose time-frame.
- [ ] Choose single day data.
- [ ] Web support (PySimpleGUIWeb)
- [x] Add weekly data.
- [x] Menu options.

Alpha Vantage Documentation:
https://www.alphavantage.co/documentation/

PySimpleGUI Documentation:
https://pysimplegui.readthedocs.io/en/latest/
