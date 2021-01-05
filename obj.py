from time import time

def collision(a,b):

    if (a[0] > b[2]) or (a[2] < b[0]) or (a[1] > b[3]) or (a[3] < b[1]):
        return False #  oklm c'est bon ca collisionne PAS
    else:
        return True # aoutch ca collisionne

class Tir():

    def __init__(self,x,y,canvas,color='yellow'):

        self.x = x
        self.y = y
        self.img = canvas.create_rectangle(x-1,y-1,x+1,y+1,fill=color)
        canvas.focus_set()

#classe mere de tous les vaisseaux
class Vaisseau():

    def __init__(self,x,y,canvas,fen,mechants):

        self.vie = 3

        self.x = x
        self.y = y
        self.canva = canvas
        self.img = self.canva.create_rectangle(x-20,y-10,x+10,y+10,width=5,fill='white')
        self.canva.focus_set()
        self.fen = fen

        self.mechants = mechants

        self.depl = 20
        self.depl_tir = -10

        self.tirs = []
        self.peut_tirer = True
        self.deplacer_tirs()

    def deplacer(self,dx):

        if self.vie > 0:

            self.x += dx
            if self.x>480:
                self.x=480
            elif self.x<30:
                self.x=30
            self.canva.coords(self.img,self.x -20, self.y -10, self.x +10, self.y +10)

    def tirer(self,color="yellow"):

        self.tirs.append(Tir(self.x,self.y,self.canva,color))

    def deplacer_tirs(self):

        tirs_a_suppr = []
        # on boucle sur chaque tir
        for i in range(len(self.tirs)):
            tir = self.tirs[i]
            if tir.y > 0 and tir.y < 500:
                tir.y += self.depl_tir
                self.canva.coords(tir.img,tir.x-4,tir.y,tir.x,tir.y+10)

                # on verifie les collisions avec chaque mechant
                for mechant in self.mechants :
                    if collision(self.canva.coords(mechant.img),self.canva.coords(tir.img)):
                        tirs_a_suppr += [i]
                        mechant.perdre_vie()
            else:
                tirs_a_suppr += [i]

        # on supprime les tirs qui sont arrivés à la fin ou ont touché un mechant
        di = 0
        for i in tirs_a_suppr:
            self.canva.delete(self.tirs[i-di].img)
            del self.tirs[i-di]
            di+= 1

        self.fen.after(50,self.deplacer_tirs)

    def perdre_vie(self):
        self.vie -= 1

    def connect_mechants(self,mechants):
        self.mechants = mechants

class Mechant(Vaisseau):

    def __init__(self,x,y,canvas,fen,mechants):

        self.vie = 1

        self.x = x
        self.y = y
        self.canva = canvas
        self.img = self.canva.create_rectangle(x-20,y-10,x+10,y+10,width=5,fill='blue')
        self.canva.focus_set()
        self.fen = fen

        self.mechants = mechants
        self.depl = 10
        self.depl_tir = 10

        self.tirs = []
        self.peut_tirer = True
        self.deplacer_tirs()

    def deplacer(self):

        self.x += self.depl
        if self.x>480:
            self.x=480
            self.y += 40
            self.depl = -self.depl
        elif self.x<30:
            self.x=30
            self.y += 40
            self.depl = -self.depl
        self.canva.coords(self.img,self.x -20, self.y -10, self.x +10, self.y +10)

class GroMechan(Mechant):

    def __init__(self,x,y,canvas,fen,mechants):

        self.vie = 1

        self.x = x
        self.y = y
        self.canva = canvas
        self.img = self.canva.create_rectangle(x-20,y,x+10,y+10,width=5,fill='red')
        self.canva.focus_set()
        self.fen = fen

        self.mechants = mechants
        self.depl = 20
        self.depl_tir = 10

        self.tirs = []
        self.peut_tirer = True
        self.deplacer_tirs()

class Gentil(Vaisseau):

    def __init__(self,x,y,canvas,fen,mechants):

        super(Gentil,self).__init__(x,y,canvas,fen,mechants)
        self.delay_tir = 1
        self.last_tir = 0

    def tirer(self,color="yellow"):

        if time()-self.last_tir > self.delay_tir:
            self.last_tir = time()
            self.tirs.append(Tir(self.x,self.y,self.canva,color))
