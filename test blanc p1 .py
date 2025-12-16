from abc import ABC, abstractmethod

class CapaciteError(Exception):
    """Exception levée si la capacité est négative."""
    def __init__(self, message="La capacité ne peut pas être négative."):
        super().__init__(message)

class Vehicule(ABC):
    """Classe abstraite pour les véhicules."""
    
    def __init__(self, nom_client, matricule, capacite):
        self.nom_client = nom_client
        self.matricule = matricule
        self.capacite = capacite  # Utilisation du setter

    @property
    def capacite(self):
        """Getter pour récupérer la capacité."""
        return self._capacite

    @capacite.setter
    def capacite(self, valeur):
        """Setter pour définir la capacité en vérifiant qu’elle n’est pas négative."""
        if valeur < 0:
            raise CapaciteError(f"Capacité invalide ({valeur}kg) : La capacité doit être positive.")
        self._capacite = valeur

    def ajuster_capacite(self, valeur):
        """Ajuste la capacité de transport sans tomber en négatif."""
        nouvelle_capacite = self.capacite + valeur
        if nouvelle_capacite < 0:
            raise CapaciteError(f"L'ajustement de capacité ({valeur}kg) est invalide.")
        self.capacite = nouvelle_capacite

    @abstractmethod
    def calculer_efficiency(self):
        """Méthode abstraite qui doit être implémentée dans les sous-classes."""
        raise NotImplementedError("La méthode calculer_efficiency() doit être définie dans la sous-classe.")

    def __str__(self):
        return f"Client: {self.nom_client} | Matricule: {self.matricule} | Capacité: {self.capacite}kg"

    def __eq__(self, other):
        """Compare deux véhicules selon leur matricule."""
        if isinstance(other, Vehicule):
            return self.matricule == other.matricule
        return False

class Voiture(Vehicule):
    """Classe représentant une voiture."""
    
    def __init__(self, nom_client, matricule, capacite, consommation, carburant_disponible):
        super().__init__(nom_client, matricule, capacite)
        self.consommation = consommation  # litres/100 km
        self.carburant_disponible = carburant_disponible  # litres de carburant disponibles

    def calculer_efficiency(self):
        if self.consommation > 0:
            return (self.carburant_disponible / self.consommation) * 100
        return 0

class Camion(Vehicule):
    """Classe représentant un camion."""
    
    def __init__(self, nom_client, matricule, capacite, charge_max, consommation_par_tonne):
        super().__init__(nom_client, matricule, capacite)
        self.charge_max = charge_max  # Charge maximale en kg
        self.consommation_par_tonne = consommation_par_tonne  # litres/100 km par tonne

    def calculer_efficiency(self):
        """Estime l'autonomie du camion en fonction de la charge transportée."""
        if self.capacite == 0:
            return float('inf')  # Si aucune charge, autonomie infinie théorique
        consommation_totale = (self.capacite / 1000) * self.consommation_par_tonne
        return 100 / consommation_totale if consommation_totale > 0 else 0

# === Exemple d'utilisation ===
try:
    # Création d'un véhicule Voiture
    voiture = Voiture("XYZ Logistics", "123-ABC", 500, 6, 50)  # 6 L/100km, 50L disponibles
    print(voiture)
    print(f"Autonomie estimée: {voiture.calculer_efficiency()} km")
    
    # Création d'un véhicule Camion
    camion = Camion("ABC Transport", "789-XYZ", 1000, 5000, 30)  # 30 L/100 km/tonne
    print(camion)
    print(f"Autonomie estimée: {camion.calculer_efficiency()} km")

    # Comparaison des véhicules
    voiture2 = Voiture("DEF Freight", "123-ABC", 400, 5, 60)
    print(f"Les véhicules sont identiques : {voiture == voiture2}")  # True (même matricule)

    # Ajustement de la capacité
    voiture.ajuster_capacite(-200)  # Réduction de 200 kg
    print(f"Nouvelle capacité voiture: {voiture.capacite}kg")

    # Tentative de capacité négative -> Exception levée
    voiture.ajuster_capacite(-400)

except CapaciteError as e:
    print(f"Erreur de capacité : {str(e)}")
except Exception as e:
    print(f"Erreur inconnue : {str(e)}")
