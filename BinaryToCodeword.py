##### Call 'f(String)' to translate a binary string to a PAM code, returns a list of pairs '+-1'

# 1 -> -1, 0 -> 1

def f(s):
    res = []
    for c in s:
        if(c == '1'):
            res.append(-1)
        else:
            res.append(1)    
    return res
