import Pyfhel
from Pyfhel import PyCtxt,PyPtxt,Pyfhel
import time
import math
import numpy as np
from random import randint

def encrypt_as_bits(x,alpha,HE):
    #takes in input a plaintext integer x =< 2^alpha -1
    #returns a list of the encrypted bits of x
    a='{0:0'+str(alpha)+'b}'
    x_bits=[int(i) for i in list(a.format(x))]
    x_bits_enc=[]
    print("Encrypting "+str(x)+" in bits ",x_bits)
    for i in x_bits:
        x_bits_enc.append(HE.encrypt(PyPtxt([i], HE)))
    return x_bits_enc

def is_smaller(x_bits,y_bits,HE,alpha,n=1000):
    #takes in input 2 encrypted number (st 0=< x,y < n) given in their binary form
    #coded on alpha bits
    #returns [1] iff y<x , [0] otherwise  (where [1]= encrypt(1))
    #HE is the Homomorphic Encryption scheme (Pyfhel object)

    #Initialisation of same_prefix and same_bit
    #print("Initisalisation")
    c_1=HE.encrypt(PyPtxt([1], HE))
    same_prefix=[c_1]
    same_bit=[]
    res=(c_1-y_bits[0])*x_bits[0]
    for i in range(alpha):                        #min(alpha,int(math.floor(math.log(n))+1))):
        same_bit.append(HE.encrypt(PyPtxt([1], HE))-((x_bits[i]-y_bits[i])**2))
        tmp=HE.encrypt(PyPtxt([1], HE))
        for j in range(i+1):
            #print("same_bit : "+str(j),HE.decrypt(same_bit[j]))
            tmp*=same_bit[j]
        #print("tmp : ",HE.decrypt(tmp))
        same_prefix.append(tmp)
        if i>0:  #since the 1st term of the sum is already computed before the loop
            res+=(HE.encrypt(PyPtxt([1], HE))-y_bits[i])*x_bits[i]*same_prefix[i]
            #print("res : ",HE.decrypt(res))
    return res

def coinToss(x_bits,n,HE,deg,alpha):
#Takes in input an integer n, and an encrypted number 0=< x_bits <n as a list of alpha bits
#generates a random number r between 0 and n  (potentially drawn from a distribution D)
#Returns an encrypted bit b=[1] if r^(1/deg)<x (ie : with probability x/n) otherwise [0]
    #print("Random number between 0 and "+str(n))
    r=randint(0, n)
    print("r : ",r)
    r=int(math.floor((r**(1/float(deg)))))
    print(r)
    if r>((2**alpha) -1) : #rq : x=< 2**alpha -1 so if r>2**alpha-1, then r>x
        c_0=HE.encrypt(PyPtxt([0], HE))
        return c_0
    else :
        #encrypt r as a list of bits
        r_bits_enc=encrypt_as_bits(r,alpha,HE)
        #compare r_bits and x_bits
        return is_smaller(x_bits,r_bits_enc,HE,alpha=alpha)

def probabilisticAverage(list_x_bits,n,HE,deg,alpha):
    #Takes in input a list of integers (each integer is a list of encrypted bits)
    #n=size of the vector input
    #alpha=number of bits on which each elt of the vector is encoded
    #deg is the degree of the moment to compute (deg=1 : average, deg=2 : second order moment)
    #HE is the Homomorphic Encryption scheme (Pyfhel object)

    #Returns an approximation of the statistical function (ie : average, 2nd order moment..) computed on the integer list
    
    #Initialize
    L=2**alpha
    c=int(math.ceil((L**deg)/n))
    a=[]
    res=HE.encrypt(PyPtxt([0], HE))
    print("c*n="+str(c*n))
    for i in range((c*n)):       #rq : pour L=8 et n=3, c=3 et c*n=9 (environ 440sec)
        tmp=int(math.floor(i/c))    #(rq le dernier i sera c*n-1 donc le dernier tmp sera n-1)
        print("")
        print("tmp="+str(tmp))
        print("")
        a.append(coinToss(list_x_bits[tmp],c*n,HE,deg=deg,alpha=alpha))
        decrypted_res=HE.decrypt(a[i])
        print("result of the coin toss : ",decrypted_res)
        res+=a[i]  #peut etre pas besoin d'une liste (sommer directement les elts dans res)
    return res

start = time.time()
HE = Pyfhel()
#Generate Key
KEYGEN_PARAMS={ "p":2,        "r":32,
                "d":0,        "c":3,
                "sec":128,    "w":64,
                "L":40,       "m":-1,
                "R":3,        "s":0,
                "gens":[],    "ords":[]}

print("  Running KeyGen with params:")
print(KEYGEN_PARAMS)
HE.keyGen(KEYGEN_PARAMS)
end=time.time()
print("  KeyGen completed in "+str(end-start)+" sec." )


alpha=4
list_nb=[4,8,12]  #we want to compute the average of these numbers
list_x_bits=[encrypt_as_bits(x,alpha,HE) for x in list_nb]

#Compute the probabilistic average of the list of int


#Compute the 2nd order moment of the list of int
print("")
print("Compute 2nd moment order of ",list_nb)
print("")
start = time.time()
result=probabilisticAverage(list_x_bits,len(list_nb),HE,2,alpha)
decrypted_res=HE.decrypt(result)
print("decrypted result : ",decrypted_res)
end=time.time()
print(str(end-start)+" sec." )