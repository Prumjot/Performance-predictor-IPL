import pandas as  pd
import glob
import numpy as np




def cleaning_match(path):
    df = pd.read_csv(path,sep="/t")


    if (df.loc[9][0]).split(',')[1] =='neutralvenue':
        date = (df.loc[4][0]).split(',')[2]
        season = (df.loc[3][0]).split('season,')[1]
        match_venue = (df.loc[7][0]).split(',')[2]
        match_toss = (df.loc[10][0]).split('toss_winner,')[1]
        match_toss_decision = (df.loc[11][0]).split('toss_decision,')[1]
        match_MOM = (df.loc[12][0]).split('player_of_match,')[1]
        if df.loc[18][0].split(',')[0]== 'winner':
            team_won = df.loc[18][0].split(',')[2]
        else:
            team_won = df.loc[17][0].split(',')[2]




        #(match_result_description = df.loc[18][0])
        #team_won  = team_won.split('winner,')[1]
        #match_result_description  = match_result_description.split('info,')[1]

        #innings = df[21:]

    elif (df.loc[8][0]).split(',')[1] =='neutralvenue':
        date = (df.loc[4][0]).split(',')[2]
        season = (df.loc[3][0]).split('season,')[1]
        match_venue = (df.loc[6][0]).split(',')[2]
        match_toss = (df.loc[9][0]).split('toss_winner,')[1]
        match_toss_decision = (df.loc[10][0]).split('toss_decision,')[1]
        match_MOM = (df.loc[11][0]).split('player_of_match,')[1]
        if df.loc[18][0].split(',')[0]== 'winner':
            team_won = df.loc[18][0].split(',')[1]
        else:
            team_won = df.loc[17][0].split(',')[1]




        #(match_result_description = df.loc[18][0])
        #team_won  = team_won.split('winner,')[1]
        #match_result_description  = match_result_description.split('info,')[1]


        #innings = df[19:]


    elif (df.loc[6][0]).split(',')[1] =='match_number':

        match_date = df.loc[4]
        match_season = df.loc[3]
        match_venue = df.loc[7]
        match_toss = df.loc[9]
        match_toss_decision = df.loc[10]
        match_MOM = df.loc[11]
        team_won = df.loc[17]
        match_result_description = df.loc[18]

        #step2
        date = match_date[0]
        season = match_season[0]
        match_venue = match_venue[0]
        match_toss = match_toss[0]
        match_toss_decision = match_toss_decision[0]
        MOM = match_MOM[0]
        team_won = team_won[0]
        match_result_description = match_result_description[0]

        #step3
        date  = date.split(',')[2]
        season  = season.split('season,')[1]
        match_venue  = match_venue.split(',')[2]
        match_toss  = match_toss.split('toss_winner,')[1]
        match_toss_decision  = match_toss_decision.split('toss_decision,')[1]
        if  MOM.split('player_of_match,')[0] == 'player_of_match':
            player_of_the_match  = MOM.split('player_of_match,')[1]
        else:
            player_of_match = ''
        team_won  = team_won.split(',')[2]
        #match_result_description  = match_result_description.split('info,')[1]

        if df.loc[18][0].split(',')[0]== 'ball':
            pass
            #innings = df[18:]
        else:
            pass    #innings = df[19:]


    elif ((df.loc[4][0]).split(',')[0]) =='date' and ((df.loc[5][0]).split(',')[0]) =='date':
        match_date = df.loc[5]
        match_season = df.loc[3]
        match_venue = df.loc[7]#one lower
        match_toss = df.loc[9]
        match_toss_decision = df.loc[10]
        match_MOM = df.loc[11]
        team_won = df.loc[17]
        match_result_description = df.loc[18]

        #step2
        date = match_date[0]
        season = match_season[0]
        match_venue = match_venue[0]
        match_toss = match_toss[0]
        match_toss_decision = match_toss_decision[0]
        MOM = match_MOM[0]
        team_won = team_won[0]
        match_result_description = match_result_description[0]

        #step3
        print(date)
        date  = date.split(',')[2]
        season  = season.split('season,')[1]
        match_venue  = match_venue.split(',')[2]
        match_toss  = match_toss.split('toss_winner,')[1]
        match_toss_decision  = match_toss_decision.split('toss_decision,')[1]
        player_of_the_match  = MOM.split('player_of_match,')[1]
        team_won  = team_won.split(',')[2]
        #match_result_description  = match_result_description.split('info,')[1]

        #innings = df[19:]



    else:

        match_date = df.loc[4]#earlier 4
        match_season = df.loc[3] #earlier 4
        match_venue = df.loc[6]
        match_toss = df.loc[8]
        match_toss_decision = df.loc[9]
        match_MOM = df.loc[10]
        team_won = df.loc[16]
        match_result_description = df.loc[17]
    #step2
        date = match_date[0]
        season = match_season[0]
        match_venue = match_venue[0]
        match_toss = match_toss[0]
        match_toss_decision = match_toss_decision[0]
        MOM = match_MOM[0]
        team_won = team_won[0]
        match_result_description = match_result_description[0]

        #step3

        date  = date.split(',')[2]
        season  = season.split('season,')[1]
        match_venue  = match_venue.split(',')[2]
        match_toss  = match_toss.split('toss_winner,')[1]
        match_toss_decision  = match_toss_decision.split('toss_decision,')[1]
        player_of_the_match  = MOM.split('player_of_match,')[1]
        team_won  = team_won.split(',')[2]
        #match_result_description  = match_result_description.split('info,')[1]

        #innings = df[18:]


    #add columns to data frame
    i= 0
    while (df.loc[i][0]).split(',')[0]== 'info':
        i+=1
    innings = df[i:]

    match_df= innings['version,1.3.0'].str.split(',', expand = True).add_prefix('sec')
    match_df.rename(columns = {'sec1': 'balls', 'sec2':'over_ball',
                            'sec3':'batting_team', 'sec4':'batsman_striker',
                            'sec5':'batsman_non_striker', 'sec6':'bowler',
                            'sec7':'runs_scored', 'sec8':'extras?',
                            'sec9':'dissmisal_type','sec10':'batsman_out'},
                            inplace = True)


    match_df['match_venue']= match_venue
    match_df['match_toss_winner']= match_toss
    match_df['match_toss_decision']= match_toss_decision
    #match_df['player_of_the_match']= player_of_the_match
    match_df['team_won']= team_won
    #match_df['match_result_description']= match_result_description
    match_df['date'] = date
    match_df['season']= season

    return match_df





def cleaning_replacing(path):
    '''takes the path to the folder,cleans and replaces existing
    path example  = 'Data/Untitled_Folder/'''
    for file in glob.glob(path+'*.csv'):
        df = cleaning_match(file)
        unique_id = (file.split('/')[-1]).split('.')[0]
        df['match_id']= unique_id
        df.rename(columns={'extras?':'extra'}, inplace=True)
        df.drop(['sec0','balls'], axis = 1, inplace = True)
#making all season dates as string, because some are string, some are int
        df['season'] = df['season'].astype(str)
        df.season[df.season == '2007/08'] = '2008'
        df.season[df.season == '2009/10'] = '2010'

#cleaning the names of the venue, some venues have extra " in the front of the string
        clean_venue = []
        for value in df['match_venue'].values:
            if value[0] =='"':
                value = value.lstrip('"')
                clean_venue.append(value)
            else:
                clean_venue.append(value)
            pass
        df['match_venue'] = clean_venue


        bat = df['match_toss_winner']==df['batting_team']
        df['inning']= bat
        if df.match_toss_decision.iloc[0] == 'bat':
            df.inning.loc[df.inning == True] = '1'
            df.inning.loc[df.inning == False] = '2'
        else:
            df.inning.loc[df.inning == False] = '1'
            df.inning.loc[df.inning == True] = '2'



        df.to_csv(file,index = False)

def concating_dataframes(path):
    '''input: path to the folder with csv files
        output: concatenated all the files in one'''

    allFiles = glob.glob(path + "/*.csv")
    frame = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_,index_col=None, header=0)
        list_.append(df)
    frame = pd.concat(list_)
    return frame

if __name__ == "__main__":
    cleaning_match()
    cleaning_replacing()
    concating_dataframes()
