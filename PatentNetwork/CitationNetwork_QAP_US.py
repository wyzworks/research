# Patent data retrieval query: (Urban air mobility OR UAM OR vertical takeoff and landing OR air navigation OR air control) NOT (air conditioning) NOT (air conditioner) NOT (국토) NOT (epoxy) NOT (공조) NOT (청소기) NOT (cleaner) AND (항공).TI,AB,TF,BT,CLA.
# Duplicates removed, patent only in active status collected

import pandas as pd 
import networkx as nx 
import sys 
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import rc 
from matplotlib import font_manager as fm 
from operator import itemgetter 
import itertools
from libs.qap import QAP
from libs.mrqap import MRQAP

plt.rcParams['font.family'] = 'NanumGothic'
# mpl.rcParams['axes.unicode_minus'] = False


data1 = pd.read_csv('./data/US/TextDown_20230802_pm101758_2500.csv', encoding = 'EUC-KR', sep=',')
data2 = pd.read_csv('./data/US/TextDown_20230802_pm102253_2500.csv', encoding = 'EUC-KR', sep=',')
data3 = pd.read_csv('./data/US/TextDown_20230803_pm101054_2500.csv', encoding = 'EUC-KR', sep=',')
data4 = pd.read_csv('./data/US/TextDown_20230803_pm101455_2500.csv', encoding = 'EUC-KR', sep=',')
data5 = pd.read_csv('./data/US/TextDown_20230804_pm063639_2500.csv', encoding = 'EUC-KR', sep=',')
data6 = pd.read_csv('./data/US/TextDown_20230804_pm064117_2500.csv', encoding = 'EUC-KR', sep=',')
data7 = pd.read_csv('./data/US/TextDown_20230805_pm024757_2500.csv', encoding = 'EUC-KR', sep=',')
data8 = pd.read_csv('./data/US/TextDown_20230805_pm025100_761.csv', encoding = 'EUC-KR', sep=',')

# concat all data sheets 
data = pd.concat([data1, data2, data3, data4, data5, data6, data7, data8], ignore_index = True )

# drop patent without any backward citations
data.drop(data[data['인용 문헌 수(B1)'] ==0].index, inplace = True)

# explode for patent having co-applicants 
# invent_firm_df = data['출원인'].str.split('|')
data['출원인'] = data['출원인'].str.split('|')  # 출원인 = firm name 
data = data.explode('출원인')
data['출원인'] = data['출원인'].str.replace(' ', '') 
# firm_list = data['출원인'].unique().tolist()
# print(firm_list)


# # 인용 번호만 포함 
# data = data.dropna(subset=['인용 문헌번호(B1)'])
# data['인용 문헌번호(B1)'] = data['인용 문헌번호(B1)'].str.split('|')
# data = data.explode('인용 문헌번호(B1)')

##### 심사관 인용번호 포함 ####
data['citenum'] = data.apply(lambda row: row['인용 문헌번호(B1)'] + '|' + row['심사관인용 문헌번호(FE)[KR,US,JP,EP]'] if pd.notna(row['심사관인용 문헌번호(FE)[KR,US,JP,EP]']) else row['인용 문헌번호(B1)'], axis = 1)
data['citenum'] = data['citenum'].str.replace(' ', '')
data['citenum'] = data['citenum'].str.replace('(BE)', '')
data['citenum'] = data['citenum'].str.replace('(미포함)', '')
data['citenum'] = data['citenum'].str.split('|')

data = data.explode('citenum')
print(data['citenum'].tail(10))
###########################

# match patent numbering for citation 
data['number'] = data['국가코드'].astype(str) + data['등록번호'].astype(str) + data['문헌종류 코드'].astype(str)

import re 
data['citeNumber'] = data['citenum']

### Data cleansing for patent numbering
data['citeNumber'] = data['citeNumber'].apply(lambda x: re.sub(r'\([^)]*\)', '', x)) # remove non-alphabet
data['citeNumber'] = data['citeNumber'].str.replace(r'^KR', '')
data['citeNumber'] = data['citeNumber'].apply(lambda x: re.sub(r'[A-Za-z]', '', x))
data['citeNumber'] = data['citeNumber'].str.replace(r'(A|B\d+)$', '', regex=True)

data['citeNumber'] = data['citenum'].str.replace(' ', '')
data['citeNumber'] = data['citenum'].str.replace('(BE)', '')
data['citeNumber'] = data['citenum'].str.replace('(미포함)', '')

data['citeNumber'] = data['인용 문헌번호(B1)'].str.replace(' ', '')
data['citeNumber'] = data['citeNumber'].str.replace('(BE)', '')
data['citeNumber'] = data['citeNumber'].str.replace('(미포함)', '')


# Create a new dataframe to store the firm citation counts
firm_citations = pd.DataFrame(columns=['source_firm', 'target_num', 'citation_count', 'application_date'])

# Iterate over the rows of the original dataframe
for _, row in data.iterrows():
    citenumber = row['citeNumber']
    source_firm = row['출원인']
    # Check if the cited patent number matches the patent number for a different firm
    matches = data[(data['citeNumber'] == citenumber) & (data['number'] != row['number'])]
    data = data.drop(matches.index)

    for _, match_row in matches.iterrows():
        # print(match_row['number'], match_row['citeNumber'])
        source_firm = match_row['출원인'] 
        source_num = match_row['number']
        target_num = match_row['citeNumber']
        date = match_row['출원일'].split('-')[0]    # in yearly basis 

        # print(source_firm, target_firm )

        # Check if there's an existing row with the same 'source_firm', 'target_num', and 'application_date'
        existing_row = firm_citations[(firm_citations['source_firm'] == source_firm) &
                              (firm_citations['target_num'] == target_num) &
                              (firm_citations['application_date'] == date)]

# If the row exists, increment the 'citation_count'
        if not existing_row.empty:
             firm_citations.loc[(firm_citations['source_firm'] == source_firm) &
                       (firm_citations['target_num'] == target_num) &
                       (firm_citations['application_date'] == date), 'citation_count'] += 1
        else:
            # If the row does not exist, add a new row
            new_row = {'source_firm': source_firm, 'target_num': target_num, 'citation_count': 1, 'application_date': date}
            new_row_df = pd.DataFrame([new_row])
            firm_citations = pd.concat([firm_citations, new_row_df], ignore_index=True)

    print(firm_citations.tail(20))

print('citation matrix generation complete')
print(firm_citations.shape)

# save generated citation matrix
firm_citations.to_csv('./data/US/UScitation_examine.csv', index = True)

### QAP Analysis Start ###

firm_citations = pd.read_csv('./data/UScitation_examine.csv', encoding = 'UTF-8', sep=',')

dfs_by_year = {}
for year in firm_citations['application_date'].unique():
    filtered_df = firm_citations[firm_citations['application_date'] == year]
    dfs_by_year[f'dataframe{year}'] = filtered_df

# year: 2022~1993

### Case3 ### 
# row: patent, col: firm 

adj_matrix_year = {}
dot_result = {}
revised_dfs_by_year = {}

num = 1

for year in range(2012, 2023):
    dfindex = f'dataframe{year}'
    dfindex_before = f'dataframe{year-1}'
    dfindex_next = f'dataframe{year+1}'

    revised_dfs_by_year[dfindex] = dfs_by_year[dfindex]
    # print(dfindex, revised_dfs_by_year[dfindex].shape)
    # print(dfindex, revised_dfs_by_year[dfindex].head(5))

for year in range(2012, 2022):
    dfindex = f'dataframe{year}'
    dfindex_next = f'dataframe{year+num}'
    df1 = revised_dfs_by_year[dfindex]
    df2 = revised_dfs_by_year[dfindex_next]
    df12 = pd.merge(df1, df2, on = 'source_firm', suffixes=('_df1', '_df2'), how = 'inner')

    adj_matrix_year[f'adj{year}_{year+num}'] = df12.pivot_table(index = ['source_firm'], columns ='target_num_df1', values = 'citation_count_df1', fill_value=0)
    adj_matrix_year[f'adj{year+num}_{year}'] = df12.pivot_table(index = ['source_firm'], columns ='target_num_df2', values = 'citation_count_df2', fill_value=0)

    # print('adj', year,'_', year+num, adj_matrix_year[f'adj{year}_{year+num}'].shape)
    # print('adj', year+num,'_', year, adj_matrix_year[f'adj{year+num}_{year}'].shape)
    # print(adj_matrix_year[f'adj{year}_{year+num}'])

    firm_list = df12['source_firm'].unique()
    # print(firm_list)

    dot_result[f'result{year}_{year+num}'] = np.dot(adj_matrix_year[f'adj{year}_{year+num}'], adj_matrix_year[f'adj{year}_{year+num}'].T)
    dot_result[f'result{year+num}_{year}'] = np.dot(adj_matrix_year[f'adj{year+num}_{year}'], adj_matrix_year[f'adj{year+num}_{year}'].T)

    # print('dot', year,'_', year+num, dot_result[f'result{year}_{year+num}'].shape)
    # print('dot', year+num,'_', year, dot_result[f'result{year+num}_{year}'].shape)

    # print(dot_result[f'result{year}_{year+num}'])
    # print(dot_result[f'result{year+num}_{year}'])

    # print(dot_result[f'result{year}_{year+num}'])

print(adj_matrix_year)
print('adj')
print(dot_result)
print('dot')

print('conversion completed')

avgbeta = []
for year in range(2012, 2023):
    X = dot_result[f'result{year}_{year+num}']
    Y = dot_result[f'result{year+num}_{year}']
    print(year)
    # print(X)
    # print(Y)
    qap = QAP(Y, X, 1000)
    qap.qap()
    qap.summary()
    qap.plot()
    dot_result[year] = qap.correlation(X, Y)[0]
    print('--------------')

# corr_value = []
from scipy.stats import pearsonr

for year in range(2006, 2022):
    X = dot_result[f'result{year}_{year+num}']
    Y = dot_result[f'result{year+num}_{year}']
    
    correlation_coefficient, p_value = pearsonr(X.flatten(), Y.flatten())
    plt.plot(year , correlation_coefficient, marker = 'o')
    print(year, correlation_coefficient, p_value)

plt.show()

# qap added 
for year in range(2012, 2022):
    X = dot_result[f'result{year}_{year+num}']
    Y = dot_result[f'result{year+num}_{year}']
    print(year)
    X1 = {'year': X}
    Y1 = {'next': Y}
    qap = QAP(Y1, X1, 1000)
    qap.qap()
    qap.summary()

print(timeline.head(50))

degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)

centrality = nx.degree_centrality(G)
sorted_centrality = sorted(centrality.items(), key=itemgetter(1), reverse=True)
top_10_centrality = sorted_centrality[:10]

for node, centrality_value in top_10_centrality:
    print(f"Node: {node}, Centrality: {centrality_value}")
