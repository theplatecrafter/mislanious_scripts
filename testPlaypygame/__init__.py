import pygame as p
import math as m
import random as r
p.init()


screenWidth = p.display.get_desktop_sizes()[0][0]-100
screenHeight = p.display.get_desktop_sizes()[0][1]-200

screen = p.display.set_mode([screenWidth,screenHeight])

speed = 1
particles = []
collidedParticles = []
NumberOfParticles = 20
for i in range(NumberOfParticles):
  particles.append({
    "mass":30,
    "pos":[r.randrange(25,screenWidth-25),r.randrange(25,screenHeight-25)],
    "vel":[r.random()*2-1,r.random()*2-1],
    "bounciness":1
    })

def calculate_collision_velocity(V0x, V0y, V1x, V1y, m0, m1, bounciness):
    V0x_prime = ((m0 - m1) * V0x + 2 * m1 * V1x) / (m0 + m1)
    V0y_prime = ((m0 - m1) * V0y + 2 * m1 * V1y) / (m0 + m1)
    V1x_prime = ((m1 - m0) * V1x + 2 * m0 * V0x) / (m0 + m1)
    V1y_prime = ((m1 - m0) * V1y + 2 * m0 * V0y) / (m0 + m1)
    
    V0x_prime *= bounciness
    V0y_prime *= bounciness
    V1x_prime *= bounciness
    V1y_prime *= bounciness
    
    return (V0x_prime, V0y_prime), (V1x_prime, V1y_prime)

running = True
while running:
  for event in p.event.get():
    if event.type == p.QUIT:
      running = False
  
  screen.fill(255)

  collidedParticles = []
  maxSpeed = 0
  for a in range(len(particles)):
    i = particles[a]
    i["pos"][0] += i["vel"][0]
    i["pos"][1] += i["vel"][1]
    if i["pos"][0] <= 0 or i["pos"][0] >= screenWidth - i["mass"]:
      i["vel"][0] *= -1 * i["bounciness"]
    if i["pos"][1] <= 0 or i["pos"][1] >= screenHeight - i["mass"]:
      i["vel"][1] *= -1 * i["bounciness"]
    tmpRect = p.Rect(i["pos"][0], i["pos"][1], i["mass"], i["mass"])

    for b in range(a + 1, len(particles)):
      j = particles[b]
      if tmpRect.colliderect(p.Rect(j["pos"][0], j["pos"][1], j["mass"], j["mass"])):
        v0 = i["vel"]
        v1 = j["vel"]
        m0 = i["mass"]
        m1 = j["mass"]
        v0Prime, v1Prime = calculate_collision_velocity(v0[0], v0[1], v1[0], v1[1], m0, m1,(i["bounciness"]+j["bounciness"])/2)

        i["vel"] = [v0Prime[0], v0Prime[1]]
        j["vel"] = [v1Prime[0], v1Prime[1]]
        collidedParticles.append((a, b))
    if m.sqrt(pow(i["vel"][0],2)+m.pow(i["vel"][1],2)) > maxSpeed:
      maxSpeed = m.sqrt(pow(i["vel"][0],2)+m.pow(i["vel"][1],2))
    p.draw.rect(screen, (m.sqrt(pow(i["vel"][0],2)+m.pow(i["vel"][1],2))/maxSpeed*255,0,0), tmpRect)

  
  p.display.update()

p.quit()