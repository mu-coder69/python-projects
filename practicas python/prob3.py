#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

#si la celda vale 1 significa que esta vivo, en el caso opuesto estará muerto. 

def estado_prox(estado_ac):
    estado_n=np.zeros(np.shape(estado_ac)[0])
    for i in range(np.shape(estado_ac)[0]-1):
        celula=estado_ac[i]                
        if estado_ac[i+1]==1 and estado_ac[i-1]==1 and estado_ac[i]==1:
            celula=0
        elif estado_ac[i+1]==0 and estado_ac[i-1]==1 and estado_ac[i]==1:
            celula=0
        elif estado_ac[i+1]==1 and estado_ac[i-1]==1 and estado_ac[i]==0:
            celula=0
        elif estado_ac[i+1]==0 and estado_ac[i-1]==1 and estado_ac[i]==0:
            celula=1
        elif estado_ac[i+1]==1 and estado_ac[i-1]==0 and estado_ac[i]==1:
            celula=1
        elif estado_ac[i+1]==0 and estado_ac[i-1]==0 and estado_ac[i]==1:
            celula=1
        elif estado_ac[i+1]==1 and estado_ac[i-1]==0 and estado_ac[i]==0:
            celula=1
        elif estado_ac[i+1]==0 and estado_ac[i-1]==0 and estado_ac[i]==0:
            celula=0
        estado_n[i]=celula
    return estado_n
#     # print('estadado luego de condiciones',estado_n)
#     k=0
#     for i in range(np.shape(estado_n)[0]):
#         if estado_n[i]==0:
#             k+=1
#         else:
#             break
#     estado_n=estado_n[k:]
#     # print('estdado luego de eliminar ceros izq',estado_n)
#     k2=0
#     for i in range(1,np.shape(estado_n)[0],1):
#         # print(-i)
#         if estado_n[-i]==0:
#             # print(estado_n[-i])
#             k2+=1
#         else:
#             break
#     estado_n=estado_n[:np.shape(estado_n)[0]-k2]
#     # print('estado luego de eliminar ceros derc',estado_n)
#     return estado_n
# # print('estado inicial',estado_inicial)
t=200
n=256
estado_inicial=np.random.randint(0,2,n)
x=np.zeros([t,n])
for i in range(t):
    siguiente=estado_prox(estado_inicial)
    x[i,:]=siguiente
    print(f'estado en el tiempo{i}\n',siguiente)
    estado_inicial=siguiente


color_map=plt.imshow(x)
color_map.set_cmap('Greys_r')
plt.show()
