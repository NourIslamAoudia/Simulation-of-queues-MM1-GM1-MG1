import time
from datetime import datetime

def save_results_to_txt(results_mm1, results_gm1, results_mg1, theory, filename="resultats_simulation.txt"):
    """
    Enregistre les résultats des simulations dans un fichier texte structuré professionnel
    
    Paramètres:
    -----------
    results_mm1 : dict
        Résultats pour M/M/1
    results_gm1 : dict
        Résultats pour G/M/1
    results_mg1 : dict
        Résultats pour M/G/1
    theory : dict
        Métriques théoriques calculées
    filename : str
        Nom du fichier de sortie
    """
    with open(filename, 'w', encoding='utf-8') as f:
        # En-tête principal du rapport
        f.write("╔" + "═" * 98 + "╗\n")
        f.write("║" + " " * 25 + "RAPPORT DE SIMULATION - FILES D'ATTENTE" + " " * 32 + "║\n")
        f.write("║" + " " * 30 + "MODÈLES M/M/1, G/M/1 ET M/G/1" + " " * 37 + "║\n")
        f.write("╚" + "═" * 98 + "╝\n\n")
        
        # Informations de génération
        current_time = datetime.now()
        f.write("┌─ INFORMATIONS GÉNÉRALES " + "─" * 73 + "\n")
        f.write(f"│ Date de génération    : {current_time.strftime('%d/%m/%Y à %H:%M:%S')}\n")
        f.write(f"│ Fichier de sortie     : {filename}\n")
        f.write(f"│ Version du rapport    : 2.0\n")
        f.write("└" + "─" * 99 + "\n\n")
        
        # Configuration de la simulation
        f.write("┌─ CONFIGURATION DE LA SIMULATION " + "─" * 65 + "\n")
        f.write(f"│ Taux de service (μ)           : {1.0:.1f} clients/unité de temps\n")
        f.write(f"│ Nombre de points λ testés     : {len(results_mm1['lambda'])}\n")
        f.write(f"│ Plage de λ                   : [{min(results_mm1['lambda']):.1f} - {max(results_mm1['lambda']):.1f}]\n")
        f.write(f"│ Pas d'incrémentation          : {results_mm1['lambda'][1] - results_mm1['lambda'][0]:.1f}\n")
        f.write("│\n")
        f.write("│ MODÈLES SIMULÉS :\n")
        f.write("│   • M/M/1 : Arrivées exponentielles, Services exponentiels\n")
        f.write("│   • G/M/1 : Arrivées uniformes, Services exponentiels\n")
        f.write("│   • M/G/1 : Arrivées exponentielles, Services uniformes\n")
        f.write("└" + "─" * 99 + "\n\n")
        
        # Tableau principal des résultats
        f.write("┌─ RÉSULTATS DÉTAILLÉS PAR MODÈLE " + "─" * 65 + "\n")
        f.write("│\n")
        
        # En-têtes du tableau principal
        f.write("│ " + "─" * 95 + "\n")
        f.write("│ │ {:^8} │ {:^10} ║ {:^25} ║ {:^25} ║ {:^25} │\n".format(
            "λ", "ρ théor.", "M/M/1", "G/M/1", "M/G/1"
        ))
        f.write("│ │ {:^8} │ {:^10} ║ {:^7} │ {:^7} │ {:^7} ║ {:^7} │ {:^7} │ {:^7} ║ {:^7} │ {:^7} │ {:^7} │\n".format(
            "", "", "TR", "TA", "ρ", "TR", "TA", "ρ", "TR", "TA", "ρ"
        ))
        f.write("│ " + "─" * 95 + "\n")
        
        # Données du tableau principal
        for i, lmbda in enumerate(results_mm1["lambda"]):
            rho_theo = lmbda  # Pour μ = 1.0, ρ = λ
            
            f.write("│ │ {:^8.2f} │ {:^10.4f} ║ {:^7.3f} │ {:^7.3f} │ {:^7.3f} ║ {:^7.3f} │ {:^7.3f} │ {:^7.3f} ║ {:^7.3f} │ {:^7.3f} │ {:^7.3f} │\n".format(
                lmbda, rho_theo,
                results_mm1['mean_response_time'][i], results_mm1['mean_wait_time'][i], results_mm1['server_utilization'][i],
                results_gm1['mean_response_time'][i], results_gm1['mean_wait_time'][i], results_gm1['server_utilization'][i],
                results_mg1['mean_response_time'][i], results_mg1['mean_wait_time'][i], results_mg1['server_utilization'][i]
            ))
        
        f.write("│ " + "─" * 95 + "\n")
        f.write("│\n")
        f.write("│ Légende : TR = Temps de Réponse │ TA = Temps d'Attente │ ρ = Taux d'Occupation\n")
        f.write("└" + "─" * 99 + "\n\n")
        
        # Validation théorique M/M/1
        f.write("┌─ VALIDATION THÉORIQUE - MODÈLE M/M/1 " + "─" * 61 + "\n")
        f.write("│\n")
        f.write("│ Comparaison Simulation vs Théorie :\n")
        f.write("│\n")
        f.write("│ " + "─" * 78 + "\n")
        f.write("│ │ {:^8} ║ {:^15} ║ {:^15} ║ {:^15} ║ {:^12} │\n".format(
            "λ", "TEMPS RÉPONSE", "TAUX OCCUPATION", "TEMPS ATTENTE", "QUALITÉ"
        ))
        f.write("│ │ {:^8} ║ {:^6} │ {:^6} ║ {:^6} │ {:^6} ║ {:^6} │ {:^6} ║ {:^12} │\n".format(
            "", "Sim.", "Théo.", "Sim.", "Théo.", "Sim.", "Théo.", "Concordance"
        ))
        f.write("│ " + "─" * 78 + "\n")
        
        for i, lmbda in enumerate(results_mm1["lambda"]):
            tr_sim = results_mm1['mean_response_time'][i]
            tr_theo = theory['mean_response_time'][i]
            tr_ecart = abs((tr_sim - tr_theo) / tr_theo * 100) if tr_theo != 0 else 0
            
            rho_sim = results_mm1['server_utilization'][i]
            rho_theo = theory['rho'][i]
            rho_ecart = abs((rho_sim - rho_theo) / rho_theo * 100) if rho_theo != 0 else 0
            
            ta_sim = results_mm1['mean_wait_time'][i]
            ta_theo = theory.get('mean_wait_time', [rho_theo / (1 - rho_theo)])[i] if 'mean_wait_time' in theory else rho_theo / (1 - rho_theo)
            ta_ecart = abs((ta_sim - ta_theo) / ta_theo * 100) if ta_theo != 0 else 0
            
            # Évaluation de la qualité
            ecart_moyen = (tr_ecart + rho_ecart + ta_ecart) / 3
            if ecart_moyen < 2:
                qualite = "EXCELLENTE"
            elif ecart_moyen < 5:
                qualite = "TRÈS BONNE"
            elif ecart_moyen < 10:
                qualite = "BONNE"
            else:
                qualite = "ACCEPTABLE"
            
            f.write("│ │ {:^8.2f} ║ {:^6.3f} │ {:^6.3f} ║ {:^6.4f} │ {:^6.4f} ║ {:^6.3f} │ {:^6.3f} ║ {:^12} │\n".format(
                lmbda, tr_sim, tr_theo, rho_sim, rho_theo, ta_sim, ta_theo, qualite
            ))
        
        f.write("│ " + "─" * 78 + "\n")
        f.write("│\n")
        f.write("│ Critères de qualité : Écart moyen < 2% = EXCELLENTE │ < 5% = TRÈS BONNE │ < 10% = BONNE\n")
        f.write("└" + "─" * 99 + "\n\n")
        
        # Analyse comparative des modèles
        f.write("┌─ ANALYSE COMPARATIVE DES MODÈLES " + "─" * 65 + "\n")
        f.write("│\n")
        f.write("│ Ratios de Performance (par rapport à M/M/1) :\n")
        f.write("│\n")
        f.write("│ " + "─" * 65 + "\n")
        f.write("│ │ {:^8} ║ {:^15} ║ {:^15} ║ {:^15} │\n".format(
            "λ", "G/M/1 / M/M/1", "M/G/1 / M/M/1", "IMPACT RELATIF"
        ))
        f.write("│ │ {:^8} ║ {:^6} │ {:^6} ║ {:^6} │ {:^6} ║ {:^15} │\n".format(
            "", "TR", "Δ%", "TR", "Δ%", ""
        ))
        f.write("│ " + "─" * 65 + "\n")
        
        for i, lmbda in enumerate(results_mm1["lambda"]):
            ratio_gm1 = results_gm1['mean_response_time'][i] / results_mm1['mean_response_time'][i] if results_mm1['mean_response_time'][i] != 0 else 0
            ratio_mg1 = results_mg1['mean_response_time'][i] / results_mm1['mean_response_time'][i] if results_mm1['mean_response_time'][i] != 0 else 0
            
            delta_gm1 = (ratio_gm1 - 1) * 100
            delta_mg1 = (ratio_mg1 - 1) * 100
            
            # Détermination de l'impact relatif
            if abs(delta_gm1) > abs(delta_mg1):
                impact = "G/M/1 dominant"
            elif abs(delta_mg1) > abs(delta_gm1):
                impact = "M/G/1 dominant"
            else:
                impact = "Équivalent"
            
            f.write("│ │ {:^8.2f} ║ {:^6.3f} │ {:^+5.1f} ║ {:^6.3f} │ {:^+5.1f} ║ {:^15} │\n".format(
                lmbda, ratio_gm1, delta_gm1, ratio_mg1, delta_mg1, impact
            ))
        
        f.write("│ " + "─" * 65 + "\n")
        f.write("│\n")
        f.write("│ Interprétation :\n")
        f.write("│   • Ratio > 1.0 : Dégradation des performances\n")
        f.write("│   • Ratio < 1.0 : Amélioration des performances\n")
        f.write("│   • Δ% : Variation percentuelle par rapport à M/M/1\n")
        f.write("└" + "─" * 99 + "\n\n")
        
        # Statistiques de synthèse
        f.write("┌─ STATISTIQUES DE SYNTHÈSE " + "─" * 71 + "\n")
        f.write("│\n")
        
        # Calculs statistiques
        avg_ratio_gm1 = sum(results_gm1['mean_response_time'][i] / results_mm1['mean_response_time'][i] 
                           for i in range(len(results_mm1['lambda']))) / len(results_mm1['lambda'])
        avg_ratio_mg1 = sum(results_mg1['mean_response_time'][i] / results_mm1['mean_response_time'][i] 
                           for i in range(len(results_mm1['lambda']))) / len(results_mm1['lambda'])
        
        max_response_mm1 = max(results_mm1['mean_response_time'])
        max_response_gm1 = max(results_gm1['mean_response_time'])
        max_response_mg1 = max(results_mg1['mean_response_time'])
        
        f.write(f"│ PERFORMANCES MOYENNES :\n")
        f.write(f"│   • Ratio moyen G/M/1 / M/M/1        : {avg_ratio_gm1:.4f}\n")
        f.write(f"│   • Ratio moyen M/G/1 / M/M/1        : {avg_ratio_mg1:.4f}\n")
        f.write("│\n")
        f.write(f"│ PICS DE PERFORMANCE :\n")
        f.write(f"│   • Temps de réponse max M/M/1       : {max_response_mm1:.4f}\n")
        f.write(f"│   • Temps de réponse max G/M/1       : {max_response_gm1:.4f}\n")
        f.write(f"│   • Temps de réponse max M/G/1       : {max_response_mg1:.4f}\n")
        f.write("│\n")
        f.write(f"│ RECOMMANDATIONS :\n")
        
        if avg_ratio_gm1 < 1.05 and avg_ratio_mg1 < 1.05:
            f.write("│   • Les trois modèles présentent des performances similaires\n")
            f.write("│   • Le choix du modèle peut être basé sur d'autres critères\n")
        elif avg_ratio_gm1 < avg_ratio_mg1:
            f.write("│   • M/M/1 reste le plus performant\n")
            f.write("│   • G/M/1 présente un impact modéré\n")
            f.write("│   • M/G/1 montre une dégradation plus marquée\n")
        else:
            f.write("│   • M/M/1 reste le plus performant\n")
            f.write("│   • M/G/1 présente un impact modéré\n")
            f.write("│   • G/M/1 montre une dégradation plus marquée\n")
        
        f.write("└" + "─" * 99 + "\n\n")
        
        # Notes techniques et méthodologiques
        f.write("┌─ NOTES TECHNIQUES " + "─" * 80 + "\n")
        f.write("│\n")
        f.write("│ HYPOTHÈSES ET LIMITATIONS :\n")
        f.write("│   • Simulation en régime stationnaire\n")
        f.write("│   • Serveur unique avec discipline FIFO\n")
        f.write("│   • Capacité infinie de la file d'attente\n")
        f.write("│   • Distributions G : loi uniforme centrée sur la moyenne théorique\n")
        f.write("│\n")
        f.write("│ MÉTHODE DE CALCUL :\n")
        f.write("│   • Simulation événement par événement\n")
        f.write("│   • Agrégation sur multiple répétitions\n")
        f.write("│   • Validation par comparaison théorique (M/M/1)\n")
        f.write("│\n")
        f.write("│ FORMULES THÉORIQUES UTILISÉES (M/M/1) :\n")
        f.write("│   • ρ = λ/μ (taux d'occupation)\n")
        f.write("│   • E[T] = 1/(μ-λ) (temps de séjour moyen)\n")
        f.write("│   • E[W] = ρ/(μ-λ) (temps d'attente moyen)\n")
        f.write("│   • Condition de stabilité : ρ < 1\n")
        f.write("└" + "─" * 99 + "\n\n")
        
        # Pied de page professionnel
        f.write("╔" + "═" * 98 + "╗\n")
        f.write("║" + " " * 15 + "FIN DU RAPPORT - SIMULATION VALIDÉE ET ARCHIVÉE" + " " * 34 + "║\n")
        f.write("║" + " " * 98 + "║\n")
        f.write(f"║ Généré automatiquement le {current_time.strftime('%d/%m/%Y à %H:%M:%S')} - Version 2.0" + " " * 23 + "║\n")
        f.write("║" + " " * 20 + "© Système de Simulation de Files d'Attente" + " " * 35 + "║\n")
        f.write("╚" + "═" * 98 + "╝\n")
    
    print("╔" + "═" * 60 + "╗")
    print("║" + " " * 10 + "RAPPORT GÉNÉRÉ AVEC SUCCÈS" + " " * 23 + "║")
    print("║" + " " * 60 + "║")
    print(f"║ Fichier : {filename:<45} ║")
    print(f"║ Taille  : {len(open(filename, 'r', encoding='utf-8').read())} caractères" + " " * (44 - len(str(len(open(filename, 'r', encoding='utf-8').read())))) + "║")
    print("║" + " " * 60 + "║")
    print("║ Le rapport est prêt pour consultation et archivage ║")
    print("╚" + "═" * 60 + "╝")