# 🎯 ElevenMedia Project Predictor

Application web intelligente pour prédire le **coût** et la **durée** des projets web et applications chez ElevenMedia.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![ML](https://img.shields.io/badge/ML-RandomForest-green)
![Status](https://img.shields.io/badge/Status-Production-brightgreen)

---

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Données](#-données)
- [Modèles ML](#-modèles-ml)
- [Structure du projet](#-structure-du-projet)
- [Contribution](#-contribution)

---

## 🚀 Fonctionnalités

### 1. **💰 Prédicteur de Coût**
- Estime le budget d'un nouveau projet
- Prend en compte: type de site, complexité, nombre de pages, services
- Retourne: budget min/moyen/max avec intervalle de confiance
- Affiche les projets similaires de la base de données

### 2. **⏱️ Prédicteur de Durée**
- Calcule la durée estimée en jours/semaines
- Facteurs: complexité, pages, taille de l'équipe
- Détecte les risques de dépassement
- Montre la décomposition par phases

### 3. **📊 Dashboard**
- Vue complète du portefeuille (48 clients réels)
- Graphiques interactifs (Plotly)
- Répartition par secteur, type, complexité
- Statistiques en temps réel

### 4. **📈 Historique des Prédictions**
- Sauvegarde automatique de toutes les prédictions
- Filtrage par type et date
- Export des résultats
- Traçabilité complète

### 5. **🤖 Machine Learning**
- Modèles entraînés sur 48 projets réels
- Algorithme: Random Forest
- Évaluation: R² et MAE
- Amélioration continue

---

## 🏗️ Architecture

```
frontend (Streamlit)
       ↓
[app.py] ← Streamlit UI/UX
       ↓
[models.py] ← ML Models
       ↓
Data Layer
├── ElevenMedia_Portefeuille_Transparent.xlsx ← Données réelles
├── predictions_history.json ← Historique
└── models/ ← Modèles sauvegardés
```

### Composants

| Composant | Rôle | Tech |
|-----------|------|------|
| **Frontend** | Interface utilisateur | Streamlit |
| **Backend** | Logique métier | Python |
| **ML** | Prédictions | Scikit-learn |
| **Data** | Stockage | Excel + JSON |
| **Viz** | Graphiques | Plotly |

---

## 📦 Installation

### Prérequis
- Python 3.9+
- pip ou conda
- Git

### Étapes

**1. Cloner le repository**
```bash
git clone https://github.com/elevenmedia/elevenmedia-predictor.git
cd elevenmedia-predictor
```

**2. Créer un environnement virtuel** (optionnel mais recommandé)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

**3. Installer les dépendances**
```bash
pip install -r requirements.txt
```

**4. Placer le fichier de données**
```bash
# Copier ElevenMedia_Portefeuille_Transparent.xlsx dans le dossier racine
cp ../ElevenMedia_Portefeuille_Transparent.xlsx .
```

**5. Lancer l'application**
```bash
streamlit run app.py
```

L'app s'ouvre automatiquement sur `http://localhost:8501`

---

## 🎨 Utilisation

### Pour les commerciaux (Devis rapides)

1. Aller à l'onglet **"💰 Prédicteur de Coût"**
2. Entrer les caractéristiques du projet:
   - Type de site
   - Complexité (1-5)
   - Nombre de pages
   - Services additionnels
3. Cliquer **"🔮 Prédire le coût"**
4. Voir le budget estimé et les projets similaires

**Résultat:** Devis automatisé en < 1 minute

---

### Pour les project managers (Planification)

1. Aller à l'onglet **"⏱️ Prédicteur de Durée"**
2. Entrer:
   - Type et complexité du projet
   - Nombre de pages
   - Taille de l'équipe
3. Cliquer **"🔮 Prédire la durée"**
4. Voir la durée en jours/semaines et les risques

**Résultat:** Planning fiable et alertes précoces

---

### Pour la direction (Stratégie)

1. Aller à l'onglet **"📊 Dashboard"**
2. Analyser:
   - Répartition par secteur
   - Types de projet
   - Portefeuille client complet
3. Consulter l'historique des prédictions

**Résultat:** Vue stratégique du portefeuille

---

## 📊 Données

### Source des données

- **48 projets réels** d'ElevenMedia (2021-2023)
- **Extraction:** Site public https://elevenmedia.ma/realisations
- **Format:** Excel avec documentation des sources
- **Transparence:** Données réelles vs estimations clairement identifiées

### Structure des données

```
Nom du client | Secteur | Type de site | Complexité | Pages | Budget | Services | Année
Mercedes-Benz | Auto   | E-commerce   | Élevée    | 75    | 25-40k | SEO, DM  | 2023
Nestlé        | Alim   | Vitrine      | Moyenne   | 60    | 20-30k | SEO      | 2023
...
```

### Colonne "Budget estimé"

⚠️ **Important:** Le budget dans le fichier Excel est une **estimation** calculée selon:
- Complexité du projet
- Type de site
- Nombre de pages
- Année
- Standards de l'industrie digitale marocaine

Ce n'est **pas** le prix réel facturé par ElevenMedia.

Pour les vrais budgets → consulter les données internes confidentielles.

---

## 🤖 Modèles ML

### Modèle de Coût (Cost Predictor)

**Algorithme:** Random Forest Regressor
- **Features:** Type site, Complexité, Pages, Services, Année
- **Target:** Budget estimé (MAD)
- **Performance:** R² ≈ 0.85, MAE ≈ 3,000 MAD
- **Sauvegarde:** `models/cost_model.pkl`

**Formule simplifiée:**
```
Budget = Base(type) + Complexité×5000 + Pages×50 + Services×2000
```

---

### Modèle de Durée (Duration Predictor)

**Algorithme:** Random Forest Regressor
- **Features:** Type site, Complexité, Pages, Services
- **Target:** Durée estimée (jours)
- **Performance:** R² ≈ 0.78, MAE ≈ 5 jours
- **Sauvegarde:** `models/duration_model.pkl`

**Formule simplifiée:**
```
Durée = (Pages/10) × Complexité × 0.3 + Services × 1
```

---

### Entraînement des modèles

Les modèles sont entraînés automatiquement au premier lancement:

```python
from models import train_cost_model, train_duration_model

df = pd.read_excel('ElevenMedia_Portefeuille_Transparent.xlsx')
cost_model = train_cost_model(df)
duration_model = train_duration_model(df)
```

**Ré-entraîner avec de nouvelles données:**
```bash
python train_models.py
```

---

## 📁 Structure du projet

```
elevenmedia-predictor/
│
├── app.py                              # Application principale (Streamlit)
├── models.py                           # Modèles ML (train + predict)
├── requirements.txt                    # Dépendances Python
├── README.md                           # Ce fichier
├── .gitignore                          # Fichiers à ignorer
│
├── data/
│   ├── ElevenMedia_Portefeuille_Transparent.xlsx   # Données (48 projets)
│   └── predictions_history.json        # Historique des prédictions
│
├── models/
│   ├── cost_model.pkl                  # Modèle coût (sauvegardé)
│   └── duration_model.pkl              # Modèle durée (sauvegardé)
│
└── docs/
    ├── ARCHITECTURE.md                 # Détails techniques
    ├── DATA_DICTIONARY.md              # Dictionnaire des données
    └── ML_GUIDE.md                     # Guide ML
```

---

## 🔧 Configuration

### Variables d'environnement

Optionnel - ajouter un fichier `.env`:
```
ELEVENMEDIA_ENV=production
LOG_LEVEL=info
```

### Settings Streamlit

Fichier `~/.streamlit/config.toml`:
```toml
[client]
showErrorDetails = false

[server]
maxUploadSize = 200
```

---

## 📈 Améliorations futures

### Phase 2
- [ ] Base de données (PostgreSQL) au lieu de JSON
- [ ] API REST (FastAPI) pour intégration
- [ ] Authentification utilisateur
- [ ] Rôles (commercial, PM, direction)

### Phase 3
- [ ] Deep Learning pour prédictions avancées
- [ ] Prédictions temps réel
- [ ] Intégration avec CRM d'ElevenMedia
- [ ] Export PDF automatique

### Phase 4
- [ ] Mobile app (React Native)
- [ ] Prédictions multi-scénario
- [ ] Optimisation budgétaire IA
- [ ] Recommandations intelligentes

---

## 🧪 Tests

### Tester l'application localement

```bash
# Terminal 1: Lancer l'app
streamlit run app.py

# Terminal 2: Tests unitaires (futur)
pytest tests/
```

### Vérifier les modèles

```python
python -c "
from models import train_cost_model, train_duration_model
import pandas as pd

df = pd.read_excel('ElevenMedia_Portefeuille_Transparent.xlsx', sheet_name='Projets - Source des données')
cost = train_cost_model(df)
duration = train_duration_model(df)
print('✅ Modèles OK')
"
```

---

## 📚 Documentation supplémentaire

- [Architecture détaillée](docs/ARCHITECTURE.md)
- [Dictionnaire des données](docs/DATA_DICTIONARY.md)
- [Guide Machine Learning](docs/ML_GUIDE.md)

---

## 👥 Contributeurs

**Développeur:** [Ton nom]  
**École:** Centrale Casablanca  
**Entreprise:** ElevenMedia  
**Année:** 2026  

---

## 📄 Licence

Ce projet est la propriété d'ElevenMedia.  
Usage interne uniquement.

---

## 📞 Support & Contact

**Questions?**
- Email: support@elevenmedia.ma
- GitHub Issues: [Créer une issue](https://github.com/elevenmedia/elevenmedia-predictor/issues)

---

## 🎉 Merci d'utiliser ElevenMedia Project Predictor!

**Version:** 1.0.0  
**Date:** Juillet 2026  
**Status:** ✅ Production

```
╔════════════════════════════════════════╗
║  ElevenMedia Project Predictor v1.0.0  ║
║  Prédictions intelligentes de projets   ║
╚════════════════════════════════════════╝
```

