#Riemann Integration Technique adapted from
#https://www.instructables.com/id/How-to-Make-a-Numerical-Integration-Program-in-Pyt/
#The more complicated the integral the more interations you want. 10000 is a good bet
def RI(lowerbound,upperbound,equation, iterations):
    bigsum=0
    totalvalue=0
    for i in range(1,iterations+1):
        funkynumber=lowerbound+((i-(1/2))*((upperbound-lowerbound)/iterations))
        bigsum+=(eval(equation,{'x':funkynumber}))
    totalvalue=((upperbound-lowerbound)/iterations)*bigsum
    return totalvalue

#equation must be a string (in ""), shouldequal is the LHS of the equation (integral evaluates to what?), intits is number integration iterations for RI function
def UBS(lowerbound, initialguess, equation, shouldequal, intits): #Upperbound Solver
    count=0
    printcount=0
    triescounter=0
    upperbound=initialguess
    upperbounddelta=(upperbound+lowerbound)/2
    check0=RI(lowerbound, 0, equation, intits)
    print("check0 =",check0)
    if shouldequal-.01 < check0 and check0 < shouldequal+.01:
        print("probably equals 0")
        return [0,check0]
    else:
        while count<1000:
            if printcount==20:
                print("Upperbound =",upperbound,"result =",result)
                printcount=0
                triescounter+=1
                if triescounter==10:
                    print("count =", count)
                    triescounter=0
            result=RI(lowerbound, upperbound, equation, intits)
            if  shouldequal - result > 0: #evaluates to positive, means x in result(x) should increase
                upperbound+=upperbounddelta
            elif shouldequal - result < 0: #evaluates to negative, means x in result(x) should decrease
                #print("You have to go back!")
                upperbound-=upperbounddelta
                upperbounddelta=upperbounddelta/2
            elif shouldequal - result == 0:
                print("Exactly Done! Upperbound =",upperbound,"result =",result)
                break
            if shouldequal-.000001 < result and result < shouldequal+.000001:
                        print("Close enough! Upperbound =",upperbound,"result =",result)
                        break
            count+=1
            printcount+=1
        if count==1000: print("ran out of tries")
        else: return [upperbound, result]
def LBS(initialguess, upperbound, equation, shouldequal, intits): #Lowerbound Solver
    count=0
    printcount=0
    triescounter=0
    lowerbound=initialguess
    lowerbounddelta=(upperbound+lowerbound)/2
    check0=RI(0, upperbound, equation, intits)
    print("check0 =",check0)
    if shouldequal-.01 < check0 and check0 < shouldequal+.01:
        print("probably equals 0")
        return [0,check0]
    else:
        while count<100:
            if printcount==20:
                print("Lowerbound =",lowerbound,"result =",result)
                printcount=0
                triescounter+=1
                if triescounter==10:
                    print("count =", count)
                    triescounter=0
            result=RI(lowerbound, upperbound, equation, intits)
            if  shouldequal - result > 0: #evaluates to positive, means x in result(x) should decrease
                lowerbound-=lowerbounddelta
            elif shouldequal - result < 0: #evaluates to negative, means x in result(x) should increase
                #print("You have to go back")
                lowerbound+=lowerbounddelta
                lowerbounddelta=lowerbounddelta/2
            elif shouldequal - result == 0:
                print("Done! Lowerbound =",lowerbound,"result =",result)
                break
            if shouldequal-.000001 < result and result < shouldequal+.000001:
                        print("Close enough! Lowerbound =",lowerbound,"result =",result)
                        break
            count+=1
            printcount+=1
        if count==100: print("ran out of tries")
        else: return [lowerbound, result]
"end defs"
def main():
    print("test equations")
    #UBS(0, 6, ".5*x**2", 562.5, 10000) #answer should be 15
    #UBS(0,.3,"(1+30*(1-x)**2)/(.01*(1-x))",1021.7968,1000) #answer should be 0.4054686
    #UBS(6,10, ".5*x**2", -36, 1000) #should equal 0
    #UBS(0, .2,"1/(1.28*(1-x)-.557*x)", 1.3636, 10000) #answer should be .639873, note that if intits is 1,000 and not 10,000, a wrong answer will result

    #LBS(6, 10, ".5*x**2", 166.667, 1000) #answer should be 0
    #LBS(.4,.40547,"(1+30*(1-x)**2)/(.01*(1-x))",1021.7968,10000) #answer should be 0
    #LBS(14, 15, ".5*x**2", 526.5, 1000) #answer should be 6
    #LBS(0, .5,"1/(1.28*(1-x)-.557*x)", .604, 10000) #should equal .1
if __name__ == "__main__": main()
