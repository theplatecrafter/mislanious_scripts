import numpy as np
import copy

objCount = 2

objState = [
    {"mass":1,"pos":np.array([0,0]).astype("float64"),"vel":np.array([0,0]).astype("float64"),"q":-1},
    {"mass":2,"pos":np.array([1,0]).astype("float64"),"vel":np.array([0,0]).astype("float64"),"q":1}
]


globalForces = {
    "gravity":np.array([0,-1])
}

consideredForces = {
    "gravity":{"G":1},
    "electric":{"K":1}
}

def tick(deltaT:float=0.01):
    new_state = copy.deepcopy(objState)
    for i in objState:
        forces = np.array([0,0]).astype("float64")
        #Static forces
        if "gravity" in globalForces:
            forces += globalForces["gravity"]
        
        #Dynamic forces
        for j in objState:
            distanceSquared = np.dot(j["pos"]-i["pos"],j["pos"]-i["pos"])
            unitDirection = (j["pos"]-i["pos"])/np.sqrt(distanceSquared)
            
            if consideredForces["electric"]:
                forces += unitDirection*(-1)*i["q"]*j["q"]*consideredForces["electric"]["K"]/distanceSquared
            
            if consideredForces["gravity"]:
                forces += unitDirection*(-1)*i["mass"]*j["mass"]*consideredForces["gravity"]["G"]/distanceSquared
        
        
        #next v and pos
        for f in forces:
            i["vel"] += deltaT*f/i["mass"]
        i["pos"] += i["vel"]*deltaT


while True:
    i = 0
    for obj in objState:
        i+=1
        print(f"{i}: pos-{obj["pos"]}  vel-{obj["vel"]}")
    print("\n")
    
    tick()