import random
from datetime import datetime

class Periodo:
    def __init__(self, check_in, check_out):
        # Uso datetime per formattare la data di check in e check out
        self.check_in = datetime.strptime(check_in, '%Y-%m-%d')
        self.check_out = datetime.strptime(check_out, '%Y-%m-%d')

class Camera:
    def __init__(self, nPosti, con_vista):
        self.id_camera = random.randint(1000, 9999) # Uso randint per generare un numero cauale sempre diverso per l'ID della camera
        self.nPosti = nPosti
        self.con_vista = con_vista
        self.nominativo = None
        self.periodo = None

    def calcola_prezzo_base(self):
        return (1998 * self.nPosti) / 8

    def calcola_prezzo_vista(self, prezzo_base):
        prezzo_vista = (prezzo_base * 0.03) + prezzo_base
        return prezzo_vista if self.con_vista else prezzo_base

    def calcola_prezzo(self):
        prezzo_base = self.calcola_prezzo_base()
        prezzo_vista = self.calcola_prezzo_vista(prezzo_base)
        return prezzo_vista

class Hotel:
    def __init__(self, nome):
        self.nome = nome
        self.camere_libere = []
        self.camere_occupate = []
        self.camere_prenotate = []

    def situazione_camere(self):
        print("\nCamere libere:")
        for camera in self.camere_libere:
            print(f"ID Camera: {camera.id_camera}, Posti letto disponibili: {camera.nPosti}, Vista: {camera.con_vista}")

        print("\nCamere occupate:")
        for camera in self.camere_occupate:
            print(f"ID Camera: {camera.id_camera}, Posti letto occupati: {camera.nPosti}, Nominativo prenotazione: {camera.nominativo}, Vista: {camera.con_vista}")

        print("\nCamere prenotate:")
        for camera in self.camere_prenotate:
            print(f"ID Camera: {camera.id_camera}, Posti letto prenotati: {camera.nPosti}, Nominativo prenotazione: {camera.nominativo}, Vista: {camera.con_vista}")
            
    def valida_data(self, data):
        # Verifica della formattazione della data
        try:
            datetime.strptime(data, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def resoconto_camere(self, file):
        with open(file, 'w') as f:
            f.write("Camere libere:\n")
            for camera in self.camere_libere:
                f.write(f"ID: {camera.id_camera}, Posti: {camera.nPosti}, Vista: {camera.con_vista}\n")
            
            f.write("Camere occupate:\n")
            for camera in self.camere_occupate:
                f.write(f"ID: {camera.id_camera}, Posti: {camera.nPosti}, Vista: {camera.con_vista}, Cliente: {camera.nominativo}, Periodo: {camera.periodo.check_in.strftime('%Y-%m-%d')} - {camera.periodo.check_out.strftime('%Y-%m-%d')}\n")
            
            f.write("Camere prenotate:\n")
            for camera in self.camere_prenotate:
                f.write(f"ID: {camera.id_camera}, Posti: {camera.nPosti}, Vista: {camera.con_vista}, Cliente: {camera.nominativo}, Periodo: {camera.periodo.check_in.strftime('%Y-%m-%d')} - {camera.periodo.check_out.strftime('%Y-%m-%d')}\n")

    def prenotazione_camera(self, check_in, check_out, nominativo, nPosti, con_vista):
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
        
        # Funzione di prenotazione camera, inclusa anche la parte facoltativa della verifica
        for camera in self.camere_libere + self.camere_occupate:
            if camera.nPosti == nPosti and (camera.con_vista == con_vista or not con_vista):
                if camera not in self.camere_occupate or camera.periodo.check_out <= check_in_date or camera.periodo.check_in >= check_out_date:
                    if camera in self.camere_libere:
                        self.camere_libere.remove(camera)
                    else:
                        self.camere_occupate.remove(camera)
                    self.camere_prenotate.append(camera)
                    camera.periodo = Periodo(check_in, check_out)
                    camera.nominativo = nominativo
                    prezzo = camera.calcola_prezzo()
                    print(f"Prenotazione avvenuta con successo: ID Camera: {camera.id_camera}, Nominativo: {camera.nominativo}, Posti letto: {camera.nPosti}, Periodo: {check_in, check_out}, Prezzo calcolato: {prezzo}") 
                    return camera.id_camera, prezzo
        
        return (None, 0.0)

    def assegna_camera(self, id_camera, nominativo): 
        for camera in self.camere_prenotate:
            if camera.id_camera == id_camera and camera.nominativo == nominativo:
                self.camere_prenotate.remove(camera)
                self.camere_occupate.append(camera)
                camera.periodo = None
                return "Camera assegnata con successo"
        return "Camera già occupata o nominativo errato"

    def libera_camera(self, id_camera, nominativo):
        for camera in self.camere_occupate:
            if camera.id_camera == id_camera and camera.nominativo == nominativo:
                self.camere_occupate.remove(camera)
                self.camere_libere.append(camera)
                camera.nominativo = None
                camera.periodo = None
                return "Camera liberata con successo"
        return "Camera non trovata o nominativo errato"

    def disdici_prenotazione(self, id_camera, nominativo):
        for camera in self.camere_prenotate:
            if camera.id_camera == id_camera and camera.nominativo == nominativo:
                self.camere_prenotate.remove(camera)
                self.camere_libere.append(camera)
                tassa_disdetta = camera.calcola_prezzo() * 0.05
                camera.nominativo = None
                camera.periodo = None
                return f"Camera disdetta con successo. Tassa di disdetta: {tassa_disdetta}"
        return "La camera non era prenotata o nominativo errato"
    
    def menu_prenotazioni(self):
     while True:
        print("\n--- Benvenuti all'Hotel Bella Vista ---")
        print("1. Prenotazione camera")
        print("2. Assegna camera")
        print("3. Libera camera")
        print("4. Disdici prenotazione")
        print("5. Esci")
        scelta = input("Inserisci il numero corrispondente all'azione che desideri svolgere: ")

        if scelta == "1":
            # Controllo data check-in
            check_in = input("Inserisci la data di check-in (YYYY-MM-DD): ")
            while not self.valida_data(check_in):
                print("Formato data non valido. Inserisci la data nel formato YYYY-MM-DD.")
                check_in = input("Inserisci la data di check-in (YYYY-MM-DD): ")

            # Controllo data check-out
            check_out = input("Inserisci la data di check-out (YYYY-MM-DD): ")
            while not self.valida_data(check_out):
                print("Formato data non valido. Inserisci la data nel formato YYYY-MM-DD.")
                check_out = input("Inserisci la data di check-out (YYYY-MM-DD): ")

            # Verifica che la data di check-out sia successiva alla data di check-in
            if datetime.strptime(check_in, '%Y-%m-%d') >= datetime.strptime(check_out, '%Y-%m-%d'):
                print("La data di check-out deve essere successiva alla data di check-in.")
                continue
            # Controllo nominativo
            nominativo = input("Inserisci il nome del cliente: ").strip()
            while not nominativo:
                print("Il nome non può essere vuoto.")
                nominativo = input("Inserisci il nome del cliente: ").strip()

            try:
                # Controllo insrimento numero posti
                nPosti = int(input("Inserisci il numero di posti letto: "))
                if nPosti <= 0:
                    raise ValueError
            except ValueError:
                print("Il numero di posti letto deve essere un numero intero positivo.")
                continue
            
             # Controllo camera con o senza vista
            con_vista = None
            while con_vista is None:
                vista_input = input("Inserisci la preferenza per la vista (s/n): ").lower()
                if vista_input == "s":
                    con_vista = True
                elif vista_input == "n":
                    con_vista = False
                else:
                    print("Inserisci 's' per vista o 'n' per senza vista.")

            id_camera, prezzo = self.prenotazione_camera(check_in, check_out, nominativo, nPosti, con_vista)
            if id_camera is not None:
                print(f"\nPrenotazione camera con ID: {id_camera}, Prezzo: {prezzo}")
            else:
                print("\nImpossibile prenotare")
        
        elif scelta == "2":
            try:
                # Controllo sull'inserimento dell'ID
                id_camera = int(input("Inserisci l'ID della camera da assegnare: "))
            except ValueError:
                print("L'ID della camera deve essere un numero intero.")
                continue
            nominativo = input("Inserisci il nome del cliente: ").strip()
            while not nominativo:
                print("Il nome non può essere vuoto.")
                nominativo = input("Inserisci il nome del cliente: ").strip()
            print(self.assegna_camera(id_camera, nominativo))
        
        elif scelta == "3":
            try:
                id_camera = int(input("Inserisci l'ID della camera da liberare: "))
            except ValueError:
                print("L'ID della camera deve essere un numero intero.")
                continue
            nominativo = input("Inserisci il nome del cliente: ").strip()
            while not nominativo:
                print("Il nome non può essere vuoto.")
                nominativo = input("Inserisci il nome del cliente: ").strip()  
            print(self.libera_camera(id_camera, nominativo))
        
        elif scelta == "4":
            try:
                id_camera = int(input("Inserisci l'ID della camera da disdire: "))
            except ValueError:
                print("L'ID della camera deve essere un numero intero.")
                continue
            
            nominativo = input("Inserisci il nome del cliente: ").strip()
            while not nominativo:
                print("Il nome non può essere vuoto.")
                nominativo = input("Inserisci il nome del cliente: ").strip()        
            print(self.disdici_prenotazione(id_camera, nominativo))
        
        elif scelta == "5":
            print("Programma terminato")
            break    
        else:
            print("Scelta non valida, riprova.")

# Test per il programma
hotel = Hotel("Hotel Test")

# Aggiungi camere libere
# La creazione delle camere influisce anche sulla prenotazione fatta dall'interfaccia del menu
# Si può prenotare solo una camera effettivamente creata
camera1 = Camera(2, True)
camera2 = Camera(3, False)
camera3 = Camera(2, True)
hotel.camere_libere.extend([camera1, camera2, camera3])

# Test situazione_camere
print("\n--- Situazione iniziale delle camere ---")
hotel.situazione_camere()

print("\n--- Test prenotazione camere ---")
# Test prenotazione_camera
id_camera, prezzo = hotel.prenotazione_camera("2024-08-10", "2024-08-15", "Mario Rossi", 2, True)
id_camera, prezzo = hotel.prenotazione_camera("2024-08-20", "2024-08-25", "Luca Bianchi", 3, False)


# Test situazione_camere dopo prenotazione
print("\n--- Situazione delle camere dopo prenotazione ---")
hotel.situazione_camere()

# Test resoconto_camere
hotel.resoconto_camere("resoconto.txt")
with open("resoconto.txt", 'r') as f:
    print("\n--- Contenuto del file resoconto.txt ---")
    print(f.read())

# Test assegna_camera
assegna = hotel.assegna_camera(id_camera, "Luca Bianchi")
print(f"\n{assegna}")

# Test situazione_camere dopo assegnazione
print("\n--- Situazione delle camere dopo assegnazione ---")
hotel.situazione_camere()

# Test libera_camera
libera = hotel.libera_camera(id_camera, "Luca Bianchi")
print(f"\n{libera}")

# Test situazione_camere dopo liberazione
print("\n--- Situazione delle camere dopo liberazione ---")
hotel.situazione_camere()

# Test disdici_prenotazione
id_camera, prezzo = hotel.prenotazione_camera("2024-08-20", "2024-08-25", "Luca Bianchi", 3, False)
disdetta = hotel.disdici_prenotazione(id_camera, "Luca Bianchi")
print(f"\n{disdetta}")

# Test situazione_camere dopo disdetta
print("\n--- Situazione delle camere dopo disdetta ---")
hotel.situazione_camere()

# Test menu prenotazioni
hotel.menu_prenotazioni()

