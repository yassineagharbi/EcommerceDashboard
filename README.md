# Tableau de Bord Business E-commerce 🚀

![Dashboard Power BI](Dashboard/rapport_powerbi.png)

## Présentation du projet

Ce projet a pour objectif de créer un dashboard interactif et automatisé pour une activité e-commerce, permettant de piloter l’ensemble des KPIs majeurs : Chiffre d’Affaires, nombre de clients, panier moyen, répartition géographique des ventes, top produits et évolution mensuelle.

Il vise à remplacer le reporting classique sous Excel par des visualisations dynamiques dans Power BI, à partir d’un modèle Data Warehouse construit sous SQL Server et alimenté par un pipeline ETL Python.

---

## Architecture Technique
![Dashboard Power BI - KPI E-commerce](Dashboard/architecture_technique.png)

- **Données sources** : Fichier "Online Retail" UCI 
- **ETL** : Python + pandas + SQLAlchemy pour extraction/transform/load
- **Base** : Modèle en étoile dans SQL Server (staging, dimensions, faits)
- **BI** : Power BI Desktop (visualisations professionnelles, DAX)
- **Reporting** : Dashboard interactif & partage en ligne

---

## Contenu du dépôt

- `data/data_retail_online.xlsx` : Données brutes e-commerce
- `src/etl_pipeline.py` : Script d’extraction/chargement vers SQL Server
- `src/ingestion.py` : Script de modélisation DW et alimentations dimensions/faits
- `sql/requete_table.sql` : Script SQL pour création tables et index
- `Dashboard/rapport.pbix` : Exemple de rapport Power BI prêt à l’emploi
- `README.md` : Présentation, explications et architecture

---

## Extrait du dashboard



- Synthèse des ventes et top KPIs
- Evolution du CA mensuel
- Carte géographique des ventes
- Histogramme top 10 produits vendus
- Filtres dynamiques par période, pays, produits

---

## Comment l'utiliser

1. Cloner le repo :  
   `git clone https://github.com/tonpseudo/EcommerceDashboard.git`
2. Installer Python et librairies : pandas, SQLAlchemy, pyodbc
3. Exécuter les scripts pour charger et modéliser les données
4. Ouvrir le fichier `.pbix` dans Power BI Desktop pour personnaliser visuels et analyses

---

## Pourquoi ce projet ?

Ce dashboard facilite la prise de décision business, l’analyse des performances et la visualisation instantanée des tendances qui comptent vraiment pour une activité e-commerce.

---

## Licence & Auteurs

Projet proposé dans le cadre d’un portfolio Data/BI & Open Source.  
Développé par Yassine AGHARBI – 2024 
Dataset original : UCI Machine Learning Repository

---
