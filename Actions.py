from random import random
from math import ceil
from Utility import generate_board, bitwise_add, find_dir
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
        persons,direc,letter, area,=world.values()
        if s in ["u","d","l","r"]:
            for i in range(0,self.equipped["speed"]):
                t=self.move(area,direc[s])
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
            t=bitwise_add(self.coordinate, direc[s[2]],True)
            name=area[t[0]][t[1]]
            if not name in persons:
                return {"print":"No enemy to attack"}
            u=persons[name]
            u.health=self.attack(u)
            if u.health<=0:
                area[t[0]][t[1]]=". "
                return {"print":"Enemy killed" if u!="P " else "You died","area":area,"persons":persons}
            return{"print":u.health}
class NPC(Person):
    def __init__(self,kill:bool,follow:Person,health:int, inventory:list, equipped:dict,coordinate:list,name:str,loot:dict):
        super().__init__(health, inventory, equipped,coordinate,name)
        self.kill=kill
        self.follow=follow
        self.loot=loot
    def movement(self,letter:dict, area:list,direc:dict):
        diff=bitwise_add(self.follow.coordinate,self.coordinate,False)
        if abs(diff[0])+abs(diff[1])==1 and self.kill:
            return "a "+letter[tuple(diff)]
        r=random()
        possible=set()
        for i in direc.keys():
            if 0<=self.coordinate[0]+direc[i][0]<=5 and 0<=self.coordinate[1]+direc[i][1]<=5:
                if area[self.coordinate[0]+direc[i][0]][self.coordinate[1]+direc[i][1]]==". ":
                    possible.add(i)
        want={letter[(find_dir(diff[0]),0)],letter[(0,find_dir(diff[1]))]}
        will=list(possible & want)
        if r<0.5 and len(will)==2:
            return will[1]
        if len(will)>0:
            return will[0]
        will=list(possible)
        if r<0.5 and len(will)==2:
            return will[1]
        if len(will)>0:
            return will[0]
def spawn_npc(kill:bool,follow:Person,health:int, inventory:list, equipped:dict,coordinate:list,name:str,world:dict,loot:dict):
    if world["area"][coordinate[0]][coordinate[1]]==". ":
        world["persons"][name]=NPC(kill,follow,health,inventory,equipped,coordinate,name,loot)
        world["area"][coordinate[0]][coordinate[1]]=name
    return {"persons":world["persons"],"area":world["area"]}