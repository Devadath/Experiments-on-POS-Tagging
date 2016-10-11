#!/usr/bin/python
'''
A code for finding the Inter-Annotator-Agreement for POS tagged data(using BIS Tagset).
'''
import sys, os
 
class AgreementMatrix():
 '''
 This class creates the inter annotator matrix.
 
 '''
 
    def __init__(self):
        self.i = 0
       
        #Tagset : One may change the tagset below according to your purpose.
        self.tags = ["unk","N","N_NN","N_NNP","N_NST","PR","PR_PRP","PR_PRF","PR_PRL","PR_PRC","PR_PRQ","DM","DM_DMD","DM_DMR","DM_DMQ","V","V_VM","V_VM_VF","V_VM_VNF","V_VM_VINF","V_VN","V_VAUX","JJ","RB","PSP","CC","CC_CCD","CC_CCS","CC_CCS_UT","RP","RP_RPD","RP_CL","RP_INJ","RP_INTF","RP_NEG","QT","QT_QTF","QT_QTC","QT_QTO","RD","RD_RDF","RD_SYM","RD_PUNC","RD_UNK","RD_ECH"]
        
        #This creates a matrix of size - No(Tokens)*No(Tags). Here '45' = No(Tags), '666' = No(Tokens)
        self.matrix = [[0 for i in range(45)]for j in range(666)]
 
    def openFile(self,data):
        Data = open(data,"r",encoding = "UTF-8")
        tokens = Data.readlines()
        self.splitLine(tokens)
        self.i = 0
    def splitLine(self,lists):
        flag=0
        sentence=""
        for line in lists:
            line=line.rstrip()
            if flag==0 and line[:9] == "<Sentence":
                flag=1
                sentence=""
                continue
 
            if flag==1 and line == "</Sentence>":
                flag=0
                continue
 
            if flag==0:
                continue
 
            if flag==1:
                line = line.strip().split("\t")
                wordTag = line[1:]
                #print (wordTag)
                self.updateMatrix(wordTag)
    def updateMatrix(self,wordtag):
        if wordtag[1] in self.tags:
            if self.matrix[self.i][self.tags.index(wordtag[1])] != 0 and self.i < 666:
                self.matrix[self.i][self.tags.index(wordtag[1])] = self.matrix[self.i][self.tags.index(wordtag[1])]+1
                self.i+=1
            else:
                self.matrix[self.i][self.tags.index(wordtag[1])] = 1
                self.i+=1
        return self.matrix
 
class AgreementClass():
 
    def __init__(self):
        self.rowList = []
        self.colList = []
        self.N = 666
        self.n = 3
        self.k = 2
 
    def takeSum(self,lists):
        sumof = sum(lists)
        return sumof
 
    def takeSquare(self, List):
        self.Slist = [i*i for i in List]
        return self.Slist
 
    def tagCount(self, matrix):
        for i in range(45):
            row = [k[i] for k in matrix]
            rowSum = self.takeSum(row)
            self.findPofJ(rowSum)
 
    def subCount(self,matrix):
        for i in range(666):
            item = matrix[i]
            print (item)
            sumitem = self.takeSquare(item)
            print (sumitem)
            colSum = self.takeSum(sumitem)
            self.findPofI(colSum)
 
    def findPofJ(self,rowsum):
        Pj = (float(1)/(self.N*self.n))*rowsum
        self.colList.append(Pj)
 
    def findPofI(self,colsum):
        Pi = (float(1)/(self.n*(self.n-1)))*(colsum-self.n)
        #print (self.n,"n")
        #print (self.n - 1, "n - 1")
        print (colsum, "colsum")
        print (colsum - self.n, "colsum -n")
        self.rowList.append(Pi)
 
    def findPbar(self):
        #print (len(self.rowList))
        sumitem = self.takeSum(self.rowList)
        #print (sumitem, self.N)
        Pbar = (float(1)/self.N)*sumitem
        #print (Pbar)
        return Pbar
 
    def findPe(self):
        Psquare = self.takeSquare(self.colList)
        pe = self.takeSum(Psquare)
        #print (pe)
        return pe
 
    def KaPPa(self):
        Pbar = self.findPbar()
        Pe = self.findPe()
        Kappa = (Pbar - Pe)/(1-Pe)
        return Kappa
 
if (__name__ == "__main__"):
    FileFolder = sys.argv[1]
    Main = AgreementMatrix()
    for files in os.listdir(FileFolder):
        data = os.path.join(FileFolder,files)
        Main.openFile(data)
    Matrix = Main.matrix
    #print (Matrix)
    Agreement = AgreementClass()
    Agreement.tagCount(Matrix)
    Agreement.subCount(Matrix)
    kappa = Agreement.KaPPa()
    print (kappa)
