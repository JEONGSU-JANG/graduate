from scipy import *
from scipy.linalg import pinv
import sys
import openpyxl
import pagerank
import pagerankSuccess
import time
from operator import eq



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
        self._sigma()
        G=[]
        for i in range(self.numTest):
            A=[]
            for j in range(self.numCenters):
                A.append(self._basicfunc(self.indim[i], self.centers[j]))
            G.append(A)
        self.W=dot(pinv(G), self.outdim)


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



def weightInput(LOC, intrain, outtrain, fail, success):
    failfile=open(fail, "r")
    successfile=open(success,"r")
    N=0
    failtrain=[]

    while True:
        failline = failfile.readline()
        if not failline: break
        temp = failline.split("\n")
        failtrain.append(float(1)*float(temp[0]))

    successtrain=[]

    while True:
        successline = successfile.readline()
        if not successline: break
        temp = successline.split("\n")
        successtrain.append(float(1)*float(temp[0]))

    newintrain=[]

    while True:
        if N==len(outtrain): break
        if outtrain[N][0]==1:
            newintrain.append(failtrain)
        else:
            newintrain.append(successtrain)
        N=N+1

    return newintrain


def weightOutput(outtrain, fail, success):
    failfile=open(fail, "r")
    successfile=open(success, "r")
    testNum=len(outtrain)
    N=0
    temptrain=[]


    while (N<testNum):
        if outtrain[N][0]==1:
            failline=failfile.readline()
            if not failline: break
            temp=failline.split("\n")
            temptrain.append([float(1)*float(temp[0])])

        else:
            successline=successfile.readline()
            if not successline: break
            temp=successline.split("\n")
            temptrain.append([float(0)*float(temp[0])])

        N=N+1

    failfile.close()
    successfile.close()
    return temptrain


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
    c=2
    while(Matrix[rows-1][c]=="PASS" or Matrix[rows-1][c]=="FAIL"):
        for r in range(2, rows-1):
            if Matrix[r][c]==1L or Matrix[r][c]=="1":
                tempIn.append(1)
            else:
                tempIn.append(0)

        intrain.append(tempIn)
        tempIn=[]
        c=c+1

    for c in range(2, columns):
        if Matrix[rows-1][c]=="PASS":
            outtrain.append([0])
        elif Matrix[rows-1][c]=="FAIL":
            outtrain.append([1])

def extractFailureIntrain(intrain, outtrain):
    tempin=[]
    intt=0
    outt=0
    while True:
        if outt==len(outtrain):
            break
        if outtrain[outt][0]==1:
            tempin.append(intrain[intt])
        intt=intt+1
        outt=outt+1
    return tempin

def extractSuccessIntrain(intrain, outtrain):
    tempin=[]
    intt=0
    outt=0
    while True:
        if outt==len(outtrain):
            break
        if outtrain[outt][0]==0:
            tempin.append(intrain[intt])
        intt=intt+1
        outt=outt+1
    return tempin


if __name__=="__main__":
    start_time=time.time()
    sys.setrecursionlimit(1000000000)

    version=1
    while(version<=41):
        if version==38:
            version=version+1

        start_time=time.time()
        fileintrain=[]
        intrain = []
        outtrain = []
        cover=[]
        MM=[]
        temp=[]

        fileN = "C:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/experiment/tcas/tcas.xlsx"
        print fileN
        print "version"+str(version)

        traceFileOpen(fileintrain, outtrain, fileN, version)
        intrain=extractSuccessIntrain(fileintrain, outtrain)

        LOC = len(intrain[0])
        numTest=len(intrain)

        MM=[]
        for i in range(0, LOC):
            for j in range(0, LOC):
                temp.append(0)
            MM.append(temp)
            temp=[]

        MM[157][48]=1
        MM[75][56]=1
        MM[79][56]=1
        MM[93][56]=1
        MM[97][56]=1
        MM[90][61]=1
        MM[126][66]=1
        MM[127][84]=1
        MM[75][102]=1
        MM[93][102]=1
        MM[126][102]=1
        MM[97][107]=1
        MM[127][107]=1
        MM[171][112]=1
        MM[72][61]=1


        for i in range(0, LOC):
            for j in range(0, LOC):
                if MM[i][j]!=0:
                    MM[j][i]=MM[i][j]

        for i in range(0, LOC):
            for j in range(0, numTest):
                temp.append(intrain[j][i])
            cover.append(temp)
            temp=[]


        print "start pagerankSuccess"
        pr=pagerankSuccess.pagerankSuccess(cover,MM)
        pr.calCompute()
        pr.calNormalized()


        save='C:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/experiment/tcas/SuccessTestv'+str(version)+'.txt'
        f=open(save, 'w+')
        for i in range(0, numTest):
            f.write(str(pr.norTest[i][0])+"\n")

        f.close()

        save='C:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/experiment/tcas/SuccessXv'+str(version)+'.txt'
        f=open(save, 'w+')
        for i in range(0, LOC):
            f.write(str(pr.norX[i])+"\n")
        f.close()



        intrain=[]
        print fileN
        intrain=extractFailureIntrain(fileintrain, outtrain)

        LOC = len(intrain[0])
        numTest=len(intrain)

        cover=[]
        for i in range(0, LOC):
            for j in range(0, numTest):
                temp.append(intrain[j][i])
            cover.append(temp)
            temp=[]

        print "start pagerank"
        pr=pagerank.pageRank(cover,MM)
        pr.calCompute()
        pr.calNormalized()

        save='C:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/experiment/tcas/Testv'+str(version)+'.txt'
        f=open(save, 'w+')
        for i in range(0, numTest):
            f.write(str(pr.norTest[i][0])+"\n")

        f.close()

        save='C:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/experiment/tcas/Xv'+str(version)+'.txt'
        f=open(save, 'w+')
        for i in range(0, LOC):
            f.write(str(pr.norX[i])+"\n")

        f.close()


        fail="c:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/experiment/tcas/Xv"+str(version)+".txt"
        success="c:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/experiment/tcas/SuccessXv"+str(version)+".txt"
        intrain=weightInput(LOC, fileintrain, outtrain, fail, success)

        fail = "C:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/experiment/tcas/Testv" + str(
            version) + ".txt"
        success = "C:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/experiment/tcas/SuccessTestv" + str(
            version) + ".txt"
        outtrain = weightOutput(outtrain, fail, success)

        rbf = RBF(intrain, outtrain)
        print "training start"
        rbf.train()
        z=rbf.test()

        save='C:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/experiment/tcas/newWeight_v'+str(version)+'.txt'
        f=open(save, 'w+')
        quicksort(z, 0, LOC-1)
        for i in range(LOC):
            ranking=str(z[i][1]) + "\n"
            f.write("suspiciousness:"+str(z[i][0])+":number:"+ranking)
        f.close()

        timefile = "C:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/experiment/tcas/timefile2.txt"
        f = open(timefile, 'a')
        t=time.time()-start_time
        f.write(str(t)+"\n")
        f.close()



        print(time.time()-start_time)

        version=version+1
