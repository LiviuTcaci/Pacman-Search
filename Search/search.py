# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    from util import Stack  # Importăm stiva din util.py

    # 1. Inițializăm stiva și lista de stări vizitate
    frontier = Stack()
    # Adăugăm în stivă starea de start și o listă goală de acțiuni
    frontier.push((problem.getStartState(), []))
    visited = set()

    # 2. Procesăm cât timp avem elemente în stivă
    while not frontier.isEmpty():
        # Scoatem nodul curent și calea asociată din stivă
        state, actions = frontier.pop()

        # 3. Verificăm dacă am atins ținta; dacă da, returnăm lista de acțiuni
        if problem.isGoalState(state):
            return actions

        # 4. Dacă nodul nu a fost vizitat, îl marcăm ca vizitat
        if state not in visited:
            visited.add(state)

            # 5. Generăm și procesăm succesorii nodului curent
            for successor, action, cost in problem.getSuccessors(state):
                # Actualizăm lista de acțiuni și adăugăm succesorul în stivă
                new_actions = actions + [action]
                frontier.push((successor, new_actions))

    # Dacă nu găsim soluția, returnăm o listă goală (fallback)
    return []
#testare:
# python pacman.py -l tinyMaze -p SearchAgent
# python pacman.py -l mediumMaze -p SearchAgent
# python pacman.py -l bigMaze -z .5 -p SearchAgent


def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    from util import Queue  # Importăm coada din util.py

    # 1. Inițializăm coada și lista de stări vizitate
    frontier = Queue()
    # Adăugăm în coadă starea de start și o listă goală de acțiuni
    frontier.push((problem.getStartState(), []))
    visited = set()

    # 2. Procesăm cât timp avem elemente în coadă
    while not frontier.isEmpty():
        # Extragem nodul curent și calea asociată din coadă
        state, actions = frontier.pop()

        # 3. Verificăm dacă am atins ținta; dacă da, returnăm lista de acțiuni
        if problem.isGoalState(state):
            return actions

        # 4. Dacă nodul nu a fost vizitat, îl marcăm ca vizitat
        if state not in visited:
            visited.add(state)

            # 5. Generăm și procesăm succesorii nodului curent
            for successor, action, cost in problem.getSuccessors(state):
                # Actualizăm lista de acțiuni și adăugăm succesorul în coadă
                new_actions = actions + [action]
                frontier.push((successor, new_actions))

    # Dacă nu găsim soluția, returnăm o listă goală (fallback)
    return []
#testare: python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs ; python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=bfs

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    from util import PriorityQueue  # Importăm coada de priorități din util.py

    # 1. Inițializăm coada de priorități și lista de stări vizitate
    frontier = PriorityQueue()
    # Adăugăm starea de start în coadă, cu costul inițial de 0
    frontier.push((problem.getStartState(), []), 0)
    visited = {}

    # 2. Procesăm cât timp avem elemente în coadă
    while not frontier.isEmpty():
        # Extragem nodul curent și calea asociată din coadă
        state, actions = frontier.pop()

        # 3. Verificăm dacă am atins ținta; dacă da, returnăm lista de acțiuni
        if problem.isGoalState(state):
            return actions

        # 4. Dacă nodul nu a fost vizitat sau are un cost mai mic decât cel anterior
        cost_so_far = problem.getCostOfActions(actions)
        if state not in visited or visited[state] > cost_so_far:
            visited[state] = cost_so_far

            # 5. Generăm și procesăm succesorii nodului curent
            for successor, action, step_cost in problem.getSuccessors(state):
                new_actions = actions + [action]
                new_cost = cost_so_far + step_cost
                frontier.push((successor, new_actions), new_cost)

    # Dacă nu găsim soluția, returnăm o listă goală (fallback)
    return []

# python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
# python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
# python pacman.py -l mediumScaryMaze -p StayWestSearchAgent


def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    from util import PriorityQueue  # Importăm coada de priorități din util.py

    # 1. Inițializăm coada de priorități și lista de stări vizitate
    frontier = PriorityQueue()
    # Adăugăm în coadă starea de start cu costul inițial de 0 + euristică
    start_state = problem.getStartState()
    frontier.push((start_state, []), heuristic(start_state, problem))
    visited = {}

    # 2. Procesăm cât timp avem elemente în coadă
    while not frontier.isEmpty():
        # Extragem nodul curent și calea asociată din coadă
        state, actions = frontier.pop()

        # 3. Verificăm dacă am atins ținta; dacă da, returnăm lista de acțiuni
        if problem.isGoalState(state):
            return actions

        # 4. Dacă nodul nu a fost vizitat sau are un cost mai mic decât cel anterior
        cost_so_far = problem.getCostOfActions(actions)
        if state not in visited or visited[state] > cost_so_far:
            visited[state] = cost_so_far

            # 5. Generăm și procesăm succesorii nodului curent
            for successor, action, step_cost in problem.getSuccessors(state):
                new_actions = actions + [action]
                new_cost = cost_so_far + step_cost
                total_cost = new_cost + heuristic(successor, problem)
                frontier.push((successor, new_actions), total_cost)

    # Dacă nu găsim soluția, returnăm o listă goală (fallback)
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
