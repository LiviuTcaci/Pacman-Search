# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Evaluează calitatea unei acțiuni pe baza stării succesoare.
        """
        # Obține informații despre succesor
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()

        # Penalizare pentru oprire
        if action == Directions.STOP:
            return -float('inf')

        # Distanța până la cel mai apropiat punct de hrană
        foodDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        nearestFoodDistance = min(foodDistances) if foodDistances else 1

        # Penalizare pentru apropierea de fantome
        ghostPenalty = 0
        for ghost in newGhostStates:
            ghostDistance = manhattanDistance(newPos, ghost.getPosition())
            if ghostDistance == 0:  # Fantoma este pe aceeași poziție cu Pacman
                ghostPenalty += 1e6  # Penalizare foarte mare
            elif ghostDistance < 2:  # Penalizare crescută pentru distanțe mici
                ghostPenalty += 200 / ghostDistance

        # Bonus pentru mâncat
        foodBonus = 0
        if currentGameState.getFood()[newPos[0]][newPos[1]]:
            foodBonus = 50

        # Calculul final al scorului
        score = successorGameState.getScore()
        return score + foodBonus - ghostPenalty - 1.5 * nearestFoodDistance


def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        """
        def minimax(agentIndex, depth, state):
            # Stare terminală: câștig, pierdere sau adâncime maximă
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            if agentIndex == 0:  # Pacman (MAX)
                return maxValue(depth, state)
            else:  # Fantome (MIN)
                return minValue(agentIndex, depth, state)

        def maxValue(depth, state):
            value = float('-inf')
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                value = max(value, minimax(1, depth, successor))
            return value

        def minValue(agentIndex, depth, state):
            value = float('inf')
            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            nextDepth = depth + 1 if nextAgent == 0 else depth

            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                value = min(value, minimax(nextAgent, nextDepth, successor))
            return value

        # Alegerea celei mai bune acțiuni pentru Pacman
        bestAction = None
        bestValue = float('-inf')
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = minimax(1, 0, successor)
            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction,
        applying alpha-beta pruning.
        """
        def alphaBeta(agentIndex, depth, state, alpha, beta):
            # Stare terminală: câștig, pierdere sau adâncime maximă
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            if agentIndex == 0:  # Pacman (MAX)
                return maxValue(depth, state, alpha, beta)
            else:  # Fantome (MIN)
                return minValue(agentIndex, depth, state, alpha, beta)

        def maxValue(depth, state, alpha, beta):
            value = float('-inf')
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                value = max(value, alphaBeta(1, depth, successor, alpha, beta))
                if value > beta:
                    return value  # Prune
                alpha = max(alpha, value)
            return value

        def minValue(agentIndex, depth, state, alpha, beta):
            value = float('inf')
            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            nextDepth = depth + 1 if nextAgent == 0 else depth

            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                value = min(value, alphaBeta(nextAgent, nextDepth, successor, alpha, beta))
                if value < alpha:
                    return value  # Prune
                beta = min(beta, value)
            return value

        # Alegerea celei mai bune acțiuni pentru Pacman
        bestAction = None
        bestValue = float('-inf')
        alpha, beta = float('-inf'), float('inf')

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = alphaBeta(1, 0, successor, alpha, beta)
            if value > bestValue:
                bestValue = value
                bestAction = action
            alpha = max(alpha, bestValue)

        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
