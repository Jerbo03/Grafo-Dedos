from grafo import Grafo

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

import pygraphviz
import matplotlib.pyplot as plt

import random
import math
import copy
import csv
  
dedos = 3 # dedos necesitados para perder
manos = 2 # manos
jugadores = 2 # jugadores

turno_inicial = 1

#################

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

with open("grupos.csv","w+") as my_csv:
  csvWriter = csv.writer(my_csv,delimiter=',')
  csvWriter.writerow(buenos)
  csvWriter.writerow(malos)
  csvWriter.writerow(ambos)

#################

# Nodos buenos: victoria para el primer jugador
# Nodos malos: victoria para el segundo jugador

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
  # Ahora se evalúan los "primos"
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
    nietos = list(nx.neighbors(G2, hijos[i]))
    print(f'nietos de {hijos[i]}: {nietos}')
    for nieto in nietos:
      fila_evaluar = not turno_actual                  # Paso 1: turno_act 0 -> fila_ev 1
      fila = conversionMatriz(hijos[i])[fila_evaluar]  # Paso 2: fila del que le toca
      if fila_evaluar:                                 # Paso 3.1: si el turno es de 0
        diferencias = [(dedos**3)*fila[0], (dedos**2)*fila[1]]
      else:                                            # Paso 3.2: si el turno es de 1
        diferencias = [dedos*fila[0], fila[1]]
      if impulsivo(rawIndex(hijos[i]), rawIndex(nieto), diferencias):# Paso 4 y 5
        #Si la impulsividad lleva a que gane
        if nieto in malos:
          hijos[i] = 0
          break
  hijos = [x for x in hijos if ( x != 0)]
  return hijos

#################

def graficarActual(JUEGO):
  # Actualización del grafo en tiempo real
  nodo_pasado = nodo_actual
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
      print(f'El nodo {nodo} está en el ciclo {ciclo}')
      return
  hijos = list(nx.neighbors(JUEGO, nodo))
  for h in hijos:
    if JUEGO.in_degree(h) < 2 and JUEGO.out_degree(h) < 2:
      borrarNodos(h, JUEGO)
  print(f'Borrando nodo {nodo}')
  borrados.append(nodo)
  JUEGO.remove_node(nodo)

def borrarCiclos(nodo_actual, JUEGO):
  global ciclos
  for ciclo in ciclos:
    nodo = ciclo[0]
    #Si hay unión entre el punto actual o el nodo actual es igual al nodo evaluado siguiente iteración
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
        print(f'El nodo {nodos_borrar[0]} está en el ciclo {ciclo}')
        found = True
        break
    if not found:
      print(f'Borrando nodo {nodos_borrar[0]}')
      borrados.append(nodos_borrar[0])
      JUEGO.remove_node(nodos_borrar[0])
    
  borrarCiclos(nodo_actual, JUEGO)
  print(f'Ciclos restantes: {len(ciclos)}')

  print('Actualizando juego...')
  graficarActual(JUEGO)
  print(f'Nodos restantes {JUEGO.number_of_nodes()}')
  print(f'Nodos borrados: {borrados}')
  #print(list(JUEGO.nodes))
  nodos_borrar = [nodo_actual]

  with open("ciclos.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(ciclos)
  
  if (nodo_actual in hojas):
    break
  
  contador += 1
  print(f'\nTurno n°{contador}')
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
        print(f' - Opción {h}')
        print(f'\tMano Computadora:\t{matriz_opcion[0]}')
        print(f'\tMano Jugador:\t\t{matriz_opcion[1]}')
      h = int(input(f'Elige un elemento de la lista {hijos}: '))
    nodo_actual = h
    turno_actual = not turno_actual
    continue

  # Turno de la computadora
  turno_actual = not turno_actual

  if (len(hijos)==1): # No es necesario un análsis
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
  print('Predicción Estratega:', probsEstratega)
  if probsEstratega: # Lista de probabilidades no vacía
    nodo_actual = random.choice(probsEstratega)
    print(f'\tNodo siguiente: {nodo_actual}')
    continue

  #Revisión de Impulsividad
  probsImpulsivo = getProbsImpulsivo(hijos)
  print('Predicción Impulsiva:', probsImpulsivo)
  if probsImpulsivo: # Lista de probabilidades no vacía
    nodo_actual = random.choice(probsImpulsivo)
    print(f'\tNodo siguiente: {nodo_actual}')
    continue

  if nodo_actual in malos:
  # Si la derrota es absoluta
    nodo_actual = random.choice(hijos)
    print(f'\tNodo siguiente: {nodo_actual}')  

print(f'\n\tNodo final: {nodo_actual}')
matriz_final = conversionMatriz(nodo_actual)
print(f'\tMano Computadora:\t{matriz_final[0]}')
print(f'\tMano Jugador:\t\t{matriz_final[1]}')

if (nodo_actual in hojas_buenas):
  print('\nGANÓ LA COMPUTADORA')
else:
  print('\nGANÓ EL JUGADOR')
  
print('\n\n#################')

#################

"""
print(ambos)
nodos_pesos = {}
ambos_inv = ambos[::-1]
print('\nEvaluando nodos Verdes')

for n in ambos_inv:
  if (G.out_degree(n)!=1):
    nodos_pesos[str(n)] = []
    nodos_pesos['34'] = [[111,-2],[116,0]]
    ramas = list(nx.neighbors(G, n))
    for nodoEvaluar in ramas:
      peso = 0
      nodoCont = nodoEvaluar
      if (n>g.RL):
        peso+=1
      else:
        peso-=1
      while(True):
        #Evaluar hasta que sea 0 o una ramificacion
        if (G.out_degree(nodoCont)==0 or G.out_degree(nodoCont)==2 or G.out_degree(nodoCont)==4):
          #Si tiene ramas contenidas, quiere decir que estará previamente almacenado en el diccionario
          ramas_contenidas = G.out_degree(nodoCont)
          break
        elif (G.out_degree(nodoCont)==1):
            neighborsCopy = list(nx.neighbors(G, nodoCont))
            nodoCont = neighborsCopy[0]
      #nodoCont tendrá ese último
      if (G.out_degree(nodoCont)==0):
        #En el diccionario será indice que es el nodo y un arreglo
        #Si es 0, entonces almacenara el peso del final
        if (nodoCont<g.RL):
          peso+=1
        else:
          peso-=1
      elif (G.out_degree(nodoCont)==2 or G.out_degree(nodoCont)==4):
        peso += mayor(nodos_pesos[str(nodoCont)])
      #Aumentar o quitarle al peso segun el peso de la rama
      print(f'{n}\t{peso}')
      nodos_pesos[str(n)].append([nodoEvaluar, peso])

print(nodos_pesos)
#34 tiene más de dos hijos?
#Dar el valor de 34 previamente, corregir


print('\nEvaluando nodos Verdes')
#Los que se encuentran en ambos? 
for n in ambos:
  neighbors = list(nx.neighbors(G, n))
  nodoCont = n
  #Solo necesario evaluar las que son verdes que tienen ramificación roja
  #Maquina mayor a 81
  while(True):
    #Si es ramificacion, desechar cuando es final
    if (G.out_degree(nodoCont)==2 or G.out_degree(nodoCont)==4):
      #Ramfiicacion siguiente mmm 
      if ()
    elif (G.out_degree(nodoCont)==0):
      
    elif (G.neighbors(nodoCont)==1):
        neighborsCopy = list(nx.neighbors(G, nodoCont))
        nodoCont = neighborsCopy[0]
  neighbors = list(map(lambda x: 0 if x in ambos else (-1 if x in malos else 1), neighbors))
  print(f'{n}\t{neighbors}')

while(True):
        cont=0
        #Que no haya un solo camino
        if (G.out_degree(nodoCont)==0 or G.out_degree(nodoCont)==2 or G.out_degree(nodoCont)==4):
          orientacion = G.out_degree(nodoCont)
          break
        elif (G.out_degree(nodoCont)==1):
          neighborsCopy = list(nx.neighbors(G, nodoCont))
          nodoCont = neighborsCopy[0]
"""