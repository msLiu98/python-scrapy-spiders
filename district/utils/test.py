import pandas as pd

if __name__ == '__main__':
    dfTmp = pd.DataFrame({'1': [1, 2, 3], '2': [3, 4, 5]})
    dfTmp.to_csv(r'..\data\test.csv', mode='a+')
