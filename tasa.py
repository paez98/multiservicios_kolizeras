from pyBCV import Currency

currency = Currency()

usd_rate = currency.get_rate(currency_code="USD", prettify=True)
print(usd_rate)
