from feature_extraction import extracting_total_outs_per_batsman, runs_per_season, all_features, player_info, extracting_age
from cleaning_data import concating_dataframes, cleaning_replacing
import pandas as pd


def train_and_test(train_inp, test_inp):
    '''input train : input upto the season for training'''

    all_df =concating_dataframes('../../capstone_project/ipl_csv/Data/trial/')
    player = player_info()



    train = all_df[(all_df.season <=train_inp)]
    test = all_df[all_df.season == test_inp]

    train = all_features(train)

    test = test.groupby(['batsman_striker','player_id']).count().reset_index()
    test = test[['batsman_striker', 'player_id']]
    test = test.merge(player, on=['batsman_striker'], how = 'left')


    # next step would add recent stats of the player to 2017 list.
    test = test.merge(train, on=['batsman_striker', 'player_id', 'DOB', 'Right_hand_bat',
                                'Bowling_skill', 'Australia','Bangladesh','England',
                                'India','Netherlands','New Zealand','Pakistan',
                                'South Africa','Sri Lanka','West Indies','Zimbabwea'], how='left')


    #test = test.fillna('')
    test.dropna(inplace=True)
    test['season'] = test.season.replace('', 2017)

    test.drop('age', axis=1, inplace = True)
    age = []
    for value in test.values:
        if (int(value[2].split('/')[0]))<=3:
            age.append(value[16]-(int(value[2].split('/')[2]))-1)
        else:
            age.append(value[16]-(int(value[2].split('/')[2])))

    test['age']= age
    return train, test




    # def replace(df):
    # cols = df.columns
    # for col in cols:
    #     col_avg = train[col].values.mean()
    #     df[col] = df[col].replace('', col_avg)
    # return test
