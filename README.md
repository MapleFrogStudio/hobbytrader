# Maple Frog Studio - Hobby Trader Package 

## Hobby trader is a python project for manipulating historical price data for stock trading  

This project uses github actions to download daily minute price data and archive the results as a CSV or PARQUET file. The generated files cover the following groups of symbols:
* TSX
* S&P500
* Each sector (CS - Consumer Defensive, FS - Financial Services, HC - Healthcare, IN - Industrials, TE - technology, CC - Consumer Cyclical, BM - Basic Materials, UT - Utilisities, CS - Communication Services, RE - Real Estate, EN - Energy)

## Modules 
  
**Download** : module to automatically download minute price data for the previous day using Github Actions (please remember non trading days will have duplicate data)  


## Limitations
- Lists of symbols come from statc symbols files that are updated on a random frequency
- Minuet Price Data are stored in blocks of symbols to helps keep files under Github limitations

## Possible Data sources to investigate
[NASDAQ Stick Screener](https://www.nasdaq.com/market-activity/stocks/screener) to download csv files  
[ADVFN](https://ca.advfn.com/investing/stocks/canada/tsx?letter=A)

<!-- 
1) # Title of your project
2) ## Short project description
3) Introduction paragraph, used for SEO Value
4) Simple diagram or Youtube video link
5a) User instructions for user (not for coders)
5b) Developer instructions (for contributors)
6) Contributor expectations
7) Known Issues
8) Beg for money


Readme != full documentation
https://github.com/matiassingers/awesome-readme

external tools:
Banner Maker : https://banner.godori.dev/
Shields : https://shields.io/
Carbon : https://carbon.now.sh/  (for code presentation)


-->