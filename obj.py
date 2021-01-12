from time import time

## fichier contenant les classes utiles à spaceinvader.py

class Tir():

    def __init__(self,x,y,canvas,color='yellow'):

        self.x = x
        self.y = y
        self.img = canvas.create_rectangle(x-1,y-1,x+1,y+1,fill=color)
        canvas.focus_set()

#classe mere de tous les élements qui ont une vie -> Ilot
class Bloc():

    def __init__(self,x,y,canvas,fen):

        self.vie = 1

        self.x = x
        self.y = y
        self.canva = canvas
        self.img = self.canva.create_rectangle(x-10,y-10,x+10,y+10,width=2,fill='grey')
        self.canva.focus_set()
        self.fen = fen

    def perdre_vie(self,nbvie=1):
        self.vie -= nbvie
        # l'objet n'est pas détruit si il a une vie <= 0 , cela se fait dans la
        # fonction update_vaisseaux() de spaceinvader.py

#classe mere de tous les vaisseaux
class Vaisseau(Bloc):

    def __init__(self,x,y,canvas,fen,ennemis):

        self.vie = 3

        # variables 'graphiques'
        self.x = x
        self.y = y
        self.canva = canvas
        self.img = self.canva.create_rectangle(x-20,y-10,x+10,y+10,width=5,fill='white')
        self.canva.focus_set()
        self.fen = fen

        # on désigne qui sont les ennemis de CE vaisseau
        self.ennemis = ennemis

        # vitesses de déplacement respectives
        self.depl = 20
        self.depl_tir = -10

        # liste contenant tous les tirs du vaisseau
        self.tirs = []
        self.deplacer_tirs()

    def tirer(self,color="yellow"):

        # on crée un objet tir
        self.tirs.append(Tir(self.x,self.y,self.canva,color))

    def deplacer_tirs(self): #

        tirs_a_suppr = []
        # on boucle sur chaque tir
        for i in range(len(self.tirs)):
            tir = self.tirs[i]
            if tir.y > 0 and tir.y < 500:

                # on déplace le tir
                tir.y += self.depl_tir
                self.canva.coords(tir.img,tir.x-4,tir.y,tir.x,tir.y+10)

                # on verifie les collisions avec chaque mechant
                for mechant in self.ennemis :
                    if mechant.vie > 0 :
                        collisions_ennemis=self.canva.find_overlapping(*self.canva.coords(mechant.img))
                        if tir.img in collisions_ennemis : # si ce tir touche ce méchant :
                            tirs_a_suppr += [i] # on ajoute aux tirs à supprimer
                            mechant.perdre_vie()
            else:
                # si le tir est trop haut, on l'ajoute aux tirs à supprimer
                tirs_a_suppr += [i]

        # on supprime les tirs qui sont arrivés à la fin ou ont touché un mechant
        di = 0
        for i in tirs_a_suppr:
            self.canva.delete(self.tirs[i-di].img)
            del self.tirs[i-di]
            di+= 1

        # cette fonction se fait en boucle
        self.fen.after(50,self.deplacer_tirs)

    def connect_ennemis(self,ennemis):
        # on met à jour la liste des ennemis
        self.ennemis = ennemis

class Mechant(Vaisseau):

    def __init__(self,x,y,canvas,fen,ennemis,gentil_a_toucher,color='blue',deplacement=0.5,deplacement_y=30):

        self.vie = 1

        # variables 'graphiques'
        self.x = x
        self.y = y
        self.canva = canvas
        self.img = self.canva.create_rectangle(x-20,y-10,x+10,y+10,width=5,fill=color)
        self.canva.focus_set()
        self.fen = fen

        # on désigne qui sont les ennemis de CE vaisseau
        self.ennemis = ennemis

        # ennemi particulier aux méchants : si ils touchent le vaisseau gentil, on perd automatiquement la partie
        self.gentil_a_toucher = gentil_a_toucher

        # vitesses de déplacement respectives
        self.depl = deplacement
        self.depl_y = deplacement_y
        self.depl_tir = 10

        # liste contenant tous les tirs du vaisseau
        self.tirs = []
        self.deplacer_tirs()

    def deplacer(self):

        # on déplace le vaisseau
        self.x += self.depl

        # on vérifie qu'il reste dans le canevas
        if self.x>480:
            self.x=480
            self.y += self.depl_y # si il arrive à la fin d'une ligne, il descend
            self.depl = -self.depl # on inverse le mouvement
        elif self.x<30:
            self.x=30
            self.y += self.depl_y # si il arrive à la fin d'une ligne, il descend
            self.depl = -self.depl # on inverse le mouvement

        self.canva.coords(self.img,self.x -20, self.y -10, self.x +10, self.y +10)

        ## on vérifie les collisions avec le gentil_a_toucher (si on touche le vaisseau -> GAME OVER)
        collisions=self.canva.find_overlapping(*self.canva.coords(self.img))
        if self.gentil_a_toucher.img in collisions :
            self.gentil_a_toucher.perdre_vie(1000) # bon ok c'est un peu radical...

class Gentil(Vaisseau):

    def __init__(self,x,y,canvas,fen,ennemis):

        super(Gentil,self).__init__(x,y,canvas,fen,ennemis)

        # variables pour avoir un countdown pour pouvoir tirer
        self.delay_tir = 1
        self.last_tir = 0

    def tirer(self,color="yellow"):

        # on vérifie le countdown
        if time()-self.last_tir > self.delay_tir:
            self.last_tir = time()

            # et on ajout un tir
            self.tirs.append(Tir(self.x,self.y,self.canva,color))

    def perdre_vie(self,nbvie=1):

        self.vie -= nbvie

        # on déplace le vaisseau au centre quand on perd une vie
        self.x=250
        self.y=450
        self.canva.coords(self.img,self.x -20, self.y -10, self.x +10, self.y +10)

    def deplacer(self,dx): # permet de déplacer le vaisseau de dx

        if self.vie > 0:
            self.x += dx

            # on vérifie qu'on reste dans le canevas
            if self.x>480:
                self.x=480
            elif self.x<30:
                self.x=30
            self.canva.coords(self.img,self.x -20, self.y -10, self.x +10, self.y +10)
