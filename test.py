# Importations :
import csv
import tkinter as tk


# Transformation du fichier resultat.csv en dictionnaire :
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


# FONCTION MOYENNE_ELEVE
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


# FONCTION MOYENNE_DEVOIR
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


# FONCTION LISTE_TRI
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


# Affichage graphique de l'application

fenetre = tk.Tk()
fenetre.title("Pas Pronote")
fenetre.geometry('500x200')
fenetre['bg'] = '#134D32'

tk.Label(fenetre, text="Nom de l'élève", bg = '#134D32', fg = '#FFFFFF').grid(row=0)
tk.Label(fenetre, text="Nom du devoir", bg = '#134D32', fg = '#FFFFFF').grid(row=2)

nom_eleve = tk.Entry(fenetre)
nom_devoir = tk.Entry(fenetre)

nom_eleve.grid(row=0, column=1, sticky=tk.W, pady=4)
nom_devoir.grid(row=2, column=1, sticky=tk.W, pady=4)

resultat = tk.Label(fenetre, text="Resultat")

resultat.grid(row=5, column=1, columnspan=2)


def calc_eleve():
    try:
        resultat.configure(text="La moyenne de l'élève " + nom_eleve.get() +
                           " est de " + str(moyenne_eleve(nom_eleve.get()))+ ".")
    except AssertionError as msg:
        resultat.configure(text=msg)


tk.Button(fenetre, text="Calculer la moyenne de l'élève.",
          command=calc_eleve,
           bg = '#1D6D4A',
           fg = '#FFFFFF').grid(row=1, column=1, sticky=tk.W, pady=4)


def calc_devoir():
    try:
        resultat.configure(text="La moyenne du devoir de " + nom_devoir.get() +
                           " est de " + str(moyenne_devoir(nom_devoir.get()))+ ".")
    except AssertionError as msg:
        resultat.configure(text=msg)


tk.Button(fenetre, text="Calculer la moyenne du devoir.",
          command=calc_devoir,
          bg = '#1D6D4A',
          fg = '#FFFFFF' ).grid(row=3, column=1, sticky=tk.W, pady=4)





def fenetre_tableau():
    newWindow = tk.Toplevel(fenetre)
    fenetre.geometry('500x200')
    fenetre['bg'] = '#134D32'


    nbcolumn = 0
    for eleve,eleve_info in dico.items():
        nbrow = 0
        for matiere,note in eleve_info["Notes"].items():
            # pour afficher le nom du devoir :
            if nbcolumn == 0 and nbrow !=0:
                textcase = matiere
            else :
                textcase = note
            if nbrow==0:
                textcase = eleve
            frame = tk.Frame(
                master=newWindow,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame.grid(row=nbrow, column=nbcolumn, padx=5, pady=5)
            label = tk.Label(master=frame, text=textcase)
            label.pack()
            nbrow +=1
        nbcolumn += 1


tk.Button(fenetre,
  text="Elèves et devoirs enregistrés",
  command=fenetre_tableau,
  bg = '#1D6D4A',
  fg = '#FFFFFF').grid(row=4,column=1)





tk.mainloop()