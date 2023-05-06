import pandas as pd
import random

def getQuote():
    #Reading in the dataframe of quotes and determining the size
    quotes = pd.read_json('Motivational_Quotes\\Quotes\\filtered.json')
    count = len(quotes)

    #If the number of quotes is too small it resets the JSON
    if(count == 1):
        df = pd.read_json('Motivational_Quotes\\Quotes\\filtered.json')
        quotes = df.loc[df['Category'].isin(['motivation','inspiration','positive'])]
        quotes = quotes.loc[quotes.astype(str).drop_duplicates().index]
        
    #Calculates a random quote and returns it
    num = random.randint(0,count+1)
    moti = (quotes.iloc[num]['Quote'])

    #Removes the used quote
    quotes.drop([quotes.index[num]], inplace=True)

    #Rewrites the JSON with the quote removed   
    result = quotes.to_json(r'Motivational_Quotes\\Quotes\\filtered.json')
    
    #returning the quote to FocusBot
    return moti


if __name__ == "__main__":
    getQuote()
