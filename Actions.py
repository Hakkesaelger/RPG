from random import random
from math import ceil
for i in range(1,101):
    print("")
world={
    "dir":{"u":[-1,0],"d":[1,0],"l":[0,-1],"r":[0,1]},
    "area":[["P ","E ","E ","E ","E ","E ",],
        ["E ","E ","E ","O ","E ","E ",],
        ["E ","M ","E ","E ","E ","E ",],
        ["E ","E ","E ","E ","E ","E ",],
        ["E ","E ","E ","E ","E ","E ",],
        ["E ","E ","E ","E ","E ","E ",]],
    "coordinate":{"P ":[0,0],"M ":[2,1]},
    "health":{"P ":100,"M ":5},
    "inventory":{"P ":[],"M ":[]},
    "equipped":{"P ":[1,6,2,1],"M ":[1,4,1.5,1]}}

def move(lenght:list, who:str, coordinate:dict, area:dict):
        if coordinate[who][0]+lenght[0]>5:
            return [5,coordinate[who][1]+lenght[1],"Out of bounds"]
        if coordinate[who][1]+lenght[1]>5:
            return [coordinate[who][0]+lenght[0],5,"Out of bounds"]
        if coordinate[who][0]+lenght[0]<0:
            return [0,coordinate[who][1]+lenght[1],"Out of bounds"]
        if coordinate[who][1]+lenght[1]<0:
            return [coordinate[who][0]+lenght[0],0,"Out of bounds"]
        if (area[coordinate[who][0]+lenght[0]][coordinate[who][1]+lenght[1]]!="E "):
            return coordinate[who][0],coordinate[who][1],"Already occupied"
        return [coordinate[who][0]+lenght[0], coordinate[who][1]+lenght[1],""]

def attack(weapon:list, health:int, armor:int):
    return health-ceil((random()*weapon[1]+weapon[0]-1)/armor) 

#assumes equal len
def bitwise_add(list1:list, list2:list):
    res=[]
    for i in range(0,len(list1)):
        res.append(list1[i]+list2[i])
    return res

def generate_board(list:list):
    board=""
    for row in list:
        board+="".join(row)
        board+="\n"
    return board


def action(game:dict, s:str,actor:str):
    dir,area,coordinate,health,inventory,equipped=game
    if s=="u" or "d" or "l" or "r":
        for i in range(0,equipped[actor][3]):
            t=move(dir[s],actor,coordinate,area)
            area[coordinate[actor][0]][coordinate[actor][1]]="E "
            area[t[0]][t[1]]=actor
            coordinate[actor]=[t[0],t[1]]
            return {"error":t[3],"coordinate":coordinate,"area":area}
    elif s[0]=="a":
        t=bitwise_add(coordinate[actor], dir(s[2]))
        name=area[t[0]][t[1]]
        if name=="E " or "O ":
            return{"print":"No enemy to attack"}
        health[name]=attack(equipped[actor],health[name],equipped[name][2])
        if health[name]<=0:
            area[t[0]][t[1]]="E "
            del coordinate[name]
            del health[name]
            del inventory[name]
            del equipped[name]
            return {"print":"Enemy killed","area":area,"coordinate":coordinate,"health":health,"inventory":inventory,"equipped":equipped}
        return{"print":health[name],"health":health}
    else:
        print("invalid action")

while True:
    print(generate_board(world["area"]))
    print("Make an action! Move Up, Down, Left, or Right, make an attack, pick up an item on the ground, or make an inventory interaction")
    s=input("u for up, d for down, l for left, r for right, a+the direction you're attacking in(u, d, l, or r) for attack, p for pick up, and i for inventory \n")
