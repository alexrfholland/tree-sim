import math
def GetStreamKey(value, append):
        
    streamMax = 40
    streamDivision = 5
    if(value > streamMax):
        value = streamMax
    val = math.floor(value/streamDivision)

    key = f'{val}+{append}'
    return key
 
streamMax = 40
streamDivision = 5

r = streamMax/streamDivision

for i in range(int(streamMax/streamDivision)+1):
        key = f'{i}+t'
        key2 = f'{i}+i'
        print(key)
        print(key2) 


