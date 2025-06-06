def monster_movement(coordinates:list,player_coordinates:list,letter:dict):
    diff=(player_coordinates[0]-coordinates[0],player_coordinates[1]-coordinates[1])
    if abs(diff[0])+abs(diff[1])==1:
        return "a "+letter[diff]