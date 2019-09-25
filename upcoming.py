import datetime

import urllib.request
from bs4 import BeautifulSoup
import ssl
import json

# Getting upcoming matches
def get_upcoming():
    jsons = []
    newSoup = BeautifulSoup(upcoming, "lxml")
    upcomingMatches = newSoup.findAll('table', attrs={'class': 'infobox_matches_content'})
    for match in upcomingMatches:
        leftTeamNameSpan = match.find('td', attrs={'class': 'team-left'}).find('span', attrs={
            'class': 'team-template-text'})
        if leftTeamNameSpan.find('a') is None:
            # leftTeamName = "TBD"
            # leftTeamLogo = "/images/team-z_2.png"
            continue
        else:
            leftTeamName = leftTeamNameSpan.find('a').text
            leftTeamLogo = "https://liquipedia.net/" + match.find('td', attrs={'class': 'team-left'}).find('span',
                                                                                                           attrs={
                                                                                                               'class': 'team-template-image'}).find(
                'img').get('src')
        rightTeamNameSpan = match.find('td', attrs={'class': 'team-right'}).find('span', attrs={
            'class': 'team-template-text'})
        if rightTeamNameSpan.find('a') is None:
            # rightTeamName = "TBD"
            # rightTeamLogo = "/images/team-z_2.png"
            continue
        else:
            rightTeamName = rightTeamNameSpan.find('a').text
            rightTeamLogo = "https://liquipedia.net/" + match.find('td', attrs={'class': 'team-left'}).find('span',
                                                                                                            attrs={
                                                                                                                'class': 'team-template-image'}).find(
                'img').get('src')
        timeInfo = str(
            match.find('span', attrs={'class': 'timer-object'}).text).split()
        timeStart = timeInfo[4].split(":")
        timeStart.extend([timeInfo[1].rstrip(","), months.index(timeInfo[0]) + 1])
        tempDict = dict(team1=dict(name=leftTeamName, logo_url=leftTeamLogo),
                        team2=dict(name=rightTeamName, logo_url=rightTeamLogo),
                        startTime="{0}.{1} {2}.{3}".format(timeStart[0], timeStart[1], timeStart[2],
                                                           "0" + str(timeStart[3]) if len(str(timeStart[3])) < 2 else
                                                           timeStart[3]))
        jsons.append(json.dumps(tempDict))
    return jsons

# That's ass but that's what it has to be xD
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
curTime = datetime.datetime.now()
# flag to check whether there are ongoing matches
flag = False
gcontext = ssl.SSLContext()
with urllib.request.urlopen("https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches", context=gcontext) as url:
    page = url.read()
soup = BeautifulSoup(page, "lxml")
# Getting matches
find_matchbox = soup.findAll('div', attrs={'id': 'infobox_matches'})
upcoming = str(find_matchbox[0]) if len(find_matchbox) < 2 else str(find_matchbox[1])
jsonsUpcoming = get_upcoming()
# Printing json results
print(jsonsUpcoming)
