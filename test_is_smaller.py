import Pyfhel
from Pyfhel import PyCtxt,PyPtxt,Pyfhel
import pandas as pd 
import time
import math
import numpy as np

def is_smaller(x_bits,y_bits,HE=HE,n=10):
    #takes in input 2 encrypted number (st 0=< x,y < n) given in their binary form
    #returns [1] iff y<x , [0] otherwise  (where [1]= encrypt(1))
    #HE is the Homomorphic Encryption scheme (Pyfhel object)

    #Initialisation 
    p_1=PyPtxt(1,HE)
    c_1=HE.encrypt(p_1) #encrypt 1
    same_prefix=[c_1]
    same_bit=[]
    res=(c_1-y_bits[0])*x_bits[0]   ##peut etre faire deepcopy ??
    for i in range(math.floor(math.log(n))+1):
        same_bit.append(c_1-((x_bits[i]-y_bits[i])**2))   ### !!!! voir si la fct **2 marche pour les Ctxt
        tmp=c_1
        for j in range(i+1):
            tmp=tmp*same_bit[j]
        same_prefix.append(tmp)
        res+=(c_1-y_bits[i])*x_bits[i]*same_prefix[i]  ## peut etre un pb d'indice
    return res

start = time.time()
HE = Pyfhel()
#Generate Key
KEYGEN_PARAMS={ "p":2,        "r":32,
                "d":0,        "c":3,
                "sec":128,    "w":64,
                "L":30,       "m":-1,
                "R":3,        "s":0,
                "gens":[],    "ords":[]}
print("  Running KeyGen with params:")
print(KEYGEN_PARAMS)
HE.keyGen(KEYGEN_PARAMS)
end=time.time()
print("  KeyGen completed in "+str(end-start)+" sec." )


#test is_smaller with integers 5 and 6
x_bits=[int(i) for i in list('{0:08b}'.format(5))] #int 5 as a list of bits
x_bits_enc=[]
for i in x_bits :
    p_bit=PyPtxt(x_bits[i],HE)
    c_bit=HE.encrypt(p_bit)
    x_bits_enc.append(c_bit)
y_bits=[int(i) for i in list('{0:08b}'.format(6))] #int 5 as a list of bits
y_bits_enc=[]
for i in y_bits :
    p_bit=PyPtxt(y_bits[i],HE)
    c_bit=HE.encrypt(p_bit)
    y_bits_enc.append(c_bit)
result=is_smaller(x_bits_enc,y_bits_enc)
decrypted_res=HE.decrypt(result)
print("decrypted result : ",decrypted_res)