##### Call 'f(String)' to translate a binary string to a PAM code, returns a list of pairs '+-1'

# 1 -> -1, 0 -> 1

def f(s):
    string = ""
    temp = "" 
    for c in s:
        if(c == '1'):
            c = '-1'
        else:
            c = '1'    
        temp = string + c
        string = temp
    return string
