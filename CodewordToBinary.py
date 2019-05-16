##### Call 'f(String)' to translate a 4-QAM code to a binary string, return a binary string

# 4-QAM : c0 = (1,1), c1 = (1, -1), c2 = (-1, -1), c3 = (-1, 1)
# 00->c0, 01->c1, 10->c2, 11->c3

def f(codes):
    lTemp = []
    for pair in codes:
        lTemp.append(codewordToBinary(pair))
    
    return "".join(lTemp)
    
    
def codewordToBinary(x):
    if(x == (1,1)):
        return "00"
    elif(x == (1,-1)):
        return "01"
    elif(x == (-1,-1)):
        return "10"
    else:
        return "11";