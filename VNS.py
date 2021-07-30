import math
import csv
import numpy as np
import numpy.random as rd
from typing import Sequence
import pandas as pd
import time
import random

start_time = time.time()

def computiontime (I):
    CT = M[I[0],3] + M[I[0],1] + M[I[0],2]
    for k in range (1,100):
        CT = CT + ( max( M[I[k],3] , M[I[k-1],3] + M[I[k-1],1] )) + M[I[k],1] + ( max ( CT - (CT + ( max( M[I[k],3] , M[I[k-1],3] + M[I[k-1],1] ))), 0 )) + M[I[k],2]
    return CT

def Random_Sequence(n):
    MySequence=[]
    for i in range(n):
        MySequence.append(random.randint(1,n))
        while MySequence[i] in MySequence[0:i]:
            MySequence[i]=random.randint(1,n)
    return MySequence


PPW_Input=[] 
PPW_Index = [] 

File_name=input("Please Enter Input File name: ")
data = pd.read_csv(File_name, header = None, delimiter=' ')

print("Input Data is as Follows: ")
print(data)
#print(data[0][0])
n=len(data.index)

for i in range(n):
    PPW_Index.append(i+1)
    PPW_Input.append([data[1][i], data[2][i],data[3][i]])
    
print("Data After Loading to Dataset: ")
for i in range(n):
    print(PPW_Input[i])

PPW_Index=Random_Sequence(n)


#writing calculated P, W, D in a temp csv File

with open("TempMetadata.csv", "w") as temp_file:
    csv_writer = csv.writer(temp_file, delimiter='\t')
    csv_writer.writerow(['i', 'Pi', 'Wi', 'Di'])
    for i in range(1, n + 1):
        csv_writer.writerow([i, PPW_Input[i-1][0],PPW_Input[i-1][1], PPW_Input[i-1][2]])

# This Function actually calculates the cost of executing a sequence
def executionCost(MySequence):
    calcTime,calculated = 0, 0
    for i in range(len(MySequence)):
        calculated += PPW_Input[MySequence[i]-1][0]
        calcTime += PPW_Input[MySequence[i]-1][1] * max(0, calculated - PPW_Input[MySequence[i]-1][2])
    return calcTime

#Generating Neighborhoods

def NeighboursPermutation(s, i, j):
    MySequence=list(s)
    MySequence[i], MySequence[j] = MySequence[j], MySequence[i]
    return MySequence

def NeigborhoodInsertion(s, i, j):
    temp=s[j]
    del s[j]
    s.insert(i,temp)
    MySequence = s
    return MySequence

def CalcPivot(l,i):
    l1 = l[0:i]
    l1.reverse()
    l2 = l[i:len(l)]
    l = l1+l2
    return l


#This function  applies the VNS Algorithm, the parameter seq_agr is none other than the PPW_Index indexed in a list

def VNS(seq_arg):
    i = 0
    desiredTime = 50 #The execution will display the best result in 50 seconds
    Stoppage = time.time() + desiredTime
    Sxprime = [] 
    
    maxExecutionCost = 99999999999999999999999 
    finalSequence = []
    while True:
        if time.time() > Stoppage:
            break
        if i == 0:
            minimum_i = random.randint(0, len(seq_arg) - 1)
            minimum_j = random.randint(0, len(seq_arg) - 1)
            
            while minimum_i == minimum_j:
                minimum_i = random.randint(0,len(seq_arg)-1)
                
            Sxprime = NeighboursPermutation(seq_arg, minimum_i,minimum_j)
            executionCost_xp = executionCost(Sxprime)
           
            executionCost_min_xseconde = executionCost(NeighboursPermutation(Sxprime, 0, 1))
           
            for k in range(len(Sxprime)):
                for j in range(k+1, len(Sxprime)):
                    noOfsecond = NeighboursPermutation(Sxprime, k, j)
                   
                    executionCost_xsec = executionCost(noOfsecond)
                   
                    if executionCost(noOfsecond) < executionCost_min_xseconde:
                        noOfsecond_min = noOfsecond
                        executionCost_min_xseconde = executionCost_xsec
            if executionCost_min_xseconde < executionCost_xp:
                Sxprime = noOfsecond_min
                i = 0
                seq_arg = noOfsecond_min
               
            else:
                seq_arg = Sxprime
                i = 1
        
        if i == 1:
            minimum_i = random.randint(0, len(seq_arg) - 1)
            minimum_j = random.randint(1, len(seq_arg) - 1)
            while minimum_i == minimum_j:
                minimum_i = random.randint(0, len(seq_arg) - 1)
            Sxprime = NeigborhoodInsertion(seq_arg, minimum_i,minimum_j)
            executionCost_xp = executionCost(Sxprime)
            executionCost_min_xseconde = executionCost(NeigborhoodInsertion(Sxprime,0,2))
            for k in range(len(Sxprime)):
                for j in range(k+1,len(Sxprime)):
                    noOfsecond = NeigborhoodInsertion(Sxprime, k, j)
                    executionCost_xsec = executionCost(noOfsecond)
                    
                    if executionCost(noOfsecond) < executionCost_min_xseconde:
                        noOfsecond_min = noOfsecond
                        executionCost_min_xseconde = executionCost_xsec
            if executionCost_min_xseconde < executionCost_xp:

                Sxprime = noOfsecond_min
                i=0
                seq_arg = noOfsecond_min
            else:
                seq_arg = Sxprime
                i=2
        
        if i == 2:
            Sxprime = CalcPivot(seq_arg, random.randint(0,len(seq_arg)-1))
            executionCost_xp = executionCost(Sxprime)
            executionCost_min_xseconde = executionCost(CalcPivot(Sxprime,2))
            for k in range(2,len(seq_arg)):
                noOfsecond = CalcPivot(Sxprime, k)
                executionCost_xsec = executionCost(noOfsecond)
                if executionCost(noOfsecond) < executionCost_min_xseconde:
                    noOfsecond_min = noOfsecond
                    executionCost_min_xseconde = executionCost_xsec
            if executionCost_min_xseconde < executionCost_xp:
                Sxprime = noOfsecond_min
                seq_arg = noOfsecond_min
            else:
                seq_arg = Random_Sequence(n)
            i = 0
        if executionCost_min_xseconde < maxExecutionCost:
            maxExecutionCost = executionCost_min_xseconde
            finalSequence = noOfsecond_min
    return finalSequence, maxExecutionCost

min_seq, min_executionCost = VNS(PPW_Index)

print ("The optimal Set Sequence is: ", min_seq)

print ("Mimimum executution Cost will be : " ,min_executionCost)


print("---Execution took %s seconds ---" % (time.time() - start_time))