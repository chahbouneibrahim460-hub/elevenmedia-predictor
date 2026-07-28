# 🚀 Quick Start - ElevenMedia Predictor

Démarrez en **5 minutes** !

## 1️⃣ Cloner le projet

```bash
git clone https://github.com/elevenmedia/elevenmedia-predictor.git
cd elevenmedia-predictor
```

## 2️⃣ Installer les dépendances

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3️⃣ Préparer les données

1. Télécharge le fichier Excel: `ElevenMedia_Portefeuille_Transparent.xlsx`
2. Place-le dans le dossier racine du projet

```bash
cp ~/Downloads/ElevenMedia_Portefeuille_Transparent.xlsx .
```

## 4️⃣ Lancer l'application

```bash
streamlit run app.py
```

L'app s'ouvre sur: **http://localhost:8501**

## 5️⃣ Utiliser l'application

### Onglet 1: Dashboard 📊
- Vue des 48 clients réels
- Graphiques interactifs
- Statistiques du portefeuille

### Onglet 2: Prédicteur de Coût 💰
1. Sélectionner le type de site
2. Choisir la complexité (1-5)
3. Entrer le nombre de pages
4. Ajouter les services
5. Cliquer "Prédire le coût"

**→ Résultat:** Budget estimé + projets similaires

### Onglet 3: Prédicteur de Durée ⏱️
1. Sélectionner le type de site
2. Choisir la complexité
3. Entrer le nombre de pages
4. Choisir la taille de l'équipe
5. Cliquer "Prédire la durée"

**→ Résultat:** Durée en jours/semaines + alertes

### Onglet 4: Historique 📈
- Voir toutes les prédictions effectuées
- Filtrer par type
- Exporter les données

## 📝 Exemples de prédictions

### Exemple 1: Site E-commerce simple
- Type: E-commerce
- Complexité: 2/5
- Pages: 50
- Services: SEO, Digital Marketing
- **→ Budget prédit: ~25,000 MAD | Durée: 20 jours**

### Exemple 2: Application mobile complexe
- Type: App mobile
- Complexité: 5/5
- Pages: 100
- Services: API, E-learning, Maintenance
- **→ Budget prédit: ~60,000 MAD | Durée: 60 jours**

## 🔍 Dépannage

### Erreur: "Fichier Excel non trouvé"
→ Vérifier que `ElevenMedia_Portefeuille_Transparent.xlsx` est dans le dossier racine

### Erreur: "ModuleNotFoundError"
→ Relancer: `pip install -r requirements.txt`

### L'app est lente
→ Première exécution: le modèle ML s'entraîne (30 secondes)

### Données de prédiction pas sauvegardées
→ Le dossier `data/` doit être accessible en écriture

## 📊 Architecture rapide

```
Utilisateur
    ↓
[Streamlit UI] (app.py)
    ↓
[ML Models] (models.py)
    ↓
[Données Excel] + [Historique JSON]
```

## 🚀 Tips

- Les prédictions se **sauvent automatiquement**
- Consulte l'**onglet "À Propos"** pour plus de détails
- Le modèle s'**améliore avec plus de données**
- Exporte l'historique pour l'analyse

## 📚 Fichiers importants

| Fichier | Rôle |
|---------|------|
| `app.py` | Application principale |
| `models.py` | Modèles ML |
| `requirements.txt` | Dépendances |
| `README.md` | Documentation complète |
| `ElevenMedia_Portefeuille_Transparent.xlsx` | Données |

## ✅ Checklist

- [ ] Python 3.9+ installé
- [ ] Environnement virtuel créé
- [ ] Dépendances installées
- [ ] Fichier Excel placé
- [ ] App lancée avec `streamlit run app.py`
- [ ] Accessible sur http://localhost:8501

## 🎉 C'est prêt!

Enjoy the predictor! 🚀

---

**Questions?** Consulte le [README.md](README.md) complet.
