def SimpsonIntegral(lowerbound,upperbound,equation):
    b=upperbound
    a=lowerbound
    midpoint=(upperbound+lowerbound)/2
    SimpsonsRule = (b-a)/6 * (eval(equation,{'x':a}) + 4*(eval(equation,{'x':midpoint})) + eval(equation,{'x':b}))
#    print(SimpsonsRule)
    return SimpsonsRule

def RiemannIntegral(lowerbound,upperbound,equation, iterations):
    bigsum=0
    totalvalue=0
    for i in range(1,iterations+1):
        funkynumber=lowerbound+((i-(1/2))*((upperbound-lowerbound)/iterations))
        bigsum+=(eval(equation,{'x':funkynumber}))
    totalvalue=((upperbound-lowerbound)/iterations)*bigsum
    return totalvalue

def main():
    input1=float(input("Enter the lowerbound: "))
    input2=float(input("Enter the upperbound: "))
    input3=input("Enter the equation in terms of x: ")
    input4=int(input("Enter the number (integer) of iterations: "))
    print(RiemannIntegral(input1,input2,input3,input4))
    input("Press Any Key to Close")
    
if __name__ == "__main__": main()
