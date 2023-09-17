class Trades():
    def __init__(self):
        self.datas = []
        self.symbols = []
        

    def add_data(self, data_df):
        self.datas.append(data_df)
        self.symbols.append(data_df[0]['Symbol'])



