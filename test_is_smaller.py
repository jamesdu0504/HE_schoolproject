import Pyfhel
from Pyfhel import PyCtxt,PyPtxt,Pyfhel
import pandas as pd 
import time
import math
import numpy as np

def is_smaller(x_bits,y_bits,HE,alpha=8,n=1000):
    #takes in input 2 encrypted number (st 0=< x,y < n) given in their binary form
    #coded on alpha bits
    #returns [1] iff y<x , [0] otherwise  (where [1]= encrypt(1))
    #HE is the Homomorphic Encryption scheme (Pyfhel object)

    #Initialisation of same_prefix
    print("Initisalisation")
    l=[1]+[0 for i in range(alpha-1)]
    p=PyPtxt(l,HE)
    same_prefix=HE.encrypt(p) 
    #encrypt [1,1,1,..1]
    p_1=PyPtxt([1 for i in range(alpha)],HE)   
    c_1=HE.encrypt(p_1)

    same_bit=c_1.copy(c_1)
    same_bit=same_bit-((x_bits-y_bits)**2)

    ##get same_prefix as a vector
    res=(1-y_bits)*x_bits*same_prefix
    res%=c_1  #sum of all the elements of res

    print("res : ",HE.decrypt(res)) ##Dec(res) should be a vector [1,1,1,.. 1] iff x>y, else [0,...0]
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
x=6
x_bits=[int(i) for i in list('{0:08b}'.format(x))] #int 5 as a list of 8 bits
print("Encrypting "+str(x)+" in bits ",x_bits)
start = time.time()
x_bits_enc=HE.encrypt(x_bits)
print("x_bits_enc = ",x_bits_enc.getIDs(),x_bits_enc.getLen())
end=time.time()
print(str(end-start)+" sec." )

y=5
y_bits=[int(i) for i in list('{0:08b}'.format(y))] #int 6 as a list of 8 bits
print("Encrypting "+str(y)+" in bits.",y_bits)
y_bits_enc=HE.encrypt(y_bits)
#print("x_bits_enc = ",y_bits_enc.getIDs(),x_bits_enc.getLen())
end=time.time()
print(str(end-start)+" sec." )

result=is_smaller(x_bits_enc,y_bits_enc,HE)
decrypted_res=HE.decrypt(result)
print("decrypted result : ",decrypted_res)