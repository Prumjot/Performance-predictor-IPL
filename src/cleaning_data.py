import pandas as  pd
import glob



def cleaning_match(path):
    # reading with /t right now
    df = pd.read_csv(path,sep="/t")

    #extracting future columns from info
    # match_date = df.loc[4]#earlier 4
    # match_season = df.loc[3] #earlier 4
    # match_venue = df.loc[6]
    # match_toss = df.loc[8]
    # match_toss_decision = df.loc[9]
    # match_MOM = df.loc[10]
    # team_won = df.loc[16]
    # match_result_description = df.loc[17]''
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
    # all_ways_runs = [0,1,2,3,4,5,6,7,8,9] #number runs can be scored in a ball
    # i = 0
    # for run in all_ways_runs:
    #     if run in match_df.loc[i]:
    #         match_df= match_df[i:]
    #     else:
    #         i+=1
    return match_df
    #.to_csv('Data/Untitled_Folder/out1.csv')

def cleaning_replacing(path):
    '''takes the path to the folder,cleans and replaces existing
    path example  = 'Data/Untitled_Folder/'''
    for file in glob.glob(path+'*.csv'):
        df = cleaning_match(file)
        unique_id = (file.split('/')[-1]).split('.')[0]
        df['match_id']= unique_id
        df.rename(columns={'extras?':'extra'}, inplace=True)
        df.drop(['sec0','balls'], axis = 1, inplace = True)
        df.to_csv(file,index = False)

if __name__ == "__main__":
    cleaning_match()
    cleaning_replacing()
