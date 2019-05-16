##### Call 'binaryToCodeword(String)' to translate a binary string to a 4-QAM code, returns a list of pairs '(+-1, +-1)'

# 4-QAM : c0 = (1,1), c1 = (1, -1), c2 = (-1, -1), c3 = (-1, 1)
# 00->c0, 01->c1, 10->c2, 11->c3

def listCodeToBinary(codes):
    lTemp = []
    for pair in codes:
        lTemp.append(codewordToBinary(pair))
    
    return "".join(lTemp)
    
    
def codewordToBinary(x):
    print("x = ", x)
    if(x == (1,1)):
        return "00"
    elif(x == (1,-1)):
        return "01"
    elif(x == (-1,-1)):
        return "10"
    else:
        return "11";
