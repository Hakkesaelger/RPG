from Mob_ai import monster_movement
from random import random
from math import ceil
from Utility import generate_board, bitwise_add
for i in range(1,101):
    print("")
world={
    "persons":{},
    "dir":{"u":[-1,0],"d":[1,0],"l":[0,-1],"r":[0,1]},
    "letter":{(-1,0):"u",(1,0):"d",(0,-1):"l",(0,1):"r"},
    "area":[[". ","P ",". ",". ",". ",". ",],
        [". ",". ",". ","O ",". ",". ",],
        [". ","M ",". ",". ",". ",". ",],
        [". ",". ",". ",". ",". ",". ",],
        [". ",". ",". ",". ",". ",". ",],
        [". ",". ",". ",". ",". ",". ",]],}

class Person:
    def __init__(self, coordinate:list, health:int, inventory:list, equipped:list, name:str,world:dict):
        self.coordinate=coordinate
        self.health=health
        self.inventory=inventory
        self.equipped=equipped
        self.name=name
        world["persons"][self.name]=self
    def move(self,area:dict,lenght):
        if self.coordinate[0]+lenght[0]>5:
            return [5,self.coordinate[1]+lenght[1],"Out of bounds"]
        if self.coordinate[1]+lenght[1]>5:
            return [self.coordinate[0]+lenght[0],5,"Out of bounds"]
        if self.coordinate[0]+lenght[0]<0:
            return [0,self.coordinate[1]+lenght[1],"Out of bounds"]
        if self.coordinate[1]+lenght[1]<0:
            return [self.coordinate[0]+lenght[0],0,"Out of bounds"]
        if area[self.coordinate[0]+lenght[0]][self.coordinate[1]+lenght[1]]!=". ":
            return [self.coordinate[0],self.coordinate[1],"Already occupied"]
        return [self.coordinate[0]+lenght[0], self.coordinate[1]+lenght[1],""]
    def attack(self, attacked):
        return attacked.health-ceil(ceil(random()*self.equipped[1]+self.equipped[0]-1)/attacked.equipped[2]) 
    def action(self, world:dict, s:str):
        if not s:
            return {"print":"Invalid action"}
        if not s[0] in ["u","d","l","r","a"]:
            return {"print":"Invalid action"}
        persons,dir,letter, area,=world.values()
        if s in ["u","d","l","r"]:
            for i in range(0,self.equipped[3]):
                t=self.move(area,dir[s])
                area[self.coordinate[0]][self.coordinate[1]]=". "
                area[t[0]][t[1]]=self.name
                self.coordinate=[t[0],t[1]]
            return {"print":t[2],"area":area}
        elif s[0]=="a":
            if not len(s)==3:
                return {"print":"Invalid attack"}
            if not s[2] in ["u","d","l","r"]:
                return {"print":"Invalid attack"}
            t=bitwise_add(self.coordinate, dir[s[2]])
            name=area[t[0]][t[1]]
            if name in [". ","O "]:
                return{"print":"No enemy to attack"}
            u=persons[name]
            u.health=self.attack(u)
            if u.health<=0:
                area[t[0]][t[1]]=". "
                return {"del":name,"print":"Enemy killed","area":area,"persons":persons}
            return{"print":u.health}
player=Person([0,1],100,[],[1,6,2,1],"P ",world)
monster=Person([2,1],5,[],[1,4,1.5,1],"M ",world)

while True:
    print(generate_board(world["area"]))
    print("Make an action! Move Up, Down, Left, or Right, make an attack, pick up an item on the ground, or make an inventory interaction")
    s=input("u for up, d for down, l for left, r for right, a+the direction you're attacking in(u, d, l, or r) for attack, p for pick up, and i for inventory \n")
    t=player.action(world,s,)
    print(t.pop("print"))
    if "del" in t:
        del world["persons"][t["del"]]
    for i in world:
        if i in t:
            world[i]=t[i]
    for i in list(world["persons"]):
        if i!="P ":
            t=world["persons"][i].action(world,monster_movement(world["persons"][i].coordinate,player.coordinate,world["letter"]))
            for j in world:
                if j in t:
                    world[j]=t[j]
            if t["print"]=="Enemy killed":
                print("You died")
                exit
            if type(t["print"])==int:
                print(t["print"])