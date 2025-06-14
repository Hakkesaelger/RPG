from random import random
from math import ceil
from Utility import generate_board, bitwise_add, find_dir
for i in range(1,101):
    print("")
class Thing:
    def __init__(self,coordinate:list,name:str):
        self.coordinate=coordinate
        self.name=name
class Person(Thing):
    def __init__(self, health:int, inventory:list, equipped:dict,coordinate:list,name:str):
        super().__init__(coordinate,name)
        self.health=health
        self.inventory=inventory
        self.equipped=equipped
    def move(self,area:list,lenght:list):
        if not (0<=self.coordinate[0]+lenght[0]<=5 and 0<=self.coordinate[1]+lenght[1]<=5):
            return [self.coordinate[0],self.coordinate[1],"Out of bounds"]
        if area[self.coordinate[0]+lenght[0]][self.coordinate[1]+lenght[1]]!=". ":
            return [self.coordinate[0],self.coordinate[1],"Already occupied"]
        return [self.coordinate[0]+lenght[0], self.coordinate[1]+lenght[1],""]
    def attack(self, attacked):
        return attacked.health-ceil(ceil(random()*self.equipped["max_damage"]+self.equipped["min_damage"]-1)/attacked.equipped["armor"]) 
    def act(self, world:dict, s:str):
        if not s:
            return {"print":"Invalid action"}
        if not (s in ["u","d","l","r"] or s[0]=="a"):
            return {"print":"Invalid action"}
        persons,dir,letter, area,=world.values()
        if s in ["u","d","l","r"]:
            for i in range(0,self.equipped["speed"]):
                t=self.move(area,dir[s])
                if t[2]:
                    return {"print":t[2]}
                area[self.coordinate[0]][self.coordinate[1]]=". "
                area[t[0]][t[1]]=self.name
                self.coordinate=[t[0],t[1]]
            return {"print":t[2],"area":area}
        if s[0]=="a":
            if not len(s)==3:
                return {"print":"Invalid attack"}
            if not s[2] in ["u","d","l","r"]:
                return {"print":"Invalid attack"}
            t=bitwise_add(self.coordinate, dir[s[2]],True)
            name=area[t[0]][t[1]]
            if not name in persons:
                return {"print":"No enemy to attack"}
            u=persons[name]
            u.health=self.attack(u)
            if u.health<=0:
                area[t[0]][t[1]]=". "
                return {"print":"Enemy killed","area":area,"persons":persons}
            return{"print":u.health}
class NPC(Person):
    def __init__(self,kill:bool,follow:Person,health:int, inventory:list, equipped:dict,coordinate:list,name:str,loot:dict):
        super().__init__(health, inventory, equipped,coordinate,name)
        self.kill=kill
        self.follow=follow
        self.loot=loot
    def movement(self,letter:dict, area:list):
        diff=bitwise_add(self.follow.coordinate,self.coordinate,False)
        if abs(diff[0])+abs(diff[1])==1 and self.kill:
            return "a "+letter[tuple(diff)]
        r=random()
        if diff[0] and diff[1]:
            if r<0.5:
                if area[self.coordinate[0]+find_dir(diff[0])][self.coordinate[1]]==". ":
                    return letter[(find_dir(diff[0]),0)]
            if area[self.coordinate[0]][self.coordinate[1]+find_dir(diff[1])]==". ":
                return letter[(0,find_dir(diff[1]))]
        if diff[0] and area[self.coordinate[0]+find_dir(diff[0])][self.coordinate[1]]==". ":
            return letter[(find_dir(diff[0]),0)]
        if diff[1] and area[self.coordinate[0]][self.coordinate[1]+find_dir(diff[1])]==". ":
            return letter[(0,find_dir(diff[1]))]
        if r<0.5 and area[self.coordinate[0]-find_dir(diff[0])][self.coordinate[1]]==". ":
            return letter[(find_dir(-diff[0]),0)]
        if area[self.coordinate[0]][self.coordinate[1]-find_dir(diff[1])]==". ":
            return letter[(0,find_dir(-diff[1]))]
        if diff[0] and area[self.coordinate[0]+find_dir(diff[0])][self.coordinate[1]]==". ":
            return letter[(find_dir(diff[0]),0)]
def spawn_npc(kill:bool,follow:Person,health:int, inventory:list, equipped:dict,coordinate:list,name:str,world:dict,loot:dict):
    world["persons"][name]=NPC(kill,follow,health,inventory,equipped,coordinate,name,loot)
    world["area"][coordinate[0]][coordinate[1]]=name
    return {"persons":world["persons"],"area":world["area"]}
world={
    "persons":{"P ":Person(100,[],{"min_damage":1,"max_damage":6,"armor":2,"speed":1},[0,1],"P ")},
    "dir":{"u":[-1,0],"d":[1,0],"l":[0,-1],"r":[0,1]},
    "letter":{(-1,0):"u",(1,0):"d",(0,-1):"l",(0,1):"r"},
    "area":[[". ","P ",". ",". ",". ",". ",],
        [". ","W ",". ",". ",". ",". ",],
        [". ",". ","W ",". ",". ",". ",],
        [". ",". ",". ",". ",". ",". ",],
        [". ",". ",". ",". ",". ",". ",],
        [". ",". ",". ",". ",". ",". ",]],}
i=spawn_npc(True, world["persons"]["P "],5,[],{"min_damage":1,"max_damage":4,"armor":1.5,"speed":1},[2,1],"M ",world,{100:[]})
world["persons"]=i["persons"]
world["area"]=i["area"]
while True:
    print(generate_board(world["area"]))
    print("Make an action! Move Up, Down, Left, or Right, make an attack, pick up an item on the ground, or make an inventory interaction")
    s=input("u for up, d for down, l for left, r for right, a+the direction you're attacking in(u, d, l, or r) for attack, p for pick up, and i for inventory \n")
    t=world["persons"]["P "].act(world,s)
    print(t.pop("print"))
    world.update(t)
    for i in list(world["persons"]):
        if i!="P ":
            t=world["persons"][i].act(world,world["persons"][i].movement(world["letter"],world["area"]))
            if t["print"]=="Enemy killed":
                print("You died")
                exit()
            if type(t["print"])==int:
                print(t["print"])
            del t["print"]
            world.update(t)