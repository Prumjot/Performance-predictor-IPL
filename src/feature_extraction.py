
import pandas as pd


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
    df= (df.groupby(['batsman_striker','match_id']).sum()).reset_index()
    df['innings']=1
    df_sum = df.pivot_table(index='batsman_striker',values=['runs_scored', 'innings', 'ball'],aggfunc=sum)
    df_sum = df_sum.reset_index()
    #higest score for player
    df_max = df.pivot_table(index='batsman_striker',values=['runs_scored'],aggfunc=max)
    df_max = df_max.reset_index()
    df_merged = df_sum.merge(df_1, on ='batsman_striker').merge(df_max, on='batsman_striker')
    df_merged.rename(columns={'runs_scored_x':'runs_scored',' runs_scored_y':'highest_score'}, inplace =True)
    return df_merged

def average_and_strike_rate(df):
    df['Average'] = round(df.runs_scored / df.total_outs,2)
    df['strike_rate'] = round((df.runs_scored/df.ball)*100,2)
    return df

def all_features(df):
    df = runs_per_season(df)
    df = average_and_strike_rate(df)
    return df

if __name__ == "__main__":
    extracting_total_outs_per_batsman()
    runs_per_season()
    all_features()
