from pyBCV import Currency

currency = Currency()

usd_rate = currency.get_rate(currency_code="USD", prettify=True)
usd_rate_simple = currency.get_rate(currency_code="USD")
print(usd_rate_simple)
