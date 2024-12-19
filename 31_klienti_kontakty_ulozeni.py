class CKlient:
    id=int()
    jméno=str()
    pohlavi=str()
    body=int()	# např. body za aktivitu
    aktivni=bool()
    def __init__(self,aid,ajmeno,apohlavi):
        self.id=aid
        self.jmeno=ajmeno
        self.pohlavi=apohlavi
        self.body=0					# statická vlastnost se dá napsat přímo k vlastnostem (řádek 4)
        self.aktivni=True			# statická vlastnost se dá napsat přímo k vlastnostem (řádek 5)
    def vypis(self):
        print(f"{self.id}\t{self.jmeno}\t{self.pohlavi}\tbody={self.body}\taktivní={self.aktivni}")
        
class CKlienti:
    seznam=list()
    id_pristi_volne=int()
    def __init__(self):
        self.id_pristi_volne=1
    def pridej(self,ajmeno,apohlavi):
        klient=CKlient(self.id_pristi_volne,ajmeno,apohlavi.capitalize())
        self.id_pristi_volne+=1
        self.seznam.append(klient)
    def demo(self):
        print("NAHRÁNÍ DEMO DAT")
        self.pridej("Novák","muž")
        self.pridej("Nová","žena")
        self.pridej("SiriV2.0_HW","jiné")
        self.pridej("Kos","muž")
        self.pridej("Špačková","žena")
        for i in range(1,100):
            if i%2==0: 	pohlavi="muž"
            else:		pohlavi="žena"
            self.pridej("Klient"+str(i),pohlavi)
    def zadej(self):
        print("ZADÁNÍ KLIENTA")
        jmeno=input("Zadejte jméno: ")
        pohlavi=input("Zadejte pohlaví (muž/žena/jiné): ")
        self.pridej(jmeno,pohlavi)
    def hledej(self):
        print("HLEDÁNÍ KLIENTA")
        cast_jmena=input("Zadejte alespoň část jména klienta: ").lower()
        for klient in self.seznam:
            if cast_jmena in klient.jmeno.lower(): klient.vypis()
    def edituj(self):
        print("EDITACE")
        self.hledej()
        id=int(input("Zadejte ID klienta pro editaci: "))
        for klient in self.seznam:
            if klient.id==id:
                vstup=input("Jmeno: "+klient.jmeno+" (ENTER zachová): ")
                if vstup!="":klient.jmeno=vstup
    def deaktivuj(self):
        print("DEAKTIVACE")
        self.hledej()
        id=int(input("Zadejte ID klienta pro deaktivaci/aktivaci: "))
        for klient in self.seznam:
            if klient.id==id:
                klient.aktivni=not klient.aktivni
                klient.vypis()
    def vypis(self):
        print("VÝPIS KLIENTŮ")
        for klient in self.seznam:
            klient.vypis()
    def uloz_csv(self):
        fp=open("31_klienti.csv","w")
        for klient in self.seznam:
            zaznam=f"{klient.id};{klient.jmeno};{klient.pohlavi};{str(klient.body)};{str(klient.aktivni)}\n"
            fp.write(zaznam)
        fp.close()
    def nacti_csv(self):
        self.seznam.clear()				# vyčistí seznam, aby tam po načtení dat ze souboru nebyla žádná jiná data
        with open ("31_klienti.csv","r") as fp: zaznamy=fp.readlines()
        for zaznam in zaznamy:
            bunky=zaznam.split(";")		# .split rozdělí záznam v Excelu do buněk, dělícím prvkem je středník
            id=int(bunky[0])
            jmeno=bunky[1]
            pohlavi=bunky[2]
            body=int(bunky[3])
            aktivni=bool(bunky[4])
            
            klient=CKlient(id,jmeno,pohlavi)
            klient.body=body
            klient.aktivni=aktivni
            self.seznam.append(klient)
        self.id_pristi_volne=id+1
class CKontakt:
    id_klienta=int()
    typ=str()
    hodnota=str()
    def __init__(self,aid_klienta,atyp,ahodnota):
        self.id_klienta=aid_klienta
        self.typ=atyp
        self.hodnota=ahodnota
    def vypis(self):
        print(f"\t\t({self.id_klienta}) {self.typ}: {self.hodnota}")
class CKontakty:
    seznam=list()
    def pridej(self,aid_klienta,atyp,ahodnota):
        self.seznam.append(CKontakt(aid_klienta,atyp,ahodnota))
    def zadej_klienta(self,aid_klienta):					# umožní zadat všechny kontakty konkrétního klienta
        while input("Chcete zadat kontakt? a/n: ")=="a":
            typ=input("Typ kontaktu (email, mobil, pevná, adresa, ...): ")
            hodnota=input(f"{typ}: ")
            self.pridej(aid_klienta,typ,hodnota)
    def vypis_klienta(self,aid_klienta):					# vypíše všechny kontakty konkrétního klienta
        for kontakt in self.seznam:
            if kontakt.id_klienta==aid_klienta: kontakt.vypis()
    def demo(self):
        self.pridej(1,"email","prvni@seznam.cz")
        self.pridej(1,"mobil","+420603111111")
        self.pridej(1,"adresa","538 21, Malá Lhotka 4")
        self.pridej(3,"email","treti@seznam.cz")
        self.pridej(3,"mobil","+420724333333")
        self.pridej(4,"email","ctvrty@seznam.cz")
        self.pridej(4,"mobil","+420605444444")
        self.pridej(5,"email","paty@centrum.cz")
        self.pridej(6,"mobil","+420728666666")
        self.pridej(7,"email","sedmy@google.com")
class CRizeni:
    klienti=CKlienti()
    kontakty=CKontakty()
    def __init__(self):
        while True:
            print("\nMENU:")
            print("dd - demo data")
            print("zk - zadej klienta (s kontakty)")
            print("hk - hledej klienta")
            print("ek - edituj klienta")
            print("da - deaktivuj/aktivuj klienta")
            print("vk - vypiš klienty (s kontakty)")
            print("ud - ulož data do souboru (jen klienti)")
            print("nd - načti data ze souboru (jen klienti)")
            print("kp - konec programu")
            volba=input("Vaše volba: ")
            if 		volba=="kp": break
            elif 	volba=="dd": self.klienti.demo(); self.kontakty.demo()
            elif	volba=="zk": self.zadej()
            elif	volba=="hk": self.klienti.hledej()
            elif	volba=="ek": self.klienti.edituj()
            elif	volba=="da": self.klienti.deaktivuj()
            elif	volba=="vk": self.vypis()
            elif	volba=="ud": self.klienti.uloz_csv()
            elif	volba=="nd": self.klienti.nacti_csv()
            else: print("Vaší volbě nerozumím :-(")
        print("KONEC PROGRAMU")
    def zadej(self):
        print("ZADÁNÍ KLIENTA S KONTAKTY")
        self.klienti.zadej()
        id_klienta=self.klienti.id_pristi_volne-1
        self.kontakty.zadej_klienta(id_klienta)
    def vypis(self):
        print("VÝPIS KLIENTŮ S KONTAKTY:")
        for klient in self.klienti.seznam:
            klient.vypis()
            self.kontakty.vypis_klienta(klient.id)
    

rizeni=CRizeni()


