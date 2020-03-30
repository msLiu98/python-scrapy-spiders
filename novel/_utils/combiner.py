import os
import pandas as pd


def main():
    dir_chp = r'D:\Projects_Github\Projects_Scrapy\novel\chp_content'
    chps = os.listdir(dir_chp)
    df_tmp = pd.DataFrame()
    df_tmp['file_name'] = chps
    df_tmp['index'] = df_tmp['file_name'].map(lambda s: int(s.split('_')[0]))
    df_tmp = df_tmp.sort_values(by=['index'])
    f_all = open('../_txtFiles/大主宰.txt', 'a+', encoding='utf-8-sig')
    for i, row in df_tmp.iterrows():
        chp_p = os.path.join(dir_chp, row['file_name'])
        with open(chp_p, 'r', encoding='utf-8-sig') as f_tmp:
            ctn = f_tmp.read()
            f_all.write(ctn)
        # f_all.write('\n')
        print(row['file_name'], ' 录入！')


if __name__ == '__main__':
    main()
