import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import time
from datetime import datetime
from save_result import save_results_to_txt

class QueueSimulator:
    """
    Classe pour simuler différents types de files d'attente mono-serveur
    """
    
    def __init__(self, lmbda, mu, nb_clients=1000000, seed=None):
        """
        Initialisation du simulateur
        
        Paramètres:
        -----------
        lmbda : float
            Taux d'arrivée moyen (λ)
        mu : float
            Taux de service moyen (μ)
        nb_clients : int
            Nombre de clients à simuler
        seed : int
            Graine pour le générateur aléatoire
        """
        self.lmbda = lmbda          # Taux d'arrivée des clients
        self.mu = mu                # Taux de service
        self.nb_clients = nb_clients  # Nombre de clients à simuler
        self.rho = lmbda / mu       # Taux d'occupation théorique
        
        # Vérifier la stabilité de la file d'attente
        if self.rho >= 1:
            print(f"⚠️ Attention: ρ = {self.rho:.2f} ≥ 1, la file n'est pas stable")
        
        # Initialiser le générateur aléatoire
        if seed is not None:
            np.random.seed(seed)
    
    def generate_exponential(self, rate, size=1):
        """
        Génère des temps suivant une loi exponentielle
        
        Paramètres:
        -----------
        rate : float
            Paramètre de la loi exponentielle
        size : int
            Nombre de valeurs à générer
            
        Retourne:
        ---------
        np.array : Tableau de temps générés
        """
        return np.random.exponential(1.0/rate, size)
    
    def generate_uniform(self, a, b, size=1):
        """
        Génère des temps suivant une loi uniforme
        
        Paramètres:
        -----------
        a : float
            Borne inférieure
        b : float
            Borne supérieure
        size : int
            Nombre de valeurs à générer
            
        Retourne:
        ---------
        np.array : Tableau de temps générés
        """
        return np.random.uniform(a, b, size)
    
    def generate_normal(self, mean, std, size=1):
        """
        Génère des temps suivant une loi normale (avec valeurs positives uniquement)
        
        Paramètres:
        -----------
        mean : float
            Moyenne de la loi normale
        std : float
            Écart-type de la loi normale
        size : int
            Nombre de valeurs à générer
            
        Retourne:
        ---------
        np.array : Tableau de temps générés (tous positifs)
        """
        # Génère des valeurs selon une loi normale et prend la valeur absolue
        # pour s'assurer que tous les temps sont positifs
        return np.abs(np.random.normal(mean, std, size))
    
    def simulate_MM1(self):
        """
        Simule une file d'attente M/M/1
        
        Retourne:
        ---------
        dict : Dictionnaire contenant les résultats de la simulation
        """
        print("Simulation de la file M/M/1 en cours...")
        
        # Générer les temps inter-arrivées (loi exponentielle)
        inter_arrival_times = self.generate_exponential(self.lmbda, self.nb_clients)
        
        # Générer les temps de service (loi exponentielle)
        service_times = self.generate_exponential(self.mu, self.nb_clients)
        
        # Calculer les résultats avec la simulation
        return self._run_simulation(inter_arrival_times, service_times)
    
    def simulate_GM1(self, distribution="uniform"):
        """
        Simule une file d'attente G/M/1 avec une loi générale pour les arrivées
        
        Paramètres:
        -----------
        distribution : str
            Type de distribution à utiliser pour les arrivées
            
        Retourne:
        ---------
        dict : Dictionnaire contenant les résultats de la simulation
        """
        print(f"Simulation de la file G/M/1 ({distribution}) en cours...")
        
        # Générer les temps inter-arrivées selon la distribution choisie
        if distribution == "uniform":
            # Loi uniforme avec moyenne 1/lambda
            mean = 1.0/self.lmbda
            inter_arrival_times = self.generate_uniform(0.5*mean, 1.5*mean, self.nb_clients)
        elif distribution == "normal":
            # Loi normale avec moyenne 1/lambda et écart-type ajusté
            mean = 1.0/self.lmbda
            inter_arrival_times = self.generate_normal(mean, mean/3, self.nb_clients)
        else:
            raise ValueError("Distribution non supportée")
        
        # Générer les temps de service (loi exponentielle)
        service_times = self.generate_exponential(self.mu, self.nb_clients)
        
        # Calculer les résultats avec la simulation
        return self._run_simulation(inter_arrival_times, service_times)
    
    def simulate_MG1(self, distribution="uniform"):
        """
        Simule une file d'attente M/G/1 avec une loi générale pour le service
        
        Paramètres:
        -----------
        distribution : str
            Type de distribution à utiliser pour le service
            
        Retourne:
        ---------
        dict : Dictionnaire contenant les résultats de la simulation
        """
        print(f"Simulation de la file M/G/1 ({distribution}) en cours...")
        
        # Générer les temps inter-arrivées (loi exponentielle)
        inter_arrival_times = self.generate_exponential(self.lmbda, self.nb_clients)
        
        # Générer les temps de service selon la distribution choisie
        if distribution == "uniform":
            # Loi uniforme avec moyenne 1/mu
            mean = 1.0/self.mu
            service_times = self.generate_uniform(0.5*mean, 1.5*mean, self.nb_clients)
        elif distribution == "normal":
            # Loi normale avec moyenne 1/mu et écart-type ajusté
            mean = 1.0/self.mu
            service_times = self.generate_normal(mean, mean/3, self.nb_clients)
        else:
            raise ValueError("Distribution non supportée")
        
        # Calculer les résultats avec la simulation
        return self._run_simulation(inter_arrival_times, service_times)
    
    def _run_simulation(self, inter_arrival_times, service_times):
        """
        Exécute la simulation à partir des temps d'arrivée et de service
        
        Paramètres:
        -----------
        inter_arrival_times : np.array
            Tableau des temps inter-arrivées
        service_times : np.array
            Tableau des temps de service
            
        Retourne:
        ---------
        dict : Dictionnaire contenant les résultats de la simulation
        """
        # Initialisation des variables
        arrival_times = np.cumsum(inter_arrival_times)  # Temps d'arrivée absolus
        departure_times = np.zeros(self.nb_clients)     # Temps de départ
        wait_times = np.zeros(self.nb_clients)         # Temps d'attente dans la file
        
        # Premier client
        departure_times[0] = arrival_times[0] + service_times[0]
        
        # Traitement client par client
        for i in range(1, self.nb_clients):
            # Le client attend si le serveur est encore occupé à son arrivée
            wait_times[i] = max(0, departure_times[i-1] - arrival_times[i])
            
            # Le temps de départ est la somme du temps d'arrivée, du temps d'attente et du temps de service
            departure_times[i] = arrival_times[i] + wait_times[i] + service_times[i]
        
        # Calcul des métriques
        response_times = departure_times - arrival_times  # Temps de réponse = temps dans le système
        
        # Calcul du taux d'occupation (temps serveur occupé / temps total)
        total_time = departure_times[-1]  # Temps total de la simulation
        server_busy_time = np.sum(service_times)  # Temps total où le serveur est occupé
        server_utilization = server_busy_time / total_time
        
        # Retourne un dictionnaire avec les résultats
        return {
            "mean_wait_time": np.mean(wait_times),
            "mean_response_time": np.mean(response_times),
            "server_utilization": server_utilization,
            "theoretical_utilization": self.rho,
            "wait_times": wait_times,
            "response_times": response_times
        }


def run_experiments(mu=1.0, nb_clients=1000000, n_repeats=5):
    """
    Exécute les expériences pour différentes valeurs de lambda
    
    Paramètres:
    -----------
    mu : float
        Taux de service moyen
    nb_clients : int
        Nombre de clients à simuler
    n_repeats : int
        Nombre de répétitions pour chaque expérience
        
    Retourne:
    ---------
    dict : Dictionnaire contenant les résultats des expériences
    """
    # Valeurs de lambda à tester
    lambda_values = np.arange(0.1, 1.0, 0.1)
    
    # Dictionnaires pour stocker les résultats
    results_mm1 = {
        "lambda": lambda_values,
        "mean_response_time": np.zeros(len(lambda_values)),
        "mean_wait_time": np.zeros(len(lambda_values)),
        "server_utilization": np.zeros(len(lambda_values))
    }
    
    results_gm1 = {
        "lambda": lambda_values,
        "mean_response_time": np.zeros(len(lambda_values)),
        "mean_wait_time": np.zeros(len(lambda_values)),
        "server_utilization": np.zeros(len(lambda_values))
    }
    
    results_mg1 = {
        "lambda": lambda_values,
        "mean_response_time": np.zeros(len(lambda_values)),
        "mean_wait_time": np.zeros(len(lambda_values)),
        "server_utilization": np.zeros(len(lambda_values))
    }
    
    # Pour chaque valeur de lambda
    for i, lmbda in enumerate(lambda_values):
        print(f"\nExpérience pour λ = {lmbda:.1f}, μ = {mu:.1f} (ρ = {lmbda/mu:.2f})")
        
        # Répéter l'expérience plusieurs fois pour stabiliser les résultats
        mm1_response_times = []
        mm1_wait_times = []
        mm1_utilizations = []
        
        gm1_response_times = []
        gm1_wait_times = []
        gm1_utilizations = []
        
        mg1_response_times = []
        mg1_wait_times = []
        mg1_utilizations = []
        
        for j in range(n_repeats):
            print(f"Répétition {j+1}/{n_repeats}")
            
            # Simulation M/M/1
            simulator = QueueSimulator(lmbda, mu, nb_clients, seed=j)
            results = simulator.simulate_MM1()
            mm1_response_times.append(results["mean_response_time"])
            mm1_wait_times.append(results["mean_wait_time"])
            mm1_utilizations.append(results["server_utilization"])
            
            # Simulation G/M/1 (avec loi uniforme)
            simulator = QueueSimulator(lmbda, mu, nb_clients, seed=j+100)
            results = simulator.simulate_GM1(distribution="uniform")
            gm1_response_times.append(results["mean_response_time"])
            gm1_wait_times.append(results["mean_wait_time"])
            gm1_utilizations.append(results["server_utilization"])
            
            # Simulation M/G/1 (avec loi uniforme)
            simulator = QueueSimulator(lmbda, mu, nb_clients, seed=j+200)
            results = simulator.simulate_MG1(distribution="uniform")
            mg1_response_times.append(results["mean_response_time"])
            mg1_wait_times.append(results["mean_wait_time"])
            mg1_utilizations.append(results["server_utilization"])
        
        # Moyennes des répétitions
        results_mm1["mean_response_time"][i] = np.mean(mm1_response_times)
        results_mm1["mean_wait_time"][i] = np.mean(mm1_wait_times)
        results_mm1["server_utilization"][i] = np.mean(mm1_utilizations)
        
        results_gm1["mean_response_time"][i] = np.mean(gm1_response_times)
        results_gm1["mean_wait_time"][i] = np.mean(gm1_wait_times)
        results_gm1["server_utilization"][i] = np.mean(gm1_utilizations)
        
        results_mg1["mean_response_time"][i] = np.mean(mg1_response_times)
        results_mg1["mean_wait_time"][i] = np.mean(mg1_wait_times)
        results_mg1["server_utilization"][i] = np.mean(mg1_utilizations)
        
        # Afficher les résultats intermédiaires
        print(f"M/M/1 - Temps de réponse moyen: {results_mm1['mean_response_time'][i]:.4f}, "
              f"Taux d'occupation: {results_mm1['server_utilization'][i]:.4f}")
        print(f"G/M/1 - Temps de réponse moyen: {results_gm1['mean_response_time'][i]:.4f}, "
              f"Taux d'occupation: {results_gm1['server_utilization'][i]:.4f}")
        print(f"M/G/1 - Temps de réponse moyen: {results_mg1['mean_response_time'][i]:.4f}, "
              f"Taux d'occupation: {results_mg1['server_utilization'][i]:.4f}")
    
    return results_mm1, results_gm1, results_mg1


def plot_results(results_mm1, results_gm1, results_mg1):
    """
    Affiche les graphiques des résultats
    
    Paramètres:
    -----------
    results_mm1 : dict
        Résultats pour M/M/1
    results_gm1 : dict
        Résultats pour G/M/1
    results_mg1 : dict
        Résultats pour M/G/1
    """
    plt.figure(figsize=(18, 12))
    
    # Graphique du temps de réponse moyen
    plt.subplot(2, 2, 1)
    plt.plot(results_mm1["lambda"], results_mm1["mean_response_time"], 'o-', label='M/M/1')
    plt.plot(results_gm1["lambda"], results_gm1["mean_response_time"], 's-', label='G/M/1')
    plt.plot(results_mg1["lambda"], results_mg1["mean_response_time"], '^-', label='M/G/1')
    plt.xlabel('Taux d\'arrivée (λ)')
    plt.ylabel('Temps de réponse moyen')
    plt.title('Temps de réponse moyen en fonction du taux d\'arrivée')
    plt.grid(True)
    plt.legend()
    
    # Graphique du temps d'attente moyen
    plt.subplot(2, 2, 2)
    plt.plot(results_mm1["lambda"], results_mm1["mean_wait_time"], 'o-', label='M/M/1')
    plt.plot(results_gm1["lambda"], results_gm1["mean_wait_time"], 's-', label='G/M/1')
    plt.plot(results_mg1["lambda"], results_mg1["mean_wait_time"], '^-', label='M/G/1')
    plt.xlabel('Taux d\'arrivée (λ)')
    plt.ylabel('Temps d\'attente moyen')
    plt.title('Temps d\'attente moyen en fonction du taux d\'arrivée')
    plt.grid(True)
    plt.legend()
    
    # Graphique du taux d'occupation
    plt.subplot(2, 2, 3)
    plt.plot(results_mm1["lambda"], results_mm1["server_utilization"], 'o-', label='M/M/1')
    plt.plot(results_gm1["lambda"], results_gm1["server_utilization"], 's-', label='G/M/1')
    plt.plot(results_mg1["lambda"], results_mg1["server_utilization"], '^-', label='M/G/1')
    # Ligne théorique rho = lambda/mu (avec mu=1)
    plt.plot(results_mm1["lambda"], results_mm1["lambda"], 'k--', label='Théorique (ρ = λ/μ)')
    plt.xlabel('Taux d\'arrivée (λ)')
    plt.ylabel('Taux d\'occupation du serveur')
    plt.title('Taux d\'occupation du serveur en fonction du taux d\'arrivée')
    plt.grid(True)
    plt.legend()
    
    # Comparaison des distributions
    plt.subplot(2, 2, 4)
    # Calculer le ratio entre les temps de réponse
    ratio_gm1_mm1 = results_gm1["mean_response_time"] / results_mm1["mean_response_time"]
    ratio_mg1_mm1 = results_mg1["mean_response_time"] / results_mm1["mean_response_time"]
    
    plt.plot(results_mm1["lambda"], ratio_gm1_mm1, 's-', label='G/M/1 / M/M/1')
    plt.plot(results_mm1["lambda"], ratio_mg1_mm1, '^-', label='M/G/1 / M/M/1')
    plt.axhline(y=1, color='k', linestyle='--', label='Référence')
    plt.xlabel('Taux d\'arrivée (λ)')
    plt.ylabel('Ratio des temps de réponse')
    plt.title('Comparaison des modèles par rapport à M/M/1')
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('resultats_files_attente.png', dpi=300)
    plt.show()


def calculate_theoretical_metrics(lambda_values, mu=1.0):
    """
    Calcule les métriques théoriques pour le modèle M/M/1
    
    Paramètres:
    -----------
    lambda_values : np.array
        Valeurs de lambda à utiliser
    mu : float
        Taux de service moyen
        
    Retourne:
    ---------
    dict : Dictionnaire contenant les métriques théoriques
    """
    rho_values = lambda_values / mu
    
    # Pour M/M/1
    # Temps moyen de réponse: E[T] = 1 / (μ - λ)
    response_times = 1 / (mu - lambda_values)
    
    # Temps moyen d'attente: E[W] = ρ / (μ - λ)
    wait_times = rho_values / (mu - lambda_values)
    
    return {
        "lambda": lambda_values,
        "rho": rho_values,
        "mean_response_time": response_times,
        "mean_wait_time": wait_times
    }


def compare_with_theory(results_mm1, theory):
    """
    Compare les résultats de simulation avec la théorie pour M/M/1
    
    Paramètres:
    -----------
    results_mm1 : dict
        Résultats de la simulation pour M/M/1
    theory : dict
        Métriques théoriques calculées
    """
    plt.figure(figsize=(15, 10))
    
    # Temps de réponse
    plt.subplot(2, 1, 1)
    plt.plot(results_mm1["lambda"], results_mm1["mean_response_time"], 'o-', label='Simulation M/M/1')
    plt.plot(theory["lambda"], theory["mean_response_time"], 'k--', label='Théorie M/M/1')
    plt.xlabel('Taux d\'arrivée (λ)')
    plt.ylabel('Temps de réponse moyen')
    plt.title('Comparaison Simulation vs Théorie - Temps de réponse moyen')
    plt.grid(True)
    plt.legend()
    
    # Taux d'occupation
    plt.subplot(2, 1, 2)
    plt.plot(results_mm1["lambda"], results_mm1["server_utilization"], 'o-', label='Simulation M/M/1')
    plt.plot(theory["lambda"], theory["rho"], 'k--', label='Théorie M/M/1')
    plt.xlabel('Taux d\'arrivée (λ)')
    plt.ylabel('Taux d\'occupation du serveur')
    plt.title('Comparaison Simulation vs Théorie - Taux d\'occupation')
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('comparaison_theorie.png', dpi=300)
    plt.show()


def main():
    """
    Fonction principale qui exécute les simulations et affiche les résultats
    """
    print("=== TP : Simulation des files d'attente M/M/1, G/M/1 et M/G/1 ===")
    
    # Paramètres
    mu = 1.0                 # Taux de service fixé à 1
    nb_clients = 1000000     # Nombre de clients (défaut)
    n_repeats = 3            # Nombre de répétitions pour chaque expérience
    
    # Possibilité de modifier les paramètres
    print(f"Paramètres par défaut: μ = {mu}, Nombre de clients = {nb_clients}, Répétitions = {n_repeats}")
    choice = input("Voulez-vous modifier ces paramètres? (o/n): ")
    
    if choice.lower() == 'o':
        try:
            nb_clients = int(input("Nombre de clients (recommandé: 1000000): "))
            if nb_clients < 1000:
                print("⚠️ Attention: Un petit nombre de clients peut donner des résultats moins précis")
                
            n_repeats = int(input("Nombre de répétitions pour chaque expérience (recommandé: 3-5): "))
            if n_repeats < 1:
                n_repeats = 1
                print("Nombre de répétitions fixé à 1")
        except ValueError:
            print("Valeur invalide, utilisation des paramètres par défaut")
    
    start_time = time.time()
    
    # Exécuter les expériences
    print("\nExécution des simulations pour différentes valeurs de λ...")
    results_mm1, results_gm1, results_mg1 = run_experiments(mu, nb_clients, n_repeats)
    
    # Calculer les métriques théoriques pour M/M/1
    theory = calculate_theoretical_metrics(results_mm1["lambda"], mu)
    
    # Enregistrer les résultats dans un fichier texte
    save_results_to_txt(results_mm1, results_gm1, results_mg1, theory)
    
    # Afficher les résultats graphiques
    plot_results(results_mm1, results_gm1, results_mg1)
    
    # Comparer avec la théorie
    compare_with_theory(results_mm1, theory)
    
    end_time = time.time()
    print(f"\nTemps d'exécution total: {end_time - start_time:.2f} secondes")
    print("\nSimulations terminées! Les graphiques et les résultats texte ont été enregistrés.")


if __name__ == "__main__":
    main()