import pandas as pd
import numpy as np

    
class Test:
    def __init__(self, cap, margin, stoplos_per,exi, dataframe):
        self.capital = cap
        self.margin = margin
        self.stoplos_per = stoplos_per
        self.dataframe = dataframe
        self.exit_point_per = exi
######################################################
    def pricelimitHit(self):
        print("""
        ############################
        ############################
        ############################
        ######              ########
        ###### $$$$$$$$$$$$ ########
        ######              ########
        ############################
        ############################
        ############################
        """)
    def stoplossHit(self):
        print("""
        ############################
        ############################
        ############################
        ######              ########
        ###### STOPLOSS HIT ########
        ######              ########
        ############################
        ############################
        ############################
        """)

    def profit(self,value):
        print(f"######{value}######")
        
    def start(self,args):
        print(f"VVVVVVVVVVVVVVVVVVVVVVVVVVV\n{args[4]} Trade taken {args[0]}\nNumber of share:{args[1]}\ncapital :{args[2]}\nShare price:{args[3]}")
    def ending(self,args):
        print(f"{args[4]} Trade taken {args[0]}\nNumber of share:{args[1]}\ncapital :{args[2]}\nShare price:{args[3]}\n^^^^^^^^^^^^^^^^^^^^^^^^^^^")
######################################################
    def buy(self, value, flag, num_share, dif=0.0):
        global capital
        flag = flag
        buy_var = float(value) + dif
        if flag == (0,0):
            capital -= (num_share * buy_var)
        else:
            capital += (num_share * buy_var)

    def sell(self, value, flag, num_share, dif=0.0):
        global capital
        sell_var = float(value)
        flag = flag
        if flag == (0,0):
            capital -= (num_share * sell_var)

        else:
            capital += (num_share * sell_var)
##################################################################
   
    def te(self):
        global capital
        df = pd.DataFrame(self.dataframe)
        # fil = (df["Buy_Signal_Price"] == df["Close Price"]) | (df["Sell_Signal_Price"] == df["Close Price"])
        # length = len(df.loc[fil])
        # if length % 2 == 1:
        #     df.drop(df.loc[fil].tail(1).index, inplace=True)
        #     df.reset_index(inplace=True)
        print(df)
        capital = float(self.capital)
        
        stop_loss = float(self.stoplos_per)
        flag = (0,0)
        num_share = np.nan
        profit = 0
        live_profit = 0
        last_price = 0
        # last_price = float(df.loc[df[fil].head(1).index]["Buy_Signal_Price"])
        # if last_price is np.nan :
        #     last_price = df.loc[df[fil].head(1).index]["Sell_Signal_Price"]
        succes_Num = []
        # print('--->',last_price)
        exi = self.exit_point_per

        for i in range(len(df.index)):

            invest_mar = capital * float(self.margin)
            stop_price = -float(last_price * stop_loss)
            exit_price = float(last_price * exi)
            if flag == (1,1) :
                live_profit = float(df.loc[i]["Close Price"])- last_price
                if stop_price > live_profit or exit_price < live_profit:
                    self.sell(df.loc[i]["Close Price"],flag,num_share)
                    profit += ((float(df.loc[i]["Close Price"]) - last_price) * num_share)
                    flag =(0,0)
                    if stop_price > live_profit:
                        self.stoplossHit()
                    else:
                        self.pricelimitHit()
                    self.profit(profit)
                    self.ending([df.loc[i]['Date'],num_share,capital,df.loc[i]["Close Price"],"Sell"])
                    succes_Num.append(True if (last_price-float(df.loc[i]["Close Price"])) < 0 else False)
                    print(True if (last_price-float(df.loc[i]["Close Price"])) < 0 else False)
                    continue

            if flag == (0,1) :
                live_profit = last_price - float(df.loc[i]["Close Price"])
                if stop_price > live_profit or exit_price < live_profit:
                    dif = (last_price - (float(df.loc[i]["Close Price"])))
                    self.buy(last_price,flag,num_share,dif)
                    profit += ((last_price - (float(df.loc[i]["Close Price"]))) * num_share)
                    flag = (0, 0)
                    if stop_price > live_profit:
                        self.stoplossHit()
                    else:
                        self.pricelimitHit()
                    self.profit(profit)
                    self.ending([df.loc[i]['Date'],num_share,capital,df.loc[i]["Close Price"],"Buy"])
                    succes_Num.append(True if (float(df.loc[i]["Close Price"])-last_price) < 0 else False)
                    print(True if (float(df.loc[i]["Close Price"])-last_price) < 0 else False)
                    continue           
            
            if capital <= 0:
                print("######## TRADE ENDED ##########")
                break

            

######################################################################################################################################



            if df.loc[i]["Buy_Signal_Price"] == df.loc[i]["Close Price"]:

                if flag == (0,0):
                    num_share = invest_mar / float(df.loc[i]["Close Price"])
                    num_share = int(num_share)
                    self.buy(df.loc[i]["Close Price"], flag, num_share)
                    flag = (1,1)
                    last_price = float(df.loc[i]["Close Price"])
                    self.start((df.loc[i]["Date"],num_share,capital,last_price,"Buy"))
                elif flag == (0,1):
                    dif = (last_price - (float(df.loc[i]["Close Price"])))
                    self.buy(last_price, flag, num_share, dif)
                    profit += ((last_price - (float(df.loc[i]["Close Price"]))) * num_share)
                    flag = (0,0)
                    self.ending([df.loc[i]['Date'],num_share,capital,df.loc[i]["Close Price"],"Buy"])
                    succes_Num.append(True if (float(df.loc[i]["Close Price"])-last_price) < 0 else False)
                    print(True if (float(df.loc[i]["Close Price"])-last_price) < 0 else False)


            if df.loc[i]["Sell_Signal_Price"] == df.loc[i]["Close Price"]:
                if flag == (0,0):
                    num_share = invest_mar / float(df.loc[i]["Close Price"])
                    num_share = int(num_share)
                    self.sell(df.loc[i]["Close Price"], flag, num_share)
                    flag = (0,1)
                    last_price = float(df.loc[i]["Close Price"])
                    self.start((df.loc[i]["Date"],num_share,capital,last_price,"Sell"))

                elif flag == (1 , 1):
                    # dif = float(df.loc[i]["Close Price"]) - last_price
                    self.sell(df.loc[i]["Close Price"], flag, num_share, )
                    profit += ((float(df.loc[i]["Close Price"]) - last_price) * num_share)
                    flag = (0,0)
                    self.ending([df.loc[i]['Date'],num_share,capital,df.loc[i]["Close Price"],"Sell"])                    
                    succes_Num.append(True if (last_price-float(df.loc[i]["Close Price"])) < 0 else False)
                    print(True if (last_price-float(df.loc[i]["Close Price"])) < 0 else False)
        print(f"profit is {profit}\ncapital is {capital}")

        print('------>', succes_Num.count(True) / len(succes_Num))


df = pd.read_csv("test_df.csv")
te = Test(10000,1,0.04,0.1,df)
te.te()