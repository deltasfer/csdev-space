#Header

"""
TP3 version Tkinter AIVAZIAN OLIVIER
lien du github :
"""

#importation des fonction
from random import *
from tkinter import Tk,Button,Entry,Label,Frame,Canvas,PhotoImage
from time import strftime,gmtime
import obj


###INITIALISATION JEU
IN_GAME = True

### INITIALISATION FENETRE
couleur = "#3c3e43"

# fenetre
fen = Tk()
fen.title("Space Invader")
fen.geometry('650x600')
fen.configure(bg=couleur)

#Canevas
hauteur=500
largeur=500
taillecarre=20
Canevas = Canvas(fen,width=largeur,height=hauteur,bg=couleur,highlightthickness=1)
# on affecte le fond d'ecran
Canevas.grid(row=2,column=1,rowspan=4,columnspan=3,padx=10,pady=10)


#creation ilot 1
PosXi=[]
PosYi=[]
ilots=[]
for j in range (9):
    if j<=2 :
        PosYi.append(350)
        PosXi.append(75+j*20)
    elif j>2 and j<=5:
        PosYi.append(350+20)
        PosXi.append(75+(j-3)*20)
    else:
        PosYi.append(350+40)
        PosXi.append(75+(j-6)*20)

    ilots.append(Canevas.create_rectangle(PosXi[j]-10,PosYi[j]-10,PosXi[j]+10,PosYi[j]+10,width=2,fill='grey'))
    Canevas.focus_set()
    ilots.append(Canevas.create_rectangle(PosXi[j]+300-10,PosYi[j]-10,PosXi[j]+300+10,PosYi[j]+10,width=2,fill='grey'))
    Canevas.focus_set()
    ilots.append(Canevas.create_rectangle(PosXi[j]+150-10,PosYi[j]-10,PosXi[j]+150+10,PosYi[j]+10,width=2,fill='grey'))
    Canevas.focus_set()


#creationdu vaisseau
vaisseau=obj.Gentil(250,450,Canevas,fen,[])

def Deplacementvaisseau(event):
    touche= event.keysym
    #print(touche)
    if touche=='d':
        vaisseau.deplacer(20)
    if touche=='q':
        vaisseau.deplacer(-20)

#Score du joueur
score=0
score_joueur = Label(fen,text="score du joueur : 0",bg=couleur,fg="white",width=35)
score_joueur.grid(row=1,column=1,sticky="w")

#Nombre de vies du joueur
vie_joueur = Label(fen,text="Vies restantes: "+str(vaisseau.vie),bg=couleur,fg="white",width=35)
vie_joueur.grid(row=1,column=3,sticky="W")

#Recommencer une partie
def NewGame():
    PosX=250
    PosY=450
    Canevas.coords(vaisseau,PosX -20, PosY -10, PosX +10, PosY +10)
new_game = Button(fen,text="new game",fg="black",command=NewGame)
new_game.grid(row=3, column=4,sticky="w")


#Bouton Quitter
btn_propose = Button(fen,text='Quit',fg='black',command=fen.destroy)
btn_propose.grid(row=5,column=4,sticky="w")

#creationdu d'un mechant
mechants = []
for i in range(4):
    mechants.append(obj.Mechant(50+i*100,150,Canevas,fen,[vaisseau]))

#creationdu d'un mechantbonus
mechantsbonus = []
for i in range(1):
    mechantsbonus.append(obj.GroMechan(250,50,Canevas,fen,[vaisseau]))
vaisseau.connect_mechants(mechants+mechantsbonus)


#deplacement méchant
def deplacementmechant():
    if IN_GAME:
        for mechant in mechants:
            mechant.deplacer()
        for mechant in mechantsbonus:
            mechant.deplacer()

        fen.after(100,deplacementmechant)
def tir_mechant():
    if IN_GAME:
        if mechants+mechantsbonus != []:
            mechant = choice(mechants+mechantsbonus)
            mechant.tirer('black')
            fen.after(500,tir_mechant)

def Tirer(event):
    if IN_GAME:
        vaisseau.tirer()
def update_vaisseaux():


    global score,mechants,IN_GAME

    score_joueur['text'] = "score du joueur : "+str(score)
    vie_joueur['text'] = "Vies restantes: "+str(vaisseau.vie)
    if vaisseau.vie <= 0:
        print('GAME OVER')
        IN_GAME = False
    else:

        morts = []
        for i in range(len(mechants)):
            if mechants[i].vie <= 0:
                morts.append(i)

        di = 0
        for i in morts:
            Canevas.delete(mechants[i-di].img)
            del mechants[i-di]
            score+=10
            di+=1







        morts = []
        for i in range(len(mechantsbonus)):
                if mechantsbonus[i].vie <= 0:
                    morts.append(i)
        a = 0
        for i in morts:
            Canevas.delete(mechantsbonus[i-a].img)
            del mechantsbonus[i-a]
            score+=150
            a+=1

        vaisseau.connect_mechants(mechants+mechantsbonus)
        #vaisseau.connect_mechants(mechants+mechantsbonus)

        fen.after(30,update_vaisseaux)


#pour bouger le vaisseau
Canevas.bind('<q>',Deplacementvaisseau) and Canevas.bind('<d>',Deplacementvaisseau)
Canevas.bind('<space>',Tirer)


deplacementmechant()
tir_mechant()
update_vaisseaux()
fen.mainloop()
