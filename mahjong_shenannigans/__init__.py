game = [
  [], ## general info about game
  [], ## next up Hais
  [], ## player hands
]

def setupGame(NumberOfPlayers:int = 4,BaKaze:str = "East",Oya:int = 0):
  game = []
  game.append([NumberOfPlayers,BaKaze,Oya,0,])