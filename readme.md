# Simulation de Files d'Attente : M/M/1, G/M/1 et M/G/1

Ce projet est une implémentation Python de simulations de files d'attente à serveur unique pour comparer le comportement de trois modèles différents : M/M/1, G/M/1 et M/G/1.

## 📋 Description

Cette simulation permet d'analyser et de comparer les performances de différents systèmes de files d'attente en fonction du taux d'arrivée λ. Les principales métriques étudiées sont :

- **Temps de réponse moyen** (temps passé dans le système)
- **Taux d'utilisation du serveur** (ρ = λ/μ)
- **Temps d'attente moyen** dans la file

## 🔧 Prérequis

Pour exécuter ce programme, vous aurez besoin des bibliothèques Python suivantes :

- `numpy`
- `matplotlib`
- `scipy`

Installation via pip :
```bash
pip install numpy matplotlib scipy
```

## 🚀 Utilisation

Exécutez le script principal :
```bash
python simulation.py
```

## 📊 Modèles Simulés

| Modèle | Type d'Arrivées | Type de Services |
|--------|-----------------|------------------|
| **M/M/1** | Exponentielles (λ) | Exponentielles (μ) |
| **G/M/1** | Générales (uniforme ou normale, moyenne = 1/λ) | Exponentielles (μ) |
| **M/G/1** | Exponentielles (λ) | Générales (uniforme ou normale, moyenne = 1/μ) |

### Notation des Modèles
- **M** : Distribution de Poisson/Exponentielle (processus markovien)
- **G** : Distribution générale (uniforme ou normale dans notre cas)
- **1** : Un seul serveur

## ⚙️ Fonctionnalités Principales

### 🎯 Simulation
- Génération de temps d'arrivée et de service selon différentes lois de probabilité
- Simulation événement par événement avec gestion précise des files d'attente
- Calcul automatique des métriques de performance
- Agrégation sur plusieurs répétitions pour réduire la variance statistique

### 📈 Analyse Comparative
- Comparaison des résultats simulés avec les prédictions théoriques (modèle M/M/1)
- Génération de graphiques comparatifs des performances
- Calcul des ratios de performance entre modèles
- Validation de la stabilité du système (condition : ρ < 1)

### 📝 Génération de Rapports
- Visualisations graphiques détaillées avec superposition théorique
- Rapports textuels complets avec tableaux de résultats formatés
- Sauvegarde automatique des résultats avec horodatage

## 🏗️ Architecture du Code

### Classe `QueueSimulator`

#### Initialisation
```python
QueueSimulator(lmbda, mu, nb_clients, seed=None)
```

**Paramètres :**
- `lmbda (λ)` : Taux d'arrivée moyen des clients
- `mu (μ)` : Taux de service moyen du serveur
- `nb_clients` : Nombre total de clients à simuler
- `seed` : Graine aléatoire pour la reproductibilité des résultats

**Vérification automatique de stabilité :** Le système vérifie que ρ = λ/μ < 1

#### Générateurs de Durées Aléatoires

- **`generate_exponential(rate, size)`** : Distribution exponentielle pour les processus sans mémoire
- **`generate_uniform(a, b, size)`** : Distribution uniforme avec bornes ajustées pour respecter la moyenne
- **`generate_normal(mean, std, size)`** : Distribution normale tronquée (valeurs strictement positives)

### 🔄 Algorithme de Simulation

#### Calcul des Temps d'Arrivée
```python
arrival_times = np.cumsum(inter_arrival_times)
```
Le client i arrive au temps : **t_i = Σ_{k≤i} X_k** (somme cumulative des intervalles)

#### Logique de Traitement des Clients

**Premier client (i=0) :**
```python
departure_times[0] = arrival_times[0] + service_times[0]
wait_times[0] = 0  # Pas d'attente pour le premier client
```

**Clients suivants (i≥1) :**
```python
# Calcul du temps d'attente
wait_times[i] = max(0, departure_times[i-1] - arrival_times[i])

# Calcul du temps de départ
departure_times[i] = arrival_times[i] + wait_times[i] + service_times[i]
```

#### 📊 Métriques Calculées

- **Temps d'attente moyen :** `W̄ = (1/N) × Σᵢ wait_times[i]`
- **Temps de réponse moyen :** `T̄ = (1/N) × Σᵢ (departure_times[i] - arrival_times[i])`
- **Utilisation du serveur :** `U = Σᵢ service_times[i] / temps_total_simulation`

## 🎲 Méthodes de Simulation par Modèle

### M/M/1 - `simulate_MM1()`
- **Arrivées :** Distribution exponentielle Exp(λ)
- **Services :** Distribution exponentielle Exp(μ)
- **Propriété :** Processus complètement markovien (sans mémoire)

### G/M/1 - `simulate_GM1(distribution)`
- **Arrivées :** Distribution générale (uniforme ou normale) avec moyenne contrôlée = 1/λ
- **Services :** Distribution exponentielle Exp(μ)
- **Impact :** Variabilité des arrivées sur les performances

### M/G/1 - `simulate_MG1(distribution)`
- **Arrivées :** Distribution exponentielle Exp(λ)
- **Services :** Distribution générale (uniforme ou normale) avec moyenne contrôlée = 1/μ
- **Impact :** Variabilité des services sur les performances

## 🧪 Protocole d'Expérimentation

### Paramètres d'Expérience
- **Taux d'arrivée λ :** Varie de 0.1 à 0.9 par pas de 0.1
- **Taux de service μ :** Fixé à 1.0
- **Répétitions :** Nombre configurable (recommandé : ≥ 5 pour la robustesse statistique)
- **Nombre de clients :** Suffisamment grand pour la convergence (recommandé : ≥ 1000)

### Processus Expérimental
1. **Pour chaque valeur de λ :**
   - Génération de graines aléatoires différentes pour chaque répétition
   - Exécution simultanée des trois modèles (M/M/1, G/M/1, M/G/1)
   - Collecte des métriques individuelles
   - Calcul des moyennes et écarts-types sur les répétitions

2. **Stockage structuré :** Organisation des résultats dans des dictionnaires indexés par λ

## 📐 Fondements Théoriques (M/M/1)

### Formules de Référence Exactes
- **Facteur d'utilisation :** `ρ = λ/μ`
- **Temps de séjour moyen :** `E[T] = 1/(μ-λ) = 1/(μ(1-ρ))`
- **Temps d'attente moyen :** `E[W] = ρ/(μ-λ) = ρ/(μ(1-ρ))`
- **Nombre moyen de clients :** `E[N] = ρ/(1-ρ)`

### Processus de Validation
- Comparaison systématique simulation vs théorie pour chaque λ
- Calcul des écarts relatifs en pourcentage
- Vérification de la convergence pour les grandes simulations

## 📈 Visualisations et Analyses

### Graphiques Générés Automatiquement

1. **Temps de Réponse vs λ**
   - Courbes pour les trois modèles
   - Superposition de la courbe théorique M/M/1
   - Mise en évidence des écarts dus à la variabilité

2. **Temps d'Attente vs λ**
   - Comparaison des comportements
   - Validation théorique pour M/M/1

3. **Utilisation du Serveur vs λ**
   - Droite théorique ρ = λ/μ
   - Vérification de la cohérence des simulations

4. **Ratios de Performance**
   - `T̄_{G/M/1}/T̄_{M/M/1}` : Impact de la variabilité des arrivées
   - `T̄_{M/G/1}/T̄_{M/M/1}` : Impact de la variabilité des services

### Interprétation des Résultats
- **Ratios > 1 :** Dégradation des performances par rapport au cas markovien
- **Ratios < 1 :** Amélioration (rare, dépendant des distributions choisies)
- **Convergence asymptotique :** Validation de la robustesse statistique

## 📄 Système de Rapport Automatique

### Contenu du Rapport Généré
1. **En-tête avec paramètres de simulation**
   - Configuration générale
   - Nombre de répétitions et de clients
   - Distributions utilisées

2. **Tableau détaillé par valeur de λ**
   - Facteur d'utilisation théorique ρ
   - Métriques T̄, W̄, U pour chaque modèle
   - Écarts percentuels simulation/théorie (M/M/1)
   - Ratios de performance inter-modèles

3. **Section d'analyse et interprétation**
   - Notes sur la validité des résultats
   - Hypothèses du modèle et limitations
   - Recommandations d'utilisation

4. **Métadonnées**
   - Horodatage de génération
   - Configuration système utilisée

## 🔍 Points Techniques Clés

### Gestion des Événements de Simulation
1. **Génération robuste des durées** selon les lois spécifiées
2. **Calcul incrémental des arrivées** par cumul efficace
3. **Gestion rigoureuse de l'occupation du serveur**
4. **Calcul précis des temps de départ** incluant toutes les composantes
5. **Agrégation statistique multi-niveaux** (clients × répétitions)

### Robustesse et Fiabilité
- **Vérification préalable de stabilité** du système
- **Gestion des cas limites** (distributions normales négatives)
- **Reproductibilité garantie** via contrôle des graines aléatoires
- **Validation croisée** par comparaison théorique systématique
- **Gestion d'erreurs** et messages informatifs

## 💡 Applications et Cas d'Usage

### Domaines d'Application
- **Analyse de performance** de systèmes informatiques
- **Dimensionnement** de centres d'appels
- **Optimisation** de processus industriels
- **Recherche académique** en théorie des files d'attente

### Objectifs Pédagogiques
- **Illustration pratique** des concepts théoriques
- **Comparaison empirique** des modèles stochastiques
- **Validation expérimentale** des formules analytiques
- **Sensibilisation** à l'impact de la variabilité

## 🎯 Résultats Attendus et Interprétation

### Comportements Typiques Observés
- **M/M/1 :** Concordance étroite avec la théorie (validation)
- **G/M/1 :** Impact modéré de la variabilité des arrivées
- **M/G/1 :** Impact plus marqué de la variabilité des services
- **Convergence :** Stabilisation des métriques avec l'augmentation du nombre de clients

### Facteurs d'Influence
- **Niveau de charge ρ :** Impact croissant près de la saturation (ρ → 1)
- **Type de distribution :** Écarts variables selon uniforme vs normale
- **Taille d'échantillon :** Précision croissante avec le nombre de clients
- **Nombre de répétitions :** Réduction de la variance des estimateurs

## 📋 Conclusion

Cette simulation offre un environnement complet et rigoureux pour :

- **Étudier quantitativement** les performances des systèmes de files d'attente
- **Comprendre l'impact** des différentes distributions sur le comportement du système
- **Valider expérimentalement** les modèles théoriques classiques
- **Analyser finement** la variabilité et la robustesse des performances

Le framework combine rigueur mathématique, implémentation efficace et présentation claire des résultats, en faisant un outil de référence pour l'analyse des systèmes de files d'attente à serveur unique.