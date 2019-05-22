##### Call 'f(String)' to translate a PAM code to a binary string, return a binary string

# -1 -> 1, 1 -> 0

def f(s):
    string = ""
    temp = ""
    for c in s:
        if(c == -1):
            c = '1'
        else:
            c = '0'
            
        temp = string + c
        string = temp
        
    return string 
