import openpyxl
from operator import eq

def _rankfile(rankfile):
    rank=[]
    susp=[]
    f=open(rankfile, "r")
    while True:
        line=f.readline()
        if not line: break
        temp=line.split(":")
        rank.append(int(temp[3]))
        susp.append(temp[1])
    f.close()
    return rank,susp

def _ansfile(ans, version):
    excel_document=openpyxl.load_workbook(filename=ans, read_only=True)
    ver='v'+str(version)
    sheet=excel_document.get_sheet_by_name("Sheet1")

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

    r=1
    bug=0
    while(True):
        if Matrix[r][2]=="tcas" and Matrix[r][3]==ver:
            bug=Matrix[r][4]
            break
        else:
            r=r+1

    return bug


if __name__=="__main__":
    version=1
    save="c:/users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/correcting-success2/tcas/WorstExamScore-inputoutputWeight.txt"
    f=open(save, "w")
    while(version<38):
        rankfile="C:/users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/correcting-success2/tcas/input-outputWeighted/Weight_v"+str(version)+".txt"
        ans="c:/users/Jeongsu Jang/Desktop/2018-1/paper/RBF+pageRank/correcting-success2/20170621_AnswerSheet.xlsx"

        rank=[]
        susp=[]
        rank,susp=_rankfile(rankfile)
        bug=_ansfile(ans, version)

        k=0
        j=0
        key=0

        for i in range(0, len(rank)):
            if rank[i]==bug:
                key=i
                keysusp=susp[i]
                for j in range(len(rank)-1, key-1):
                    if eq(susp[j], susp[key])==True:
                        key=j
                        break


        f.write("\nWorst Examscore version"+str(version)+": "+str(float((key+1)*100)/float(len(rank))))
        version=version+1

