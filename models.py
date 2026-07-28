# -*- coding: utf-8 -*-
"""
Modèles de machine learning pour prédictions de coût et durée
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

def prepare_features(df):
    """Prépare les features pour l'entraînement du modèle."""
    
    df_copy = df.copy()
    
    # Encoder les variables catégoriques
    le_type = LabelEncoder()
    le_complexite = LabelEncoder()
    
    df_copy['type_site_encoded'] = le_type.fit_transform(df_copy['Type de site'])
    
    # Extraire le niveau de complexité
    complexity_map = {
        'Faible-Moyenne': 1,
        'Moyenne': 2,
        'Moyenne-Élevée': 3,
        'Élevée': 4,
        'Très élevée': 5
    }
    df_copy['complexite_encoded'] = df_copy['Complexité'].map(complexity_map)
    
    # Services count
    df_copy['services_count'] = df_copy['Services fournis'].str.split(',').str.len()
    
    # Extraire pages estimées
    df_copy['pages'] = df_copy['Pages estimées'].astype(int)
    
    # Extraire année
    df_copy['annee'] = df_copy['Année'].astype(int)
    
    return df_copy, le_type, complexity_map

def train_cost_model(df):
    """Entraîne le modèle de prédiction de coût."""
    
    df_prepared, le_type, complexity_map = prepare_features(df)
    
    # Créer les features
    X = df_prepared[[
        'type_site_encoded',
        'complexite_encoded',
        'pages',
        'services_count',
        'annee'
    ]].astype(float)
    
    # Target: extraire le budget min et calculer la moyenne
    y_values = []
    for budget_str in df_prepared['Budget estimé']:
        # Extraire le premier nombre (budget min)
        import re
        match = re.search(r'(\d+)', str(budget_str).replace(',', ''))
        if match:
            y_values.append(int(match.group(1)) * 1000)  # Convertir en MAD
        else:
            y_values.append(25000)  # Valeur par défaut
    
    y = np.array(y_values)
    
    # Entraîner le modèle
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X, y)
    
    # Évaluation
    y_pred = model.predict(X)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    print(f"Model Cost - MAE: {mae:.0f}, R²: {r2:.2f}")
    
    # Ajouter les encoders au modèle
    model.le_type = le_type
    model.complexity_map = complexity_map
    
    return model

def train_duration_model(df):
    """Entraîne le modèle de prédiction de durée."""
    
    df_prepared, le_type, complexity_map = prepare_features(df)
    
    # Créer les features
    X = df_prepared[[
        'type_site_encoded',
        'complexite_encoded',
        'pages',
        'services_count'
    ]].astype(float)
    
    # Target: durée estimée en jours
    # Base: 1 jour par 10 pages + multiplicateur complexité
    y_values = []
    for idx, row in df_prepared.iterrows():
        pages = row['pages']
        complexity = row['complexite_encoded']
        services = row['services_count']
        
        # Calcul heuristique
        duration = max(pages / 10, 5) * (0.8 + complexity * 0.3) + (services * 1)
        y_values.append(duration)
    
    y = np.array(y_values)
    
    # Entraîner le modèle
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X, y)
    
    # Évaluation
    y_pred = model.predict(X)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    print(f"Model Duration - MAE: {mae:.0f}, R²: {r2:.2f}")
    
    # Ajouter les encoders
    model.le_type = le_type
    model.complexity_map = complexity_map
    
    return model

def predict_cost(model, type_site, complexite, pages, services_count, annee=2026):
    """Prédit le coût d'un projet."""
    
    # Encoder les inputs
    type_encoded = model.le_type.transform([type_site])[0]
    complexity_encoded = model.complexity_map.get(complexite, 3)
    
    # Créer feature vector
    X = np.array([[
        type_encoded,
        complexity_encoded,
        pages,
        services_count,
        annee
    ]], dtype=float)
    
    # Prédiction
    prediction = model.predict(X)[0]
    
    # Intervalle de confiance (±15%)
    min_pred = prediction * 0.85
    max_pred = prediction * 1.15
    
    return prediction, min_pred, max_pred

def predict_duration(model, type_site, complexite, pages, services_count):
    """Prédit la durée d'un projet."""
    
    # Encoder les inputs
    type_encoded = model.le_type.transform([type_site])[0]
    complexity_encoded = model.complexity_map.get(complexite, 3)
    
    # Créer feature vector
    X = np.array([[
        type_encoded,
        complexity_encoded,
        pages,
        services_count
    ]], dtype=float)
    
    # Prédiction
    prediction = model.predict(X)[0]
    
    # Intervalle de confiance (±20%)
    min_pred = prediction * 0.8
    max_pred = prediction * 1.2
    
    return prediction, min_pred, max_pred
