
import pandas as pd
import random
import itertools



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

def number_of_zeros(df):
    zeros = (df.groupby(['batsman_striker','player_id','season', 'match_id']).sum()).reset_index()
    zeros = zeros[zeros.runs_scored == 0]
    zeros = (zeros.groupby(['batsman_striker', 'player_id','season']).count()).reset_index()
    zeros = zeros.pivot_table(index=['batsman_striker','player_id','season'],values=['runs_scored'],aggfunc=sum)
    (zeros.rename(columns={'runs_scored':'number_of_zeros'}, inplace=True))
    zeros = zeros.reset_index()
    return zeros

def number_30_50s_75(df):
    number_of_30s = (df.groupby(['batsman_striker','player_id','season', 'match_id']).sum()).reset_index()
    number_of_30s = number_of_30s[(number_of_30s.runs_scored >= 30) & (number_of_30s.runs_scored <50)]
    number_of_30s = (number_of_30s.groupby(['batsman_striker','player_id','season']).count()).reset_index()
    number_of_30s.rename(columns={'runs_scored':'30+'}, inplace = True)
    number_of_30s = number_of_30s[['batsman_striker', 'player_id','season', '30+']]

    number_of_50s = (df.groupby(['batsman_striker','season', 'player_id','match_id']).sum()).reset_index()
    number_of_50s = number_of_50s[(number_of_50s.runs_scored >= 50) & (number_of_50s.runs_scored <74)]
    number_of_50s = (number_of_50s.groupby(['batsman_striker','player_id','season']).count()).reset_index()
    number_of_50s.rename(columns={'runs_scored':'50+'}, inplace = True)
    number_of_50s = number_of_50s[['batsman_striker','player_id', 'season', '50+']]

    number_of_75s = (df.groupby(['batsman_striker','player_id','season', 'match_id']).sum()).reset_index()
    number_of_75s = number_of_75s[(number_of_75s.runs_scored >= 75)]
    number_of_75s = (number_of_75s.groupby(['batsman_striker','player_id','season']).count()).reset_index()
    number_of_75s.rename(columns={'runs_scored':'75+'}, inplace = True)
    number_of_75s = number_of_75s[['batsman_striker', 'player_id','season', '75+']]

    merged = number_of_30s.merge(number_of_50s, how = 'left', on= ['batsman_striker', 'player_id','season']).merge(number_of_75s, how = 'left', on=['batsman_striker', 'player_id','season'])
    merged = merged.fillna(0)
    return merged
def runs_per_season(df):
    df_1 = extracting_total_outs_per_batsman(df)
    df['ball']=1
    df= (df.groupby(['batsman_striker','match_id','player_id','season']).sum()).reset_index()
    df['matches']=1
    df_sum = df.pivot_table(index=['batsman_striker','player_id','season'],values=['runs_scored', 'matches', 'ball'],aggfunc=sum)
    df_sum = df_sum.reset_index()
    #higest score for player
    df_max = df.pivot_table(index=['batsman_striker','player_id'],values=['runs_scored'],aggfunc=max)
    df_max = df_max.reset_index()
    df_merged = df_sum.merge(df_1, on =['batsman_striker'], how ='left').merge(df_max, on=['player_id','batsman_striker'], how= 'left')
    df_merged.rename(columns={'runs_scored_x':'runs_scored','runs_scored_y':'highest_score'}, inplace =True)
    return df_merged

def batting_first(df):
    batting_first = df[df.inning == 1]
    batting_first = runs_per_season(batting_first)
    batting_first = average_and_strike_rate(batting_first)
    batting_first = batting_first[['batsman_striker', 'player_id','season', 'Average', 'strike_rate']]
    batting_first.rename(columns={'Average':'Average_1st_innings', 'strike_rate':'strike_rate_1st_innings' }, inplace=True)
    return batting_first

def batting_second(df):
    batting_second = df[df.inning == 2]
    batting_second = runs_per_season(batting_second)
    batting_second = average_and_strike_rate(batting_second)
    batting_second = batting_second[['batsman_striker', 'player_id','season', 'Average', 'strike_rate']]
    batting_second.rename(columns={'Average':'Average_2nd_innings', 'strike_rate':'strike_rate_2nd_innings' }, inplace=True)
    return batting_second


def average_and_strike_rate(df):
    df['Average'] = round(df.runs_scored / df.total_outs,2)
    df['strike_rate'] = round((df.runs_scored/df.ball)*100,2)
    return df

def toss_win_count(df):
    toss_winner = df[df.batting_team==df.match_toss_winner]
    toss_winner = toss_winner.groupby(['match_id', 'player_id','batsman_striker', 'season']).count().reset_index()
    toss_winner['toss_win_count']= 1
    toss_winner = toss_winner[['match_id', 'season','batsman_striker', 'player_id','toss_win_count']]
    toss_win_count  = toss_winner.groupby(['batsman_striker', 'player_id','season']).count().reset_index()
    toss_win_count.drop('match_id', axis = 1, inplace= True)
    return toss_win_count

def player_info():
    df = pd.read_csv('../../capstone_project/ipl_csv/Data/player_data/player_info_updated')
    df.drop('Unnamed: 0', axis =1, inplace = True)
    new_player = pd.DataFrame([['Niraj Patel', '3/26/1981', 'Left-hand bat', '', 'India' ], ['AS Yadav',  '12/23/1981', 'Right-hand bat', 'Right-arm offbreak', "India"]], columns=['batsman_striker', 'DOB','Batting_hand','Bowling_skill','Country_Name'])
    df = df.append(new_player)
    df = df.fillna('')
    dummies = pd.get_dummies(df.Country_Name,drop_first=True)
    df.drop('Country_Name', axis = 1, inplace= True)
    df = df.merge(dummies,how='right' ,left_index=True,right_index=True)

    batting_hand = []
    for value in df.Batting_hand.values:
        if value.startswith('Right'):
            batting_hand.append('Right_hand_bat')
        else:
            batting_hand.append('Left_hand_bat')

    df['Batting_hand'] = batting_hand
    batting_dummies = pd.get_dummies(df.Batting_hand,drop_first=True)
    df.drop('Batting_hand', axis = 1, inplace= True)
    df = df.merge(batting_dummies,how='right' ,left_index=True,right_index=True)


    return df


def extracting_age(zeros_merged):
    info = player_info()
    player_merged = zeros_merged.merge(info, on ='batsman_striker', how = 'left')

    age = []
    for value in player_merged.values:
        if (int(value[19].split('/')[0]))<=3:
            age.append(value[2]-(int(value[19].split('/')[2]))-1)
        else:
            age.append(value[2]-(int(value[19].split('/')[2])))
    player_merged['age']= age
    return player_merged

def normalizing_avg(df):
    #max_1 = df.groupby(['player_id', 'batsman_striker']).max()
    max_1 = df.groupby(['batsman_striker']).max()
    trial_max = max_1.reset_index()

    trial_max.rename(columns={'Average': 'max_avg'}, inplace=True)

    #trial_max = trial_max[['player_id','batsman_striker', 'max_avg']]
    trial_max = trial_max[['batsman_striker', 'max_avg']]

    #trial_max_avg = trial_max.merge(df, on= ['player_id','batsman_striker'], how='left')
    trial_max_avg = trial_max.merge(df, on= ['batsman_striker'], how='left')

    trial_max_avg['normalized_avg']= trial_max_avg.Average / trial_max_avg.max_avg

    return trial_max_avg


def all_features(df):

    df_1 = runs_per_season(df)
    df_1 = average_and_strike_rate(df_1)
    df_bf = batting_first(df)
    df_bs = batting_second(df)
    toss_win = toss_win_count(df)
    stats = number_30_50s_75(df)
    zeros = number_of_zeros(df)
    df_merged = df_1.merge(df_bf, on= ['batsman_striker','player_id', 'season'],how= 'left').merge(df_bs, on= ['batsman_striker', 'player_id','season'], how='left')
    df_merged = df_merged.merge(toss_win, on = ['batsman_striker', 'player_id','season'], how='left')
    scores_merged = df_merged.merge(stats, on=['batsman_striker','player_id', 'season'], how = 'left')
    zeros_merged = scores_merged.merge(zeros, on=['batsman_striker','player_id', 'season'], how= 'left')
    zeros_merged = zeros_merged.fillna(0)
    player_info_merged = extracting_age(zeros_merged)
    player_info_merged.sort_values('season', ascending=True, inplace=True)
    return player_info_merged

if __name__ == "__main__":
    extracting_total_outs_per_batsman()
    runs_per_season()
    batting_first()
    batting_second()
    all_features()
