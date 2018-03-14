from scipy import *
from scipy.linalg import pinv
import sys
import openpyxl


class RBF:
    def __init__(self, indim, outdim):
        self.indim=indim
        self.outdim=outdim
        self.numTest=len(indim)
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
        temp=sqrt(ci*ui)
        if(temp!=0):
            cos=double(cui/temp)
        else:
            cos=0
        return sqrt(1-cos)


    def _basicfunc(self, c, u):
        dis=self._distance(c, u)
        return exp(-(dis**2)/(2*(self.sigma**2)))

    def train(self):
        self._center()
        print "center :",self.numCenters
        self._sigma()
        print "sigma :",self.sigma
        G=[]
        for i in range(self.numTest):
            A=[]
            for j in range(self.numCenters):
                A.append(self._basicfunc(self.indim[i], self.centers[j]))
            G.append(A)
        self.W=dot(pinv(G), self.outdim)
        print "weight :",self.W


    def test(self):
        j=0
        k=1
        Y=[]
       
        while(True):
            if(j==self.numStatement):
                break        
            
            temp=[0 for value in range(self.numStatement)]
            temp[j]=j
                
            A=[]
            for i in range(self.numCenters):
                A.append(self._basicfunc(temp, self.centers[i]))

            Y.append([dot(A, self.W),k])
            print "Suspicious ",k," :",dot(A,self.W)
            j=j+1
            k=k+1

        return Y




#for swap
def swap(x, i, j):
    x[i],x[j]=x[j],x[i]


def quicksort(x, left, right): #left is left index, right is right index ex)x[1,2,3,4,5]-> left=0, right=4
    pivot=left
    j=pivot

    if(left<right): #if the left is smaller than right.=> if left==right, the function will be stop.
        for i in range(left+1, right+1):
            # starting with i+1, we will check all value in array 'x'
            # for ascending, if x[i]<x[pivot], we will swap x[i] and x[j], because j is smaller than i always.
            if(x[i]>x[pivot]):
                j=j+1
                swap(x, i, j)

        swap(x, left, j) # swap x[pivot] and x[j] for complete
        pivot=j

        quicksort(x, left, pivot-1) # do again the quicksort with left~pivot-1
        quicksort(x, pivot+1, right)  #do again the quicksort with pivot+1~right













def weightFileOpen(outtrain, source):
    f=open(source, "r")

    while True:
        line=f.readline()
        if not line: break
        temp=line.split("\n")
        outtrain.append([float(temp[0])])
    f.close()


def traceFileOpen(intrain, outtrain, fileN, version):
    excel_document=openpyxl.load_workbook(filename=fileN, read_only=True)
    ver='v'+str(version)
    sheet=excel_document.get_sheet_by_name(ver)

    Matrix=[]
    tempM=[]
    for row in sheet.iter_rows():
        for cell in row:
            cell_text=cell.value
            tempM.append(cell_text)
        Matrix.append(tempM)
        tempM=[]

    rows=len(Matrix)
    columns=len(Matrix[0])

    tempIn=[]

    for c in range(2, columns):
        for r in range(2, rows-1):
            if Matrix[r][c]==0L or Matrix[r][c]=="0":
                tempIn.append(0)
            elif Matrix[r][c]==1L or Matrix[r][c]=="1":
                tempIn.append(1)

        if tempIn!=[]:
            intrain.append(tempIn)
        tempIn=[]

    for c in range(2, columns):
        if Matrix[rows-1][c]=="PASS":
            outtrain.append([0])
        elif Matrix[rows-1][c]=="FAIL":
            outtrain.append([1])

if __name__=="__main__":
    sys.setrecursionlimit(1000000000)

    version=1
    while(version<4):
        intrain=[]
        outtrain=[]
        fileN="C:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBFtest/printtokens/printtokens.xlsx"
        print fileN
        traceFileOpen(intrain, outtrain, fileN, version)

        outtrain=[]
        source="C:/Users/Jeongsu Jang/Desktop/2018-1/paper/pageRankTest/printtokens/v"+str(version)+".txt"
        weightFileOpen(outtrain,source)

        LOC=len(intrain[0])
        rbf = RBF(intrain, outtrain)
        print "training start"
        rbf.train()
        z=rbf.test()

        save='C:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBFtest/printtokens/Weight_v'+str(version)+'.txt'
        f=open(save, 'w+')

        quicksort(z, 0, LOC-1)
        print "Ranking---------------"
        for i in range(LOC):
            print z[i][1]
            ranking=str(z[i][1]) + "\n"
            f.write("suspiciousness:"+str(z[i][0])+":number:"+ranking)

        f.close()
        version=version+1
