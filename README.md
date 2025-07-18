# Qu'est-ce que c'est?
C'est une appli qui télécharge la chanson en cours de lecture sur spotify sous Windows **sans premium**! Facile à mettre en place, et fiable. Elle récupère les infos du morceau en cours de lecture, puis télécharge la musique sur YouTube (pour des raisons de droits d'auteur), les paroles, et la couverture. Vous obtenez un fichier MP3 prêt à la lecture.


# Est-ce légal? fiable?
Oui, mais prenez quand même un compte secondaire, on sait jamais...  
Oui, mais ne me croyez pas sur parole; vous pouvez par exemple aller voir les différents scripts et les inspecter vous même, ou mieux, demander à l'IA ce qu'ils font. 

# Comment faire?

J'ai fait une [vidéo de tutoriel](https://google.com) sur YouTube que vous pouvez aller voir, qui détaille tout. Un guide texte va également suivre.

# Guide
1. Allez sur [le portail des développeurs Spotify](https://developer.spotify.com/dashboard). Vous devez bien sûr être connecté sur votre compte.
2. Acceptez les termes. (si nécessaire)
3. Appuyez sur le bouton "Créer une appli" / "Create app" (selon votre langue)
4. Renseignez les champs du nom de l'appli et de la description. `deltaplane` ira très bien.
5. Pour le champ "Redirect URIs", mettez:
```
http://127.0.0.1:8888/callback
```
6. Acceptez les termes et appuyez sur le bouton pour sauvegarder.
7. Vous devriez normalement être sur une page avec un "Client ID". Copiez ce code et gardez le quelque part.
8. Appuyez sur "View client secret", juste en bas du "Client ID". Copiez également ce code.
9. Téléchargez maintenant les deux scripts. [Installation](https://raw.githubusercontent.com/xpeuvr327/download-currently-playing-spotify/refs/heads/main/installation.bat) et [Appli](https://raw.githubusercontent.com/xpeuvr327/download-currently-playing-spotify/refs/heads/main/telecharger-la-chanson.py). Ces deux liens devraient lancer le téléchargement automatiquement, mais si ce n'est pas le cas, appuyez sur `CTRL + S` sur votre clavier et sauvegardez ces deux fichiers. Si vous recevez une alerte, c'est un faux positif, vous pouvez continuer en toute sécurité.
10. Double-cliquez sur le script d'installation (installation.bat) et suivez les instructions à l'écran. Il s'agit simplement d'appuyer sur ENTER ou Y sur votre clavier lorsqu'il y a une question.
11. Pendant ce temps, ouvrez le script python dans un éditeur de texte, par exemple Bloc-Notes. Modifiez la première ligne comme en remplaçant `votre_id_client_spotify` par votre Client ID spotify obtenu précédemment. Faites de même avec "votre_secret_client_spotify". Exemple, si votre ClientID était h4lqtwzk8imdpwi4ya8myd1n66hkkhmz et votre secret client 332xqp4ma6ml1Yt9dCJn5oRPZQBrBbPJ, vous devriez modifier les deux lignes comme suit:
```
SPOTIPY_CLIENT_ID = 'votre_id_client_spotify'
SPOTIPY_CLIENT_SECRET = 'votre_secret_client_spotify'
```
deviendrait:
```
SPOTIPY_CLIENT_ID = 'h4lqtwzk8imdpwi4ya8myd1n66hkkhmz'
SPOTIPY_CLIENT_SECRET = '332xqp4ma6ml1Yt9dCJn5oRPZQBrBbPJ'
```
12. Sauvegardez le fichier et quittez.
13. Si nécessaire, attendez que le script d'installation se finit. (Vous devriez vérifier qu'il n'y ait pas d'invites qui vous proposent d'appuyer sur entrée pour continuer, en cas de doute, répondez simplement Y ou enter)
14. Lancez spotify. Double-cliquez sur le fichier "telecharger-la-chanson.py" que vous venez de modifier pour l'ouvrir. Une fenêtre du terminal devrait s'ouvrir. Si vous voyez une fenêtre du bloc-note à la place, faites clic-droit et ouvrez avec "Python 3.13" ou "Python IDLE"
