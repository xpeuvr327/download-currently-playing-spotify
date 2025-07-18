@echo off
echo Installe spotify premium sur votre pc! c'est safe! https://github.com/mrpond/BlockTheSpot https://spicetify.app/
echo Aux questions qui vont vous être posées, appuyez sur <Enter>, ou "Y". Appuyez sur enter pour continuer
pause
powershell -Command "& { iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1 | iex }"
powershell -Command "& {iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-marketplace/main/resources/install.ps1 | iex}"
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -UseBasicParsing 'https://raw.githubusercontent.com/mrpond/BlockTheSpot/master/install.ps1' | Invoke-Expression}"
echo Check si python est installé
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python n'est pas installé. https://www.python.org/downloads/
    exit /b 1
)

echo vérifie si pip, un utilitaire requis pour la suite, est bien installé
where pip >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Installing pip...
    python -m ensurepip --upgrade
)

echo Installation des bibliothèques requises
pip install spotipy requests beautifulsoup4

echo Installe le programme qui permet de télécharger des vidéos. 
winget install --id=yt-dlp.yt-dlp  -e

echo Installe ffmpeg, qui sert à convertir des fichiers et ajouter la cover, les sous-titres, etc.
winget install -e --id Gyan.FFMpeg --accept-package-agreements --accept-source-agreements

echo All dependencies have been installed. Rendez-vous sur https://github.com/xpeuvr327/download-currently-playing-spotify pour la suite.
pause
