"""
Extract the season's per-game data for the play offs.
Source: https://www.basketball-reference.com/playoffs/NBA_
"""
# make a csv file of data for each year
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# set up driver
driver = webdriver.Chrome()
driver.minimize_window()
pd.options.display.max_rows = 4000


# Loop and make a csv for each year
years = pd.read_csv("years.csv")
for year in years['year']:
    # load and set up mainDf
    year = str(year)
    mainDf = pd.read_csv("data/" + year + ".csv")
    mainDf.set_index('Team', inplace=True, drop=True)
    mainDf["CQF GP"] = 0
    mainDf["CQF W-L%"] = 0
    mainDf["CSF GP"] = 0
    mainDf["CSF W-L%"] = 0
    mainDf["CF GP"] = 0
    mainDf["CF W-L%"] = 0
    mainDf["F GP"] = 0
    mainDf["F W-L%"] = 0

    # pull the website
    url = "https://www.basketball-reference.com/playoffs/NBA_" + year + ".html"
    driver.get(url)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "html.parser")
    # put the table into pandas df
    table = soup.find(id="all_playoffs")
    df = pd.read_html(str(table))[0]
    df = df[[1]]
    df = df.dropna()

    # Clean and input data into main database
    count = 0
    for i, row in enumerate(df.values):
        # print(mainDf)
        if "over" in row[0]:
            split = row[0].split(" over ")
            winner = split[0]
            split2 = split[1].split(" \xa0(")
            looser = split2[0]
            winnerScore = int([split2[1][0]][0])
            looserScore = int([split2[1][2]][0])
            # input the data
            if count == 0:
                mainDf.loc[winner, "F GP"] = winnerScore + looserScore
                mainDf.loc[looser, "F GP"] = winnerScore + looserScore
                mainDf.loc[winner, "F W-L%"] = winnerScore / (winnerScore + looserScore)
                mainDf.loc[looser, "F W-L%"] = looserScore / (winnerScore + looserScore)
            elif 1 <= count <= 2:
                mainDf.loc[winner, "CF GP"] = winnerScore + looserScore
                mainDf.loc[looser, "CF GP"] = winnerScore + looserScore
                mainDf.loc[winner, "CF W-L%"] = winnerScore / (winnerScore + looserScore)
                mainDf.loc[looser, "CF W-L%"] = looserScore / (winnerScore + looserScore)
            elif 3 <= count <= 6:
                mainDf.loc[winner, "CSF GP"] = winnerScore + looserScore
                mainDf.loc[looser, "CSF GP"] = winnerScore + looserScore
                mainDf.loc[winner, "CSF W-L%"] = winnerScore / (winnerScore + looserScore)
                mainDf.loc[looser, "CSF W-L%"] = looserScore / (winnerScore + looserScore)
            elif 7 <= count <= 14:
                mainDf.loc[winner, "CQF GP"] = winnerScore + looserScore
                mainDf.loc[looser, "CQF GP"] = winnerScore + looserScore
                mainDf.loc[winner, "CQF W-L%"] = winnerScore / (winnerScore + looserScore)
                mainDf.loc[looser, "CQF W-L%"] = looserScore / (winnerScore + looserScore)
            count = count + 1
    # write to CSV
    mainDf.to_csv("data/" + year + ".csv", encoding='utf-8')
# close driver
driver.close()
driver.quit()
