import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
from datetime import datetime

def load_and_process_data(uploaded_file) -> pd.DataFrame:
    """
    Charge et traite les données depuis le fichier CSV uploadé.
    """
    df = pd.read_csv(uploaded_file, sep=';')
    
    # Trouver la colonne "Période" ou similaire
    period_column = find_period_column(df)
    if period_column is None:
        raise ValueError("Aucune colonne 'Période' ou similaire trouvée dans les données.")
    
    return group_data_by_period(df, period_column)

def find_period_column(df: pd.DataFrame) -> str:
    """
    Recherche la colonne correspondant à la période dans le DataFrame.
    """
    for column in df.columns:
        if 'Période' in column:  # Recherche de 'Période' dans le nom de la colonne
            return column
    return None  # Retourne None si aucune colonne n'est trouvée

def group_data_by_period(df: pd.DataFrame, period_column: str) -> pd.DataFrame:
    """
    Groupe les données par période et calcule les parts.
    """
    metrics = [
        'Volume global contrôles',
        'Volume validés',
        'Volume mal formés',
        'Volume malfaçons',
        'Volume mensongers'
    ]
    
    df_grouped = df.groupby(period_column, as_index=False)[metrics].sum()
    
    for metric in metrics[1:]:
        part_name = f"Part {metric.split('Volume ')[1]}"
        df_grouped[part_name] = (df_grouped[metric] / df_grouped[metrics[0]] * 100).fillna(0)
    
    df_grouped[period_column] = df_grouped[period_column].astype(str)
    return df_grouped

def generate_summary(df: pd.DataFrame, period_column: str) -> str:
    """
    Génère un résumé textuel des données.
    """
    total_global = df['Volume global contrôles'].sum()
    total_valides = df['Volume validés'].sum()
    total_part_valides = (total_valides / total_global) * 100 if total_global > 0 else 0
    
    summary = []
    for _, row in df.iterrows():
        semaine = f"S{str(row[period_column])[-2:]}"
        vol_total = int(row['Volume global contrôles'])
        vol_valides = int(row['Volume validés'])
        part_valides = row['Part validés']
        summary.append(f"Part validé pour la {semaine} {part_valides:.2f}% (soit {vol_valides}/{vol_total} interventions) --> {vol_total - vol_valides} non validé")
    
    summary.append(f"\nPart validé total {total_part_valides:.2f}% (soit {total_valides}/{total_global} interventions) --> {total_global - total_valides} non validé")
    return '\n'.join(summary)

def create_visualization(df: pd.DataFrame, colors: Dict[str, str], 
                       show_volumes: bool, show_parts: bool,
                       figure_width: int, figure_height: int, period_column: str) -> plt.Figure:
    """
    Crée la visualisation selon les paramètres choisis.
    """
    fig, ax = plt.subplots(figsize=(figure_width, figure_height))
    
    if show_volumes:
        bottom = np.zeros(len(df))
        volume_metrics = ['Volume mensongers', 'Volume malfaçons', 'Volume mal formés', 'Volume validés']
        for metric in volume_metrics:
            ax.bar(df[period_column], df[metric], bottom=bottom, label=metric, color=colors[metric])
            bottom += df[metric]
    
    if show_parts:
        for metric in ['Part validés', 'Part mal formés', 'Part malfaçons', 'Part mensongers']:
            ax.plot(df[period_column], df[metric], 'o-', color=colors[metric], label=metric)
    
    plt.grid(True)
    plt.title('Évolution des volumes par période')
    plt.xlabel('Période')
    plt.ylabel('Valeurs')
    plt.legend(loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig

def main():
    st.set_page_config(page_title="Analyse PTO-CAB", layout="wide")
    
    st.title("Analyse des contrôles PTO-CAB")
    
    # Sidebar pour les paramètres
    st.sidebar.header("Paramètres")
    
    # Upload du fichier
    uploaded_file = st.sidebar.file_uploader(
        "Charger un fichier CSV",
        type=['csv'],
        help="Sélectionnez le fichier de données PTO-CAB"
    )
    
    if uploaded_file is not None:
        try:
            # Chargement et traitement des données
            df_grouped = load_and_process_data(uploaded_file)
            
            # Trouver la colonne "Période" ou similaire
            period_column = find_period_column(df_grouped)
            if period_column is None:
                st.error("Aucune colonne 'Période' ou similaire trouvée dans les données.")
                return
            
            # Sélection des périodes
            all_periods = sorted(df_grouped[period_column].unique())  # Tri des périodes
            selected_periods = st.sidebar.multiselect(
                "Sélectionner les périodes à afficher",
                options=all_periods,
                default=[]  # Aucune période sélectionnée par défaut
            )
            
            if selected_periods:  # Affiche le graphique uniquement si des périodes sont sélectionnées
                df_filtered = df_grouped[df_grouped[period_column].isin(selected_periods)]
                
                # Paramètres de visualisation
                col1, col2 = st.sidebar.columns(2)
                show_volumes = col1.checkbox("Afficher les volumes", value=True)
                show_parts = col2.checkbox("Afficher les parts", value=True)
                
                figure_width = st.sidebar.slider("Largeur du graphique", 8, 20, 15)
                figure_height = st.sidebar.slider("Hauteur du graphique", 4, 12, 8)
                
                # Paramètres de couleurs personnalisables
                colors = {
                    'Volume mensongers': st.sidebar.color_picker('Couleur Volume mensongers', '#D32F2F'),
                    'Volume malfaçons': st.sidebar.color_picker('Couleur Volume malfaçons', '#4285F4'),
                    'Volume mal formés': st.sidebar.color_picker('Couleur Volume mal formés', '#FBBC34'),
                    'Volume validés': st.sidebar.color_picker('Couleur Volume validés', '#8BD3A3'),
                    'Part validés': st.sidebar.color_picker('Couleur Part validés', '#388E3C'),
                    'Part mal formés': st.sidebar.color_picker('Couleur Part mal formés', '#1976D2'),
                    'Part malfaçons': st.sidebar.color_picker('Couleur Part malfaçons', '#FBC02D'),
                    'Part mensongers': st.sidebar.color_picker('Couleur Part mensongers', '#123465')
                }
                
                # Création du graphique
                fig = create_visualization(df_filtered, colors, show_volumes, show_parts, 
                                        figure_width, figure_height, period_column)
                st.pyplot(fig)
                
                # Affichage du résumé
                st.header("Résumé des données")
                st.text(generate_summary(df_filtered, period_column))
                
                # Export des données
                st.sidebar.header("Exporter les données")
                if st.sidebar.button("Télécharger les données analysées"):
                    csv = df_filtered.to_csv(index=False)
                    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.sidebar.download_button(
                        "Cliquez pour télécharger",
                        csv,
                        f"analyse_pto_cab_{current_time}.csv",
                        "text/csv",
                        key='download-csv'
                    )
            else:
                st.info("Veuillez sélectionner au moins une période pour afficher le graphique.")
                
        except Exception as e:
            st.error(f"Une erreur s'est produite : {str(e)}")

if __name__ == "__main__":
    main()


# Pour runner lancer commande : streamlit run streamlit_visualisation_rapport_PTO.py