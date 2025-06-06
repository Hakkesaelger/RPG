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