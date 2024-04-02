game = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]] ## 0: nothing    1: circle    2: cross

import players as p

def printGame():
  print(f"round: {round}")
  terraToe = [0,0,0,0,0,0,0,0,0]
  for i in range(9):
    if len(game[i]) != 9:
      terraToe[i] = game[i][9]
  for j in range(3):
    for i in range(3):
      print(terraToe[i+j*3],end=" ")
    print("")
  print("")
  for b in range(3):
    for a in range(3):
      for i in range(3):
        for j in range(3):
          print(game[i+b*3][j+a*3],end=" ")
        print("  ",end="")
      print("")
    print("")

def checkGame():
  for i in range(9):
    if [1,1,1] in [game[i][:3],game[i][3:6],game[i][6:]]:
      game[i].append(1)

    elif [2,2,2] in [game[i][:3],game[i][3:6],game[i][6:]]:
      game[i].append(2)

    elif (game[i][0] == 1 and game[i][3] == 1 and game[i][6] == 1) or (game[i][1] == 1 and game[i][3] == 1 and game[i][7] == 1) or (game[i][2] == 1 and game[i][5] == 1 and game[i][8] == 1):
      game[i].append(1)

    elif (game[i][0] == 2 and game[i][3] == 2 and game[i][6] == 2) or (game[i][1] == 2 and game[i][3] == 2 and game[i][7] == 2) or (game[i][2] == 2 and game[i][5] == 2 and game[i][8] == 2):
      game[i].append(2)

    elif (game[i][0] == 1 and game[i][4] == 1 and game[i][8] == 1) or (game[i][2] == 1 and game[i][4] == 1 and game[i][6] == 1):
      game[i].append(1)

    elif (game[i][0] == 2 and game[i][4] == 2 and game[i][8] == 2) or (game[i][2] == 2 and game[i][4] == 2 and game[i][6] == 2):
      game[i].append(2)

    elif not 0 in game[i]:
      game[i].append(-1)

  
  overall = [0,0,0,0,0,0,0,0,0]
  for i in range(9):
    if len(game[i]) != 9:
      overall[i] = game[i][9]
  
  if [1,1,1] in [overall[:3],overall[3:6],overall[6:]]:
    return 1
  elif [2,2,2] in [overall[:3],overall[3:6],overall[6:]]:
    return 2
  elif (overall[0] == 1 and overall[3] == 1 and overall[6] == 1) or (overall[1] == 1 and overall[3] == 1 and overall[7] == 1) or (overall[2] == 1 and overall[5] == 1 and overall[8] == 1):
    return 1
  elif (overall[0] == 2 and overall[3] == 2 and overall[6] == 2) or (overall[1] == 2 and overall[3] == 2 and overall[7] == 2) or (overall[2] == 2 and overall[5] == 2 and overall[8] == 2):
    return 2
  elif (overall[0] == 1 and overall[4] == 1 and overall[8] == 1) or (overall[2] == 1 and overall[4] == 1 and overall[6] == 1):
    return 1
  elif (overall[0] == 2 and overall[4] == 2 and overall[8] == 2) or (overall[2] == 2 and overall[4] == 2 and overall[6] == 2):
    return 2
  elif not 0 in overall:
    return -1
  return 0


################################### players
def p1(a,first,which):
  return p.rand(a,first,which)

def p2(b,which):
  return p.rand(b,False,which)
###################################

printGame()
gameON = True
round = 0
player2 = 0
player1 = 0
while gameON:

  round += 1
  if round == 1:
    player1 = p1(game,True,0)
    game[player1[0]-1][player1[1]-1] = 1
    print(player1)
    printGame()
    player2 = p2(game,player1[1])
    game[player1[1]-1][player2-1] = 2
    state = checkGame()
    print(player2)
    printGame()
    if state == 1:
      print("p1 win")
      break
    elif state == 2:
      print("p2 win")
      break
    elif state == -1:
      print("tie")
      break

    if len(game[player2-1]) != 9:
      player2 = p.r.randint(1,9)
      while len(game[player2-1]) != 9:
        player2 = p.r.randint(1,9)
  else:
    player1 = p1(game,False,player2)
    game[player2-1][player1-1] = 1
    state = checkGame()
    print(player1)
    printGame()
    if state == 1:
      print("p1 win")
      break
    elif state == 2:
      print("p2 win")
      break
    elif state == -1:
      print("tie")
      break

    if len(game[player1-1]) != 9:
      player1 = p.r.randint(1,9)
      while len(game[player1-1]) != 9:
        player1 = p.r.randint(1,9)

    player2 = p2(game,player1)
    game[player1-1][player2-1] = 2
    state = checkGame()
    print(player2)
    printGame()
    if state == 1:
      print("p1 win")
      break
    elif state == 2:
      print("p2 win")
      break
    elif state == -1:
      print("tie")
      break
    
    if len(game[player2-1]) != 9:
      player2 = p.r.randint(1,9)
      while len(game[player2-1]) != 9:
        player2 = p.r.randint(1,9)


  
  
