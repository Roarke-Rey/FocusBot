"""
Testing for getting the motivational quotes. Full documentation in the bot.py file
"""

import pandas as pd
import random

quotes = pd.read_json('Quotes/filtered.json')

def getQuote():
    count = len(quotes)
    num = random.randint(0,count+1)
    print(quotes.iloc[num]['Quote'])

    quotes.drop([quotes.index[num]], inplace=True)


if __name__ == "__main__":
    getQuote()