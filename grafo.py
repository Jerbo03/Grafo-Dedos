import networkx as nx
from copy import deepcopy

class Grafo:
  def __init__(self, dedos, manos, jugadores, turno_inicio):
    self.dedos = dedos   
    self.manos = manos
    self.jugadores = jugadores

    self.SL = pow(self.dedos, self.manos);
    self.RL = pow(self.SL, self.jugadores);
  
    self.tuno_inicial = turno_inicio

    self.inicio = []
    for i in range(self.manos):
      self.inicio.append([])
      for j in range(self.manos):
        (self.inicio)[i].append(1)

    self.raiz = self.fullIndex(self.inicio, self.tuno_inicial)
    self.nFinales = 0
    
    self.grafo = nx.DiGraph()
    self.createGraph(self.inicio, -1, self.tuno_inicial) 
    
  def odenarMayorPrimero(self, M):
    A = deepcopy(M)
    for row in range(len(A)):
      A[row].sort(reverse=True)
    return A
  
  def subIndex(self, L):
    subInd = 0
    for m in range(self.manos):
      subInd += pow(self.dedos, self.manos-m-1)*L[m]
    return subInd
  
  def rawIndex(self, M):
    rawInd = 0
    for j in range(self.jugadores):
      rawInd += pow(self.SL, self.jugadores-j-1)*self.subIndex(M[j])
    return rawInd

  def fullIndex(self, M, turno):
    # Orden: No se almacena, solo interesa el indice
    M = self.odenarMayorPrimero(M)
    if (turno):
      return (turno * self.RL + self.rawIndex(M))
    else:
      return (turno * self.RL + self.rawIndex(M[::-1]))
  
  def case1(self, M):
    A = deepcopy(M)
    A[1][0] += A[0][0]
    A[1][0] %= self.dedos
    return A
  
  def case2(self, M):
    A = deepcopy(M)
    A[1][1] += A[0][0]
    A[1][1] %= self.dedos
    return A
  
  def case3(self, M):
    A = deepcopy(M)
    A[1][0] += A[0][1]
    A[1][0] %= self.dedos
    return A
  
  def case4(self, M):
    A = deepcopy(M)
    A[1][1] += A[0][1]
    A[1][1] %= self.dedos
    return A

  def agregarNodo(self, prevNode, newNode, nivel):
    found = newNode in self.grafo.nodes
    self.grafo.add_edge(prevNode, newNode)
    #print(f'New edge: {prevNode} - {newNode}')
    return not found

  def createGraph(self, M, n, turno):
    # ignore = input('pause')
    A = deepcopy(M)
    n += 1
    #print(f'\nRepetición: {n}')
    #print(A)
    #print('Index: ', self.fullIndex(A, turno))
    
    A = A[::-1];

    if (A[0][0] == 0 and A[0][1] == 0):
      self.nFinales += 1
    
    if (A[0][0] != 0):
      if (A[1][0] != 0):
        if(self.agregarNodo(self.fullIndex(M, turno), self.fullIndex(self.case1(A), not turno), n)):
          self.createGraph(self.case1(A), n, not turno);
        
      if (A[1][1] != 0 and A[1][0] != A[1][1]):
        if(self.agregarNodo(self.fullIndex(M, turno), self.fullIndex(self.case2(A), not turno), n)):
          self.createGraph(self.case2(A), n, not turno)
    
    if (A[0][1] != 0 and A[0][0] != A[0][1]):
      if (A[1][0] != 0):
        if(self.agregarNodo(self.fullIndex(M, turno), self.fullIndex(self.case3(A), not turno), n)):
          self.createGraph(self.case3(A), n, not turno)

      if (A[1][1] != 0 and A[1][0] != A[1][1]):
        if(self.agregarNodo(self.fullIndex(M, turno), self.fullIndex(self.case4(A), not turno), n)):
          self.createGraph(self.case4(A), n, not turno)