def one_pound(c1, c2, c3):
    D = {}
    i = 0
    for n1 in range(100 // c1 + 1):
        for n2 in range(100 // c2 + 1):
            # for n3 in range(100//c3+1): #this works as well!
            # if n1*c1+n2*c2+n3*c3==100:
            rest = 100 - n1 * c1 - c2 * n2
            if rest >= 0 and rest % c3 == 0:
                D[i] = (n1, n2, rest // c3)
                i += 1
    return D


D = one_pound(10, 5, 2)
print(D)
