### Analyse Exploratoire des Données de Ventes de Supermarché

## Introduction

Ce rapport présente une analyse exploratoire des données de ventes d’un supermarché. L'objectif principal est d'identifier les performances des succursales, des villes et des catégories de produits, ainsi que les tendances temporelles et comportementales des clients. Les résultats obtenus permettront de dégager des recommandations pour optimiser les ventes et améliorer l’expérience client.

## Présentation des données

 - Dimensions du dataset : 1 000 lignes et 17 colonnes.

 - Colonnes principales :

 - City : Ville où la transaction a eu lieu.

 - Branch : Succursale (A, B, C).

 - Sales : Montant total des ventes.

 - Product line : Catégorie de produit (ex. : Health and Beauty, Food and Beverages).

  - Payment : Mode de paiement utilisé (E-wallet, Cash, Credit card).

 - Date et Time : Date et heure de la transaction.

 - gross income : Revenu brut généré par la transaction.

## Méthodologie

# Nettoyage des données :

 - Suppression des doublons et gestion des valeurs manquantes.

 - Correction des types de colonnes (conversion des dates et des chiffres).

 - Identification et suppression des valeurs aberrantes basée sur la méthode des quartiles.

 - Analyse descriptive :

 - Calcul des statistiques de base (moyenne, écart-type, distribution).

 - Visualisation des variables pour comprendre les tendances et les relations.

# Visualisation :

Utilisation de graphiques pour représenter les performances des succursales, les tendances temporelles et le comportement des clients.

# Résultats et Insights

1. Performances globales

 - Revenus par ville :

La ville de Naypyitaw  génère 34.23% des revenus totaux, tandis que la ville de yango et celle de Mandalay  generer 32% des revenus.


2. Catégories de produits
  

La catégorie Electronic accessories   est en tête, représentant 17.62% des ventes totales.


Actions :

Promouvoir davantage  home and lifestyle et sport and travel  dans les villes moins performantes comme  Napyitaw

Identifier les sous-categories à potentiel dans Food and Beverages.

3. Tendances temporelles

Périodes actives :

Les ventes sont les plus élevées entre 19, représentant 11.3% des transactions quotidiennes.

Les jours de semaine enregistrent plus de ventes que le week-end.

Saisonnalité :

Les mois de mars et janvier montrent des pics de ventes, suggérant une forte activité en début d’année.

4. Comportement des clients

- Modes de paiement :

E-wallet est le mode de paiement préféré (35% des transactions), suivi de Cash (34%) et Credit card (31%).

 - Dépenses moyennes :

Les clients membres dépensent  de plus que les non-membres.

 - Genre :

Les femmes représentent 57% des clients et achètent plus dans tous les categories sauf Health and Beauty

5- Conclusion et Recommandations

Investir dans les produits populaires :

Augmenter le stock et les promotions pour Health and Beauty

Optimiser les périodes de forte activité :

Renforcer le personnel et les promotions entre 16h et 19h.

Promouvoir les programmes de fidélité :

Inciter les clients non-membres à rejoindre le programme de fidélité.

Encourager les paiements par E-wallet :

Proposer des réductions ou des offres spéciales pour les paiements via E-wallet.



Annexes

Graphiques et tableaux supplémentaires disponibles sur demande.

Code source utilisé pour l’analyse accessible via le Notebook Python.