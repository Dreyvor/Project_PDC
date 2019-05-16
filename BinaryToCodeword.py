##### Call 'binaryToCodeword(String)' to translate a binary string to a 4-QAM code, returns a list of pairs '(+-1, +-1)'

# 4-QAM : c0 = (1,1), c1 = (1, -1), c2 = (-1, -1), c3 = (-1, 1)
# 00->c0, 01->c1, 10->c2, 11->c3

c0 = (1,1)
c1 = (1,-1)
c2 = (-1,-1)
c3 = (-1,1)

lBinPair = []

def binaryToCodeword(s):
    lBinPair = makePair(s) #add bits by pair in lBinPair
    
    lres = changeToCodeword(lBinPair)
    
    return lres
    
def makePair(s):
    lTemp = []
    counter = 0
    temp = -1
    for bit in s:
        counter += 1
        if(counter%2 != 0):
            temp = bit
        else:
            lTemp.append((temp, bit))
            temp = -1
    return lTemp
    
def changeToCodeword(l):
    lTemp = []
    lBinTemp = l.copy()
    for x in lBinTemp: #change pair to respective codewords
        lTemp.append(pairToCodeword(x))
    return lTemp
    
def pairToCodeword(x):
    if(x == ('0','0')):
        return c0
    elif(x == ('0','1')):
        return c1
    elif(x == ('1','0')):
        return c2
    else:
        return c3;