# Importations :
import csv
import tkinter as tk
from tkinter import ttk


# Transformation du fichier resultat.csv en dictionnaire : Nicolas
dico = {}  # dico est une liste
csv.register_dialect('myDialect', delimiter=';', quotechar='|')
with open('resultat.csv') as myFile:
    reader = csv.DictReader(myFile, dialect='myDialect')
    for row in reader:  # row est un dictionnaire
        prenom = row.pop("Prenom")
        nom = row.pop("Nom")
        line = {'Prenom': prenom, 'Notes': row}
        dico[nom] = line  # Ajoute le dicitionnaire row à la liste 'dico'

###


# FONCTION MOYENNE_ELEVE : Nicolas
def moyenne_eleve(eleve: str) -> float:
    """
  Prend en argument le nom d'un élève et retourne la moyenne de ses différentes notes.
  """

    # Pre-conditions
    assert eleve, "Il faut specifier le nom d'un élève."
    assert eleve in dico, "Il faut specifier un élève qui existe dans le fichier resultat.csv"

    # Programme
    notes = []
    for note in dico[eleve]["Notes"].values():
        notes.append(float(note))
    moyenne = round(sum(notes) / len(notes), 2)

    # Post-conditions
    assert len(notes) > 0, "Il n'y a pas de notes pour cet élève."
    assert moyenne, "La moyenne n'existe pas"

    # Return
    return moyenne


###


# FONCTION MOYENNE_DEVOIR : Lucas
def moyenne_devoir(devoir: str) -> float:
    """
  Prend en argument le nom d'un devoir et retourne la moyenne des notes de chaque élève de ce devoir.
  """

    # Pre-conditions
    assert devoir, "Il faut specifier le nom du devoir."

    # Programme
    note_devoir = []
    for eleve in dico.values():
        assert devoir in eleve[
            "Notes"], "Le devoir doit exister dans le fichier resultat.csv"
        note_devoir.append(float(eleve["Notes"][devoir]))

    moyenne = round(sum(note_devoir) / len(note_devoir), 2)

    # Post-conditions :
    assert len(note_devoir) > 0, "Il n'y a pas de notes pour ce devoir."
    assert moyenne, "La moyenne n'existe pas."

    # Return
    return moyenne


###


# FONCTION LISTE_TRI : Nicolas et Lucas
def liste_tri() -> list:
    """
  liste_tri retourne une liste de tuples contenant le nom d'un élève et sa moyenne, classés dans l'ordre croissant.
  """

    # Programme
    liste = []
    for eleve in dico.keys():
        liste.append(tuple((eleve, moyenne_eleve(eleve))))

    # Tri par insertiton
    N = len(liste)
    for n in range(1, N):
        cle = liste[n]
        j = n - 1
        while j >= 0 and liste[j][1] > cle[1]:
            liste[j + 1] = liste[j]  # decalage
            j = j - 1
        liste[j + 1] = cle

    # Post-conditions :
    assert liste, "le resultat est vide"
    return liste


# Affichage graphique de l'application : Nicolas et Lucas

# Base de la fenetre :
fenetre = tk.Tk()
fenetre.title("Pas Pronote")

fenetre.geometry('700x500+0+0')
fenetre.columnconfigure(0, weight=1)
fenetre.rowconfigure(0, weight=1)
fenetre['bg'] = '#134D32'

# Systeme de TABS qui permet de naviguer entre les deux onglets "Rechercher" et "Tableau de notes" :
style = ttk.Style(fenetre)
style.configure('TNotebook.Tab', width=fenetre.winfo_screenwidth())
style.configure('TFrame', background='#134D32')
tab_parent = ttk.Notebook(fenetre)
TAB1 = ttk.Frame(tab_parent)
TAB2 = ttk.Frame(tab_parent)
tab_parent.add(TAB1, text="Rechercher")
tab_parent.add(TAB2, text="Tableau des élèves")
tab_parent.grid(row=0, column=0, sticky='nsew')

# ==== TAB1 "Rechercher" ====
tk.Label(TAB1, text="Nom de l'élève   ", bg = '#134D32', fg = '#FFFFFF').grid(column=0, row=1, padx=10)
tk.Label(TAB1, text="Nom du devoir    ", bg = '#134D32', fg = '#FFFFFF').grid(column=0, row=3, padx=10)

tk.Label(TAB1, text="Copyright tout droit reservé © Pas Pronote 2021 | Nicolas et Lucas", bg = '#134D32', fg = '#FFFFFF').place(relx = 0.0,
                 rely = 1.0,anchor ='sw')

# les Inputs qui permettent de récuperer les informations :
nom_eleve = tk.Entry(TAB1)
nom_devoir = tk.Entry(TAB1)

nom_eleve.grid(row=1, column=1, ipadx=10, ipady=5, pady = 20, padx=10) # note : pour l'ensemble du projet, la methode grid est utilisé pour gérer l'affichage des éléments
nom_devoir.grid(row=3, column=1, ipadx=10, ipady=5, pady = 20, padx=10)

# affichage du resultat :
resultat = tk.Label(TAB1, text="Resultat", bg = '#1D6D4A', fg = '#FFFFFF')
resultat.grid(row=5, column=0, columnspan=4, rowspan =3,ipadx=10, ipady=40, sticky="news")

# Fonction qui est appellée lors de l'appuie sur le bouton, permet d'éxecuter l'action :
def calc_eleve():
    try:
        resultat.configure(text="La moyenne de l'élève " + nom_eleve.get() +
                           " est de " + str(moyenne_eleve(nom_eleve.get()))+ ".")
    except AssertionError as msg:
        resultat.configure(text=msg)


tk.Button(TAB1, text="Calculer la moyenne de l'élève.",
          command=calc_eleve,
           bg = '#1D6D4A',
           fg = '#FFFFFF').grid(row=1, column=3, ipadx=5, ipady=5, pady = 5,padx=10)

# Même principe que pour la fonction ci-dessus :
def calc_devoir():
    try:
        resultat.configure(text="La moyenne du devoir de " + nom_devoir.get() +
                           " est de " + str(moyenne_devoir(nom_devoir.get()))+ ".")
    except AssertionError as msg:
        resultat.configure(text=msg)


tk.Button(TAB1, text="Calculer la moyenne du devoir.",
          command=calc_devoir,
          bg = '#1D6D4A',
          fg = '#FFFFFF').grid(row=3, column=3, ipadx=5, ipady=5, pady=5,padx=10)
          
# Permet que le tableau prenne tout l'espace disponible :
#TAB1.grid_rowconfigure(0, weight=1)
TAB1.grid_columnconfigure(0, weight=1)

# ==== TAB2 "Tableau des notes" ====
# Header du tableau :
header = list(dico[next(iter(dico))]["Notes"].keys()) # Récupération de tous les noms des devoirs

# Création de l'header du tableau :
header.insert(0,"Élève")
header.append("Moyenne de l'élève")
tv = ttk.Treeview(TAB2, columns=header, show='headings') 
tv.grid(row=0, column=0, sticky="nsew")

# Permet que le tableau prenne tout l'espace disponible :
TAB2.grid_rowconfigure(0, weight=1)
TAB2.grid_columnconfigure(0, weight=1)

# Ajout de l'header configuré precedement :
for m in header:
    tv.heading(m, text=m)
    if m != "Élève" and m != "Moyenne de l'élève":
      tv.column(m, width=60, minwidth=60, stretch=tk.NO)
    else:
      tv.column(m, width=160, minwidth=160, stretch=tk.NO)


# Cette boucle permet d'ajouter chaques eleves avec leurs notes ainsi que leurs moyennes dans le tableau :
it=0
for eleve,eleve_info in dico.items():
    ligne = list(eleve_info["Notes"].values())
    ligne.insert(0,eleve) # ajout du nom de l'élève
    ligne.append(moyenne_eleve(eleve)) # ajout de la moyenne de l'élève
    tv.insert(parent='', index="end", iid=it, values=ligne)    
    it+=1

# Affichage de la moyenne de chaques devoirs en derniere ligne:
devoirs = list(dico[next(iter(dico))]["Notes"].keys())
ligneMoyenneDevoirs = ["Moyenne des devoirs : "]
for devoir in devoirs :
    ligneMoyenneDevoirs.append(moyenne_devoir(devoir))
ligneMoyenneDevoirs.append("n/a")
tv.insert(parent='', index="end", iid=it, values=ligneMoyenneDevoirs)  

###

#Executage de la fenêtre :
tk.mainloop()