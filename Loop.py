from Actions import Person,spawn_npc
from Utility import generate_board
print("\n"*100)
world={
    "persons":{"P ":Person(100,[],{"min_damage":1,"max_damage":6,"armor":2,"speed":1},[0,1],"P ")},
    "direc":{"u":[-1,0],"d":[1,0],"l":[0,-1],"r":[0,1]},
    "letter":{(-1,0):"u",(1,0):"d",(0,-1):"l",(0,1):"r",(0,0):None},
    "area":[[". ","P ",". ",". ",". ",". ",],
        [". ","W ",". ",". ",". ",". ",],
        [". ",". ","W ",". ",". ",". ",],
        [". ",". ",". ",". ",". ",". ",],
        [". ",". ",". ",". ",". ",". ",],
        [". ",". ",". ",". ",". ",". ",]],}
i=spawn_npc(True, world["persons"]["P "],5,[],{"min_damage":1,"max_damage":4,"armor":1.5,"speed":1},[2,1],"M ",world,{100:[]})
if i:
    world["persons"]=i["persons"]
    world["area"]=i["area"]
while True:
    print(generate_board(world["area"]))
    print("Make an action! Move Up, Down, Left, or Right, make an attack, pick up an item on the ground, or make an inventory interaction")
    s=input("u for up, d for down, l for left, r for right, a+the direcection you're attacking in(u, d, l, or r) for attack, p for pick up, and i for inventory \n")
    t=world["persons"]["P "].act(world,s)
    print(t.pop("print"))
    world.update(t)
    for i in list(world["persons"]):
        if i!="P ":
            t=world["persons"][i].act(world,world["persons"][i].movement(world["letter"],world["area"],world["direc"]))
            print(t["print"] if t["print"]=="Enemy killed" else "")
            if t["print"]=="You died":
                print(t["print"])
                exit()
            if type(t["print"])==int:
                print(t["print"])
            del t["print"]
            world.update(t)