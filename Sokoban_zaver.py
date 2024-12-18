import tkinter as tk
from tkinter import messagebox

VELIKOST_POLICKA = 50
POCET_SLOUPCU = 12
POCET_RAD = 12

pocet_tahu = 0
rekord_urovne = None
pozice_hrace = [10, 8]

X = "X"  # zeď
o = "o"  # volno
K = "K"  # krabice
C = "C"  # cílové místo

Okno = tk.Tk()
Hraci_plocha = tk.Canvas(Okno, width=600, height=600, bg="lightblue")

BPravidla = tk.Button()
BRestart_kola = tk.Button()
BDalsi_uroven = tk.Button()
BPredchozi_uroven = tk.Button()
BUkonci_hru = tk.Button()
LPocitadlo_tahu = tk.Label(Okno, text=f"POČET TAHŮ: {pocet_tahu}")
LRekord_urovne = tk.Label(Okno, text=f"REKORD ÚROVNĚ: {rekord_urovne}")

bludiste = [
        [X, X, X, X, X, X, X, X, X, X, X, X],
        [X, o, o, o, o, o, o, o, o, o, o, X],
        [X, o, K, o, X, X, X, X, X, X, o, X],
        [X, o, o, C, X, X, X, X, X, X, o, X],
        [X, X, X, o, X, X, X, X, X, X, o, X],
        [X, X, X, o, X, X, X, X, X, X, o, X],
        [X, X, X, o, X, X, o, o, o, o, o, X],
        [X, o, K, C, X, X, o, o, o, o, o, X],
        [X, o, K, C, X, X, o, o, X, o, o, X],
        [X, o, o, o, X, X, K, K, K, K, K, X],
        [X, X, X, X, X, X, C, C, C, C, C, X],
        [X, X, X, X, X, X, X, X, X, X, X, X]
    ]

cilova_mista = []
for rada in range(POCET_RAD):
    for sloupec in range(POCET_SLOUPCU):
        if bludiste[rada][sloupec] == C:
            cilova_mista.append((rada, sloupec))


krabice_id = {}  # slovník, který uchovává id krabic

def inicializuj():
    Okno.geometry("1000x650")
    Okno.title("Sokoban")
    BPravidla.config(text="JAK HRÁT", command=vypis_pravidla, width=20)
    BRestart_kola.config(text="NOVÁ HRA/RESTART", command=restartuj_hru, width=20)
    BDalsi_uroven.config(text="DALŠÍ ÚROVEŇ", command=dalsi_uroven, width=20)
    BPredchozi_uroven.config(text="PŘEDCHOZÍ ÚROVEŇ", command=predchozi_uroven, width=20)
    BUkonci_hru.config(text="KONEC", command=Okno.destroy, width=20)
    
    Hraci_plocha.grid(row=0, column=1, rowspan=5, padx=10, pady=10)
    BPravidla.grid(row=0, column=0, padx=10, pady=10)
    BRestart_kola.grid(row=1, column=0, padx=10, pady=10)
    BDalsi_uroven.grid(row=2, column=0, padx=10, pady=10)
    BPredchozi_uroven.grid(row=3, column=0, padx=10, pady=10)
    BUkonci_hru.grid(row=4, column=0, padx=10, pady=10)
    LPocitadlo_tahu.grid(row=0, column=6, padx=10, pady=10)
    LRekord_urovne.grid(row=1, column=6, padx=10, pady=10)
   
    ovladani_hrace()
    vykresli_bludiste()
    umisti_hrace()
    umisti_krabice()

def vykresli_bludiste():
    for rada in range(POCET_RAD):
        for sloupec in range(POCET_SLOUPCU):
            x1, y1 = sloupec * VELIKOST_POLICKA, rada * VELIKOST_POLICKA
            x2, y2 = x1 + VELIKOST_POLICKA, y1 + VELIKOST_POLICKA
            if bludiste[rada][sloupec] == X:
                Hraci_plocha.create_rectangle(x1, y1, x2, y2, fill="black", outline="grey")
            elif bludiste[rada][sloupec] == C:
                Hraci_plocha.create_rectangle(x1, y1, x2, y2, fill="#F5DEB3", outline="grey")
            else:
                Hraci_plocha.create_rectangle(x1, y1, x2, y2, fill="white", outline="grey")

def umisti_hrace():
    global hrac
    x = pozice_hrace[1] * VELIKOST_POLICKA
    y = pozice_hrace[0] * VELIKOST_POLICKA

    hrac = Hraci_plocha.create_oval(x, y, x + VELIKOST_POLICKA, y + VELIKOST_POLICKA, fill="lightblue")

def umisti_krabice():
    for rada in range(POCET_RAD):
        for sloupec in range(POCET_SLOUPCU):
            if bludiste[rada][sloupec] == K:
                x1, y1 = sloupec * VELIKOST_POLICKA, rada * VELIKOST_POLICKA
                x2, y2 = x1 + VELIKOST_POLICKA, y1 + VELIKOST_POLICKA
                id_krabice = Hraci_plocha.create_rectangle(x1, y1, x2, y2, fill="#8B4513", outline="grey")
                krabice_id[(rada, sloupec)] = id_krabice

def pohyb(ax, ay):
    global pozice_hrace, pocet_tahu
    nova_pozice = [pozice_hrace[0] + ay, pozice_hrace[1] + ax]
    if bludiste[nova_pozice[0]][nova_pozice[1]] != X:
        if bludiste[nova_pozice[0]][nova_pozice[1]] == K:
            nova_pozice_krabice = [nova_pozice[0] + ay, nova_pozice[1] + ax]
            if bludiste[nova_pozice_krabice[0]][nova_pozice_krabice[1]] in [o, C]:
                if bludiste[nova_pozice_krabice[0]][nova_pozice_krabice[1]] == C:
                    bludiste[nova_pozice_krabice[0]][nova_pozice_krabice[1]] = K  
                else:
                    bludiste[nova_pozice_krabice[0]][nova_pozice_krabice[1]] = K  
                if bludiste[nova_pozice[0]][nova_pozice[1]] == C:
                    bludiste[nova_pozice[0]][nova_pozice[1]] = C
                else:
                    bludiste[nova_pozice[0]][nova_pozice[1]] = o

                Hraci_plocha.delete(krabice_id[(nova_pozice[0], nova_pozice[1])])
                x1, y1 = nova_pozice_krabice[1] * VELIKOST_POLICKA, nova_pozice_krabice[0] * VELIKOST_POLICKA
                x2, y2 = x1 + VELIKOST_POLICKA, y1 + VELIKOST_POLICKA
                id_krabice = Hraci_plocha.create_rectangle(x1, y1, x2, y2, fill="#8B4513", outline="grey")
                krabice_id[(nova_pozice_krabice[0], nova_pozice_krabice[1])] = id_krabice

                pozice_hrace=nova_pozice
                Hraci_plocha.delete(hrac)
                umisti_hrace()
                pocet_tahu += 1
                LPocitadlo_tahu.config(text=f"POČET TAHŮ: {pocet_tahu}")
                
        elif bludiste[nova_pozice[0]][nova_pozice[1]] in [o, C]:
            pozice_hrace = nova_pozice
            Hraci_plocha.delete(hrac)
            umisti_hrace()
            pocet_tahu += 1
            LPocitadlo_tahu.config(text=f"POČET TAHŮ: {pocet_tahu}")
    if vyhodnot_vitezstvi()==True:
        messagebox.showinfo("Gratulace!", "Úroveň splněna!")
        aktualizuj_rekord()

def ovladani_hrace():
    Okno.bind("<Up>", lambda event: pohyb(0, -1))
    Okno.bind("<Down>", lambda event: pohyb(0, 1))
    Okno.bind("<Left>", lambda event: pohyb(-1, 0))
    Okno.bind("<Right>", lambda event: pohyb(1, 0))

def vyhodnot_vitezstvi():
    for rada, sloupec in cilova_mista:
        if bludiste[rada][sloupec] != K:
            return False
    return True

def aktualizuj_rekord():
    global rekord_urovne
    if rekord_urovne is None or pocet_tahu<rekord_urovne:
        rekord_urovne = pocet_tahu
        LRekord_urovne.config(text=f"REKORD ÚROVNĚ: {rekord_urovne}")
        
def vypis_pravidla():
    pravidla=("""Sokoban (倉庫番 Sōkoban, skladník) je logická hra, ve které hráč posouvá bedny v bludišti a snaží se je umístit na vyznačené pozice.
Bludiště je 2D mapa znázorňující rozmístění Sokobana (modré kolečko), beden (tmavší hnědý čtverec), zdí (černá barva) a vyznačených cílových pozic (světle hnědá). Není možné posouvat více beden naráz, vždy pouze jednu v daném okamžiku.
Dále není možné za sebou bednu táhnout.
        
        """
    )
    
    messagebox.showinfo("Jak hrát", pravidla)
        
    
def restartuj_hru():
    global pocet_tahu, pozice_hrace, bludiste, krabice_id
    pocet_tahu = 0
    pozice_hrace = [10, 8]
    bludiste = [
        [X, X, X, X, X, X, X, X, X, X, X, X],
        [X, o, o, o, o, o, o, o, o, o, o, X],
        [X, o, K, o, X, X, X, X, X, X, o, X],
        [X, o, o, C, X, X, X, X, X, X, o, X],
        [X, X, X, o, X, X, X, X, X, X, o, X],
        [X, X, X, o, X, X, X, X, X, X, o, X],
        [X, X, X, o, X, X, o, o, o, o, o, X],
        [X, o, K, C, X, X, o, o, o, o, o, X],
        [X, o, K, C, X, X, o, o, X, o, o, X],
        [X, o, o, o, X, X, K, K, K, K, K, X],
        [X, X, X, X, X, X, C, C, C, C, C, X],
        [X, X, X, X, X, X, X, X, X, X, X, X]
    ]
    krabice_id = {}
    Hraci_plocha.delete("all")
    vykresli_bludiste()
    umisti_hrace()
    umisti_krabice()
    LPocitadlo_tahu.config(text=f"POČET TAHŮ: {pocet_tahu}")
   
def dalsi_uroven():
    DEMO=("Hrajete demoverzi Sokobanu, pro odemknutí dalších úrovní si zakupte náš produkt nebo se rekvalifikujte na programátora a napište si ho sami: jubela.cz/rekvalifikacni-kurzy/kurz/programator-python")
    
    messagebox.showinfo("DEMOVERZE", DEMO)
    
def predchozi_uroven():
    DEMO=("Hrajete demoverzi Sokobanu, pro odemknutí dalších úrovní si zakupte náš produkt nebo se rekvalifikujte na programátora a napište si ho sami: jubela.cz/rekvalifikacni-kurzy/kurz/programator-python")
    
    messagebox.showinfo("DEMOVERZE", DEMO)

inicializuj()
Okno.mainloop()

