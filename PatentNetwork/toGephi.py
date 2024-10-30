import pandas as pd 
import networkx as nx 
import sys 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib
from matplotlib import rc 
from matplotlib import font_manager as fm 
from operator import itemgetter 
import itertools

firm_citations = pd.read_csv('./data/KR/KRcitation_examine.csv', encoding = 'UTF-8', sep=',')

dfs_by_year = {}
for year in firm_citations['application_date'].unique():
    filtered_df = firm_citations[firm_citations['application_date'] == year]
    dfs_by_year[f'dataframe{year}'] = filtered_df

dot_result = {}
pivot = {}
firm_list = {}

for year in range (2012, 2023):
    pivot[f'dataframe{year}'] = dfs_by_year[f'dataframe{year}'].pivot_table(index = ['source_firm'], columns ='target_num', values = 'citation_count', fill_value=0, sort = False)
    # print(dfs_by_year[f'dataframe{year}'])
    print(pivot[f'dataframe{year}'])
    firm_list[f'dataframe{year}'] = dfs_by_year[f'dataframe{year}']['source_firm'].unique().tolist()
    # print(firm_list[f'dataframe{year}'])
    dot_result[f'dataframe{year}'] = np.dot(pivot[f'dataframe{year}'], pivot[f'dataframe{year}'].T)
    print(year)
    print(dot_result[f'dataframe{year}'])
    print(dot_result[f'dataframe{year}'].shape)
    print(1)

node_centrality = pd.DataFrame(columns=['firm', 'degree centrality', 'betweenness centrality', 'eigenvector centrality', 'closeness centrality', 'year'])


####################
# for all network 
#####################
# G = nx.Graph() 

for year, dot_product_matrix in dot_result.items():
    G = nx.Graph() 

    plt.close()
    plt.figure(figsize=(20, 20))
    n = dot_product_matrix.shape[0]
    
    for i in range(n):
        for j in range(n):
            if dot_product_matrix[i][j] != 0:
            # if dot_product_matrix[i][j] != 0: # disable selflink 
                # G.add_edge(f"Node_{i}", f"Node_{j}", weight=dot_product_matrix[i][j])
                source_firm_i = firm_list[f'{year}'][i]
                source_firm_j = firm_list[f'{year}'][j]
                G.add_edge(source_firm_i, source_firm_j, weight=dot_product_matrix[i][j])

    pos = nx.spring_layout(G)
    edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}  # Extract edge weights
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=100)

    # Draw edges
    nx.draw_networkx_edges(G, pos)

    # Draw edge labels
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    node_labels = {source_firm: source_firm for source_firm in firm_list[f'{year}']}
    # nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)

    ## Display the plot
    # plt.title("US Network in Year {}".format(year))
    # plt.axis("off")
    # plt.show()
    
    # get centrality
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality_numpy(G)
    closeness_centrality = nx.closeness_centrality(G)
    clustering_coefficient = nx.clustering(G)
   

    for node in G.nodes():
        new_row = {'firm': node, 'degree centrality': degree_centrality[node], 'betweenness centrality': betweenness_centrality[node], 'eigenvector centrality': eigenvector_centrality[node], 'closeness centrality': closeness_centrality[node], 'year': year.split('dataframe')[1]}
        new_row_df = pd.DataFrame([new_row])
        node_centrality = pd.concat([node_centrality, new_row_df], ignore_index=True)
    # print(node_centrality)
        
    # nx.write_gexf(G, './Gephi/KR network_dot {}.gexf'.format(year))
    
# nx.write_gexf(G, './Gephi/KR cumulative_dot {}.gexf'.format(year))

node_centrality.to_csv('./data/KR Centrality_dot.csv')