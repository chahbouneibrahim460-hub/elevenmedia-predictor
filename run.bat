@echo off
REM ElevenMedia Project Predictor - Windows Startup Script

echo.
echo 🚀 Demarrage de ElevenMedia Project Predictor...
echo.

REM Verifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installe. Veuillez installer Python 3.9+
    pause
    exit /b 1
)

echo ✅ Python trouve
echo.

REM Creer environnement virtuel si necessaire
if not exist "venv" (
    echo 📦 Creation de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement
echo 🔌 Activation de l'environnement...
call venv\Scripts\activate.bat

REM Installer les dépendances
echo 📥 Installation des dépendances...
pip install -q -r requirements.txt

REM Verifier le fichier Excel
if not exist "ElevenMedia_Portefeuille_Transparent.xlsx" (
    echo ⚠️  Fichier Excel non trouve!
    echo 📥 Telecharge ElevenMedia_Portefeuille_Transparent.xlsx et place-le ici.
    pause
    exit /b 1
)

echo.
echo ✅ Tout est pret!
echo.
echo 🌐 Lancement de l'application...
echo L'app s'ouvrira sur: http://localhost:8501
echo.
echo 💡 Appuie sur Ctrl+C pour arreter
echo.

REM Lancer Streamlit
streamlit run app.py

pause
