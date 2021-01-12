#Header

"""
TP3 version Tkinter AIVAZIAN OLIVIER
lien du github : https://github.com/deltasfer/csdev-space
"""

#importation des fonction
from random import *
from tkinter import Tk,Button,Entry,Label,Frame,Canvas,PhotoImage
from time import strftime,gmtime
import obj

#-------------------------------------------# INITIALISATION FENETRE

couleur = "#3c3e43"

# fenetre
fen = Tk()
fen.title("Space Invader")
fen.geometry('650x600')
fen.configure(bg=couleur)


#-------------------------------------------# INITIALISATION DU JEU

#initialisation du canvas -> seulement utile pour fixer les positions des futurs labels
hauteur=500
largeur=500
Canevas = Canvas(fen,width=largeur,height=hauteur,bg=couleur,highlightthickness=1)
Canevas.grid(row=2,column=1,rowspan=4,columnspan=3,padx=10,pady=10)

# initialisation variables
score,vaisseau,mechants,mechantsbonus,IN_GAME,GAGNE,ilots,labelgagner,labelperdu \
            ,score_joueur,vie_joueur,new_game,btn_propose,I,fondecran = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[]

#Recommencer une partie
def NewGame():
    global score,vaisseau,mechants,mechantsbonus,IN_GAME,GAGNE,ilots,labelgagner,Canevas,score_joueur,vie_joueur,new_game,btn_propose,I,fondecran,labelperdu

    #----------------------# SUPPRESSION DES SPRITES DE LA PARTIE D'AVANT

    if vaisseau != []: # on vérifie qu'on est pas à la première partie
        for element in [vaisseau]+mechants+mechantsbonus+ilots:
            element.perdre_vie(1000) # oui c'est radical
        supprimer_objets_morts([vaisseau]+mechants+mechantsbonus+ilots)


    #------------------------# CREATION DU CANEVAS

    #Canevas
    hauteur=500
    largeur=500
    Canevas = Canvas(fen,width=largeur,height=hauteur,bg=couleur,highlightthickness=1)

    # on met la grille
    Canevas.grid(row=2,column=1,rowspan=4,columnspan=3,padx=10,pady=10)

    # on affecte le fond d'ecran
    hauteur=500
    largeur=500
    I=PhotoImage(file="earth.png")
    fondecran= Canevas.create_image(hauteur/2,largeur/2,image=I)



    #------------------------# JEU, CREATION DES ELEMENTS

    IN_GAME = True # variable qui vérifie si on a perdu
    GAGNE = False # variable qui vérifie si on a gagné

    #creation ilots
    ilots = create_ilots()

    #creationdu vaisseau
    vaisseau=obj.Gentil(250,450,Canevas,fen,[])

    #Score du joueur
    score=0

    #creation des mechants
    mechants = []
    for i in range(4):
        mechants.append(obj.Mechant(50+i*100,140,Canevas,fen,[vaisseau]+ilots,vaisseau))
        mechants.append(obj.Mechant(100+i*100,200,Canevas,fen,[vaisseau]+ilots,vaisseau))

    #creation d'un mechantbonus
    mechantsbonus = []
    for i in range(1):
        # ce "super" mechant est rouge et plus rapide, et il ne descend pas
        mechantsbonus.append(obj.Mechant(250,50,Canevas,fen,[vaisseau]+ilots,vaisseau,'red',3,0))

    # on dit au vaisseau que les méchants sont ses ennemis
    vaisseau.connect_ennemis(mechants+mechantsbonus)



    #------------------------# LABELS,BOUTONS


    #Label du score du joueur
    score_joueur = Label(fen,text="score du joueur : 0",bg=couleur,fg="white",width=35)
    score_joueur.grid(row=1,column=1,sticky="w")

    #Label du nombre de vies du joueur
    vie_joueur = Label(fen,text="Vies restantes: 3",bg=couleur,fg="white",width=35)
    vie_joueur.grid(row=1,column=3,sticky="W")

    #Bonton NewGame
    new_game = Button(fen,text="new game",fg="black",command=NewGame)
    new_game.grid(row=3, column=4,sticky="w")

    #Bouton Quitter
    btn_propose = Button(fen,text='Quit',fg='black',command=fen.destroy)
    btn_propose.grid(row=5,column=4,sticky="w")

    #gagner la partie
    labelgagner = Label(Canevas,text="Vous avez gagné, votre score est de : ",bg=couleur,fg="white",width=35)
    labelgagner.grid()
    labelgagner.grid_forget()

    #perdre la partie
    labelperdu = Label(Canevas,text="GAME OVER",bg=couleur,fg="white",width=35)
    labelperdu.grid()
    labelperdu.grid_forget()

    #-------------------# BINDS

    #pour bouger le vaisseau
    Canevas.bind('<q>',Deplacementvaisseau) and Canevas.bind('<d>',Deplacementvaisseau)
    #pour tirer
    Canevas.bind('<space>',Tirer)
    # cheatcode : appuyez 2 fois rapidement sur C pour gagner une vie
    Canevas.bind('<Double-c>',cheat)


#------------------------# FONCTIONS UTILES

def create_ilots():

    # on définit les positions des blocs du premier ilot
    ilots=[]
    for j in range (9):

        # on définit x et y pour chaque bloc
        x = 75
        y = 350
        if j<=2 :
            x+= j*20
        elif j>2 and j<=5:
            y += 20
            x += (j-3)*20
        else:
            y += 40
            x += (j-6)*20

        # on crée un bloc pour chaque ilot aux positions x,y
        ilots.append(obj.Bloc(x,y,Canevas,fen))
        ilots.append(obj.Bloc(x+150,y,Canevas,fen))
        ilots.append(obj.Bloc(x+300,y,Canevas,fen))
    return ilots


# deplacement vaisseau gentil
def Deplacementvaisseau(event):
    touche= event.keysym
    #print(touche)
    if touche=='d':
        vaisseau.deplacer(10)
    if touche=='q':
        vaisseau.deplacer(-10)
# tir vaisseau gentil
def Tirer(event):
    if IN_GAME:
        vaisseau.tirer()


# deplacement vaisseaux méchants
def deplacementmechant():
    if IN_GAME:
        for mechant in mechants:
            mechant.deplacer()
        for mechant in mechantsbonus:
            mechant.deplacer()

    fen.after(10,deplacementmechant)

# tir vaisseaux mechants
def tir_mechant():
    if IN_GAME:
        if mechants+mechantsbonus != []:
            mechant = choice(mechants+mechantsbonus)
            mechant.tirer('black')
    fen.after(randint(500,2000),tir_mechant)

## fonction qui met à jour la vie des vaisseaux, vérifie qu'on est pas mort, met à jour les labels ..
def update_vaisseaux():

    global score,mechants,mechantsbonus,IN_GAME,ilots

    score_joueur['text'] = "score du joueur : "+str(score)
    vie_joueur['text'] = "Vies restantes: "+str(vaisseau.vie)

    if vaisseau.vie <= 0:
        game_over()
        IN_GAME = False

    else:

        mechants = supprimer_objets_morts(mechants,10)
        mechantsbonus = supprimer_objets_morts(mechantsbonus,25)
        ilots = supprimer_objets_morts(ilots)

        vaisseau.connect_ennemis(mechants+mechantsbonus)
        for mechant in mechants+mechantsbonus:
            mechant.connect_ennemis([vaisseau]+ilots)

        if  len(mechants)==0 and len(mechantsbonus) == 0 :
            gagner()
            GAGNE = True

    fen.after(30,update_vaisseaux)

def supprimer_objets_morts(liste_blocs,points_pour_chaque_elimination=0):

    # cette fonction parcourt liste_blocs et vérifie que chaque bloc est vivant
    # s'il est mort, elle le supprime correctement et l'enlève de liste_blocs

    # si points_pour_chaque_elimination est renseigné, pour chaque mort dans liste_blocs, le score du joueur augmente

    global score

    # on check qui est mort
    morts = []
    for i in range(len(liste_blocs)):
        if liste_blocs[i].vie <= 0:
            morts.append(i)

    # on supprime les morts de liste_blocs
    di = 0
    for i in morts:
        Canevas.delete(liste_blocs[i-di].img)
        del liste_blocs[i-di]
        score+=points_pour_chaque_elimination
        di+=1

    # on retourne la nouvelle liste avec QUE des vivants
    return liste_blocs

# fonctions de fin de partie : affiche les labels assignés
def gagner():

    if GAGNE == False:
        labelgagner['text'] = "Vous avez gagné, votre score est de : "+str(score)
        labelgagner.grid()

def game_over():
    if IN_GAME == True:
        labelperdu.grid()

# fonction qui permet de rajouter une vie pour un double click sur C
def cheat(Event):
    vaisseau.vie+=1

#----------------------------# LANCEMENT

NewGame()
deplacementmechant()
tir_mechant()
update_vaisseaux()

fen.mainloop()
