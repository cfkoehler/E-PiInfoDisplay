import yfinance as yf


class stockData:

    def __init__(self, tickers):
        self.tickers = tickers
        self.data = self.getData()
        

    def getData(self):
        #data = yf.download(tickers = self.tickers, group_by = 'ticker')
        info = yf.Tickers(self.tickers)
        return info

    def returnData(self):
        return self.data
