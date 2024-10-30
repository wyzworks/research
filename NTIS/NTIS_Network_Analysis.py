# The intention of this sub-project is to analyze network dynamics between government, firms, and technology in South Korea. 
# Using a database of R&D governmental funding, on firm, and their project details 
# I hypothesized the network of firm-government would change due to technology innovation
# However, the R&D network remained surprising stability over a decade,
# but an abrupt change occurred in 2012 and 2016, when the presidential election was held. 

import networkx as nx 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

data = pd.read_csv(f'./data/2010년사업과제정보.csv', encoding = 'UTF-8', sep = ',')	# The data includes funding government department, governmental budget, R&D firm, R&D project name, R&D technology category code, ... 
# print(data.columns)

pd.set_option('display.max_seq_items', None)

for year in range (2011, 2023):
    df = pd.read_csv(f'./data/{year}년사업과제정보.csv', encoding = 'UTF-8', sep = ',')
    data = pd.concat([data, df])

# Group by '사업_부처명(Funding Government department)' '과제수행기관명(firm name)' and '중점과학기술분류코드_대(Tech code)', '제출년도(year)', then count occurrences
co_occurrence = data.groupby(['사업_부처명', '과제수행기관명', '제출년도']).size().reset_index(name='count')
# co_occurrence = data.groupby(['과제수행기관명', '중점과학기술분류코드_대', '제출년도']).size().reset_index(name='count') # Test for each combination of 과제수행기관명, 기준년도명 과학기술표준분류1-중, 사업_부처명

print(co_occurrence)

co_matrix = {}
adj_matrix = {}
# Create a co-occurrence matrix
for year in range(2010, 2023):
    co_matrix[year] = co_occurrence[co_occurrence['제출년도']==year].pivot(index='과제수행기관명', columns='사업_부처명', values='count').fillna(0) # test for each combination of 과제수행기관명, '연구수행주체명', 기준년도명


all_columns = pd.Index([])
for year in range(2010, 2023):
    all_columns = all_columns.union(co_matrix[year].columns)
for year in range(2010, 2023):
    co_matrix[year] = co_matrix[year].reindex(columns=all_columns, fill_value=0)
    adj_matrix[year] = np.dot(co_matrix[year].T, co_matrix[year])	# convert 2-mode into 1-mode
    print(adj_matrix[year])

# Draw network graph in yearly dynamics
for year in range(2010, 2023):
    
    G = nx.from_numpy_array(adj_matrix[year])
    nodes_no_edges = [node for node, degree in G.degree() if degree == 0]
    G.remove_nodes_from(nodes_no_edges)
    nx.draw(G, with_labels = True, pos = nx.spring_layout(G))
    nx.write_gexf(G, f'./gephi/firm-gov_{year}.gexf')
    plt.show()


#### if required, exclude firms that occur occasionally by merging yearly data ####

# for year in range(2013, 2022):
#     df_merge = pd.merge(co_matrix[year], co_matrix[year+1], on='과제수행기관명', how = 'inner')
#     adj_matrix[year] = np.dot(df_merge.T, df_merge)
#     print(year)
#     print(adj_matrix[year].shape)


# Calculate yearly network matrix correlation 
from scipy import stats
for year in range(2010, 2022):
    print(year, stats.pearsonr(adj_matrix[year].flatten(), adj_matrix[year+1].flatten())[0])
    # print(np.dot(adj_matrix[year], adj_matrix[year+1])/(np.linalg.norm(adj_matrix[year])*np.linalg.norm(adj_matrix[year+1])))

