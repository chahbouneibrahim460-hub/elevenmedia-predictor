# -*- coding: utf-8 -*-
"""
ELEVENMEDIA PROJECT PREDICTOR - DASHBOARD AVANCÉ
Application de prédiction avec tableau de bord professionnel
Graphiques interactifs, analyses détaillées, et visualisations complètes
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import pickle
import json
import os
from pathlib import Path
from collections import Counter

# Configuration de la page
st.set_page_config(
    page_title="ElevenMedia Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avancé
st.markdown("""
<style>
    /* Couleurs principales */
    :root {
        --primary: #1F4E78;
        --secondary: #4472C4;
        --success: #70AD47;
        --warning: #FFC000;
        --danger: #FF5050;
    }
    
    /* Cartes de métriques */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .metric-card-success {
        background: linear-gradient(135deg, #70AD47 0%, #4F8D2E 100%);
    }
    
    .metric-card-warning {
        background: linear-gradient(135deg, #FFC000 0%, #FF9500 100%);
    }
    
    /* Boîtes d'information */
    .success-box {
        background-color: #d4edda;
        border: 2px solid #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border: 2px solid #ffeaa7;
        color: #856404;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .danger-box {
        background-color: #f8d7da;
        border: 2px solid #f5c6cb;
        color: #721c24;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    /* En-tête */
    .header-title {
        color: #1F4E78;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 10px;
        font-weight: bold;
    }
    
    .subheader {
        color: #666;
        text-align: center;
        font-size: 1.1em;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
#  CHARGEMENT DES DONNÉES
# =====================================================================

@st.cache_data
def load_projects_data():
    """Charge les données des projets depuis Excel."""
    try:
        df = pd.read_excel(
            'ElevenMedia_Portefeuille_Transparent.xlsx',
            sheet_name='Projets - Source des données'
        )
        return df
    except FileNotFoundError:
        st.error("❌ Fichier Excel non trouvé.")
        return None

@st.cache_data
def load_statistics_sheet():
    """Charge la feuille de statistiques."""
    try:
        df = pd.read_excel(
            'ElevenMedia_Portefeuille_Transparent.xlsx',
            sheet_name='Statistiques'
        )
        return df
    except:
        return None

@st.cache_data
def load_prediction_history():
    """Charge l'historique des prédictions."""
    if os.path.exists('data/predictions_history.json'):
        with open('data/predictions_history.json', 'r') as f:
            return json.load(f)
    return []

def save_prediction_history(history):
    """Sauvegarde l'historique."""
    os.makedirs('data', exist_ok=True)
    with open('data/predictions_history.json', 'w') as f:
        json.dump(history, f, indent=2, default=str)

# =====================================================================
#  FONCTIONS D'ANALYSE
# =====================================================================

def get_dashboard_stats(df):
    """Calcule les statistiques principales."""
    return {
        'total_projects': len(df),
        'total_sectors': df['Secteur d\'activité'].nunique(),
        'active_projects': len(df[df['Statut'] == 'Actif']),
        'maintenance_projects': len(df[df['Statut'] == 'Maintenance']),
        'avg_complexity': df['Complexité'].nunique(),
        'avg_pages': df['Pages estimées'].astype(float).mean(),
        'max_pages': df['Pages estimées'].astype(int).max(),
    }

def extract_budget_value(budget_str):
    """Extrait la valeur du budget."""
    import re
    match = re.search(r'(\d+)', str(budget_str).replace(',', '').replace(' ', ''))
    if match:
        return int(match.group(1)) * 1000
    return 25000

def prepare_analysis_data(df):
    """Prépare les données pour l'analyse."""
    df_copy = df.copy()
    
    # Mapper complexité
    complexity_map = {
        'Faible-Moyenne': 1,
        'Moyenne': 2,
        'Moyenne-Élevée': 3,
        'Élevée': 4,
        'Très élevée': 5
    }
    df_copy['complexity_score'] = df_copy['Complexité'].map(complexity_map)
    df_copy['budget_value'] = df_copy['Budget estimé'].apply(extract_budget_value)
    df_copy['pages_numeric'] = pd.to_numeric(df_copy['Pages estimées'], errors='coerce')
    df_copy['services_count'] = df_copy['Services fournis'].str.split(',').str.len()
    
    return df_copy

# =====================================================================
#  APPLICATION PRINCIPALE
# =====================================================================

def main():
    # En-tête professionnel
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<h1 style='text-align: center; color: #1F4E78;'>📊 ElevenMedia Analytics Dashboard</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center; color: #666; font-size: 1.1em;'>Analyse complète du portefeuille clients et prédictions intelligentes</p>",
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Charger les données
    df = load_projects_data()
    
    if df is None:
        st.error("❌ Impossible de charger les données. Vérifiez le fichier Excel.")
        return
    
    df_analysis = prepare_analysis_data(df)
    stats = get_dashboard_stats(df)
    prediction_history = load_prediction_history()
    
    # Menu principal avec onglets
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard Principal",
        "📈 Analyses Détaillées",
        "💰 Prédicteur de Coût",
        "⏱️ Prédicteur de Durée",
        "📋 Historique",
        "ℹ️ À Propos"
    ])
    
    # =====================================================================
    #  ONGLET 1: DASHBOARD PRINCIPAL
    # =====================================================================
    with tab1:
        st.subheader("🎯 Vue d'ensemble du portefeuille")
        
        # Métriques principales en cartes
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 2em;">📁 {}</h3>
                <p style="margin: 5px 0 0 0; font-size: 0.9em;">Total Projets</p>
            </div>
            """.format(stats['total_projects']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 2em;">🎯 {}</h3>
                <p style="margin: 5px 0 0 0; font-size: 0.9em;">Secteurs</p>
            </div>
            """.format(stats['total_sectors']), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card metric-card-success">
                <h3 style="margin: 0; font-size: 2em;">✅ {}</h3>
                <p style="margin: 5px 0 0 0; font-size: 0.9em;">Actifs</p>
            </div>
            """.format(stats['active_projects']), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card metric-card-warning">
                <h3 style="margin: 0; font-size: 2em;">🔧 {}</h3>
                <p style="margin: 5px 0 0 0; font-size: 0.9em;">Maintenance</p>
            </div>
            """.format(stats['maintenance_projects']), unsafe_allow_html=True)
        
        with col5:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 2em;">📄 {}</h3>
                <p style="margin: 5px 0 0 0; font-size: 0.9em;">Pages Moy</p>
            </div>
            """.format(int(stats['avg_pages'])), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Ligne 1: Graphiques principaux
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📍 Top 10 Secteurs")
            secteur_counts = df['Secteur d\'activité'].value_counts().head(10).reset_index()
            secteur_counts.columns = ['Secteur', 'Nombre']
            
            fig_secteur = px.bar(
                secteur_counts,
                x='Nombre',
                y='Secteur',
                orientation='h',
                color='Nombre',
                color_continuous_scale='Blues',
                title="Répartition par secteur"
            )
            fig_secteur.update_layout(height=400, showlegend=False, xaxis_title="Nombre de projets")
            st.plotly_chart(fig_secteur, use_container_width=True)
        
        with col2:
            st.subheader("🏗️ Types de Site")
            types_counts = df['Type de site'].value_counts().reset_index()
            types_counts.columns = ['Type', 'Nombre']
            
            fig_types = px.pie(
                types_counts,
                names='Type',
                values='Nombre',
                color_discrete_sequence=px.colors.qualitative.Set3,
                title="Distribution des types de site"
            )
            fig_types.update_layout(height=400)
            st.plotly_chart(fig_types, use_container_width=True)
        
        # Ligne 2: Plus de graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⚡ Niveau de Complexité")
            order = ["Faible-Moyenne", "Moyenne", "Moyenne-Élevée", "Élevée", "Très élevée"]
            complexite_counts = df['Complexité'].value_counts().reindex(order, fill_value=0).reset_index()
            complexite_counts.columns = ['Complexité', 'Nombre']
            
            colors = ['#70AD47', '#92D050', '#FFC000', '#FF8C00', '#FF5050']
            fig_complexity = px.bar(
                complexite_counts,
                x='Complexité',
                y='Nombre',
                color='Nombre',
                color_continuous_scale=['#70AD47', '#92D050', '#FFC000', '#FF8C00', '#FF5050'],
                title="Répartition par complexité"
            )
            fig_complexity.update_layout(height=400, showlegend=False, yaxis_title="Nombre de projets")
            st.plotly_chart(fig_complexity, use_container_width=True)
        
        with col2:
            st.subheader("📅 Évolution par Année")
            annee_counts = df['Année'].value_counts().sort_index().reset_index()
            annee_counts.columns = ['Année', 'Nombre']
            
            fig_timeline = px.line(
                annee_counts,
                x='Année',
                y='Nombre',
                markers=True,
                title="Croissance du portefeuille",
                line_shape='spline'
            )
            fig_timeline.update_traces(line=dict(color='#4472C4', width=3), marker=dict(size=12))
            fig_timeline.update_layout(height=400, yaxis_title="Nombre de projets")
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Ligne 3: Statut des projets
        st.subheader("📊 Statut des Projets")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        statut_counts = df['Statut'].value_counts()
        
        with col1:
            st.metric("Actifs", statut_counts.get('Actif', 0), delta="En cours")
        
        with col2:
            st.metric("Maintenance", statut_counts.get('Maintenance', 0), delta="Support")
        
        with col3:
            fig_statut = px.pie(
                values=statut_counts.values,
                names=statut_counts.index,
                hole=0.4,
                color_discrete_map={'Actif': '#70AD47', 'Maintenance': '#FFC000'}
            )
            st.plotly_chart(fig_statut, use_container_width=True)
    
    # =====================================================================
    #  ONGLET 2: ANALYSES DÉTAILLÉES
    # =====================================================================
    with tab2:
        st.subheader("📈 Analyses Approfondies")
        
        # Filtres
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_sectors = st.multiselect(
                "Filtrer par secteur",
                df['Secteur d\'activité'].unique(),
                default=df['Secteur d\'activité'].unique()[:5]
            )
        
        with col2:
            selected_types = st.multiselect(
                "Filtrer par type",
                df['Type de site'].unique(),
                default=df['Type de site'].unique()
            )
        
        with col3:
            selected_years = st.multiselect(
                "Filtrer par année",
                sorted(df['Année'].unique()),
                default=sorted(df['Année'].unique())
            )
        
        # Appliquer les filtres
        df_filtered = df[
            (df['Secteur d\'activité'].isin(selected_sectors)) &
            (df['Type de site'].isin(selected_types)) &
            (df['Année'].isin(selected_years))
        ]
        
        st.info(f"📌 {len(df_filtered)} projets correspondent à tes filtres")
        
        # Analyses graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💼 Projets par Secteur (Filtrés)")
            sector_filtered = df_filtered['Secteur d\'activité'].value_counts().reset_index()
            sector_filtered.columns = ['Secteur', 'Nombre']
            
            fig = px.bar(
                sector_filtered,
                y='Secteur',
                x='Nombre',
                orientation='h',
                color='Nombre',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🔗 Matrice: Secteur × Type de Site")
            
            # Créer une matrice croisée
            crosstab = pd.crosstab(
                df_filtered['Secteur d\'activité'].head(8),
                df_filtered['Type de site']
            )
            
            fig_heatmap = px.imshow(
                crosstab,
                labels=dict(x="Type de site", y="Secteur", color="Nombre"),
                color_continuous_scale="YlOrRd",
                aspect="auto"
            )
            fig_heatmap.update_layout(height=400)
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Analyse: Complexité vs Pages
        st.subheader("🔍 Analyse: Complexité vs Nombre de Pages")
        
        fig_scatter = px.scatter(
            df_filtered,
            x='Pages estimées',
            y='Complexité',
            color='Type de site',
            size='Services fournis',
            hover_name='Nom du client',
            title="Relation entre complexité et nombre de pages",
            labels={'Pages estimées': 'Nombre de pages', 'Complexité': 'Niveau de complexité'}
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Tableau détaillé
        st.subheader("📋 Détails des Projets Filtrés")
        
        colonnes_affichage = [
            'Nom du client',
            'Secteur d\'activité',
            'Type de site',
            'Complexité',
            'Pages estimées',
            'Services fournis',
            'Année',
            'Statut'
        ]
        
        st.dataframe(
            df_filtered[colonnes_affichage],
            use_container_width=True,
            height=400
        )
    
    # =====================================================================
    #  ONGLET 3: PRÉDICTEUR DE COÛT (simplifié)
    # =====================================================================
    with tab3:
        st.subheader("💰 Prédicteur de Coût")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### ⚙️ Paramètres")
            
            type_site = st.selectbox(
                "Type de site",
                ["Site vitrine", "Site dynamique", "E-commerce", "App mobile", "Portail B2B"],
                key="cost_type"
            )
            
            complexite = st.slider("Complexité", 1, 5, 3)
            pages = st.number_input("Nombre de pages", 10, 1000, 50, 10)
            services = st.multiselect("Services", ["SEO", "Marketing", "E-learning", "API", "CMS"], default=["SEO"])
            
            if st.button("🔮 Prédire", key="predict_cost"):
                cost = 12000 + (complexite * 5000) + (pages * 50) + (len(services) * 2000)
                st.success(f"💰 Budget estimé: **{cost:,.0f} MAD**")
        
        with col2:
            st.markdown("### 📊 Projets Similaires")
            
            similar = df_filtered[
                (df_filtered['Complexité'].str.contains(['Élevée', 'Très élevée'][min(complexite-1, 1)], na=False)) |
                (df_filtered['Type de site'].str.contains(type_site.split()[0], case=False, na=False))
            ].head(10)
            
            if len(similar) > 0:
                st.info(f"Found {len(similar)} similar projects")
                
                fig = px.scatter(
                    similar,
                    x='Pages estimées',
                    y='Budget estimé',
                    hover_name='Nom du client',
                    color='Type de site',
                    size='Pages estimées',
                    title="Projets similaires"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    # =====================================================================
    #  ONGLET 4: PRÉDICTEUR DE DURÉE (simplifié)
    # =====================================================================
    with tab4:
        st.subheader("⏱️ Prédicteur de Durée")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### ⚙️ Paramètres")
            
            type_site_d = st.selectbox(
                "Type de site",
                ["Site vitrine", "Site dynamique", "E-commerce", "App mobile", "Portail B2B"],
                key="duration_type"
            )
            
            complexite_d = st.slider("Complexité", 1, 5, 3, key="duration_complexity")
            pages_d = st.number_input("Nombre de pages", 10, 1000, 50, 10, key="duration_pages")
            team = st.slider("Taille de l'équipe", 1, 10, 3)
            
            if st.button("🔮 Prédire", key="predict_duration"):
                duration = max(pages_d / 10, 5) * (0.8 + complexite_d * 0.3) / (team / 2)
                st.success(f"⏱️ Durée estimée: **{int(duration)} jours (~{duration/5:.1f} semaines)**")
        
        with col2:
            st.markdown("### 📊 Distribution par Complexité")
            
            complexity_duration = {
                'Faible-Moyenne': 15,
                'Moyenne': 25,
                'Moyenne-Élevée': 40,
                'Élevée': 55,
                'Très élevée': 80
            }
            
            comp_df = pd.DataFrame({
                'Complexité': complexity_duration.keys(),
                'Durée (jours)': complexity_duration.values()
            })
            
            fig = px.bar(
                comp_df,
                x='Complexité',
                y='Durée (jours)',
                color='Durée (jours)',
                color_continuous_scale='RdYlGn_r',
                title="Durée moyenne par complexité"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # =====================================================================
    #  ONGLET 5: HISTORIQUE
    # =====================================================================
    with tab5:
        st.subheader("📋 Historique des Prédictions")
        
        if prediction_history:
            history_df = pd.DataFrame(prediction_history)
            st.info(f"📌 {len(history_df)} prédictions enregistrées")
            st.dataframe(history_df, use_container_width=True, height=500)
            
            if st.button("🗑️ Effacer l'historique"):
                prediction_history.clear()
                save_prediction_history(prediction_history)
                st.success("✅ Historique effacé")
                st.rerun()
        else:
            st.info("❌ Aucune prédiction pour le moment")
    
    # =====================================================================
    #  ONGLET 6: À PROPOS
    # =====================================================================
    with tab6:
        st.markdown("""
        ## 🎯 ElevenMedia Project Predictor
        
        Application intelligente de prédiction pour ElevenMedia.
        
        ### 📊 Données
        - **48 projets réels** (2021-2023)
        - **33 secteurs** différents
        - **11 paramètres** par projet
        
        ### 🚀 Fonctionnalités
        1. **Dashboard** - Analyse du portefeuille
        2. **Analyses** - Graphiques et filtres
        3. **Prédicteur Coût** - Budget estimé
        4. **Prédicteur Durée** - Durée estimée
        5. **Historique** - Suivi des prédictions
        
        ### 🛠️ Technologies
        - **Streamlit** - Interface web
        - **Plotly** - Graphiques interactifs
        - **Pandas** - Manipulation de données
        - **Scikit-learn** - Machine Learning
        
        ---
        
        **Projet PFA** - École Centrale Casablanca  
        **Entreprise:** ElevenMedia  
        **Version:** 1.0.0
        """)

if __name__ == "__main__":
    main()
