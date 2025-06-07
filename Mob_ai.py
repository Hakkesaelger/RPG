from Utility import find_dir
def monster_movement(coordinates:list,player_coordinates:list,letter:dict, area:list):
    diff=(player_coordinates[0]-coordinates[0],player_coordinates[1]-coordinates[1])
    if abs(diff[0])+abs(diff[1])==1:
        return "a "+letter[diff]
    if diff[0] and area[coordinates[0]+find_dir(diff[0])][coordinates[1]]==". ":
        return(letter[(find_dir(diff[0]),0)])
    if area[coordinates[0]][coordinates[1]+find_dir(diff[1])]==". ":
        return(letter[(0,find_dir(diff[1]))])
    if area[coordinates[0]][coordinates[1]-find_dir(diff[1])]==". ":
        return(letter[(0,-find_dir(diff[1]))])
    return(letter[(-find_dir(diff[0]),0)])