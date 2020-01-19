# -*- coding: utf-8 -*-
"""PlottingMapsWithEdges.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QNcmjmvMpfweWnzouuvva7GJzMt61a8p
"""

#pip install python-igraph

#pip install geopandas

"""# Understanding Geopandas"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline 
## It is to avoiding to open an extra window showing maps
import geopandas as gpd

"""##Data Source

http://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2018/UFs/
"""

sp = gpd.read_file('35MUE250GC_SIR.shp')

type(sp)

sp.plot()

sp.plot(color='white', edgecolor='black', figsize=(15,8))

"""##Creating a new shapefile"""

sp = sp[sp['NM_MUNICIP'] == 'SÃO JOSÉ DOS CAMPOS']
sp.shape

sp

sp.plot(color='orange', edgecolor='black', figsize=(15,8))

"""##Saving Data"""

import os

dir = '../01.Dados/Mapas/SP-MUNIC'
if not os.path.exists(dir): 
    os.makedirs(dir)

sp.to_file(dir + '/SP-MUNIC.shp')

sjc = gpd.read_file(dir + '/SP-MUNIC.shp')

sjc.plot(color='orange', edgecolor='black', figsize=(15,8))

"""##Transforming DataFrame into GeoDataFrame"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import pandas as pd
import geopandas as gpd

data = pd.read_csv("coordinates_zones.csv", encoding = "ISO-8859-1")

data

"""##Creating geometry column"""

from shapely.geometry import Point

x =  zip(data.XCOORD, data.YCOORD)
x

geometry = [Point(x) for x in zip(data.XCOORD, data.YCOORD)]
geometry

crs = {'proj': 'latlong', 'ellps': 'WGS84', 'datum': 'WGS84', 'no_defs': True}

geo_data = gpd.GeoDataFrame(data, crs = crs, geometry = geometry)

geo_data

import os

dir = '../01.Dados/Mapas/SP-DATASET'
if not os.path.exists(dir):
    os.makedirs(dir)

geo_data.to_file(dir + '/DATASET.shp')

geo_data.plot(figsize=(15,8), alpha=0.2)

"""#Modifying CRS from Files

- https://www.lapig.iesa.ufg.br/lapig/cursos_online/gvsig/a_projeo_utm_no_brasil.html

   - http://www.spatialreference.org/
"""

import geopandas as gpd

sjc = gpd.read_file('../01.Dados/Mapas/SP-MUNIC/SP-MUNIC.shp')
geo_data = gpd.read_file('../01.Dados/Mapas/SP-DATASET/DATASET.shp')

sjc

sjc.crs

geo_data.crs

"""###You should search in this website about which one is the most suitable for your area:
[link text](https://)www.spatialreference.org/

###So, try to modify your crs:
"""

sjc = sjc.to_crs('+proj=utm +zone=23 +south +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=km +no_defs')

geo_data = geo_data.to_crs('+proj=utm +zone=23 +south +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=km +no_defs')

sjc.crs

geo_data.crs

sjc.to_file('../01.Dados/Mapas/SP-MUNIC/SP-MUNIC.shp')
geo_data.to_file('../01.Dados/Mapas/SP-DATASET/DATASET.shp')

sjc2 = gpd.read_file('../01.Dados/Mapas/SP-MUNIC/SP-MUNIC.shp')
geo_data2 = gpd.read_file('../01.Dados/Mapas/SP-DATASET/DATASET.shp')

sjc2.crs

sjc2

geo_data2

"""##Plotting layers, one over another"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import geopandas as gpd

sjc = gpd.read_file('../01.Dados/Mapas/SP-MUNIC/SP-MUNIC.shp')
geo_data = gpd.read_file('../01.Dados/Mapas/SP-DATASET/DATASET.shp')

sjc.crs

geo_data.crs

base = sjc.plot(color='black', edgecolor='black', figsize=(15,8))
base

base = sjc.plot(color='orange', edgecolor='orange', figsize=(15,8))
geo_data.plot(ax=base, figsize=(15,8), color='black', alpha=0.2)

"""##Filtering points, only which one inside the base should be plotted"""

sjc.iloc[0].geometry

geo_data.iloc[0].geometry

geo_data.iloc[0].geometry.within(sjc.iloc[0].geometry)

sjc.iloc[0].geometry.contains(geo_data.iloc[0].geometry)

geo_data['geometry'].within(sjc.iloc[0].geometry)

sample_geo_data = geo_data.iloc[0:12]
sample_geo_data

sample = geo_data.iloc[:12]
base = sjc.plot(color='white', edgecolor='black', figsize=(15,8))
sample.plot(ax=base, figsize=(15,8), alpha=1)

before = geo_data.shape[0]
before

geo_data = geo_data[geo_data['geometry'].within(sjc.iloc[0].geometry)]

geo_data

after = geo_data.shape[0]

before-after

base = sjc.plot(color='white', edgecolor='black', figsize=(25,18))
geo_data.plot(ax=base, figsize=(25,18), alpha=0.2)

geo_data.to_file('../01.Dados/Mapas/SP-DATASET/DATASET.shp')

"""###Reading x1x2_correlation.csv"""

def calculate_correlation_with_limiar_x(limiar):
  correlation_dataframe = pd.read_csv("x1x2_correlations.csv", encoding = "ISO-8859-1")
  
  correlation_dataframe = correlation_dataframe[correlation_dataframe['corr'] > limiar]
    
  correlation_dataframe = correlation_dataframe.reset_index(drop=True)
  correlation_dataframe = correlation_dataframe.astype({"X1": int, "X2": int})
    
  return correlation_dataframe

#Creating our graph

from igraph import *

def create_graph(limiar):
  correlation_dataframe = calculate_correlation_with_limiar_x(limiar)

  g = Graph()
  g.add_vertices(56)

  #Adding edges to the graph
  lista = [tuple(r) for r in correlation_dataframe[['X1', 'X2']].values]
  
  g.add_edges(lista)
  return g


# def calculate_avg_shortest_path(g):
#     print("Shortest path from node: ")
#     for v in g.vs:
#       print(g.get_shortest_paths(v, to=None, weights=None, mode=OUT, output="vpath"))
#       # print(g.shortest_paths_dijkstra(source=None, target=None, weights=None, mode=OUT))
#       # print(g.shortest_paths(source=None, target=None, weights=None, mode=ALL))

def calculate_avg_eccentricity(g):
  return sum(g.eccentricity(vertices=None, mode=IN))/len(g.vs)


list_of_metrics = []

import numpy

max_diam = 0.0
max_limiar_diam = 0.9

for i in numpy.arange(0, 1, 0.025):
    limiar = round(i, 2)
    g = create_graph(limiar)
    
    diam = g.diameter(directed=False, unconn=True, weights=None)

    if(diam > max_diam):
        max_diam = diam
        max_limiar_diam = limiar

    list_of_metrics.append(tuple((limiar, calculate_avg_eccentricity(g), g.average_path_length(directed=True, unconn=True),
                                  g.transitivity_undirected(mode="nan"),
                                  round(mean(g.degree()), 4), g.vcount(), g.ecount(), 
                                  diam, 
                                  len(g.clusters(mode=STRONG)))))

#g = create_graph(round(0, 2))

g = create_graph(max_limiar_diam)

list_degree_max_diam = g.vs.degree()

metrics = pd.DataFrame(list_of_metrics, columns = ['Limiar', 'avg_eccentricity', 'avg_path_len', 'transitivity' ,'avg_degree', 'num_nodes', 'num_edges', 'diameter', 'clusters'])
metrics

metrics.to_csv('metrics.csv')

import pandas as pd
from sklearn import preprocessing

limiar = metrics[['Limiar']]

metrics_to_plot = metrics[['avg_eccentricity', 'avg_path_len','transitivity', 'diameter']]
metrics2_to_plot = metrics[['avg_degree', 'clusters']]

# #This lines is to normalize the dataframe
# x = metrics_to_plot.values #returns a numpy array
# min_max_scaler = preprocessing.MinMaxScaler()
# x_scaled = min_max_scaler.fit_transform(x)
# metrics_to_plot = pd.DataFrame(x_scaled, columns = ['avg_eccentricity', 'avg_path_len','transitivity','avg_degree', 'diameter', 'clusters'])
# #####


metrics_to_plot = pd.concat([limiar, metrics_to_plot], axis=1)
metrics_to_plot2 = pd.concat([limiar, metrics2_to_plot], axis=1)
# metrics_to_plot

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

fig, axs = plt.subplots(2, sharex=True)

#http://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/Show_colormaps
ax1 = metrics_to_plot.plot.bar(ax=axs[0], x = 'Limiar', rot=0, figsize=(30,20), stacked=True, colormap='Accent')
ax1.legend(loc='best', fontsize=20)

ax2 = metrics_to_plot2.plot.bar(ax=axs[1], x = 'Limiar', rot=0, figsize=(30,20), stacked=True,  colormap='Paired')
ax2.legend(loc='best', fontsize=20)

plt.xlabel('Limiar', fontsize=50)

plt.setp(ax1.get_xticklabels(), rotation='45', fontsize=25)
plt.setp(ax1.get_yticklabels(), rotation='45', fontsize=25)

plt.setp(ax2.get_xticklabels(), rotation='45', fontsize=25)
plt.setp(ax2.get_yticklabels(), rotation='45', fontsize=25)

leg = plt.legend(fontsize=25)

plt.savefig('metrics.pdf')
plt.show()

correlations = calculate_correlation_with_limiar_x(max_limiar_diam)
correlations = correlations.astype({"X1": int, "X2": int})

correlations['X1Coord'] = correlations['X1'].apply(lambda x: geo_data.iloc[x-1, 3])
correlations['X2Coord'] = correlations['X2'].apply(lambda x: geo_data.iloc[x-1, 3])
correlations

from shapely.geometry import LineString

y =  zip(correlations.X1Coord, correlations.X2Coord)
y

geometry = [LineString(xy) for xy in zip(correlations.X1Coord, correlations.X2Coord)]
#geometry

crs = {'proj': 'latlong', 'ellps': 'WGS84', 'datum': 'WGS84', 'no_defs': True}

geo_data_correlations = gpd.GeoDataFrame(correlations, crs = crs, geometry = geometry)
geo_data_correlations

geo_data_correlations.crs

geo_data_correlations = geo_data_correlations[['X1','X2','geometry']]
type(geo_data_correlations)

import os

dir = '../01.Dados/Mapas/SP-DATASET'
if not os.path.exists(dir):
    os.makedirs(dir)

geo_data_correlations.to_file(dir + '/DATASET_CORRELATIONS.shp')

"""##**Plotting** layers"""

from matplotlib import pyplot as plt
# Setup figure and axis
f, ax = plt.subplots(1, figsize=(1, 1))
# Add tidal water (remove boundary lines for the polygons)

base = sjc.plot(color='white', edgecolor='black', figsize=(25,18), linewidth=4)
geo_data.plot(ax=base, color='green', figsize=(25,18), alpha=0.8, linewidth=6)
geo_data_correlations.plot(ax=base, color='blue', figsize=(25,18), alpha=0.2, linewidth=3)

# Remove axes
ax.set_axis_off()
# Impose same size for units across axes
plt.axis('equal')

plt.savefig('sjc09.png')
plt.savefig('sjc09.pdf')

# Display
plt.show()

"""##Generating several images for each limiar"""

list_of_metrics = []

for i in numpy.arange(0, 1, 0.2):
  limiar = round(i, 2)
  g = create_graph(limiar)
  diam = g.diameter(directed=False, unconn=True, weights=None)

  list_of_metrics.append(tuple((limiar, calculate_avg_eccentricity(g), g.average_path_length(directed=True, unconn=True),
                                  g.transitivity_undirected(mode="nan"),
                                  round(mean(g.degree()), 4), g.vcount(), g.ecount(), 
                                  diam, 
                                  len(g.clusters(mode=STRONG)))))

# Create the pandas DataFrame 
metrics = pd.DataFrame(list_of_metrics, columns = ['Limiar', 'avg_eccentricity', 'avg_path_len', 'transitivity' ,'avg_degree', 'num_nodes', 'num_edges', 'diameter', 'clusters'])
metrics

"""##Calculating correlations"""

count=0
for i in numpy.arange(0, 1, 0.01):
  correlations = calculate_correlation_with_limiar_x(i)
  correlations = correlations.astype({"X1": int, "X2": int})

  correlations['X1Coord'] = correlations['X1'].apply(lambda x: geo_data.iloc[x-1, 3])
  correlations['X2Coord'] = correlations['X2'].apply(lambda x: geo_data.iloc[x-1, 3])
  correlations
  
  from shapely.geometry import LineString

  y =  zip(correlations.X1Coord, correlations.X2Coord)
  
  geometry = [LineString(xy) for xy in zip(correlations.X1Coord, correlations.X2Coord)]
  crs = {'proj': 'latlong', 'ellps': 'WGS84', 'datum': 'WGS84', 'no_defs': True}

  geo_data_correlations = gpd.GeoDataFrame(correlations, crs = crs, geometry = geometry)
  geo_data_correlations = geo_data_correlations[['X1','X2','geometry']]

  import os

  dir = '../01.Dados/Mapas/SP-DATASET'
  if not os.path.exists(dir):
      os.makedirs(dir)

  geo_data_correlations.to_file(dir + '/DATASET_CORRELATIONS'+str(count)+'.shp')

  from matplotlib import pyplot as plt
  # Setup figure and axis
  f, ax = plt.subplots(1, figsize=(1, 1))
  # Add tidal water (remove boundary lines for the polygons)

  base = sjc.plot(color='white', edgecolor='black', figsize=(25,18))
  geo_data_correlations.plot(ax=base, color='blue', figsize=(25,18), alpha=0.2)
  geo_data.plot(ax=base, color='green', figsize=(25,18), alpha=0.8)

  # Remove axes
  ax.set_axis_off()
  # Impose same size for units across axes
  plt.axis('equal')

  plt.savefig('sjc'+str(count)+'.png')
  count+=1

