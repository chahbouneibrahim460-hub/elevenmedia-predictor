#!/bin/bash

# ElevenMedia Project Predictor - Startup Script

echo "🚀 Démarrage de ElevenMedia Project Predictor..."
echo ""

# Vérifier Python
if ! command -v python &> /dev/null; then
    echo "❌ Python n'est pas installé. Veuillez installer Python 3.9+"
    exit 1
fi

echo "✅ Python trouvé: $(python --version)"
echo ""

# Créer environnement virtuel si nécessaire
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python -m venv venv
fi

# Activer l'environnement
echo "🔌 Activation de l'environnement..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -q -r requirements.txt

# Vérifier le fichier Excel
if [ ! -f "ElevenMedia_Portefeuille_Transparent.xlsx" ]; then
    echo "⚠️  Fichier Excel non trouvé!"
    echo "📥 Télécharge ElevenMedia_Portefeuille_Transparent.xlsx et place-le ici."
    exit 1
fi

echo ""
echo "✅ Tout est prêt!"
echo ""
echo "🌐 Lancement de l'application..."
echo "L'app s'ouvrira sur: http://localhost:8501"
echo ""
echo "💡 Appuie sur Ctrl+C pour arrêter"
echo ""

# Lancer Streamlit
streamlit run app.py
