#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for ElevenMedia Project Predictor
Initialise le projet et les dépendances
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Vérifier que Python >= 3.9"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ requis")
        print(f"Version actuelle: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} OK")

def create_directories():
    """Créer les répertoires nécessaires"""
    dirs = ['data', 'models', 'docs', 'logs']
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
        print(f"📁 Dossier {d}/ créé")

def check_files():
    """Vérifier les fichiers essentiels"""
    required = ['app.py', 'models.py', 'requirements.txt']
    for f in required:
        if not Path(f).exists():
            print(f"❌ Fichier manquant: {f}")
            sys.exit(1)
        print(f"✅ {f} trouvé")

def install_dependencies():
    """Installer les dépendances"""
    print("\n📥 Installation des dépendances...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
    print("✅ Dépendances installées")

def check_excel_file():
    """Vérifier la présence du fichier Excel"""
    excel_file = 'ElevenMedia_Portefeuille_Transparent.xlsx'
    if not Path(excel_file).exists():
        print(f"\n⚠️  {excel_file} non trouvé")
        print("📥 Télécharge le fichier et place-le dans le répertoire racine")
        return False
    print(f"✅ {excel_file} trouvé")
    return True

def initialize_history():
    """Initialiser l'historique des prédictions"""
    import json
    history_file = 'data/predictions_history.json'
    if not Path(history_file).exists():
        with open(history_file, 'w') as f:
            json.dump([], f)
        print(f"✅ {history_file} initialisé")

def main():
    """Exécuter le setup complet"""
    print("=" * 50)
    print("🚀 Setup ElevenMedia Project Predictor")
    print("=" * 50)
    print()
    
    try:
        print("1️⃣  Vérification Python...")
        check_python_version()
        print()
        
        print("2️⃣  Création des dossiers...")
        create_directories()
        print()
        
        print("3️⃣  Vérification des fichiers...")
        check_files()
        print()
        
        print("4️⃣  Installation des dépendances...")
        install_dependencies()
        print()
        
        print("5️⃣  Vérification du fichier Excel...")
        excel_ok = check_excel_file()
        print()
        
        print("6️⃣  Initialisation de l'historique...")
        initialize_history()
        print()
        
        print("=" * 50)
        print("✅ Setup terminé!")
        print("=" * 50)
        print()
        
        if excel_ok:
            print("🚀 Prêt à démarrer! Exécute:")
            print("   streamlit run app.py")
        else:
            print("⚠️  Place le fichier Excel et relance le setup")
        print()
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
