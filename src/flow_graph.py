# -*- coding: utf-8 -*-
"""flow_graph.py
"""

from graph_point import graphPoint

"""# GRAPH"""

class flowGraph:
  '''A directed graph of ordered points.
  Each flow of the graph is from one two-dimensional
  object to another.
  '''
  def __init__(self, Nperiods):
    self.points = [None]*Nperiods

  def __len__(self):
    return len(self.points)

  def __repr__(self):
    return str(self.points)

  def __iter__(self):
    for k in range(len(self)):
      self.balances(k)
      yield k

  def __getitem__(self, k):
    return self.points[k]

  def getPoint(self, k, _fromNode, _toNode):
    p = self.points[k]
    if p == None:
      return graphPoint()
    for f, t, a in p:
      if f == _fromNode and t == _toNode:
        return a
    raise IndexError('Node not found: %d, %s, %s' % (k,_fromNode, _toNode) )

  def addFlow(self, k, _fromNode, _toNode, value):
    '''addFlow(self, k, _fromNode, _toNode, value)
    Add flow from point _fromNode to point _toNode 
    of value value in period k to the graph.
    k: integer
    _fromNode: length-2 tuple (x,y)
    _toNode: length-2 tuple (x,y)
    value: graphPoint(P,N)
    '''
    assert len(_fromNode) == 2, "_fromNode must be length 2"
    assert len(_toNode) == 2, "_toNode must be length 2"
    assert type(value) == type(graphPoint()), "value must be type graphPoint"
    if value.iszero():
      return
    assert k < len(self), "k must be less than the length of the graph"
    try:
      self.points[k].append((_fromNode, _toNode, value))
    except AttributeError:
      self.points[k] = [(_fromNode, _toNode, value)]

  def inflows(self, k):
    '''Calculate all of the inflows to each node in period k'''
    retVal = {}
    if self.points[k] == None:
      return retVal
    for (fromNode, toNode, amount) in self.points[k]:
      try:
        retVal[toNode] += amount
      except KeyError:
        retVal[toNode] = amount
    return retVal

  def outflows(self, k):
    '''Calculate all of the outflows from each node in period k'''
    retVal = {}
    if self.points[k] == None:
      return retVal
    for (fromNode, toNode, amount) in self.points[k]:
      try:
        retVal[fromNode] += amount
      except KeyError:
        retVal[fromNode] = amount
    return retVal

  def balances(self, k):
    '''Calculate the balances at period k and store along the diagonal.
    Balances are calculated as inflows - outflows.
    '''
    ins = self.inflows(k)
    outs = self.outflows(k)
    allNodes = set(ins.keys()).union(set(outs.keys()))
    for each in allNodes:
      if k == 0:
        previousBalance = graphPoint()
      else:
        try:
          previousBalance = self.getPoint(k-1, each, each)
        except IndexError:
          previousBalance = graphPoint()
      try:
        inAmt = ins[each]
      except KeyError:
        inAmt = graphPoint()
      try:
        outAmt = outs[each]
      except KeyError:
        outAmt = graphPoint()
      self.addFlow(k, each, each, previousBalance + inAmt - outAmt)

  def addFromArray(self, k, fromNode, toNode, valueArray, skip=None):
    '''addFromArray(self, k, fromNode, toNode, valueArray, skip=None)
    k: insert into graph starting with this period
    fromNode: for all of the entries
    toNode: for all of the entries
    valueArray: array of prices, units will be 1
    skip: number of periods to skip between array entries, if None, don't skip any
    '''
    for i in range(len(valueArray)):
      if skip == None:
        self.addFlow(k+i, fromNode, toNode, graphPoint(valueArray[i],1))
      else:
        self.addFlow(k+i*skip, fromNode, toNode, graphPoint(valueArray[i],1))

if __name__ == '__main__':
        
  G = flowGraph(5)
  a = graphPoint(7, 2)
  b = graphPoint(1.5, 4)
  
  G.addFlow(1, (1,1), (2,3), a)
  G.addFlow(1, (3,4), (2,3), b)
  print('G:',G)
  
  retVal = G.inflows(1)
  print('inflows:', retVal)
  
  retVal = G.outflows(1)
  print('outflows:', retVal)
  
  print()
  G.addFlow(2, (5,1), (1,1), graphPoint(1.0, 10))
  print('G=',G)
  print()
  
  print()
  import numpy as np
  print('addFlow from an array')
  ar = np.array([11, 13])
  
  G.addFromArray(k=3, fromNode=(1,1), toNode=(5,1), valueArray=ar)
  
  print('balances:')
  for period in G:
    print('\t%d: %s' % (period, G[period]))

