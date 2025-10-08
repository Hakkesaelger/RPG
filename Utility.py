def bitwiseAdd(list1:list, list2:list,add:bool):
    res=[]
    if add:
        for i in range(0,len(list1)):
            res.append(list1[i]+list2[i])
    else:
        for i in range(0,len(list1)):
            res.append(list1[i]-list2[i])
    return res

def findDir(number):
    if number<0:
        return -1
    if number>0:
        return 1
    if number==0:
        return 0

def findFile(toOpen:str):
    file=open(toOpen,"r")
    txt=file.readlines()
    file.close()
    return txt

def replace(str, index, rep):
    return str[:index]+rep+str[index+1:]