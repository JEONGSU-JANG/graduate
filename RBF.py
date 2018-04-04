from scipy import *
from scipy.linalg import norm, pinv
from matplotlib import pyplot as plt
import numpy as np

class RBF:
    def __init__(self, indim, outdim):
        self.indim=indim
        self.outdim=outdim
        self.numStatement=len(indim[0])
        self.numCenters=0
        self.centers=[]
        self.W=[]
        self.sigma=0

    def _sigma(self):
        near=[10000]*self.numCenters
        for i in range(self.numCenters):
            for j in range(self.numCenters):
                if i!=j:
                    dis=self._distance(self.centers[i], self.centers[j])
                    if near[i]>dis:
                        near[i]=dis
        sigma=sum(near)/self.numCenters
        self.sigma=sigma

    def _center(self):
        output=[]
        for cover in self.indim:
            temp=False
            for u in output:
                dis=self._distance(cover, u)
                if(dis<0.1):
                    temp=True
                    break
            if(temp==False):
                output.append(cover)

        self.numCenters=len(output)
        self.centers=output


    def _distance(self, c, u):  
        ci, ui, cui=0, 0, 0
        for i in range(self.numStatement):
            ci=ci+c[i]**2
            ui=ui+u[i]**2
            cui=cui+c[i]*u[i]
        cos=cui/(sqrt(ci*ui))
        return sqrt(1-cos)


    def _basicfunc(self, c, u):
        dis=self._distance(c, u)
        return exp(-(dis**2)/(2*(self.sigma**2)))

    def train(self):
        self._center()
        self._sigma()
        G=[]
        for i in range(len(self.indim)):
            A=[]
            for j in range(len(self.centers)):
                A.append(self._basicfunc(self.indim[i], self.centers[j]))
            G.append(A)
        self.W=dot(pinv(G), self.outdim)


    def test(self, X):
        vt=eye(X)
        G=[]
        for i in range(len(vt)):
            A=[]
            for j in range(len(self.centers)):
                A.append(self._basicfunc(vt[i], self.centers[j]))
            G.append(A)
        Y=dot(G, self.W)
        return Y






















#for swap
def swap(x, i, j):
    x[i],x[j]=x[j],x[i]


def quicksort(x, index, left, right): #left is left index, right is right index ex)x[1,2,3,4,5]-> left=0, right=4
    pivot=left
    j=pivot

    if(left<right): #if the left is smaller than right.=> if left==right, the function will be stop.
        for i in range(left+1, right+1):
            # starting with i+1, we will check all value in array 'x'
            # for ascending, if x[i]<x[pivot], we will swap x[i] and x[j], because j is smaller than i always.
            if(x[i]<x[pivot]):
                j=j+1
                swap(x, i, j)
                swap(index, i, j)

        swap(x, left, j) # swap x[pivot] and x[j] for complete
        swap(index, left, j)
        pivot=j

        quicksort(x, index, left, pivot-1) # do again the quicksort with left~pivot-1
        quicksort(x, index, pivot+1, right)  #do again the quicksort with pivot+1~right



if __name__=="__main__":
   
    intrain = [[1,1,1,1,0,1,0,0,1,1],
               [1,0,0,1,1,0,1,0,0,1],
               [1,1,1,0,0,1,0,0,1,1],
               [1,0,1,0,0,1,1,0,1,1],
               [1,1,1,0,1,0,0,0,1,0],
               [1,1,1,1,0,0,0,1,1,1],
               [1,0,1,1,1,1,1,1,0,1]]

    outtrain = [[0],
                [0],
                [0],
                [0],
                [0],
                [1],
                [1]]
    
    rbf = RBF(intrain, outtrain)
    rbf.train()
    z=rbf.test(len(intrain[0]))
    print "Suspiciousness :", z
    index=[]
    for i in range(len(z)):
        index.append(i+1)
    quicksort(z, index, 0, len(z)-1)
    index.reverse()
    print "Ranking :", index
    print " "
    print "sigma :", rbf.sigma
    print " "
    print "Number of Centers :", rbf.numCenters
    print "centers :", rbf.centers
    print " "
    print "weight :", rbf.W
