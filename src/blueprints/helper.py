def get_currency_symbol(currency):
    currency_to_symbol_dict = {
        "INR" : "₹",
        "USD" : "$ ",
        "EUR" : "€ ",
        "GBP" : "£ ",
        "JPY" : "¥ ",
        "AUD" : "A$ ",
    }
    return currency_to_symbol_dict.get(currency, currency)
