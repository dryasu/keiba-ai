import requests
from bs4 import BeautifulSoup

def url_to_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

tag_to_text = lambda x: p.sub("", x).split('\n') 
split_tr = lambda x: str(x).split('</tr>')

def get_previous_race_row(soup):
    race_table = soup.select("table.tb01")[2]
    return [tag_to_text(x)  for x in split_tr(race_table)]

def horse_data(url, race_date):
    soup = url_to_soup(url)

    # 過去のレースデータ
    pre_race_data = get_previous_race_row(soup)
    df = pd.DataFrame(pre_race_data)[1:][[2,3,10,11,13,14,15,19,23]].dropna().rename(columns={
        2:'date', 3:'place', 10:'len', 11:'wether', 13:'popularity', 14:'rank', 15:'time',19:'weight',23:'money'})
    return df

def result_data(url):
    soup = url_to_soup(url)

    # 土の状態
    condition = soup.find(id="race-data02").get_text().replace('\n','').split(';')[1].split('　')[2][0:1]

    # レースの長さ
    race_len = int(soup.find(id="race-data01-a").get_text().replace('\n','').split('　')[3].replace(',','')[1:5])

    # 1位
    hukusyo_list = []
    hukusyo_list.append(int(p.sub("", str(soup.find_all('tr', class_='bg-1chaku')[0]).split('</td>')[2]).replace('\n','') ))

    # レース日
    race_date_str = soup.find(id="race-data01-a").get_text().replace('\n','').split(';')[0].split('日')[0]
    race_date = dt.strptime(race_date_str, '%Y年%m月%d')
    return hukusyo_list, condition, race_len, race_date