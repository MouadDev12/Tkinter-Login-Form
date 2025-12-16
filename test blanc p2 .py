import tkinter as tk
from tkinter import ttk, messagebox

class CapaciteError(Exception):
    """Exception levée si la capacité est négative."""
    def __init__(self, message="La capacité ne peut pas être négative."):
        super().__init__(message)

class Vehicule:
    """Classe de base pour les véhicules."""
    
    def __init__(self, matricule, capacite):
        self.matricule = matricule
        self.capacite = capacite

    @property
    def capacite(self):
        return self._capacite

    @capacite.setter
    def capacite(self, valeur):
        if valeur < 0:
            raise CapaciteError("La capacité ne peut pas être négative.")
        self._capacite = valeur

    def calculer_efficiency(self):
        return "N/A"

    def __str__(self):
        return f"{self.matricule} - {self.capacite}kg"

class Voiture(Vehicule):
    """Classe représentant une voiture."""
    def __init__(self, matricule, capacite):
        super().__init__(matricule, capacite)

    def calculer_efficiency(self):
        return "100 km/L"  # Exemple statique

class Camion(Vehicule):
    """Classe représentant un camion."""
    def __init__(self, matricule, capacite):
        super().__init__(matricule, capacite)

    def calculer_efficiency(self):
        return "50 km/L"  # Exemple statique

class Moto(Vehicule):
    """Classe représentant une moto."""
    def __init__(self, matricule, capacite):
        super().__init__(matricule, capacite)

    def calculer_efficiency(self):
        return "200 km/L"  # Exemple statique

class GestionFlotteApp:
    """Interface graphique pour la gestion des véhicules."""

    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Flotte Automobile")

        self.vehicules = []

        # === Interface ===
        tk.Label(root, text="Matricule:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_matricule = tk.Entry(root)
        self.entry_matricule.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Capacité (kg ou L):").grid(row=1, column=0, padx=5, pady=5)
        self.entry_capacite = tk.Entry(root)
        self.entry_capacite.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Type de Véhicule:").grid(row=2, column=0, padx=5, pady=5)
        self.type_vehicule = ttk.Combobox(root, values=["Voiture", "Camion", "Moto"])
        self.type_vehicule.grid(row=2, column=1, padx=5, pady=5)
        self.type_vehicule.current(0)

        # === Boutons ===
        self.btn_ajouter = tk.Button(root, text="Ajouter", command=self.ajouter_vehicule)
        self.btn_ajouter.grid(row=3, column=0, columnspan=2, pady=10,)

        self.btn_supprimer = tk.Button(root, text="Supprimer", command=self.supprimer_vehicule)
        self.btn_supprimer.grid(row=4, column=0, columnspan=2, pady=5)

        self.btn_modifier = tk.Button(root, text="Modifier", command=self.modifier_vehicule)
        self.btn_modifier.grid(row=5, column=0, columnspan=2, pady=5)

        # === Treeview (Tableau) ===
        self.tree = ttk.Treeview(root, columns=("Matricule", "Capacité", "Type", "Efficacité"), show="headings")
        self.tree.heading("Matricule", text="Matricule")
        self.tree.heading("Capacité", text="Capacité (kg ou L)")
        self.tree.heading("Type", text="Type de Véhicule")
        self.tree.heading("Efficacité", text="Efficacité Estimée")


        self.tree.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def ajouter_vehicule(self):
        """Ajoute un véhicule à la liste et à la Treeview."""
        matricule = self.entry_matricule.get().strip()
        try:
            capacite = int(self.entry_capacite.get())
        except ValueError:
            messagebox.showerror("Erreur", "Capacité invalide, entrez un nombre entier.")
            return

        type_vehicule = self.type_vehicule.get()

        if matricule in self.vehicules:
            messagebox.showerror("Erreur", "Matricule déjà existant.")
            return

        try:
            if type_vehicule == "Voiture":
                vehicule = Voiture(matricule, capacite)
            elif type_vehicule == "Camion":
                vehicule = Camion(matricule, capacite)
            else:
                vehicule = Moto(matricule, capacite)

            self.vehicules[matricule] = vehicule

            self.tree.insert("", "end", values=(matricule, f"{capacite} kg", type_vehicule, vehicule.calculer_efficiency()))

        except CapaciteError as e:
            messagebox.showerror("Erreur", str(e))

    def supprimer_vehicule(self):
        """Supprime le véhicule sélectionné."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Aucun véhicule sélectionné.")
            return
        
        matricule = self.tree.item(selected_item, "values")[0]
        del self.vehicules[matricule]
        self.tree.delete(selected_item)

    def modifier_vehicule(self):
        """Modifie la capacité du véhicule sélectionné."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Aucun véhicule sélectionné.")
            return

        matricule = self.tree.item(selected_item, "values")[0]
        try:
            nouvelle_capacite = int(self.entry_capacite.get())
            self.vehicules[matricule].capacite = nouvelle_capacite

            self.tree.item(selected_item, values=(
                matricule,
                f"{nouvelle_capacite} kg",
                self.tree.item(selected_item, "values")[2],
                self.vehicules[matricule].calculer_efficiency()
            ))

        except ValueError:
            messagebox.showerror("Erreur", "Capacité invalide.")
        except CapaciteError as e:
            messagebox.showerror("Erreur", str(e))
            

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionFlotteApp(root)
    root.mainloop()
