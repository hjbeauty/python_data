# -*- coding: utf-8 -*-
#
# =====Simple analysis of kakaotalk chat =====
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Mobile(IOS)로 내보낸 대화내용을 dataframe에 넣기
def ios_parse_to_df(file_name):
    hours = []
    for i in range(24):
         hours.append(i)
    hour = ''
    df = pd.DataFrame(columns=hours)
    print('ios')
    return df

# PC version으로 내보낸 대화내용을 dataframe에 넣기
def pc_parse_to_df(file_name):
    hours = []
    for i in range(24):
         hours.append(i)
    hour = ''
    df = pd.DataFrame(columns=hours)
    with open(file_name, 'r', encoding='utf-8') as file: 
        line = file.readline()
        count = 1
        while line != '':
            line = file.readline()
            if(line == ''):
                break
            if(line != '\n' and line[0] == '-'):
                date = line.strip('-') #뒷부분 strip이 잘 안됨 (issue#1)
                year = date.split(' ')[1][:-1]
                month = date.split(' ')[2][:-1]
                day = date.split(' ')[3][:-1]
                date = year+'-'+month+'-'+day
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
        df = df.fillna(0)
        return df
        # df.to_csv('talktalk', sep='\t', encoding='utf-8')
    
# Mobile(Android) 로 내보낸 대화내용을 dataframe에 넣기 
def android_parse_to_df(file_name):
    print('android')
    hours = []
    for i in range(24):
         hours.append(i)
    df = pd.DataFrame(columns=hours)
    return df

# 차트 표현하기(plot) _ 시간대별/일별 은 매개변수로 넣기
def visualize(df, file_name):
    fig = plt.figure()
    df.mean().plot(kind='bar')
    new_file_name = file_name[:-4] + '.png'
    fig.savefig(new_file_name)
    # df.to_excel('test.xlsx', sheet_name='Sheet1' )
    print(new_file_name + '으로 저장되었습니다.\n')

# 1. 시간대별 사용량
def show_time_usage(file_name, file_ver):
    if(file_ver.upper() == 'PC'):
        df = pc_parse_to_df(file_name)
        print(df.tail())
    elif(file_ver.upper() == 'IOS'):
        df = ios_parse_to_df(file_name)
    else:
        df = android_parse_to_df(file_name)
    visualize(df, file_name)


# 2. 일별 사용량
def show_day_usage(file_name, file_ver):
    print('show time_usage')

# 3. 특정 단어를 입력받아, 전체 대화내용 중에서 단어의 개수(사용자별) 알려주기
# 아직 형태소분석이 안되서 한글자 밖에 못함 ㅜㅜ 
# total count까지만 함 / 사용자별 count dictionary에 저장해야함
def count_word(file_name):
    find_word = input('찾고싶은 단어가 무엇인가요? \n')
    count = 0
    with open(file_name, 'r', encoding='utf-8') as file: 
        for line in file:
            for word in line:
                if(word == find_word):
                    count+=1
        print("count:",count)

# 사용자 입력 받기
def get_user_input(file_name='',file_ver='', init=0):
    if(init == 0):
        print("========================")
        print(' ▶▶  kakaotalk 분석기 :-) ◀◀ \n')
        file_name = input('내보내기 한 대화 파일이름을 입력해주세요.(파일이름.txt)\n')
        file_ver = input('어디에서 내보내기 했나요? (PC/IOS/Android)\n')
    print('-----------MENU-------------')
    print('1. 시간대별 카톡 사용량을 보고싶어요')
    print('2. 일별 카톡사용량을 보고싶어요')
    print('3. 누가 얼마나 OO 단어/이모티콘을 쓰는지 알고싶어요')
    print('4. 종료')
    print('-----------------------------')
    user_input = input('숫자를 입력하세요 :')
    print(' ')
    return file_name, file_ver, user_input

# Main
if __name__ == '__main__':
    file_name, file_ver, user_input = get_user_input()
    while(True):
        if(user_input == '1'):
            show_time_usage(file_name, file_ver)
        elif (user_input == '2'):  
            show_day_usage(file_name, file_ver)
        elif (user_input == '3'):
            count_word(file_name)
        else:
            answer = input('정말 그만할래요? (y/n) : ')
            if(answer == 'y'):
                print('============종료 ============')
                break
        filename, file_ver, user_input = get_user_input(file_name, file_ver, 1)