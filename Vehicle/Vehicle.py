import random

class Vehicle:
    tipologia = "Veicolo" 
    
    def __init__(self, nome, cilindrata, km=0):
        self.nome = nome
        self.cilindrata = cilindrata
        self.km = km

    def simula_viaggio(self):
        # Simula un viaggio e aggiorna km con un valore casuale
        km_percorsi = random.randint(5, 500)
        self.km += km_percorsi
        return self.km

    def describe(self):
        # Stampa le intestazioni della tabella
        print(f"{'Nome':<15} {'Cilindrata':<15} {'KM':<15} {'Tipologia':<10} {'Posti':<5}")
        # Stampa i dati del veicolo
        print(f"{self.nome:<15} {self.cilindrata:<15} {self.km:<15} {self.tipologia:<10} {'N/A':<5}")

class Car(Vehicle):
    def __init__(self, nome, cilindrata, posti):
        super().__init__(nome, cilindrata)
        self.posti = posti
        self.tipologia = "Auto"  # Imposta il valore specifico per Car

    def describe(self):
        # Chiama il metodo describe della classe base e aggiunge i posti
        print(f"{'Nome':<15} {'Cilindrata':<15} {'KM':<15} {'Tipologia':<10} {'Posti':<5}")
        print(f"{self.nome:<15} {self.cilindrata:<15} {self.km:<15} {self.tipologia:<10} {self.posti:<5}")

class Bus(Vehicle):
    def __init__(self, nome, cilindrata, posti):
        super().__init__(nome, cilindrata)
        self.posti = posti
        self.tipologia = "Bus"  # Imposta il valore specifico per Bus

    def describe(self):
        # Chiama il metodo describe della classe base e aggiunge i posti
        print(f"{'Nome':<15} {'Cilindrata':<15} {'KM':<15} {'Tipologia':<10} {'Posti':<5}")
        print(f"{self.nome:<15} {self.cilindrata:<15} {self.km:<15} {self.tipologia:<10} {self.posti:<5}")

# Esempio di utilizzo
car = Car("Fiat Panda", 1200, 5)
print("Prima del viaggio:")
car.describe()
car.simula_viaggio()
print("\nDopo il viaggio:")
car.describe()

bus = Bus("Mercedes", 5000, 40)
print("\nPrima del viaggio:")
bus.describe()
bus.simula_viaggio()
print("\nDopo il viaggio:")
bus.describe()