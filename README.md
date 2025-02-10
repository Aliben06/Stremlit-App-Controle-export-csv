Voici le fichier `README.md` sous forme de texte :

---

# Analyse et Visualisation des Contrôles PTO-CAB

Description
Ce projet consiste en une application web interactive développée avec Python et Streamlit pour l'analyse des données des contrôles PTO-CAB. L'application permet de visualiser les volumes d'interventions, calculer les taux de validation et générer des rapports détaillés avec des graphiques et des résumés.

 Fonctionnalités
- Importation de fichiers CSV avec traitement automatique des données.
- Visualisation interactive avec des graphiques empilés et des courbes représentant les volumes validés, mal formés, malfaçons, et mensongers.
- Résumé des performances avec calcul des parts et des pénalités.
- Export des résultats sous format CSV pour un suivi facile et la possibilité de télécharger les données analysées.

 Technologies utilisées
- Python
- Streamlit
- Pandas
- Matplotlib
- NumPy

 Installation

1. Clonez ce dépôt :

```
git clone https://github.com/ton-utilisateur/ton-repository.git
cd ton-repository
```

2. Créez un environnement virtuel (optionnel, mais recommandé) :

```
python3 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. Installez les dépendances nécessaires :

```
pip install -r requirements.txt
```

4. Lancez l'application Streamlit :

```
streamlit run streamlit_visualisation_rapport_PTO.py
```

 Usage
1. Ouvrez l'application Streamlit dans votre navigateur.
2. Chargez le fichier CSV "Données de test" avec les données des contrôles.
3. Sélectionnez les périodes à afficher et configurez les options de visualisation.
4. Exportez les données analysées en format CSV.

 Exemples de Visualisation
L'application vous permettra de visualiser des graphiques montrant l'évolution des volumes par période, ainsi que les parts de chaque catégorie (validés, mal formés, malfaçons, etc.).

 Auteurs
- Ali BENNEJMA (https://github.com/Aliben06)

 Licence
Ce projet est propriétaire et ne peut être utilisé, copié, modifié, ou distribué sans l'autorisation explicite de l'auteur.
Tous droits réservés.

