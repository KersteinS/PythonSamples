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

def MinimumerProvideFunction(start,function,stepsize,countmax):
    count=1
    lastpoint=start
    minimum=None
    while count<countmax:
        lastguess=eval(function,{'x':lastpoint})
        currentpoint=start+stepsize*count
        currentguess=eval(function,{'x':currentpoint})
        nextpoint=currentpoint+stepsize
        nextguess=eval(function,{'x':nextpoint})
        if (lastguess < currentguess and currentguess < nextguess) or (lastguess > currentguess and currentguess > nextguess):
            count+=1
            lastpoint=currentpoint
        else:
            minimum=currentpoint
            print("Success! Count was ",count)
            break
    if count==countmax:
        count=1
        lastpoint=start
        while count<countmax:
            lastguess=eval(function,{'x':lastpoint})
            currentpoint=start-stepsize*count
            currentguess=eval(function,{'x':currentpoint})
            nextpoint=currentpoint-stepsize
            nextguess=eval(function,{'x':nextpoint})
            if (lastguess < currentguess and currentguess < nextguess) or (lastguess > currentguess and currentguess > nextguess):
                count+=1
                lastpoint=currentpoint
            else:
                minimum=currentpoint
                print("Reverse Succeeded! Count was ",count)
                break
    if minimum != None:
        return minimum
    else: 
        print("Minimum not found, function outputs start guess by default")
        return start
def MinimumerProvideList(totalvalues):
    count=1
    while count<len(totalvalues):
        if (totalvalues[count-1][1]<totalvalues[count][1] and totalvalues[count][1]<totalvalues[count+1][1]) or (totalvalues[count-1][1]>totalvalues[count][1] and totalvalues[count][1]>totalvalues[count+1][1]):
            count+=1
        else: 
            minimumpair=[totalvalues[count][0], totalvalues[count][1]]
            break
    if count==len(totalvalues): print("minimum not found")
    else: return minimumpair
def MinimumerWithIntegral(lowerbound, upperbound, function, intits, stepsize, countmax): #currently does not work
    count=1
    start=upperbound
    lastpoint=upperbound
    minimum=None
    while count<countmax:
        lastguess=RI(lowerbound, lastpoint, function, intits)
        currentpoint=start+stepsize*count
        currentguess=RI(lowerbound, currentpoint, function, intits)
        nextpoint=currentpoint+stepsize
        nextguess=RI(lowerbound, nextpoint, function, intits)
        print([lastpoint,lastguess], [currentpoint,currentguess], [nextpoint,nextguess])
        if (lastguess < currentguess and currentguess < nextguess) or (lastguess > currentguess and currentguess > nextguess):
            count+=1
            lastpoint=currentpoint
        else:
            minimum=currentpoint
            print("Success! Count was ",count)
            break
    if count==countmax:
        count=1
        lastpoint=upperbound
        while count<countmax:
            lastguess=RI(lowerbound, lastpoint, function, intits)
            currentpoint=start-stepsize*count
            currentguess=RI(lowerbound, currentpoint, function, intits)
            nextpoint=currentpoint-stepsize
            nextguess=RI(lowerbound, nextpoint, function, intits)
            print([lastpoint,lastguess], [currentpoint,currentguess], [nextpoint,nextguess])
            if (lastguess < currentguess and currentguess < nextguess) or (lastguess > currentguess and currentguess > nextguess):
                count+=1
                lastpoint=currentpoint
            else:
                minimum=currentpoint
                print("Reverse Succeeded! Count was ",count)
                break
    if minimum != None:
        print("Done! minumum =",minimum)
        return minimum
    else: 
        print("Minimum not found, function outputs start guess by default")
        return upperbound

def main() :
    fxn="(x-3)**2+1"
    print(MinimumerProvideFunction(2,fxn,1,100))
"end defs"
if __name__== "__main__": main()
