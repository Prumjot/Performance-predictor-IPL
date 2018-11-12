
import pandas as pd
import random
import itertools


def uniqueid():
    seed = random.getrandbits(2)
    while True:
       yield seed
       seed += 1

def player_id(df):
    unique_sequence = uniqueid()
    ids = list(itertools.islice(unique_sequence, 1000))
    player_list = df.batsman_striker.unique()
    dic = {}
    i = 0
    for player in sorted(player_list):
        if player in dic.keys():
            pass
        else:
            dic[player]=ids[i]
            i+=1
    player_id = pd.DataFrame.from_dict(dic, orient = 'index' ).reset_index()
    player_id.rename(columns={'index':'batsman_striker', 0: 'player_id'}, inplace=True)
    df  = df.merge(player_id, on='batsman_striker')
    return df
#total out





def extracting_total_outs_per_batsman(df):
    player = {}
    for value in df['batsman_out'].values:
        if value not in player.keys():
            player[value]=1

        else:
            player[value]+=1
        #player.pop('""')

    df_1 = pd.DataFrame.from_dict(player,orient='index',columns=['total_outs'])
    df_1 = df_1.reset_index()
    df_1.rename(columns={'index':'batsman_striker'}, inplace=True)


    return df_1

def runs_per_season(df):
    df_1 = extracting_total_outs_per_batsman(df)
    df['ball']=1
    df= (df.groupby(['batsman_striker','match_id','season']).sum()).reset_index()
    df['matches']=1
    df_sum = df.pivot_table(index=['batsman_striker','season'],values=['runs_scored', 'matches', 'ball'],aggfunc=sum)
    df_sum = df_sum.reset_index()
    #higest score for player
    df_max = df.pivot_table(index='batsman_striker',values=['runs_scored'],aggfunc=max)
    df_max = df_max.reset_index()
    df_merged = df_sum.merge(df_1, on ='batsman_striker').merge(df_max, on='batsman_striker')
    df_merged.rename(columns={'runs_scored_x':'runs_scored','runs_scored_y':'highest_score'}, inplace =True)
    df_merged = player_id(df_merged)
    return df_merged

def batting_first(df):
    batting_first = df[df.inning == 1]
    batting_first = runs_per_season(batting_first)
    batting_first = average_and_strike_rate(batting_first)
    batting_first = batting_first[['batsman_striker', 'season', 'Average', 'strike_rate']]
    batting_first.rename(columns={'Average':'Average_1st_innings', 'strike_rate':'strike_rate_1st_innings' }, inplace=True)
    return batting_first

def batting_second(df):
    batting_second = df[df.inning == 2]
    batting_second = runs_per_season(batting_second)
    batting_second = average_and_strike_rate(batting_second)
    batting_second = batting_second[['batsman_striker', 'season', 'Average', 'strike_rate']]
    batting_second.rename(columns={'Average':'Average_2nd_innings', 'strike_rate':'strike_rate_2nd_innings' }, inplace=True)
    return batting_second


def average_and_strike_rate(df):
    df['Average'] = round(df.runs_scored / df.total_outs,2)
    df['strike_rate'] = round((df.runs_scored/df.ball)*100,2)
    return df

def all_features(df):
    df_1 = runs_per_season(df)
    df_1 = average_and_strike_rate(df_1)
    df_bf = batting_first(df)
    df_bs = batting_second(df)
    df_merged = df_1.merge(df_bf, on= ['batsman_striker', 'season']).merge(df_bs, on= ['batsman_striker', 'season'])
    df_merged.sort_values('season', ascending=True, inplace=True)
    return df_merged

if __name__ == "__main__":
    extracting_total_outs_per_batsman()
    runs_per_season()
    batting_first()
    batting_second()
    all_features()
