'''
Determine if a number is or not a prime


'''

def divisibility(list_):
    ## check for 1
    if list(list_.keys())[0] == 1:
        list_[list(list_.keys())[0]] = "YES"

    ## check for 2
    for num in list_:
        if num != 2:
            if num % 2:
                list_[num] = "YES"
        else: 
            list_[num] = "YES"

    

def check(ni, nf):
    list_ = {i:"NO" for i in range(ni, nf+1)}
    divisibility(list_)
    for elem in list_:
        print(elem, list_.get(elem), sep=":")



check(1, 100)
