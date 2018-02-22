def removeAka(s):
    l = []
    words = s.split()
    for x in words:
        if x=='aka':
            break
        else:
            l.append(x)
    return ' '.join(l)

print removeAka('parker (1998) aka Sparky')
