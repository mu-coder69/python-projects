import numpy as np
class particula:
    def __init__(self,x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
    n=5
    
    def grilla(self,xubic,yubic,c=True,n=n):
        grilla_=np.ones([n,n])
        grilla_[xubic,yubic]=77
        if c==True:
            return grilla_
        else:
            return grilla_,[xubic,yubic] 
    
    
    def vel(self,vx,vy,dt=0.5,n=n-1,x=0,y=0):
        x_n=round(x+vx*dt)
        y_n=round(y+vy*dt)
        if x_n>n:
            return self.grilla(1,y_n),[1,y_n]
        elif y_n>n:
            return self.grilla(x_n,1),[x_n,1]
        elif x_n<0:
            return self.grilla(n,y_n),[n,y_n]
        elif y_n<0:
            return self.grilla(x_n,n),[x_n,n]
        else:
            return self.grilla(x_n,y_n),[x_n,y_n]
    
    def choque(self,obj1,obj2,t=5):
        x,y,vx,vy=getattr(obj1,'x'),getattr(obj1,'y'),getattr(obj1,'vx'),getattr(obj1,'vy')
        x2,y2,vx2,vy2=getattr(obj2,'x'),getattr(obj1,'y'),getattr(obj2,'vx'),getattr(obj2,'vy')
        print('colisiones')
        for i in range(t):
            ubic1_n=self.vel(vx,vy,x=x,y=y)
            ubic2_n=self.vel(vx2,vy2,x=x2,y=y2)
            if ubic1_n[1][0]+1==ubic2_n[1][0] or ubic1_n[1][0]-1==ubic2_n[1][0]:
                vx,vx2 = -vx,vx2
            elif ubic1_n[1][1]+1==ubic2_n[1][1] or ubic1_n[1][1]-1==ubic2_n[1][1]:
                vy,vy2 = vy,-vy2
            elif ubic1_n[1][0]==ubic2_n[1][0] or ubic1_n[1][0]==ubic2_n[1][0]:
                vx,vx2 = vx,-vx2
            elif ubic1_n[1][1]==ubic2_n[1][1] or ubic1_n[1][1]==ubic2_n[1][1]:
                vy,vy2 = -vy,vy2
            print(f'para el tiempo{i}')
            print('p1\n',ubic2_n[0])
            print('p2\n',ubic1_n[0])
        return ubic2_n[0],ubic1_n[0]

    

x1,y1,vx1,vy1 = 1,1,2,4
x2,y2,vx2,vy2 = 2,2,2,4
particula1=particula(x1,y1,vx1,vy1)
particula2=particula(x2,y2,vx2,vy2)
grilla__=particula1.grilla(x1,y1)
grilla___=particula2.grilla(x2,y2)

colision=particula1.choque(particula1,particula2,t=5)
