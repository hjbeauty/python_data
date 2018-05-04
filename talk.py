import pandas as pd
import numpy as np
#import datetime

# ===Simple analysis of kakaotalk chat ===

### ideas ### 
#user interface: open할 파일명, oo와의 대화, 분석결과 etc.
#use 'find' method to get # of certain word(or emoji)
#단체카톡: differently .
#dataframe에 저장
#차트 그려주기

# !! NEED TO MAKE IN MODULE 

if __name__ == '__main__':
    #hours = []
    hour = ''
    # for i in range(24):
    #     hours.append(i)
    df = pd.DataFrame()
    with open('talk_short.txt', 'r', encoding='utf-8') as file: 
        line = file.readline()
        count = 1
        while line != '':
            line = file.readline()
            if(line == ''):
                break
            if(line != '\n' and line[0] == '-'):
                date = line.strip('-') #뒷부분 strip이 잘 안됨 (issue#1)
                year = date.split(' ')[1]
                month = date.split(' ')[2]
                day = date.split(' ')[3]
                date = year+month+day
            if(line != '\n' and line[0] == '['):
                linelist = line.split(' ')
                prev_hour = hour
                #time = linelist[1] + linelist[2]
                hour = int(linelist[2].split(':')[0]) if (linelist[1][1:] == '오전') else int(linelist[2].split(':')[0])+12
                if(prev_hour == hour):
                    count +=1
                else:
                    df.loc[date, hour] = count
                    count = 1
        print(df)
        df.to_csv('talktalk', sep='\t', encoding='utf-8')
