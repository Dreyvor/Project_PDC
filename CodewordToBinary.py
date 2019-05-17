##### Call 'f(String)' to translate a PAM code to a binary string, return a binary string

# -1 -> 1, 1 -> 0

def f(s):
    jump = False
    string = ""
    temp = ""
    for c in s:
        if(jump):
            jump = False
            continue
        if(c == '1'):
            c = '0'
        elif(c == '-'):
            c = '1'
            jump = True
        temp = string + c
        string = temp
    return string 
