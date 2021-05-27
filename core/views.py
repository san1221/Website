from django.shortcuts import render
from urllib.request import Request, urlopen
import pandas as pd

def get_html_content(request):
    import requests
    song = request.GET.get('song')
    song = song.replace(" ", "-")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    url = 'https://genius.com/'+song+'-lyrics'
    req = Request(url, headers = {'User-Agent' : 'Mozilla/5.0'})
    html_content = urlopen(req).read()
    return html_content

def get_html_content2(request):
    import requests
    city = request.GET.get('city')
    city = city.replace(' ', '+')
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content2 = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content2

def home(request):
    return render(request, 'core/home.html')

def aboutus(request):
    return render(request,'core/aboutus.html')

def contactus(request):
    return render(request,'core/contactus.html')

def stock(request):
    return render(request,'core/stock.html')

def sports(request):
    return render(request,'core/sports.html')

def songs(request):
    result = None
    if 'song' in request.GET:
        # fetch the weather from Google.
        html_content = get_html_content(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        result = dict()
        result["lyrics"] = []
        result["release"] = []
        # extract songname
        for title in soup.findAll('title'):
            result["title"] = title.text.strip()
        # get lyrics
        for div in soup.findAll('div', attrs = {'class':'lyrics'}):
            result["lyrics"].append(div.text.strip().split("\n"))
    return render(request, 'core/songs.html', {'result': result})

def weather(request):
    result = None
    if 'city' in request.GET:
        # fetch the weather from Google.
        html_content2 = get_html_content2(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content2, 'html.parser')
        result = dict()
        # extract region
        result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
        # extract temperature now
        result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
        # get the day and hour now
        result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
        # get the actual weather
        result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text

    return render(request, 'core/weather.html', {'result': result})

def scrapingCurrencies(request):
    import requests
    from bs4 import BeautifulSoup
    names = []
    prices = []
    changes = []
    percentChanges = []
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    data = session.get('https://in.finance.yahoo.com/currencies?guccounter=1').text
    soup = BeautifulSoup(data,'html.parser')
    for i in range(40, 404, 14):
        for listing in soup.find_all('tr', attrs={'data-reactid': i}):
            for name in listing.find_all('td', attrs={'data-reactid': i + 3}):
                names.append(name.text)
            for price in listing.find_all('td', attrs={'data-reactid': i + 4}):
                prices.append(price.text)
            for change in listing.find_all('td', attrs={'data-reactid': i + 5}):
                changes.append(change.text)
            for percentChange in listing.find_all('td', attrs={'data-reactid': i + 7}):
                percentChanges.append(percentChange.text)
    df = pd.DataFrame({"Names": names, "Prices": prices, "Change": changes, "% Change": percentChanges})
    data=df.to_html()
    return render(request,'core/scrapingCurrencies.html',{'data': data})

def worldIndices(request):
    import requests
    from bs4 import BeautifulSoup
    prices = []
    names = []
    changes = []
    percentChanges = []
    CryptoCurrenciesUrl = "https://in.finance.yahoo.com/world-indices"
    r = requests.get(CryptoCurrenciesUrl)
    data = r.text
    soup = BeautifulSoup(data)
    for i in range(40, 404, 14):
        for row in soup.find_all('tbody'):
            for srow in row.find_all('tr'):
                for name in srow.find_all('td', attrs={'class': 'data-col1'}):
                    names.append(name.text)
                for price in srow.find_all('td', attrs={'class': 'data-col2'}):
                    prices.append(price.text)
                for change in srow.find_all('td', attrs={'class': 'data-col3'}):
                    changes.append(change.text)
                for percentChange in srow.find_all('td', attrs={'class': 'data-col4'}):
                    percentChanges.append(percentChange.text)
    df=pd.DataFrame({"Names": names, "Prices": prices, "Change": changes, "% Change": percentChanges})
    data = df.to_html()
    return render(request, 'core/worldIndices.html', {'data': data})

def commodities(request):
    import requests
    from bs4 import BeautifulSoup
    prices = []
    names = []
    changes = []
    percentChanges = []
    marketTimes = []
    totalVolumes = []
    openInterests = []
    CryptoCurrenciesUrl = "https://in.finance.yahoo.com/commodities"
    r = requests.get(CryptoCurrenciesUrl)
    data = r.text
    soup = BeautifulSoup(data)
    for i in range(40, 404, 14):
        for row in soup.find_all('tbody'):
            for srow in row.find_all('tr'):
                for name in srow.find_all('td', attrs={'class': 'data-col1'}):
                    names.append(name.text)
                for price in srow.find_all('td', attrs={'class': 'data-col2'}):
                    prices.append(price.text)
                for time in srow.find_all('td', attrs={'class': 'data-col3'}):
                    marketTimes.append(time.text)
                for change in srow.find_all('td', attrs={'class': 'data-col4'}):
                    changes.append(change.text)
                for percentChange in srow.find_all('td', attrs={'class': 'data-col5'}):
                    percentChanges.append(percentChange.text)
                for volume in srow.find_all('td', attrs={'class': 'data-col6'}):
                    totalVolumes.append(volume.text)
                for openInterest in srow.find_all('td', attrs={'class': 'data-col7'}):
                    openInterests.append(openInterest.text)
    df=pd.DataFrame({"Names": names, "Prices": prices, "Change": changes, "% Change": percentChanges, "Market Time": marketTimes,'Open Interest': openInterests, "Volume": totalVolumes})
    data = df.to_html()
    return render(request, 'core/commodities.html', {'data': data})

def premierTable(request):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    result = requests.get("https://www.bbc.co.uk/sport/football/tables")
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')
    table = soup.find_all("table")
    league_table = table[0]
    teams = league_table.find_all("tr")
    position = []
    team_name = []
    played = []
    won = []
    drawn = []
    lost = []
    for_goals = []
    against_goals = []
    goal_diff = []
    points = []
    for team in teams[1:21]:
        stats = team.find_all("td")
        position.append(stats[0].text)
        team_name.append(stats[2].text)
        played.append(stats[3].text)
        won.append(stats[4].text)
        drawn.append(stats[5].text)
        lost.append(stats[6].text)
        for_goals.append(stats[7].text)
        against_goals.append(stats[8].text)
        goal_diff.append(stats[9].text)
        points.append(stats[10].text)
    df=pd.DataFrame({"Position": position, "Team Name": team_name, "Played": played, "Won": won, "Drawn": drawn, "Lost": lost,"lost": lost, "For Goals": for_goals, "Against Goals": against_goals, "Goal Diff": goal_diff,"Points": points})
    data = df.to_html()
    return render(request, 'core/premierTable.html', {'data': data})

def spanishTable(request):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    result = requests.get("https://www.bbc.com/sport/football/spanish-la-liga/table")
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')
    table = soup.find_all("table")
    league_table = table[0]
    teams = league_table.find_all("tr")
    position = []
    team_name = []
    played = []
    won = []
    drawn = []
    lost = []
    for_goals = []
    against_goals = []
    goal_diff = []
    points = []
    for team in teams[1:21]:
        stats = team.find_all("td")
        position.append(stats[0].text)
        team_name.append(stats[2].text)
        played.append(stats[3].text)
        won.append(stats[4].text)
        drawn.append(stats[5].text)
        lost.append(stats[6].text)
        for_goals.append(stats[7].text)
        against_goals.append(stats[8].text)
        goal_diff.append(stats[9].text)
        points.append(stats[10].text)
    df=pd.DataFrame({"Position": position, "Team Name": team_name, "Played": played, "Won": won, "Drawn": drawn, "Lost": lost,"lost": lost, "For Goals": for_goals, "Against Goals": against_goals, "Goal Diff": goal_diff,"Points": points})
    data = df.to_html()
    return render(request, 'core/spanishTable.html', {'data': data})

def italianTable(request):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    result = requests.get("https://www.bbc.com/sport/football/italian-serie-a/table")
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')
    table = soup.find_all("table")
    league_table = table[0]
    teams = league_table.find_all("tr")
    position = []
    team_name = []
    played = []
    won = []
    drawn = []
    lost = []
    for_goals = []
    against_goals = []
    goal_diff = []
    points = []
    for team in teams[1:21]:
        stats = team.find_all("td")
        position.append(stats[0].text)
        team_name.append(stats[2].text)
        played.append(stats[3].text)
        won.append(stats[4].text)
        drawn.append(stats[5].text)
        lost.append(stats[6].text)
        for_goals.append(stats[7].text)
        against_goals.append(stats[8].text)
        goal_diff.append(stats[9].text)
        points.append(stats[10].text)
    df=pd.DataFrame({"Position": position, "Team Name": team_name, "Played": played, "Won": won, "Drawn": drawn, "Lost": lost,"lost": lost, "For Goals": for_goals, "Against Goals": against_goals, "Goal Diff": goal_diff,"Points": points})
    data = df.to_html()
    return render(request, 'core/italianTable.html', {'data': data})

def f1(request):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    result = requests.get("https://www.bbc.com/sport/formula1/drivers-world-championship/standings")
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')
    table = soup.find_all("table")
    league_table = table[0]
    teams = league_table.find_all("tr")
    position = []
    driver = []
    team_name = []
    point = []
    wins = []
    for team in teams[1:23]:
        stats = team.find_all("td")
        position.append(stats[0].text)
        driver.append(stats[1].text)
        team_name.append(stats[2].text)
        wins.append(stats[3].text)
        point.append(stats[4].text)
    df=pd.DataFrame({"Position": position, "Driver": driver, "Team": team_name, "Wins": wins, "Points": point})
    data = df.to_html()
    return render(request, 'core/f1.html', {'data': data})



