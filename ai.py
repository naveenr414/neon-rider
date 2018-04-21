import random
import geometry

def basic(state,player):
    currentPlayer = state.players[player]
    currentPlayer.speed = random.randint(1,10)
    currentPlayer.direction = geometry.up
