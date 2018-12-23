import requests
from bs4 import BeautifulSoup

def url_to_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

def horse_page_link(url, HOME_URL):
    soup = url_to_soup(url)
    link_list = [HOME_URL + x.get('href') for x in soup.find_all('a', class_='tx-mid tx-low') ]
    return link_list

def get_previous_race_row(soup):
    tag_to_text = lambda x: p.sub("", x).split('\n') 
    split_tr = lambda x: str(x).split('</tr>')
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

def add_soil_columns(row):
        row['soil_heavy'] = 1 if row['wether'][-2:] =='/重'  else 0
        row['soil_s_heavy'] = 1 if row['wether'][-2:] =='稍重'  else 0
        row['soil_good'] = 1 if row['wether'][-2:] =='/良'  else 0
        row['soil_bad'] = 1 if row['wether'][-2:] =='不良'  else 0
        return row

def add_race_data(df):
    df_ =pd.DataFrame()
    for idx, row in df.iterrows():
        if row['popularity'] == '':
            continue

        # 馬場状態
        row = add_soil_columns(row)

        row['money']=int(row['money'].replace(',','')) 
        row['horse_cnt'] = int(row['rank'].split('/')[1])
        row['result_rank'] = int(row['rank'].split('/')[0])
        row['len'] = int(row['len'][0:4])
        row['popularity'] = int(row['popularity'])
        row['weight'] = int(row['weight'])

        # 　競馬場の一致
        row['same_place'] = 1 if row['place'].startswith(PLACE)  else 0

        # タイム(秒)
        try:
            time = datetime.datetime.strptime(row['time'], '%M:%S.%f')
            row['sec'] = time.minute*60 + time.second + time.microsecond/1000000 
        except ValueError:
            time = datetime.datetime.strptime(row['time'], '%S.%f')
            row['sec'] = time.second + time.microsecond/1000000

        row['sec'] = int(row['sec']) 

        df_ = df_.append(row, ignore_index=True)
    return df_


if __name__ == "__main__":
    
    url = "https://www.nankankeiba.com/race_info/2018120720150501.do"

    HOME_URL = "https://www.nankankeiba.com/"

    link_list = horse_page_link(url, HOME_URL)

    print(link_list)
