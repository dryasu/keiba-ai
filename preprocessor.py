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
