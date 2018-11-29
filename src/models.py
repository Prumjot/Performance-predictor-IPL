from feature_extraction import extracting_total_outs_per_batsman, runs_per_season, all_features, player_info, extracting_age
from cleaning_data import concating_dataframes, cleaning_replacing
from train_test import train_and_test
from collections import Counter
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler



#
def train(df):
    df = df[df.career_age >= 5]

    # making sure that i have same players in y_train and x_train
    target_year = sorted(df.season.unique())[-1]
    y_players = df[df.season == target_year][['batsman_striker']]
    df = df.merge(y_players, on='batsman_striker')
    y = df[df.season == target_year]
    X = df[df.season != target_year]


    season_stats = calculating_season_stats(X)
    career_stats = calculating_career_stats(X)

    all_stats = season_stats.merge(career_stats, on=['batsman_striker'], how='outer').fillna(0)

    #dropping player id, batsman_striker, and all the ages, expcept career age
    all_stats = all_stats.sort_values(('player_id', ''), ascending=True)
    all_stats.drop(all_stats.columns[[0,1,2,3,4,5,6,7]], axis =1, inplace=True)
    #drops consistency and career_runs_match
    all_stats.drop(['consistency', 'career_runs_match'], axis=1, inplace=True)
    X = all_stats
    y = calculating_y_stats(y)
    mapper = {('runs_per_match_avg', 2009):'2009,runs_per_match', ('runs_per_match_avg', 2010):'2010,runs_per_match',
       ('runs_per_match_avg', 2011):'2011,runs_per_match', ('runs_per_match_avg', 2012):'2012,runs_per_match',
       ('runs_per_match_avg', 2013):'2013,runs_per_match', ('runs_per_match_avg', 2014):'2014,runs_per_match',
       ('runs_per_match_avg', 2015):'2015,runs_per_match',('runs_per_match_avg', 2016):'2016,runs_per_match',
          ('runs_per_match_avg', 2017):'2017,runs_per_match',('runs_per_match_avg', 2008):'2008,runs_per_match',
          ('std', ''):'std','career_age':'career_age'}
    label = []
    for col in X.columns:
        if col not in mapper.keys():
            label.append(col)
    X.drop(label, axis=1, inplace=True)
    X.rename(columns=mapper, inplace=True)
    X_col = sorted(X.columns.tolist())
    cols = X_col[::-1]
    X = X[cols]

    return X,y


def test(df):
    df = df[df.career_age >= 5]

    # making sure that i have same players in y_train and x_train
    target_year = sorted(df.season.unique())[-1]
    y_players = df[df.season == target_year][['batsman_striker']]
    df = df.merge(y_players, on='batsman_striker')
    y = df[df.season == target_year]
    X = df[df.season != target_year]


    season_stats = calculating_season_stats(X)
    career_stats = calculating_career_stats(X)

    all_stats = season_stats.merge(career_stats, on=['batsman_striker'], how='outer').fillna(0)

    #dropping player id, batsman_striker, and all the ages, expcept career age
    all_stats = all_stats.sort_values(('player_id', ''), ascending=True)
    #drops all ages
    all_stats.drop(all_stats.columns[[0,1,2,3,4,5,6,7]], axis =1, inplace=True)
    #drops consistency and career_runs_match
    all_stats.drop(['consistency', 'career_runs_match'], axis=1, inplace=True)
    X = all_stats
    y = calculating_y_stats(y)
    mapper = {('runs_per_match_avg', 2009):'2009,runs_per_match', ('runs_per_match_avg', 2010):'2010,runs_per_match',
       ('runs_per_match_avg', 2011):'2011,runs_per_match', ('runs_per_match_avg', 2012):'2012,runs_per_match',
       ('runs_per_match_avg', 2013):'2013,runs_per_match', ('runs_per_match_avg', 2014):'2014,runs_per_match',
       ('runs_per_match_avg', 2015):'2015,runs_per_match',('runs_per_match_avg', 2016):'2016,runs_per_match',
          ('runs_per_match_avg', 2017):'2017,runs_per_match',('runs_per_match_avg', 2008):'2008,runs_per_match',
          ('std', ''):'std', 'career_age':'career_age'}
    label = []
    for col in X.columns:
        if col not in mapper.keys():
            label.append(col)
    X.drop(label, axis=1, inplace=True)
    X.rename(columns=mapper, inplace=True)
    X_col = sorted(X.columns.tolist())
    cols = X_col[::-1]
    X = X[cols]

    return X,y

def calculating_season_stats(df_X_train):
    bat_avg= (df_X_train.groupby(['batsman_striker', 'season','career_age']).sum()).reset_index()
    bat_avg['runs_per_match_avg'] = bat_avg['runs_scored']/bat_avg['matches']
    bat_avg = bat_avg[['player_id', 'batsman_striker', 'season', 'age', 'runs_per_match_avg']]
    bat_avg = (bat_avg.pivot_table(index=['player_id', 'batsman_striker'], columns=['season'], values=['runs_per_match_avg', 'age']))
    bat_avg = bat_avg.reset_index()

    #calculating standard deviation of runs per match through out the career upto target year
    std = bat_avg.reindex_axis(sorted(bat_avg.columns), axis=1)
    std.drop(std.columns[[0,1,2,3,4]], axis =1, inplace=True)
    std = std.T.fillna(bat_avg.mean(axis=1)).T
    #adding mean to not nan seasons(season missed by players)

    std_l = []
    for i in range(len(std)):
        std_l.append(stats.tstd(std.iloc[i][3:10]))
    std['std']= std_l
    std = std[['player_id', 'batsman_striker', 'std']]
    bat_avg_std= bat_avg.merge(std, on=['batsman_striker'])
    bat_avg_std = bat_avg_std.rename(columns={'player_id_x': 'player_id'}).drop('player_id_y', axis=1)
    return bat_avg_std

def calculating_career_stats(df_X_train):
    #calculating runs_per_match for each season
    bat_avg= (df_X_train.groupby(['batsman_striker', 'season','career_age']).sum()).reset_index()
    bat_avg['runs_per_match_avg'] = bat_avg['runs_scored']/bat_avg['matches']

    #calculating runs_per_match for upto the year
    bat_avg= (bat_avg.groupby(['batsman_striker','career_age']).sum()).reset_index()
    bat_avg['career_runs_match']= bat_avg['runs_per_match_avg']/ bat_avg['career_age']

    #calculating career strike rate upto the year
    bat_avg['SR'] = (bat_avg['runs_scored']  / bat_avg['ball'])*100



    #calculating career strike rate upto the year
    bat_avg['consistency'] = 0.4262*bat_avg.career_runs_match + 0.2566*bat_avg.matches + 0.1510*bat_avg.SR + 0.0787*bat_avg['75+']+0.0556*bat_avg['50+'] - 0.0328*bat_avg.number_of_zeros
    bat_avg = bat_avg[['batsman_striker', 'career_runs_match', 'career_age','consistency']]
    return bat_avg

def calculating_y_stats(df_y):
    y = (df_y.groupby(['player_id', 'batsman_striker', 'season']).sum()).reset_index()
    y['runs_per_match']= y['runs_scored'] / y['matches']
    y = y[['player_id', 'batsman_striker', 'season', 'age', 'runs_per_match']]
    y = (y.pivot_table(index=['player_id', 'batsman_striker'], columns=['season'], values=['runs_per_match', 'age']))
    y = y.sort_values('player_id', ascending=True)

    return y

def train_test_for_model(From,To):
#we only want batsman that will play in year i am testing for!
    ''' From: starting year
        To =  target year(validation/ testing year)'''
    df_train = train_and_test(To)
    df_test = train_and_test(To+1)
    #train = all_df[all_df.season<=  To   ]
    df_train = df_train[(df_train.season >=From) & (df_train.season <=To)]
    df_test = df_test[(df_test.season >=From+1) & (df_test.season <=To+1)]


    X_train, y_train = train(df_train)
    X_test, y_test = test(df_test)





    #return X_train.values, y_train.iloc[:,1].values, X_test.values, y_test.iloc[:,1].values
    return X_train, y_train.iloc[:,1], X_test, y_test.iloc[:,1]

# def train():
#     train = train_and_test(2015)
#     reg_X = train.copy()
#     reg_X = reg_X.drop_duplicates()
#     reg_X = reg_X.sort_values(['player_id', 'season'])
#     reg_X = reg_X[reg_X.batsman_striker != 'BB McCullum']
#     #reg[reg.season !=2013]
#     cnt = Counter()
#     for player in reg_X.batsman_striker:
#         cnt[player] += 1
#     a = pd.DataFrame.from_dict(cnt, orient = 'index').reset_index()
#     a = a.sort_values(0, ascending=False).reset_index()
#     a = a.rename(columns={'level_0':'player_id', 'index':'batsman_striker', 0:'seasons_played'})
#     a.drop('player_id',axis= 1 ,inplace= True)
#     reg_X= pd.merge(reg_X, a, on= 'batsman_striker', how='outer')
#     # 1 - the season played because data frame includes the testing year.
#     reg_X['total_seasons_played']= reg_X['seasons_played']-1
#     reg_X.drop(columns='seasons_played', axis=1, inplace=True)
#
#     # ## keeping only batsman that played the testing year 2016 and played more than
#     reg_X = reg_X[reg_X.total_seasons_played >= 5]
#     batin_y = reg_X[reg_X.season ==2015]
#     batin_y = batin_y[['batsman_striker']]
#     reg_X = reg_X.merge(batin_y, on='batsman_striker')
#     reg_y = reg_X[reg_X.season == 2015]
#     reg_X = reg_X[reg_X.season != 2015]
#
#     average_upto_2015= (reg_X.groupby(['batsman_striker', 'season','total_seasons_played']).sum()).reset_index()
#     average_upto_2015['runs_per_match_avg'] = average_upto_2015['runs_scored']/average_upto_2015['matches']
#     average_upto_2015= (average_upto_2015.groupby(['batsman_striker','total_seasons_played']).sum()).reset_index()
#     average_upto_2015['career_runs_match']= average_upto_2015['runs_per_match_avg']/ average_upto_2015['total_seasons_played']
#     average_upto_2015 = average_upto_2015.rename(columns={'total_seasons_played':'career_age'})
#     average_upto_2015['SR'] = (average_upto_2015['runs_scored']  / average_upto_2015['ball'])*100
#     average_upto_2015['consistency'] = 0.4262*average_upto_2015.career_runs_match + 0.2566*average_upto_2015.matches + 0.1510*average_upto_2015.SR + 0.0787*average_upto_2015['75+']+0.0556*average_upto_2015['50+'] - 0.0328*average_upto_2015.total_outs
#     average_upto_2015 = average_upto_2015[['batsman_striker', 'career_runs_match', 'career_age','consistency']]
#
#     reg_y = (reg_y.groupby(['player_id', 'batsman_striker', 'season']).sum()).reset_index()
#     reg_y['runs_per_match']= reg_y['runs_scored'] / reg_y['matches']
#     reg_y = reg_y[['player_id', 'batsman_striker', 'season', 'age', 'runs_per_match']]
#     reg_y = (reg_y.pivot_table(index=['player_id', 'batsman_striker'], columns=['season'], values=['runs_per_match', 'age']))
#     #y_train = reg_y[('runs_per_match',2015)].values
#     reg_x = (reg_X.groupby(['player_id', 'batsman_striker', 'season']).sum()).reset_index()
#     reg_x['runs_per_match']= reg_x['runs_scored'] / reg_x['matches']
#     reg_x = reg_x[['player_id', 'batsman_striker', 'season', 'age', 'runs_per_match']]
#     reg_x = (reg_x.pivot_table(index=['player_id', 'batsman_striker'], columns=['season'], values=['runs_per_match', 'age']))
#     reg_x = reg_x.reset_index()
#     reg_x_std = reg_x.drop([('age', 2008),('age', 2009),('age', 2010),('age', 2011),('age', 2012),('age', 2013),('age', 2014)],axis =1 )
#     reg_x_std = reg_x_std.T.fillna(reg_x.mean(axis=1)).T
#     l = []
#     for i in range(len(reg_x_std)):
#         l.append(stats.tstd(reg_x_std.iloc[i][3:10]))
#     reg_x_std['std']= l
#     reg_x_std = reg_x_std[['player_id', 'batsman_striker', 'std']]
#     reg_x= reg_x.merge(reg_x_std, on=['batsman_striker'])
#     reg_x = reg_x.rename(columns={'player_id_x': 'player_id'}).drop('player_id_y', axis=1)
#     reg_x = reg_x.merge(average_upto_2015, on=['batsman_striker'], how='outer')
#     reg_x = reg_x.fillna(0)
#     reg_y = reg_y.sort_values('player_id', ascending=True)
#     reg_x = reg_x.sort_values(('player_id', ''), ascending=True)
#     reg_x.drop(('batsman_striker', ''), axis=1, inplace=True)
#     reg_x.drop('batsman_striker', axis=1, inplace=True)
#     reg_1_train = reg_x[[('std', ''),'career_runs_match','career_age',('consistency'),('runs_per_match', 2014),('runs_per_match', 2013),('runs_per_match', 2012),('runs_per_match', 2011),('runs_per_match', 2010),('runs_per_match', 2009),('runs_per_match', 2008)]]
#     X_train = reg_1_train
#     y_train = reg_y
#
#     return (X_train,y_train)
#
# def validate():
#
#     train = train_and_test(2016)
#     reg_X = train.copy()
#     reg_X = reg_X.drop_duplicates()
#     reg_X = reg_X[reg_X.season!=2008]
#     reg_X = reg_X.sort_values(['player_id', 'season'])
#     reg_X = reg_X[reg_X.batsman_striker != 'BB McCullum']
#     #reg[reg.season !=2013]
#     cnt = Counter()
#     for player in reg_X.batsman_striker:
#         cnt[player] += 1
#     a = pd.DataFrame.from_dict(cnt, orient = 'index').reset_index()
#     a = a.sort_values(0, ascending=False).reset_index()
#     a = a.rename(columns={'level_0':'player_id', 'index':'batsman_striker', 0:'seasons_played'})
#     a.drop('player_id',axis= 1 ,inplace= True)
#     reg_X= pd.merge(reg_X, a, on= 'batsman_striker', how='outer')
#     # 1 - the season played because data frame includes the testing year.
#     reg_X['total_seasons_played']= reg_X['seasons_played']-1
#     reg_X.drop(columns='seasons_played', axis=1, inplace=True)
#
#     # ## keeping only batsman that played the testing year 2016 and played more than
#     reg_X = reg_X[reg_X.total_seasons_played >= 5]
#     batin_y = reg_X[reg_X.season ==2016]
#     batin_y = batin_y[['batsman_striker']]
#     reg_X = reg_X.merge(batin_y, on='batsman_striker')
#     reg_y = reg_X[reg_X.season == 2016]
#     reg_X = reg_X[reg_X.season != 2016]
#     average_upto_2015= (reg_X.groupby(['batsman_striker', 'season','total_seasons_played']).sum()).reset_index()
#     average_upto_2015['runs_per_match_avg'] = average_upto_2015['runs_scored']/average_upto_2015['matches']
#     average_upto_2015= (average_upto_2015.groupby(['batsman_striker','total_seasons_played']).sum()).reset_index()
#     average_upto_2015['career_runs_match']= average_upto_2015['runs_per_match_avg']/ average_upto_2015['total_seasons_played']
#     average_upto_2015 = average_upto_2015.rename(columns={'total_seasons_played':'career_age'})
#     average_upto_2015['SR'] = (average_upto_2015['runs_scored']  / average_upto_2015['ball'])*100
#     average_upto_2015['consistency'] = 0.4262*average_upto_2015.career_runs_match + 0.2566*average_upto_2015.matches + 0.1510*average_upto_2015.SR + 0.0787*average_upto_2015['75+']+0.0556*average_upto_2015['50+'] - 0.0328*average_upto_2015.total_outs
#     average_upto_2015 = average_upto_2015[['batsman_striker', 'career_runs_match', 'career_age','consistency']]
#     reg_y = (reg_y.groupby(['player_id', 'batsman_striker', 'season']).sum()).reset_index()
#     reg_y['runs_per_match']= reg_y['runs_scored'] / reg_y['matches']
#     reg_y = reg_y[['player_id', 'batsman_striker', 'season', 'age', 'runs_per_match']]
#     reg_y = (reg_y.pivot_table(index=['player_id', 'batsman_striker'], columns=['season'], values=['runs_per_match', 'age']))
#     #y_train = reg_y[('runs_per_match',2016)]
#     reg_x = (reg_X.groupby(['player_id', 'batsman_striker', 'season']).sum()).reset_index()
#     reg_x['runs_per_match']= reg_x['runs_scored'] / reg_x['matches']
#     reg_x = reg_x[['player_id', 'batsman_striker', 'season', 'age', 'runs_per_match']]
#     reg_x = (reg_x.pivot_table(index=['player_id', 'batsman_striker'], columns=['season'], values=['runs_per_match', 'age']))
#     reg_x = reg_x.reset_index()
#     reg_x_std = reg_x.drop([('age', 2015),('age', 2009),('age', 2010),('age', 2011),('age', 2012),('age', 2013),('age', 2014)],axis =1 )
#     reg_x_std = reg_x_std.T.fillna(reg_x.mean(axis=1)).T
#     l = []
#     for i in range(len(reg_x_std)):
#         l.append(stats.tstd(reg_x_std.iloc[i][3:10]))
#     reg_x_std['std']= l
#     reg_x_std = reg_x_std[['player_id', 'batsman_striker', 'std']]
#     reg_x= reg_x.merge(reg_x_std, on=['batsman_striker'])
#     reg_x = reg_x.rename(columns={'player_id_x': 'player_id'}).drop('player_id_y', axis=1)
#     reg_x = reg_x.merge(average_upto_2015, on=['batsman_striker'], how='outer')
#     reg_x = reg_x.fillna(0)
#     reg_y = reg_y.sort_values('player_id', ascending=True)
#     reg_x = reg_x.sort_values(('player_id', ''), ascending=True)
#     reg_x.drop(('batsman_striker', ''), axis=1, inplace=True)
#     reg_x.drop('batsman_striker', axis=1, inplace=True)
#     reg_1_train = reg_x[[('std', ''),'career_runs_match','career_age',('consistency'),('runs_per_match', 2015),('runs_per_match', 2014),('runs_per_match', 2013),('runs_per_match', 2012),('runs_per_match', 2011),('runs_per_match', 2010),('runs_per_match', 2009)]]
#     X_validate = reg_1_train
#     y_validate = reg_y
#
#     return (X_validate,y_validate)
#
# def test():
#
#     train = train_and_test(2017)
#     reg_X = train.copy()
#     reg_X = reg_X.drop_duplicates()
#     reg_X = reg_X[reg_X.season!=2008]
#     reg_X = reg_X[reg_X.season!=2009]
#     reg_X = reg_X.sort_values(['player_id', 'season'])
#     reg_X = reg_X[reg_X.batsman_striker != 'BB McCullum']
#     #reg[reg.season !=2013]
#     cnt = Counter()
#     for player in reg_X.batsman_striker:
#         cnt[player] += 1
#     a = pd.DataFrame.from_dict(cnt, orient = 'index').reset_index()
#     a = a.sort_values(0, ascending=False).reset_index()
#     a = a.rename(columns={'level_0':'player_id', 'index':'batsman_striker', 0:'seasons_played'})
#     a.drop('player_id',axis= 1 ,inplace= True)
#     reg_X= pd.merge(reg_X, a, on= 'batsman_striker', how='outer')
#     # 1 - the season played because data frame includes the testing year.
#     reg_X['total_seasons_played']= reg_X['seasons_played']-1
#     reg_X.drop(columns='seasons_played', axis=1, inplace=True)
#
#     # ## keeping only batsman that played the testing year 2016 and played more than
#     reg_X = reg_X[reg_X.total_seasons_played >= 5]
#     batin_y = reg_X[reg_X.season ==2017]
#     batin_y = batin_y[['batsman_striker']]
#     reg_X = reg_X.merge(batin_y, on='batsman_striker')
#     reg_y = reg_X[reg_X.season == 2017]
#     reg_X = reg_X[reg_X.season != 2017]
#     average_upto_2015= (reg_X.groupby(['batsman_striker', 'season','total_seasons_played']).sum()).reset_index()
#     average_upto_2015['runs_per_match_avg'] = average_upto_2015['runs_scored']/average_upto_2015['matches']
#     average_upto_2015= (average_upto_2015.groupby(['batsman_striker','total_seasons_played']).sum()).reset_index()
#     average_upto_2015['career_runs_match']= average_upto_2015['runs_per_match_avg']/ average_upto_2015['total_seasons_played']
#     average_upto_2015 = average_upto_2015.rename(columns={'total_seasons_played':'career_age'})
#     average_upto_2015['SR'] = (average_upto_2015['runs_scored']  / average_upto_2015['ball'])*100
#     average_upto_2015['consistency'] = 0.4262*average_upto_2015.career_runs_match + 0.2566*average_upto_2015.matches + 0.1510*average_upto_2015.SR + 0.0787*average_upto_2015['75+']+0.0556*average_upto_2015['50+'] - 0.0328*average_upto_2015.total_outs
#     average_upto_2015 = average_upto_2015[['batsman_striker', 'career_runs_match', 'career_age','consistency']]
#     reg_y = (reg_y.groupby(['player_id', 'batsman_striker', 'season']).sum()).reset_index()
#     reg_y['runs_per_match']= reg_y['runs_scored'] / reg_y['matches']
#     reg_y = reg_y[['player_id', 'batsman_striker', 'season', 'age', 'runs_per_match']]
#     reg_y = (reg_y.pivot_table(index=['player_id', 'batsman_striker'], columns=['season'], values=['runs_per_match', 'age']))
#     #y_train = reg_y[('runs_per_match',2017)]
#     reg_x = (reg_X.groupby(['player_id', 'batsman_striker', 'season']).sum()).reset_index()
#     reg_x['runs_per_match']= reg_x['runs_scored'] / reg_x['matches']
#     reg_x = reg_x[['player_id', 'batsman_striker', 'season', 'age', 'runs_per_match']]
#     reg_x = (reg_x.pivot_table(index=['player_id', 'batsman_striker'], columns=['season'], values=['runs_per_match', 'age']))
#     reg_x = reg_x.reset_index()
#     reg_x_std = reg_x.drop([('age', 2015),('age', 2016),('age', 2010),('age', 2011),('age', 2012),('age', 2013),('age', 2014)],axis =1 )
#     reg_x_std = reg_x_std.T.fillna(reg_x.mean(axis=1)).T
#     l = []
#     for i in range(len(reg_x_std)):
#         l.append(stats.tstd(reg_x_std.iloc[i][3:10]))
#     reg_x_std['std']= l
#     reg_x_std = reg_x_std[['player_id', 'batsman_striker', 'std']]
#     reg_x= reg_x.merge(reg_x_std, on=['batsman_striker'])
#     reg_x = reg_x.rename(columns={'player_id_x': 'player_id'}).drop('player_id_y', axis=1)
#     reg_x = reg_x.merge(average_upto_2015, on=['batsman_striker'], how='outer')
#     reg_x = reg_x.fillna(0)
#     reg_y = reg_y.sort_values('player_id', ascending=True)
#     reg_x = reg_x.sort_values(('player_id', ''), ascending=True)
#     reg_x.drop(('batsman_striker', ''), axis=1, inplace=True)
#     reg_x.drop('batsman_striker', axis=1, inplace=True)
#     reg_1_train = reg_x[[('std', ''),'career_runs_match','career_age',('consistency'),('runs_per_match', 2016),('runs_per_match', 2015),('runs_per_match', 2014),('runs_per_match', 2013),('runs_per_match', 2012),('runs_per_match', 2011),('runs_per_match', 2010)]]
#     X_test = reg_1_train
#     y_test = reg_y
#
#     return (X_test,y_test)
if __name__ == "__main__":
    train()
    test()
    calculating_season_stats()
    calculating_career_stats()
    train_test_for_model()
