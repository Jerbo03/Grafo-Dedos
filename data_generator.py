# data_generator

from grafo import Grafo

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

import pygraphviz
import matplotlib.pyplot as plt

import random
import math
import copy
import csv
import pickle

dedos = 4 # dedos necesitados para perder
manos = 2 # manos
jugadores = 2 # jugadores

turno_inicial = 0

dibujar = False

#################

print(f'\nCREANDO DATOS PARA {dedos} DEDOS\n')

print('Creando grafo principal')
g = Grafo(dedos, manos, jugadores, turno_inicial)
G = g.grafo

print('\nEvaluando hojas')
hojas = [x for x in G.nodes() if G.out_degree(x)==0]
hojas_malas = [x for x in hojas if x < g.RL]
hojas_buenas = [x for x in hojas if x >= g.RL]

print('Hojas:\t\t\t', hojas)
print('Hojas buenas:\t', hojas_buenas)
print('Hojas malas:\t', hojas_malas)

print('\nEvaluando ciclos')
ciclos = list(nx.simple_cycles(G))
print(f'Ciclos encontrados: {len(ciclos)}')

with open("ciclos.csv","w+") as my_csv:
  csvWriter = csv.writer(my_csv,delimiter=',')
  csvWriter.writerows(ciclos)

if dibujar:
  #Dibujo del grafo
  plt.clf()
  color_map = []
  for node in G:
    if node < g.RL: # RL for d=3, m=2, j=2
      color_map.append('blue')
    else: 
      color_map.append('red')
  options = {
    "font_size": 6,
    "font_color": "white",
    "node_size": 300,
    "node_color": color_map,
    "edgecolors": "black",
    "linewidths": 0.3,
    "width": 0.2,
  }
  plt.figure(1,figsize=(16,14))   
  pos = graphviz_layout(G, prog="dot")
  nx.draw_networkx(G, pos=pos, **options)
  ax = plt.gca()
  ax.margins(0.25)
  plt.axis("off")
  plt.savefig('grafo.png')

#################

print('\nCreado grafo de caminos buenos')
H = G.copy()

for n in G:
  if n == g.raiz:
    continue
    
  if n in hojas_buenas:
    continue
  
  if H.in_degree(n)==0:
    H.remove_node(n)
    continue
    
  if n in hojas_malas:
    H.remove_node(n)
    continue

  flag = True
  for h in hojas_buenas:
    if nx.has_path(H, n, h):
      flag = False
      break   
  if flag:
    H.remove_node(n)
    continue

if dibujar:
  #Dibujo del grafo
  plt.clf()
  color_map = []
  for node in H:
    if node < g.RL: # RL for d=3, m=2, j=2
      color_map.append('blue')
    else: 
      color_map.append('red')
  options = {
    "font_size": 6,
    "font_color": "white",
    "node_size": 300,
    "node_color": color_map,
    "edgecolors": "black",
    "linewidths": 0.3,
    "width": 0.2,
  }
  plt.figure(1,figsize=(16,14))   
  pos = graphviz_layout(H, prog="dot")
  nx.draw_networkx(H, pos=pos, **options)
  ax = plt.gca()
  ax.margins(0.25)
  plt.axis("off")
  plt.savefig('buenos.png')

#################

print('\nCreado grafo de caminos malos')
F = G.copy()

for n in G:
  if n == g.raiz:
    continue    
  if n in hojas_malas:
    continue
  if F.in_degree(n)==0:
    F.remove_node(n)
    continue
  if n in hojas_buenas:
    F.remove_node(n)
    continue
  flag = True
  for h in hojas_malas:
    if nx.has_path(F, n, h):
      flag = False
      break   
  if flag:
    F.remove_node(n)
    continue

if dibujar:
  #Dibujo del grafo
  plt.clf()
  color_map = []
  for node in F:
    if node < g.RL: # RL for d=3, m=2, j=2
      color_map.append('blue')
    else: 
      color_map.append('red')
  options = {
    "font_size": 6,
    "font_color": "white",
    "node_size": 300,
    "node_color": color_map,
    "edgecolors": "black",
    "linewidths": 0.3,
    "width": 0.2,
  }
  plt.figure(1,figsize=(16,14))   
  pos = graphviz_layout(F, prog="dot")
  nx.draw_networkx(F, pos=pos, **options)
  ax = plt.gca()
  ax.margins(0.25)
  plt.axis("off")
  plt.savefig('malos.png')

#################

print('\nEvaluando nodos en el grafo principal')
# Nodos:
ambos = []
buenos = []
malos = []
ignorados = []

# G: todos los nodos
# H: nodos buenos (favorecen al primer jugador)
# F: nodos malos (favorecen al segundo jugador)
for n in G:
  if n in H or n in F:
    if n in H and n in F:
      ambos.append(n)
    elif n in H: 
      buenos.append(n)
    else:
      malos.append(n)
  else:
    ignorados.append(n)

# Los buenos siempre benefician a la máquina, independiente de quién empiece
# Esto porque el grafo se genera en función a quién empiece
print('Ambos', ambos)
print('Buenos', buenos)
print('Malos', malos)
print('Ignorados', ignorados)

if dibujar:
  #Dibujo del grafo resumen
  plt.clf()
  color_map = []
  for node in G:
    if node in ambos:
      if node < g.RL:
        color_map.append('limegreen')
      else:
        color_map.append('green')
    elif node in buenos: 
      color_map.append('blue')
    elif node in malos: 
      color_map.append('red')
    else: 
      color_map.append('white')
  options = {
    "font_size": 6,
    "font_color": "white",
    "node_size": 300,
    "node_color": color_map,
    "edgecolors": "black",
    "linewidths": 0.3,
    "width": 0.2,
  }
  plt.figure(1,figsize=(16,14))   
  pos = graphviz_layout(G, prog="dot")
  nx.draw_networkx(G, pos=pos, **options)
  ax = plt.gca()
  ax.margins(0.25)
  plt.axis("off")
  plt.savefig('resumen.png')

def save_object(obj, filename):
  with open(filename, 'wb') as outp:  # Overwrites any existing file.
    pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

def save_list(lista, filename):
  with open(filename, 'w') as f:
    write = csv.writer(f)
    write.writerow(lista)

def save_array(arr, filename):
  with open(filename, 'w') as f:
    write = csv.writer(f)
    write.writerows(arr)

# Saving files
save_object(g, f'{dedos}_dedos/Grafo Obj.pkl')
save_list(buenos, f'{dedos}_dedos/list_buenos.csv')
save_list(malos, f'{dedos}_dedos/list_malos.csv')
save_list(ambos, f'{dedos}_dedos/list_ambos.csv')
save_array(ciclos, f'{dedos}_dedos/list_ciclos.csv')
save_list(hojas, f'{dedos}_dedos/list_hojas.csv')
save_list(hojas_buenas, f'{dedos}_dedos/list_hojas_buenas.csv')