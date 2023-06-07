from Functions import *

class Problem:
    '''
    Abstract base class for problem formulation.
    It declares the expected methods to be used by a search algorithm.
    All the methods declared are just placeholders that throw errors if not overriden by child "concrete" classes!
    '''
    
    def __init__(self):
        '''Constructor that initializes the problem. Typically used to setup the initial state and, if applicable, the goal state.'''
        self.init_state = None
    
    def actions(self, state):
        '''Returns an iterable with the applicable actions to the given state.'''
        raise NotImplementedError
    
    def result(self, state, action):
        '''Returns the resulting state from applying the given action to the given state.'''
        raise NotImplementedError
    
    def goal_test(self, state):
        '''Returns whether or not the given state is a goal state.'''
        raise NotImplementedError
    
    def step_cost(self, state, action):
        '''Returns the step cost of applying the given action to the given state.'''
        raise NotImplementedError

    def heuristic(self, state):
      '''Returns the heuristic of applying the given action to the given state.'''
      raise NotImplementedError




class Node:
    '''Node data structure for search space bookkeeping.'''
    
    def __init__(self, state, parent, action, path_cost, heuristic,Level = 0):
        '''Constructor for the node state with the required parameters.'''
        self.state = state
        self.parent = parent
        self.action = action
        self.g = path_cost
        self.h = heuristic
        self.Level = Level
        self.f = path_cost + heuristic

    @classmethod
    def root(cls, problem):
        '''Factory method to create the root node.'''
        init_state = problem.init_state 
        return cls(init_state, None, None, 0, problem.heuristic(init_state),0)

    @classmethod
    def child(cls, problem, parent, action):
        '''Factory method to create a child node.'''
        child_state = problem.result(parent.state, action)
        return cls(
            child_state,
            parent,
            action,
            parent.g + problem.step_cost(parent.state, action),
            problem.heuristic(child_state),
            parent.Level+1)

def solution(node):
    '''A method to extract the sequence of actions representing the solution from the goal node.'''
    actions = []
    cost = node.g
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    actions.reverse()
    return actions, cost

def solution(node):
    '''A method to extract the sequence of actions representing the solution from the goal node.'''
    actions = []
    cost = node.g
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    actions.reverse()
    return actions, cost






class Map(Problem):
    '''
    Abstract base class for problem formulation.
    It declares the expected methods to be used by a search algorithm.
    All the methods declared are just placeholders that throw errors if not overriden by child "concrete" classes!
    '''
    
    def __init__(self,init_state, goal_state):
        '''Constructor that initializes the problem. Typically used to setup the initial state and, if applicable, the goal state.'''
        self.init_state = init_state
        self.goal_state = goal_state
        # Node json file has all inter and intra nodes in the map and their adjecents... 

        with open('Nodes.json') as f:
            self.Nodes=  json.load(f)
        # Actions for each node...

        with open('Actions.json') as f:
            self.new_actions=  json.load(f)    
        # json file that contains coordinate of each node in the map...   

        with open('roads.json') as f:
            self.Road_dict = json.load(f)
        # dict contains all possible routes with their cost and estimated number of pumps...
        
        self.Road_cost = {'R1' : (200,0) , 'R2' : (200,1)  ,'R3' : (200,0)  , 'R4' : (72,1)   ,'R5' : (76,0)   ,'R6' : (60,0)   , 'R7' : (140,0)  ,'R8' : (75,0)   ,
                          'R9' : (170,0)  , 'R10' : (180,2)  , 'R11' : (180,2)  , 'R12' : (220,2)  , 'R13' : (240,2)  , 'R14' : (110,1)  , 'R15' : (200,2)  ,
                          'R16' : (250,1)  , 'R17' : (150,1)  , 'R18' : (240,0)  , 'R19' : (300,2)  , 'R20' : (300,2)  , 'R21' : (170,1)  , 'R22' : (260,2)  , 
                          'R23' : (70,0)  , 'R24' : (120,0)  , 'R25' : (60,1)  , 'R26' : (240,2)  , 'R27' : (210,2)  , 'R28' : (300,1)  , 'R29' : (350,1)  ,
                          'R30' : (180,2)  , 'R31' : (350,0)  , 'R32' : (60,0)  , 'R33' : (450,0)  , 'R34' : (240,1)  , 'R35' : (190,0)  , 'R36' : (160,1)  ,
                          'HB_elvator' : (5,0),  'HB_stairs': (10,0), 'NB_elvator': (5,0), 'NB_stairs': (10,0), 'cafeteria_elevator' :(5,0),'cafeteria_stairs': (10,0),
                         }

        
    def actions(self, state):
      
      '''Returns an iterable with the applicable actions to the given state.'''
      #if type(self.new_actions[state]) == str:
      return (self.new_actions[state])
    

    def result(self, state, action):
        '''Returns the resulting state from applying the given action to the given state.'''
        action = action.split(":")[1]
       
        return (action)

    def goal_test(self, state):
        '''Returns whether or not the given state is a goal state.'''
        return state == self.goal_state
    
    def step_cost(self, state, action):
        '''Returns the step cost of applying the given action to the given state.'''
        return self.Road_cost[action][0] + (20 * self.Road_cost[action][1]) if action in self.Road_cost else 5
  
    def heuristic(self, state):

      if state in self.Road_dict and  self.goal_state in self.Road_dict:
        return Heuristic_1(state, self.goal_state, self.Road_dict)
      else:
        return 0