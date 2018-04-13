from scipy import *
import numpy as np
import sys
import openpyxl

class pagerankSuccess:

    def __init__(self, cover, MM):
        self.damping=0.7
        self.epsilon=1
        self.cover=cover
        self.alpha=0.001
        self.MM=MM
        self.Pmm=[]
        self.Ptm=[]
        self.Pmt=[]
        self.P=[]
        self.x=[]
        self.norX=[]
        self.norTest=[]

    def caldistance(self, c, u):
        length=len(c)
        ci, ui, cui = 0, 0, 0
        for i in range(length):
            ci = ci + c[i] ** 2
            ui = ui + u[i] ** 2
            cui = cui + c[i] * u[i]
        temp = sqrt(ci * ui)
        if (temp != 0):
            cos = double(cui / temp)
        else:
            cos = 0
        return sqrt(1 - cos)

    def calvector(self):
        plen=len(self.cover[0])+len(self.cover)
        vector=[]

        for i in range(0, plen):
            vector.append(float(1)/float(plen))

        return vector


    def calPmm(self):
        N=len(self.MM)
        self.Pmm=[]
        temp=[]

        for i in range(0, N):
            for j in range(0, N):
                temp.append(float(self.alpha)*float(self.MM[i][j]))
            self.Pmm.append(temp)
            temp=[]


    def calPtm(self):

        numTest=len(self.cover[0])
        numMethod=len(self.cover)
        d=np.zeros(numTest)

        for i in range(0, numTest):
            for j in range(0, numMethod):
                if self.cover[j][i]==1:
                    d[i]=d[i]+1

        temp=[]
        for i in range(0, numMethod):
            for j in range(0, numTest):
                if d[j]!=0:
                    temp.append(float(float(self.cover[i][j])/float(d[j])))
                else:
                    temp.append(0)
            self.Ptm.append(temp)
            temp=[]



    def calPmt(self):

        numTest=len(self.cover[0])
        numMethod=len(self.cover)
        d=np.zeros(numMethod)

        for i in range(0, numMethod):
            for j in range(0, numTest):
                if self.cover[i][j]==1:
                    d[i]=d[i]+1

        temp=[]
        for i in range(0, numTest):
            for j in range(0, numMethod):
                if d[j]!=0:
                    temp.append(float(float(self.cover[j][i])/float(d[j])))
                else:
                    temp.append(0)
            self.Pmt.append(temp)
            temp=[]

    def calP(self):
        self.calPmm()
        self.calPtm()
        self.calPmt()

        numTest=len(self.cover[0])
        numMethod=len(self.cover)
        pLen=numMethod+numTest

        count=0

        temp=[]
        while (count<numMethod):

            for i in range(0, numMethod):
                temp.append(float(0.01)*float(self.MM[count][i]))
            for i in range(0, numTest):
                temp.append(self.Ptm[count][i])
            self.P.append(temp)
            temp=[]
            count=count+1

        for i in range(0, numTest):
            for j in range(0, numMethod):
                temp.append(self.Pmt[i][j])
            for j in range(0, numTest):
                temp.append(float(0))
            self.P.append(temp)
            temp=[]

    def calCompute(self):

        self.calP()
        plen=len(self.P)
        vector=self.calvector()
        x0=[]
        for i in range(0, plen):
            x0.append(float(0))

        counting=1

        while True:

            temp = dot(self.P, x0)
            temp1 = []
            for i in range(0, plen):
                temp1.append(self.damping * temp[i])
            temp2 = []
            for i in range(0, plen):
                temp2.append((1 - self.damping) * vector[i])
            x1 = []
            for i in range(0, plen):
                x1.append(temp1[i] + temp2[i])

            dist = self.caldistance(x1, x0)
            if dist < self.epsilon:
                break
            else:
                x0 = x1
                counting=counting+1
                for i in range(0, plen):
                    vector[i]=vector[i]**counting

        self.x=x1

    def calNormalized(self):
        numMethod=len(self.cover)
        numTest=len(self.cover[0])

        max=0
        for i in range (numMethod):
            if max<self.x[i]:
                max=self.x[i]

        for i in range(numMethod):
            self.norX.append(self.x[i]/max)

        max=0
        for j in range (numMethod, numMethod+numTest):
            if max<self.x[j]:
                max=self.x[j]

        for j in range(numMethod, numMethod+numTest):
            self.norTest.append([self.x[j]/max])

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

    c = 2
    while (True):
        if Matrix[rows - 1][c] != "FAIL" and Matrix[rows - 1][c] != "PASS":
            break

        if Matrix[rows - 1][c] == "FAIL":
            outtrain.append([1])
        else:
            outtrain.append([0])
        for r in range(2, rows - 1):
            if Matrix[r][c] == "0" or Matrix[r][c] == 0L:
                tempIn.append(0)
            elif Matrix[r][c] == "1" or Matrix[r][c] == 1L:
                tempIn.append(1)
            else:
                tempIn.append(0)

        if tempIn != []:
            intrain.append(tempIn)
        tempIn = []
        c = c + 1

if __name__=='__main__':
    sys.setrecursionlimit(1000000000)

    version = 1
    while(version<38):
        intrain = []
        outtrain = []
        fileN = "C:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/experiment/schedule/schedule.xlsx"
        print fileN
        print "version"+str(version)
        traceFileOpen(intrain, outtrain, fileN, version)

        intrain=extractSuccessIntrain(intrain, outtrain)

        LOC = len(intrain[0])
        numTest=len(intrain)

        temp=[]
        MM=[]
        for i in range(0, LOC):
            for j in range(0, LOC):
                temp.append(0)
            MM.append(temp)
            temp=[]


        cover=[]

        for i in range(0, LOC):
            for j in range(0, numTest):
                temp.append(intrain[j][i])
            cover.append(temp)
            temp=[]

        pr=pagerankSuccess(cover,MM)
        pr.calCompute()
        pr.calNormalized()


        save='C:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/experiment/schedule/SuccessTestv'+str(version)+'.txt'
        f=open(save, 'w+')
        for i in range(0, numTest):
            f.write(str(pr.norTest[i][0])+"\n")

        f.close()

        save='C:/Users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/experiment/schedule/SuccessXv'+str(version)+'.txt'
        f=open(save, 'w+')
        for i in range(0, LOC):
            f.write(str(pr.norX[i])+"\n")

        f.close()
        version=version+1

