import os


def main():
    chpDir = r'..\data'
    chpFiles = os.listdir(chpDir)
    chpDict = {
        int(i.split('_')[0]): i for i in chpFiles
    }
    chpDict = sorted(chpDict.items(), key=lambda i: i[0])
    fpTo = r'..\_txtFiles\斗破苍穹.txt'
    f_all = open(fpTo, 'a+', encoding='utf-8-sig')
    for _, chp in chpDict:
        with open(os.path.join(chpDir, chp), 'r', encoding='utf-8-sig') as f_tmp:
            ctn = f_tmp.read()
            f_all.write(ctn)
    f_all.close()


if __name__ == '__main__':
    main()