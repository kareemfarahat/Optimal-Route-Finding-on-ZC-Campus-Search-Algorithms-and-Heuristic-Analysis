
from itertools import count
from collections import deque
import datetime
from heapq import heappush, heappop
from Classes import *


counter = count()
def bfs_graph(problem, verbose=False):
    '''Breadth-first graph search implementation.'''
    if problem.goal_test(problem.init_state): return solution(Node.root(problem))
    frontier = deque([Node.root(problem)])
    explored = {problem.init_state}
    if verbose: visualizer = Visualizer(problem)
    while frontier:
        if verbose: visualizer.visualize(frontier)
        node = frontier.pop()
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if child.state not in explored:
                if problem.goal_test(child.state):
                    return solution(child)
                frontier.appendleft(child)
                explored.add(child.state)
      
 
def dfs_graph(problem):
    '''Depth-first graph search implementation.'''
    if problem.goal_test(problem): return solution(problem)
    frontier = deque([Node.root(problem)])
    explored = {problem.init_state}
    while frontier:
        node = frontier.popleft()
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if child.state not in explored:
                if problem.goal_test(child.state):
                    return solution(child)
                frontier.appendleft(child)
                explored.add(child.state)


def dls_tree(problem, limit, verbose=False):
    if problem.goal_test(problem.init_state): return solution(Node.root(problem))
    frontier = deque([Node.root(problem)])
    if verbose: visualizer = Visualizer(problem)
    while frontier:
        if verbose: visualizer.visualize(frontier)
        node = frontier.popleft()
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if problem.goal_test(child.state):
                return solution(child)
            if child.Level > limit:
              break
            frontier.appendleft(child)


def Ids_tree(problem, verbose=False):
  limit = 0
  value = None
  while value == None:
    value = dls_tree(problem,limit,verbose)
    limit+=1
  return value

def A_star_search(problem, verbose=False):
    '''A* search implementation.'''
    frontier = [(None, None, Node.root(problem))]
    explored = set()
    if verbose: visualizer = Visualizer(problem)
    while frontier:
        if verbose: visualizer.visualize(frontier)
        _, _, node = heappop(frontier)
        if node.state in explored: continue
        if problem.goal_test(node.state):
            return solution(node)
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if child.state not in explored:
                heappush(frontier, (child.f, next(counter), child))


def greedy_best_first(problem, verbose=False):
    '''Greedy best-first search implementation.'''
    frontier = [(None, None, Node.root(problem))]
    explored = set()
    if verbose: visualizer = Visualizer(problem)
    while frontier:
        if verbose: visualizer.visualize(frontier)
        _, _, node = heappop(frontier)
        if node.state in explored: continue
        if problem.goal_test(node.state):
            return solution(node)
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if child.state not in explored:
                heappush(frontier, (child.h, next(counter), child))

def hill_climbing(problem, verbose=False):
    '''Hill climbing search implementation.'''
    current_state = problem.init_state
    current_value = problem.heuristic(current_state)
    if verbose: visualizer = Visualizer(problem)
    while True:
        if verbose: visualizer.visualize([current_state],'Local')
        next_state, next_value = None, None
        for action in problem.actions(current_state):
            new_state = problem.result(current_state, action)
            new_value = problem.heuristic(new_state)
            if next_value is None or next_value > new_value:
                next_state, next_value = new_state, new_value
        if current_value <= next_value: return current_state
        current_state, current_value = next_state, next_value

