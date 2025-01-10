
# Dashboard des Tendances d'Achat

Ce projet est un tableau de bord interactif conçu pour analyser et visualiser les tendances d'achat des clients en utilisant des indicateurs clés de performance (KPI). Le tableau de bord utilise Streamlit pour l'interface utilisateur et Plotly pour des graphiques interactifs, ainsi que FastAPI pour l'API backend.

## Fonctionnalités

### API Backend (FastAPI)

- **Total des revenus** : Affiche le revenu total généré par les achats.
- **Revenu par catégorie** : Calcule et affiche les revenus générés par chaque catégorie de produit.
- **Article le plus acheté** : Affiche l'article le plus acheté.
- **Revenu par saison** : Affiche les revenus générés par chaque saison.
- **Répartition des clients par tranche d'âge** : Affiche la répartition des clients en fonction de leur tranche d'âge.
- **Taux d'abonnés** : Affiche le pourcentage d'abonnés parmi les clients.
- **Taux d'utilisation des codes promo** : Affiche le pourcentage de clients utilisant des codes promo.
- **Taux de clients fréquents** : Affiche le pourcentage de clients effectuant des achats fréquents.

### Tableau de bord Frontend (Streamlit)

Le tableau de bord Streamlit se connecte à l'API FastAPI pour récupérer les données et affiche les KPI ainsi que des graphiques interactifs.

- **KPIs** : Affichage des métriques comme le revenu total, la valeur moyenne des commandes, le taux d'abonnés, etc.
- **Graphiques interactifs** : Utilisation de Plotly pour afficher des graphiques interactifs pour les revenus par catégorie, saison, location et plus.
- **Filtres** : Permet aux utilisateurs de filtrer les données par catégorie, saison et location.
- **Carte des revenus par état** : Affiche une carte interactive des revenus par état.

## Prérequis

- Python 3.x
- Les bibliothèques suivantes doivent être installées :
  - `streamlit`
  - `plotly`
  - `requests`
  - `pandas`
  - `fastapi`
  - `uvicorn`

### Installation

1. Clonez ce repository :
   ```bash
   git clone https://github.com/Diviini/fastapi_data_python
   cd fastapi_data_python
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Exécutez le backend (API) :
   ```bash
   uvicorn back:app --reload
   ```

4. Lancez le tableau de bord :
   ```bash
   streamlit run front.py
   ```

## Membres du groupe:

- Robin LE BROZEC
- Achraf CHARDOUDI
- Elyes Ouramdane
- Kaoutar Jabri
- Ines Dhouibi

## API Endpoints

Voici les principaux endpoints de l'API pour récupérer les données des KPIs :
- `/kpi/total_revenue` : Retourne le revenu total.
- `/kpi/revenue_by_category` : Retourne le revenu par catégorie.
- `/kpi/most_purchased_item` : Retourne l'article le plus acheté.
- `/kpi/average_review_rating` : Retourne la moyenne des avis.
- `/kpi/revenue_by_season` : Retourne le revenu par saison.
- `/kpi/subscription_percentage` : Retourne le pourcentage d'abonnés.
- `/kpi/promo_code_usage_rate` : Retourne le taux d'utilisation des codes promo.
- `/kpi/frequent_shopper_rate` : Retourne le taux de clients fréquents.
- `/kpi/best_selling_item_by_category` : Retourne le meilleur article vendu par catégorie.
- `/kpi/customer_age_rate` : Retourne la répartition des clients par tranche d'âge.
- `/kpi/subscriber_frequent_relation` : Retourne la proportion d'abonnés qui sont des acheteurs fréquents.

## Contribution

Les contributions sont les bienvenues ! Si vous avez des idées pour améliorer ce projet, veuillez soumettre une pull request.

## License

Ce projet est sous licence MIT.
