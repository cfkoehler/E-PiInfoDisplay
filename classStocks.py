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


"""
msft = yf.Ticker("MSFT")

# get stock info
#print(type(msft.info))
#print(msft.info)
print("")
print(msft.info["regularMarketPrice"])
print(msft.info["bid"])
print(msft.info["regularMarketPreviousClose"])
print(msft.info["regularMarketDayHigh"])
print(msft.info["open"])

# get historical market data
#hist = msft.history(period="max")

# show actions (dividends, splits)
#msft.actions

# show dividends
#msft.dividends

# show splits
#msft.splits

# show financials
#msft.financials
#msft.quarterly_financials

# show major holders
#msft.major_holders

# show institutional holders
#msft.institutional_holders

# show balance sheet
#msft.balance_sheet
#msft.quarterly_balance_sheet

# show cashflow
#msft.cashflow
#msft.quarterly_cashflow

# show earnings
#msft.earnings
#msft.quarterly_earnings

# show sustainability
#msft.sustainability

# show analysts recommendations
#msft.recommendations

# show next event (earnings, etc)
#msft.calendar

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
#msft.isin

# show options expirations
#msft.options

# get option chain for specific expiration
#opt = msft.option_chain('YYYY-MM-DD')
# data available via: opt.calls, opt.puts
 """