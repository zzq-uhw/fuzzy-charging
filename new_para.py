import numpy as np
import random
import helics as h

def rand(p):
    R = random.random()
    if(R < p):
        return True
    else:
        return False

def read(p0, p1, p2, p3, p4, p5):
    """read in 6 price to find the 1st and 2nd low price, define a0, a1"""
    global a0,a1
    price = np.array([p0, p1, p2, p3, p4, p5])
    print(price)
    min1 = np.argmin(price)
    price[min1] = 999999
    min2 = np.argmin(price)
    print("min1 and min2 are ", min1, min2)
    
    para_low1 = "para"+ str(min1)
    a0 = np.load(para_low1, allow_pickle=True)
    
    para_low2 = "para"+ str(min2)
    a1 = np.load(para_low2, allow_pickle=True)
    a0.dump('para0')
    a1.dump('para1')

def crossover():
    """do crossover to a0, a1 and form a2, a3"""
    global a2, a3
    a2 = a0
    a3 = a1
    for i in range(27):
        if(rand(0.3)):
            a2[i], a3[i] = a3[i], a2[i]
    a2.dump('para2')
    a3.dump('para3')

def mutation():
    """do mutation to a2, a3 and form a4, a5"""
    global a4, a5
    a4 = a2
    a5 = a3
    for i in range(27):
        if(rand(0.15)):
            a4[i] = np.random.randint(0, 3)
            a5[i] = np.random.randint(0, 3)
    a4.dump('para4')
    a5.dump('para5')

def show():
    ok0 = np.load('para0', allow_pickle=True)
    ok1 = np.load('para1', allow_pickle=True)
    ok2 = np.load('para2', allow_pickle=True)
    ok3 = np.load('para3', allow_pickle=True)
    ok4 = np.load('para4', allow_pickle=True)
    ok5 = np.load('para5', allow_pickle=True)
    print("para0 is ", ok0)
    print("para1 is ", ok1)
    print("para2 is ", ok2)
    print("para3 is ", ok3)
    print("para4 is ", ok4)
    print("para5 is ", ok5)

def main():
    fed = h.helicsCreateValueFederateFromConfig("new_para.json")
    sub_0 = h.helicsFederateGetInputByIndex(fed, 0)
    sub_1 = h.helicsFederateGetInputByIndex(fed, 1)

    hours = 24
    last_sec = int(60 * 60 * 24)
    h.helicsFederateEnterExecutingMode(fed)
    grantedtime = h.helicsFederateRequestTime(fed, last_sec)

    price_0 = h.helicsInputGetDouble(sub_0)
    price_1 = h.helicsInputGetDouble(sub_1)
    print('price_0 at %d is %f' % (grantedtime, price_0))
    print('price_1 at %d is %f' % (grantedtime, price_1))

    h.helicsFederateFinalize(fed)
    h.helicsFederateFree(fed)
    h.helicsCloseLibrary()
    """
    read(1, 25.3, 0, 1.1, 888, 77777)
    crossover()
    mutation()
    show()
    """

if __name__ == '__main__':
    main()
