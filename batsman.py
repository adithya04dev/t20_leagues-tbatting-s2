import pandas as pd
import numpy as np
import pickle
# df=pd.read_csv("C:/Users/adith/Documents/ds/t20_leagues/ball_ball_data/set2_player_info_t20_combined_batting_bowling_style.csv")


class Batsmant():

    def __init__(self,deliveries_df):

        self.df = deliveries_df.copy()
        self.players = self.df['batter'].unique()
        self.teams = self.df['BattingTeam'].unique()
        self.pac=['LAP','RAP']
        self.spi=['OB','LB','SLA','LWS']
        self.bowt=["Pace","Spin"]
        self.bowty={"Pace":["LAP","RAP"],"Spin":["OB","LB","SLA","LWS"]}
        self.league=self.df['LeagueName'].unique()


        self.dic={1:[i for i in range(0,6)],2:[i for i in range(6,11)],3:[i for i in range(11,16)],4:[i for i in range(16,21)]}


    def create_df(self,leagues,team,overs,BowlingType,Season):
            batsman_df = pd.DataFrame(columns=['team_name','total_runs','outs','balls_played','average_runs','strike_rate','bpercent','dpercent'])

            run = int(self.df.loc[(self.df["BattingTeam"] == team) & (self.df["LeagueName"].isin(leagues))  & (self.df["BowlingType"].isin(BowlingType)) & (self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))].batsman_run.sum())
            run+= int(self.df.loc[(self.df["BattingTeam"] == team)  & (self.df["LeagueName"].isin(leagues))  & (self.df["BowlingType"].isin(BowlingType)) & (self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))].Extras_Run.sum())

            balls=len(self.df.loc[(self.df['extra_type']!="wides") & (self.df["LeagueName"].isin(leagues))  & (self.df["BowlingType"].isin(BowlingType)) & (self.df["overs"].isin(overs))  & (self.df["Season"].isin(Season)) & (self.df['extra_type']!="noballs") & (self.df['BattingTeam'] == team) ] )
            out = len(   self.df.loc[(self.df["BattingTeam"] == team) & (self.df["LeagueName"].isin(leagues)) & (self.df["player_out"].notnull()) & (self.df["BowlingType"].isin(BowlingType))   & (self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))])
            boundary = len(self.df.loc[(self.df["BattingTeam"] == team) & (self.df["LeagueName"].isin(leagues))  & ((self.df["batsman_run"] == 4) | (self.df["batsman_run"] == 6)  ) & (self.df["BowlingType"].isin(BowlingType)) & (self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))])
            dots=len(self.df.loc[(self.df["BattingTeam"] == team) & (self.df["LeagueName"].isin(leagues))  & (self.df["Extras_Run"]==0) & (self.df["batsman_run"]==0) & (self.df["BowlingType"].isin(BowlingType)) & (self.df["overs"].isin(overs))  & (self.df["Season"].isin(Season))  ] )



            avg_run=(run/out) if out!=0 else np.inf
            strk_rate=(run * 100)/balls if balls!=0 else 0
            dpercent=(dots/balls)*100 if balls!=0 else 0
            bpercent=(boundary/balls) if balls!=0 else 0

            df2 = {'team_name':team,'total_runs': int(run), 'outs':int(out),'balls_played': int(balls),'average_runs':avg_run,'strike_rate': strk_rate,'bpercent':bpercent,'dpercent':dpercent}
            batsman_df =pd.concat([batsman_df ,pd.DataFrame(df2, index=[0])],ignore_index =True)
            return batsman_df
    def calculate(self,leagues,name,phase,bow,Season):
        self.ovdf = self.create_df(leagues,name,[i for i in range(0,21)],self.pac+self.spi,Season)
        self.ovsdf = self.create_df(leagues,name,[i for i in range(0,21)],self.spi,Season,)
        self.ovpdf = self.create_df(leagues,name,[i for i in range(0,21)],self.pac,Season)


        self.ovdf["Phase"]="Overall"
        self.ovsdf["Phase"]="Overall-Spin"
        self.ovpdf["Phase"]="Overall-Pace"
        self.ovdf=pd.concat([self.ovdf,self.ovpdf,self.ovsdf],ignore_index=True)

        ph1={1:'Powerplay',2:'Middle1',3:'Middle2',4:'Slog'}
        self.phasewise_df = pd.DataFrame(columns=['team_name', 'total_runs', 'outs', 'balls_played', 'average_runs', 'strike_rate','BowlingType','phase','bpercent','dpercent'])



        bow1=[]
        for bo in bow:
                bow1=bow1+self.bowty[bo]
        overs1=[]
        for ph in phase:

            overs1+=self.dic[ph]
        self.comb_df=self.create_df(leagues,name,overs1,bow1,Season)


        for ph in phase:
            overs1=self.dic[ph]
            for bo in bow1:
                      
                d1=self.create_df(leagues,name, overs1, [bo], Season)
                d1["BowlingType"]=bo
                d1["phase"]=ph1[ph]
                self.phasewise_df = pd.concat([self.phasewise_df ,pd.DataFrame(d1, index=[0])], ignore_index=True)

            
        return self.phasewise_df

    def overall(self):
        return self.ovdf    
    def combined(self):
        return self.comb_df    

# bat=Batsmant(df)
# #result=bat.calculate('H Klaasen',[1,2,3],["Spin"],[2023]) 
# result=bat.calculate(['SA20'],'Sunrisers Eastern Cape',[1,2,3],["Pace","Spin"],[2023]) 
# #print(result)
# result1=bat.overall()
# print(result1['strike_rate'])
# #print(result['balls_played'])


# with open('C:/Users/adith/Documents/ds/t20_leagues/set_2_all_t20_app/teams/batting/batting1.pkl', 'wb') as f:
#     pickle.dump(bat, f)