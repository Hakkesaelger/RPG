from Actions import Person,spawnNpc
world={
    "items":{},
    "persons":{"P":[Person(100,[],{"min_damage":1,"max_damage":6,"armor":2,"speed":1},[4,2],"P"),"Player"]},
    "direc":{"u":[-1,0],"d":[1,0],"l":[0,-2],"r":[0,2]},
    "letter":{(-1,0):"u",(1,0):"d",(0,-2):"l",(0,2):"r",(0,0):None}}
i=spawnNpc(True, world["persons"]["P"][0],5,[],{"min_damage":1,"max_damage":4,"armor":1.5,"speed":1},[0,2],"M",world,{100:[]},"Ork")
if i:
    world["persons"]=i["persons"]
    area=open("playArea.txt","w")
    for j in i["area"]:
        area.write(j.strip()+"\n")
    area.close()
while True:
    print("Make an action! Move Up, Down, Left, or Right, make an attack, or make an inventory interaction")
    s=input("u for up, d for down, l for left, r for right, a+the direcection you're attacking in(u, d, l, or r) for attack, and i for inventory \n")
    t=world["persons"]["P"][0].act(world,s)
    print(t.pop("print"))
    if "area" in t:
        area=open("playArea.txt","w")
        for i in t["area"]:
            area.write(i.strip()+"\n")
        area.close()
        del t["area"]
    world.update(t)
    for i in list(world["persons"]):
        if i!="P":
            t=world["persons"][i][0].act(world,world["persons"][i][0].movement(world["letter"],world["direc"]))
            print(t["print"] if t["print"]=="Enemy killed" else "")
            if t["print"]=="You died":
                print(t["print"])
                exit()
            if type(t["print"])==int:
                print(t["print"])
            del t["print"]
            if "area" in t.keys():
                area=open("playArea.txt","w")
                for i in t["area"]:
                    area.write(i.strip()+"\n")
                area.close()
                del t["area"]
            world.update(t)