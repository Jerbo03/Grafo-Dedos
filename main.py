# game

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

#################

dedos = 4      # dedos necesitados para perder
manos = 2      # manos
jugadores = 2  # jugadores

turno_inicial = 0

actualizar = False

#################

g = 0

with open(f'{dedos}_dedos/Grafo Obj.pkl', 'rb') as obj:
  g = pickle.load(obj)

def read_csv(filename):
  with open(filename, newline='') as f:
    reader = list(csv.reader(f))
    for r in range(len(reader)):
      reader[r] = [int(x) for x in reader[r]]
    return reader

buenos  = read_csv(f'{dedos}_dedos/list_buenos.csv')[0]
malos   = read_csv(f'{dedos}_dedos/list_malos.csv')[0]
ambos   = read_csv(f'{dedos}_dedos/list_ambos.csv')[0]
ciclos  = read_csv(f'{dedos}_dedos/list_ciclos.csv')
hojas   = read_csv(f'{dedos}_dedos/list_hojas.csv')[0]
hojas_buenas = read_csv(f'{dedos}_dedos/list_hojas_buenas.csv')[0]

print(f'Lista de buenos:\t{buenos}')
print(f'Lista de malos:\t{malos}')
print(f'Lista de ambos:\t{ambos}')
print(f'Lista de ciclos:\t{ciclos}')
print(f'Lista de hojas:\t{hojas}')
print(f'Lista de hojas buenas:\t{hojas_buenas}')

#################

G = g.grafo

def getProbsEstratega(hijosOriginales):
  hijos = copy.deepcopy(hijosOriginales)
  G2 = G.copy()
  for i in range(len(hijos)):
    if hijos[i] in buenos:
      return [hijos[i]]
    if hijos[i] in malos:
      hijos[i] = 0
      continue
    nietos = list(nx.neighbors(G2, hijos[i]))
    for nieto in nietos:
      if nieto in malos:
        hijos[i] = 0
        break
  hijos = [x for x in hijos if ( x != 0)]
  return hijos

def rawIndex(fullIndex):
  if (fullIndex>=g.RL):
    fullIndex -= g.RL
  return fullIndex

def conversionMatriz(nodo):
  nodo = rawIndex(nodo)
  mat = [[0,0],[0,0]]
  #SubIndex1
  si1 = math.floor(nodo/g.SL)
  mat[0][0]=math.floor(si1/dedos)
  mat[0][1]=si1%dedos
  #SubIndex2
  si2 = nodo%g.SL
  mat[1][0]=math.floor(si2/dedos)
  mat[1][1]=si2%dedos
  return mat
  
def impulsivo(hijo, nieto, diferencias):
  # nieto = primo A (mayor)
  if ((hijo-nieto) in diferencias):
    return True
  # Ahora se eval??an los "primos"
  A = conversionMatriz(nieto)
  deltaB = A[1][0] - A[1][1]
  # Primo B = A-2|delta b|, Cambio en fila inferior
  difCoeficientesB = dedos - 1
  primoB = nieto - difCoeficientesB*deltaB
  if ((hijo-primoB) in diferencias):
    return True
  # Primo C = A-18|delta a|, Cambio en fila superior
  difCoeficientesA = (dedos**2)*difCoeficientesB
  deltaA = A[0][0] - A[0][1]
  primoC = nieto - difCoeficientesA*deltaA
  if ((hijo-primoC) in diferencias):
    return True
  # Primo D = C-2|delta  b|, Cambio en ambas filas
  primoD = primoC - difCoeficientesB*deltaB
  if ((hijo-primoD) in diferencias):
    return True
  # Si no dio con ninguno...
  return False

def getProbsImpulsivo(hijosOriginales):
  hijos = copy.deepcopy(hijosOriginales)
  G2 = G.copy()
  for i in range(len(hijos)):
    if hijos[i] in malos:
      hijos[i] = 0
    nietos = list(nx.neighbors(G2, hijos[i]))
    print(f'nietos de {hijos[i]}: {nietos}')
    fila_evaluar = not turno_actual                  # Paso 1: turno_act 0 -> fila_ev 1
    fila = conversionMatriz(hijos[i])[fila_evaluar]  # Paso 2: fila del que le toca
    if fila_evaluar:                                 # Paso 3.1: si el turno es de 0
      diferencias = [(dedos**3)*fila[0], (dedos**2)*fila[1]]
    else:                                            # Paso 3.2: si el turno es de 1
      diferencias = [dedos*fila[0], fila[1]]
    for nieto in nietos:
      if impulsivo(rawIndex(hijos[i]), rawIndex(nieto), diferencias):# Paso 4 y 5
        #Si la impulsividad lleva a que gane
        if nieto in malos:
          hijos[i] = 0
          break
  hijos = [x for x in hijos if ( x != 0)]
  return hijos

#################

def graficarActual(JUEGO):
  # Actualizaci??n del grafo en tiempo real
  plt.clf()
  color_map = []
  for node in JUEGO:
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
  pos = graphviz_layout(JUEGO, prog="dot")
  nx.draw_networkx(JUEGO, pos=pos, **options)
  ax = plt.gca()
  ax.margins(0.25)
  plt.axis("off")
  plt.savefig('juego.png')

borrados = []

def borrarNodos(nodo, JUEGO):
  global ciclos
  global borrados
  for ciclo in ciclos:
    if nodo in ciclo:
      print(f'El nodo {nodo} est?? en el ciclo {ciclo}')
      return
  hijos = list(nx.neighbors(JUEGO, nodo))
  for h in hijos:
    if JUEGO.in_degree(h) < 2 and JUEGO.out_degree(h) < 2:
      borrarNodos(h, JUEGO)
  print(f'Borrando nodo {nodo}')
  borrados.append(nodo)
  JUEGO.remove_node(nodo)

def borrarCiclos(nodo_actual, JUEGO):
  #stop = input('Pausa-----')
  print(f"Borrando ciclos: {ciclos}")
  for ciclo in ciclos:
    if not ciclo:
      continue
    nodo = ciclo[0]
    #Si hay uni??n entre el punto actual o el nodo actual es igual al nodo evaluado siguiente iteraci??n
    if nx.has_path(JUEGO, nodo_actual, nodo) or nodo_actual == nodo:
      continue
    print(f'Hijos de {nodo}: {list(nx.neighbors(JUEGO, nodo))}')
    for h in list(nx.neighbors(JUEGO, nodo)):
      if h in ciclo:
        JUEGO.remove_edge(nodo, h)
    print(f'\tQUITANDO CICLO: {ciclo}')
    ciclos.remove(ciclo)
    #borrarNodos(ciclo[0], JUEGO)
    borrarNodos(ciclo[0], JUEGO)

#################

print('\n\n#################')

print('\nJUEGO:')
print('Comienza', ("Computadora" if turno_inicial==0 else "Jugador"))

nodos_borrar = []
nodo_actual = g.raiz
turno_actual = turno_inicial
contador = 0 # Contador de turnos
JUEGO = G.copy()

while(True):
  borrarCiclos(nodo_actual, JUEGO)
  print(f'Ciclos restantes: {len(ciclos)}')
  
  if nodos_borrar:
    for hijo in list(nx.neighbors(JUEGO, nodos_borrar[0])):
      if hijo != nodo_actual:
        nodos_borrar.append(hijo)
    print(nodos_borrar, nodo_actual)
    for nodo in nodos_borrar[1:]:
      borrarNodos(nodo, JUEGO)
    found = False
    for ciclo in ciclos:
      if nodos_borrar[0] in ciclo:
        print(f'El nodo {nodos_borrar[0]} est?? en el ciclo {ciclo}')
        found = True
        break
    if not found:
      print(f'Borrando nodo {nodos_borrar[0]}')
      borrados.append(nodos_borrar[0])
      JUEGO.remove_node(nodos_borrar[0])
    
  borrarCiclos(nodo_actual, JUEGO)
  print(f'Ciclos restantes: {len(ciclos)}')

  if actualizar:
    print('Actualizando juego...')
    graficarActual(JUEGO)
  print(f'Nodos restantes {JUEGO.number_of_nodes()}')
  print(f'Nodos borrados: {borrados}')
  #print(list(JUEGO.nodes))
  nodos_borrar = [nodo_actual]

  with open("ciclos.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(ciclos)
  
  print(f'Comprobando si el nodo actual es una hoja {nodo_actual}\t:\t{hojas}')
  if (nodo_actual in hojas):
    break
  
  contador += 1
  print(f'\nTurno n??{contador}')
  print(f'\tTurno: {("Computadora" if turno_actual==0 else "Jugador")}')
  print(f'\tNodo actual: {nodo_actual}')
  matriz_actual = conversionMatriz(nodo_actual)
  print(f'\tMano Computadora:\t{matriz_actual[0]}')
  print(f'\tMano Jugador:\t\t{matriz_actual[1]}')
  hijos = list(nx.neighbors(JUEGO, nodo_actual))
  print(f'Hijos: {hijos}')

  # Turno del jugador
  if (turno_actual==1):
    h = -1
    while (not h in hijos):
      print('OPCIONES:')
      for h in hijos:
        matriz_opcion = conversionMatriz(h)
        print(f' - Opci??n {h}')
        print(f'\tMano Computadora:\t{matriz_opcion[0]}')
        print(f'\tMano Jugador:\t\t{matriz_opcion[1]}')
      h = int(input(f'Elige un elemento de la lista {hijos}: '))
    nodo_actual = h
    turno_actual = not turno_actual
    continue

  # Turno de la computadora
  turno_actual = not turno_actual

  if (len(hijos)==1): # No es necesario un an??lsis
    nodo_actual = hijos[0]
    continue

  
  #Corroborar: AGREGAR CONDICIONAL-Si se encuentra ya en un Camino Desfavorable
  #entonces saltar de frente al random

  if nodo_actual in malos:
  # Si la derrota es absoluta
    nodo_actual = random.choice(hijos)
    print(f'\tNodo siguiente: {nodo_actual}')
    continue
    
  probsEstratega = getProbsEstratega(hijos)
  print('Predicci??n Estratega:', probsEstratega)
  if probsEstratega: # Lista de probabilidades no vac??a
    nodo_actual = random.choice(probsEstratega)
    print(f'\tNodo siguiente: {nodo_actual}')
    continue

  #Revisi??n de Impulsividad
  probsImpulsivo = getProbsImpulsivo(hijos)
  print('Predicci??n Impulsiva:', probsImpulsivo)
  if probsImpulsivo: # Lista de probabilidades no vac??a
    nodo_actual = random.choice(probsImpulsivo)
    print(f'\tNodo siguiente: {nodo_actual}')
    continue

  # Si ni impulsivamente se puede hallar un camino favorable:
  nodo_actual = random.choice(hijos)
  print(f'\tNodo siguiente: {nodo_actual}')  

print(f'\n\tNodo final: {nodo_actual}')
matriz_final = conversionMatriz(nodo_actual)
print(f'\tMano Computadora:\t{matriz_final[0]}')
print(f'\tMano Jugador:\t\t{matriz_final[1]}')

if (nodo_actual in hojas_buenas):
  print('\nGAN?? LA COMPUTADORA')
else:
  print('\nGAN?? EL JUGADOR')
  
print('\n\n#################')
