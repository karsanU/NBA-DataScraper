"""
Extracts play-off aggregate stats for each team per that year and exports it into a excel file with each sheet
representing a season.
Source: https://www.basketball-reference.com/playoffs/NBA_
"""
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# start web driver
driver = webdriver.Chrome()
driver.minimize_window()

# loop over each year that data is to be collected.
allData = {}
years = pd.read_csv("years.csv")
for year in years["year"]:
    # pull the website
    year = str(year)
    url = "https://www.basketball-reference.com/playoffs/NBA_" + year + ".html"
    driver.get(url)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "lxml")

    # read tables from website
    df = soup.find(id="misc")
    teamTable = soup.find(id="team-stats-base")
    oppTable = soup.find(id="opponent-stats-base")
    df = pd.read_html(str(df))[0]
    teamTable = pd.read_html(str(teamTable))[0]
    oppTable = pd.read_html(str(oppTable))[0]

    # only take 'Team','G','W','L','W/L%' columns from misc tables
    df.columns = df.columns.droplevel()
    df = df[['Team', 'G', 'W', 'L', 'W/L%']]
    df = df.rename(columns={'G': 'GP'})

    # set the index as team names
    df.set_index('Team', inplace=True, drop=True)
    teamTable.set_index('Team', inplace=True, drop=True)
    oppTable.set_index('Team', inplace=True, drop=True)

    # add the team points and apponent points columns, then crt
    df['G'] = teamTable.PTS
    df['GA'] = oppTable.PTS
    df['DIFF'] = df.G - df.GA
    allData[year] = df

    # write to CSV
    df.to_csv("data/" + year + ".csv", encoding='utf-8')
driver.close()
driver.quit()

