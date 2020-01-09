"""
Extracts the regular season game data fro the teams that made it to the play offs after the trade dead-lines.
Combines the games after the trades deadline with the regular season for each playoff team.
Source: https://stats.nba.com/teams/
"""
import pandas as pd
from selenium import webdriver
from waitTillLoaded import waitTillLoaded
from tradeDeadLineDates import *

pd.options.display.max_rows = 4000
driver = webdriver.Chrome()
driver.minimize_window()

# go though each year and extract
for year in tradeDeadLineConst:
    # load and set up mainDf
    mainDf = pd.read_csv("data/" + year + ".csv")
    mainDf.set_index('Team', inplace=True, drop=True)

    # pull the websites
    season = tradeDeadLineConst[year][0]
    startDate = tradeDeadLineConst[year][1]
    url = "https://stats.nba.com/teams/traditional/?Season=" + season + "&SeasonType=Regular%20Season&sort=W&dir=-1" \
                                                                        "&PerMode=Totals&DateFrom=" + startDate + \
          year + "&DateTo=07%2F01%2F" + year + " "
    urlOpp = "https://stats.nba.com/teams/opponent/?sort=OPP_PTS&dir=-1&Season=" + season + "&SeasonType=Regular" \
                                                                                            "%20Season&PerMode=Totals" \
                                                                                            "&DateFrom=" + startDate \
             + year + "&DateTo=07%2F01%2F" + year + " "
    driver.get(url)
    waitTillLoaded(driver, "/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody", 60)
    teamTable = pd.read_html(driver.page_source, encoding='utf8')[0]
    driver.get(urlOpp)
    waitTillLoaded(driver, "/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody", 60)
    oppTable = pd.read_html(driver.page_source, encoding='utf8')[0]

    # put the table into pandas df
    teamTable.set_index('TEAM', inplace=True, drop=True)
    oppTable.set_index('TEAM', inplace=True, drop=True)
    teamTable = teamTable.loc[mainDf.index.values, :]
    oppTable = teamTable.loc[mainDf.index.values, :]

    # drop league avg
    mainDf = mainDf.drop("League Average")

    # add the games played
    mainDf["GReg"] = teamTable.GP
    mainDf.GP = mainDf.GP + mainDf.GReg
    mainDf = mainDf.drop(['GReg'], axis=1)

    # add reg wins
    mainDf["GReg"] = teamTable.W
    mainDf.W = mainDf.W + mainDf.GReg
    mainDf = mainDf.drop(['GReg'], axis=1)

    # add reg loss
    mainDf["GReg"] = teamTable.L
    mainDf.L = mainDf.L + mainDf.GReg
    mainDf = mainDf.drop(['GReg'], axis=1)

    # add reg Goals
    mainDf["GReg"] = teamTable.PTS
    mainDf.G = mainDf.G + mainDf.GReg
    mainDf = mainDf.drop(['GReg'], axis=1)

    # add reg Goals against
    mainDf["GReg"] = oppTable.PTS
    mainDf.GA = mainDf.GA + mainDf.GReg
    mainDf = mainDf.drop(['GReg'], axis=1)
    # recalculate win-loss, and difference
    mainDf['DIFF'] = mainDf.G - mainDf.GA
    mainDf['W/L%'] = mainDf.W / mainDf.GP

    # write to CSV
    mainDf.to_csv("data/" + year + ".csv", encoding='utf-8')

# close driver
driver.close()
driver.quit()
