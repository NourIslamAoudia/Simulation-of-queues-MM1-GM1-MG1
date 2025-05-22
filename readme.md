# Queue Simulation: M/M/1, G/M/1 and M/G/1

This project is a Python implementation of single-server queue simulations to compare the behavior of three different models: M/M/1, G/M/1, and M/G/1.

## Description

This simulation allows analyzing and comparing the performance of different queueing systems based on the arrival rate λ. The main metrics studied are:

- Average response time (time spent in the system)
- Server utilization rate (ρ = λ/μ)
- Average waiting time in the queue

## Prerequisites

To run this program, you'll need the following Python libraries:
- numpy
- matplotlib
- scipy

You can install them with pip:
```bash
pip install numpy matplotlib scipy
```

## Usage

Execute the main script:
```bash
python simulation.py
```
# Simulation de Files d'Attente à Un Serveur

## Description

Ce projet simule et compare trois modèles de file d'attente à un seul serveur : M/M/1, G/M/1, et M/G/1. Il fournit une analyse comparative complète avec validation théorique, visualisations graphiques et rapports détaillés.

## Modèles Simulés

| Modèle | Arrivées | Services |
|--------|----------|----------|
| **M/M/1** | Exponentielles (λ) | Exponentielles (μ) |
| **G/M/1** | Générales (uniforme ou normale, moyenne = 1/λ) | Exponentielles (μ) |
| **M/G/1** | Exponentielles (λ) | Générales (uniforme ou normale, moyenne = 1/μ) |

## Fonctionnalités

### Simulation
- Génération de temps d'arrivée et de service selon différentes lois de probabilité
- Simulation événement par événement
- Calcul des métriques de performance : temps d'attente, temps de réponse, utilisation du serveur
- Agrégation sur plusieurs répétitions pour réduire la variance

### Analyse
- Comparaison des résultats simulés avec les prédictions théoriques (M/M/1)
- Graphiques comparatifs des performances
- Ratios de performance entre modèles
- Validation de la stabilité du système (ρ < 1)

### Génération de Rapports
- Graphiques détaillés avec comparaisons théoriques
- Rapports textuels complets avec tableaux de résultats
- Sauvegarde automatique des résultats

## Structure du Code

### Classe QueueSimulator

#### Initialisation
```python
QueueSimulator(lmbda, mu, nb_clients, seed)
```

**Paramètres :**
- `lmbda (λ)` : taux d'arrivée moyen
- `mu (μ)` : taux de service moyen  
- `nb_clients` : nombre total de clients à simuler
- `seed` : graine pour reproductibilité

**Vérification de stabilité :** ρ = λ/μ < 1

#### Générateurs de Durées Aléatoires

- **Exponentielle** : `generate_exponential(rate, size)` - pour processus sans mémoire
- **Uniforme** : `generate_uniform(a, b, size)` - distribution uniforme centrée
- **Normale** : `generate_normal(mean, std, size)` - distribution normale tronquée (valeurs positives)

### Algorithme de Simulation

#### Calcul des Temps d'Arrivée
```python
arrival_times = np.cumsum(inter_arrival_times)
```
Le client i arrive à t_i = Σ_{k≤i} X_k

#### Calcul des Départs
- **Premier client (i=0) :**
  ```python
  departure_times[0] = arrival_times[0] + service_times[0]
  wait_times[0] = 0
  ```

- **Clients suivants (i≥1) :**
  ```python
  wait_times[i] = max(0, departure_times[i-1] - arrival_times[i])
  departure_times[i] = arrival_times[i] + wait_times[i] + service_times[i]
  ```

#### Métriques Calculées

- **Temps d'attente moyen :** W̄ = (1/N) Σᵢ wait_times[i]
- **Temps de réponse moyen :** T̄ = (1/N) Σᵢ (departure_times[i] - arrival_times[i])
- **Utilisation du serveur :** U = Σᵢ service_times[i] / temps_total

## Méthodes de Simulation

### M/M/1 (`simulate_MM1`)
- Arrivées : distribution exponentielle Exp(λ)
- Services : distribution exponentielle Exp(μ)

### G/M/1 (`simulate_GM1(distribution)`)
- Arrivées : distribution générale (uniforme ou normale) avec moyenne 1/λ
- Services : distribution exponentielle Exp(μ)

### M/G/1 (`simulate_MG1(distribution)`)
- Arrivées : distribution exponentielle Exp(λ)
- Services : distribution générale (uniforme ou normale) avec moyenne 1/μ

## Expérimentation

### Paramètres d'Expérience
- λ variant de 0.1 à 0.9 (pas de 0.1)
- μ = 1 (fixe)
- Nombre de répétitions configurable (typiquement ≥ 3)

### Processus
1. Pour chaque valeur de λ :
   - Exécution de multiples répétitions avec graines différentes
   - Simulation des trois modèles
   - Calcul des moyennes sur les répétitions
   - Stockage des résultats

## Analyse Théorique (M/M/1)

### Formules de Référence
- **Facteur d'utilisation :** ρ = λ/μ
- **Temps de séjour moyen :** E[T] = 1/(μ-λ)
- **Temps d'attente moyen :** E[W] = ρ/(μ-λ)

### Validation
Comparaison systématique entre résultats simulés et prédictions théoriques pour le modèle M/M/1.

## Visualisations

### Graphiques Générés
1. **Temps de réponse** vs λ pour les trois modèles
2. **Temps d'attente** vs λ 
3. **Utilisation du serveur** vs λ (avec droite théorique ρ)
4. **Ratios de performance** : T̄_{G/M/1}/T̄_{M/M/1} et T̄_{M/G/1}/T̄_{M/M/1}

### Comparaison Théorique
Superposition des courbes simulées et théoriques pour validation du modèle M/M/1.

## Rapport de Résultats

Le script génère automatiquement un rapport texte détaillé comprenant :

1. **Paramètres et résumé** des modèles simulés
2. **Tableau détaillé** pour chaque λ :
   - Valeurs théoriques de ρ
   - Métriques T̄, W̄, U pour chaque modèle
   - Écarts (%) entre simulation et théorie
   - Ratios de performance
3. **Notes d'interprétation** et hypothèses
4. **Horodatage** de génération

## Points Clés de l'Implémentation

### Événements de Simulation
1. **Génération des durées** selon les lois spécifiées
2. **Calcul des arrivées** par cumul des intervalles
3. **Gestion de l'attente** si serveur occupé
4. **Calcul des départs** incluant attente et service
5. **Agrégation statistique** sur clients et répétitions

### Robustesse
- Vérification de stabilité du système
- Gestion des valeurs négatives (distributions normales)
- Reproductibilité via graines aléatoires
- Validation par comparaison théorique

## Usage

Le code fournit un cadre complet pour :
- **Étudier empiriquement** les performances de files d'attente mono-serveur
- **Comparer** l'impact des différentes distributions
- **Valider** les modèles théoriques
- **Analyser** la variabilité des performances

## Conclusion

Cette simulation combine rigueur statistique, validation théorique et visualisation claire pour une analyse complète des systèmes de files d'attente. Elle permet de quantifier l'impact des différentes distributions sur les performances du système et de valider les modèles théoriques classiques.

