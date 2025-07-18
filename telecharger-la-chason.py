#obtenez ceci sur https://developer.spotify.com/dashboard   
SPOTIPY_CLIENT_ID = 'votre_id_client_spotify'
SPOTIPY_CLIENT_SECRET = 'votre_secret_client_spotify'

# Modèle de sortie pour yt-dlp. Voir la documentation de yt-dlp pour plus d'options : https://github.com/yt-dlp/yt-dlp#output-template
output_template = f"{title} - {artist}.%(ext)s"
#vous n'avez pas besoin de toucher au script, mais si vous êtes curieux, tout est commenté pour que vous sachiez exactement ce que chaque chose fait.

# Importer les bibliothèques nécessaires
#librarie pour se connecter à spotify; seulement avoir les infos du morceau en cours, je n'ai pas accès à ta playlist privée p.ex
import spotipy
from spotipy.oauth2 import SpotifyOAuth
#pour avoir l'image de couverture
import urllib.request
#pour télécharger les sons
import subprocess
#pour; supprimer les fichiers temporaires, et les noms de fichiers
import os
#pour avoir accès au fichiers temporaires
import tempfile
#les deux bibliothèques suivantes sont pour avoir les lyrics
import requests
from bs4 import BeautifulSoup

def get_lyrics_robust(artist, title):
    """
    Récupération robuste des paroles depuis AZLyrics avec plusieurs méthodes de repli
    """
    # Formater l'artiste et le titre pour l'URL
    artist_clean = artist.lower().replace(" ", "")
    title_clean = title.lower().replace(" ", "").replace('(', '').replace(')', '')  # supprimer les espaces et les parenthèses
    url = f"https://www.azlyrics.com/lyrics/{artist_clean}/{title_clean}.html"

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'} # usurpe le site en utilisant un UA standard pour ne pas se faire ban
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Méthode 1 : Utilisation du sélecteur CSS spécifique
        lyrics_div = soup.select_one(
            'body > div.container.main-page > div.row > div.col-xs-12.col-lg-8.text-center > div:nth-child(8)')
        if lyrics_div:
            lyrics_text = lyrics_div.get_text(separator='\n', strip=True)
            lyrics_text = '\n'.join(line for line in lyrics_text.split('\n') if line.strip())
            if len(lyrics_text) > 100:  # Assurez-vous que nous avons obtenu les vraies paroles
                return lyrics_text

        # Méthode 2 : Trouver la div principale du contenu et rechercher les paroles
        main_div = soup.find('div', class_='col-xs-12 col-lg-8 text-center')
        if main_div:
            # Obtenir toutes les divs dans la div principale
            all_divs = main_div.find_all('div')
            # Filtrer les divs qui contiennent probablement les paroles
            lyrics_candidates = []
            for div in all_divs:
                text = div.get_text(strip=True)
                # Les divs de paroles sont généralement longues, contiennent des sauts de ligne, et n'ont pas de classes
                if (len(text) > 200 and
                        text.count('\n') > 5 and
                        not div.get('class') and
                        'Submit Corrections' not in text and
                        'Writer(s):' not in text):
                    lyrics_candidates.append(div)
            if lyrics_candidates:
                # Habituellement, le premier candidat est les paroles
                lyrics_div = lyrics_candidates[0]
                lyrics_text = lyrics_div.get_text(separator='\n', strip=True)
                lyrics_text = '\n'.join(line for line in lyrics_text.split('\n') if line.strip())
                return lyrics_text

        # Méthode 3 : Rechercher la div qui vient après le texte "Submit Corrections"
        submit_corrections = soup.find(text="Submit Corrections")
        if submit_corrections:
            parent = submit_corrections.parent
            while parent and parent.name != 'div':
                parent = parent.parent
            if parent:
                prev_div = parent.find_previous_sibling('div')
                if prev_div:
                    lyrics_text = prev_div.get_text(separator='\n', strip=True)
                    lyrics_text = '\n'.join(line for line in lyrics_text.split('\n') if line.strip())
                    if len(lyrics_text) > 100:
                        return lyrics_text

        return None
    except Exception as e:
        print(f"Erreur lors de la récupération des paroles : {e}")
        return None

# Configurer l'authentification Spotify; le scope user read currently playing spécifie explicitement que ce script n'a accès qu'au titre en cours de lecture
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri='http://127.0.0.1:8888/callback',
    scope='user-read-currently-playing'
))

# Obtenir le morceau actuellement joué
current_track = sp.current_user_playing_track()
if current_track is not None and current_track['is_playing']:
    track = current_track['item']
    title = track['name']
    artist = track['artists'][0]['name']
    album_name = track['album']['name']
    album_cover_url = track['album']['images'][0]['url']
    all_artists = "; ".join([artist['name'] for artist in track['artists']])
    print(f"Morceau en cours de lecture : {title} par {artist}")
    print(f"Album : {album_name}")
    print(f"Art de l'album : {album_cover_url}")
else:
    print("Aucun morceau n'est actuellement en lecture.")
    exit()

# Créer un répertoire temporaire pour les fichiers
with tempfile.TemporaryDirectory() as temp_dir:
    # Télécharger l'art de l'album
    cover_path = os.path.join(temp_dir, "cover.jpg")
    try:
        urllib.request.urlretrieve(album_cover_url, cover_path)
        print(f"Art de l'album téléchargé vers {cover_path}")
    except Exception as e:
        print(f"Échec du téléchargement de l'art de l'album : {e}")
        exit()

    # Utiliser yt-dlp pour rechercher sur YouTube et obtenir l'ID de la vidéo
    search_query = f"{artist} {title}"
    yt_dlp_search_cmd = [
        "yt-dlp",
        f"ytsearch1:{search_query}",
        "--get-id"
    ]

    try:
        result = subprocess.run(yt_dlp_search_cmd, capture_output=True, check=True, text=False,
                                encoding='utf-8')  # Capturer en tant qu'octets
        video_id = result.stdout.strip()
        if not video_id or len(video_id) != 11:
            print("Aucun ID de vidéo valide trouvé.")
            exit()
        yt_url = f"https://youtu.be/{video_id}"
    except subprocess.CalledProcessError as e:
        print("Erreur lors de la recherche YouTube :", e.stderr.decode('utf-8', errors='replace'))
        exit()

    # Télécharger l'audio avec l'art de couverture intégré
    # D'abord, télécharger l'audio
    yt_dlp_download_cmd = [
        "yt-dlp",
        yt_url,
        "-x", "--audio-format", "mp3",
        "-f", "bestaudio",
        "--output", os.path.join(temp_dir, "%(title)s.%(ext)s"),
        "--embed-metadata",
        "--sponsorblock-remove", "intro,outro,preview,music_offtopic,filler"
    ]

    try:
        print("Téléchargement de l'audio...")
        subprocess.run(yt_dlp_download_cmd, check=True)
        # Trouver le fichier audio téléchargé
        audio_files = [f for f in os.listdir(temp_dir) if f.endswith('.mp3')]
        if not audio_files:
            print("Aucun fichier audio trouvé après le téléchargement.")
            exit()
        downloaded_file = os.path.join(temp_dir, audio_files[0])
        final_output = f"{artist} - {title}.mp3"

        # Récupérer les paroles en utilisant la méthode robuste
        lyrics = ""
        try:
            print("Récupération des paroles...")
            lyrics_data = get_lyrics_robust(artist, title)
            if lyrics_data:
                lyrics = lyrics_data
                print("Paroles récupérées avec succès")
                lyrics_available_semantic_check = 1
            else:
                print("Impossible de récupérer les paroles")
                lyrics_available_semantic_check = 0
        except Exception as e:
            print(f"Erreur lors de la récupération des paroles : {e}")
            lyrics = ""
            lyrics_available_semantic_check = 0

        # Utiliser ffmpeg pour intégrer l'art de couverture, les paroles et les métadonnées Spotify appropriées
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", downloaded_file,
            "-i", cover_path,
            "-map", "0:0",
            "-map", "1:0",
            "-c", "copy",
            "-id3v2_version", "3",
            # Intégrer les métadonnées appropriées de Spotify
            "-metadata", f"title={title}",
            "-metadata", f"artist={all_artists}",
            "-metadata", f"album={album_name}",
            "-metadata", f"album_artist={artist}",
            # Métadonnées de l'art de couverture
            "-metadata:s:v", "title=Couverture de l'album",
            "-metadata:s:v", "comment=Couverture (avant)",
            "-disposition:v", "attached_pic",
            "-y"
        ]

        # Ajouter les métadonnées des paroles si disponibles
        if lyrics and lyrics.strip():
            # Nettoyer les paroles - supprimer les espaces excessifs et assurer un encodage approprié
            clean_lyrics = lyrics.strip().replace('\r\n', '\n').replace('\r', '\n')
            # Ajouter plusieurs balises de métadonnées de paroles pour une compatibilité plus large
            ffmpeg_cmd.extend([
                "-metadata", f"USLT={clean_lyrics}",
                "-metadata", f"lyrics={clean_lyrics}",
                "-metadata", f"LYRICS={clean_lyrics}",
                "-metadata", f"unsychronised_lyric={clean_lyrics}"  # Orthographe alternative utilisée par certains lecteurs
            ])

        # Ajouter le fichier de sortie
        ffmpeg_cmd.append(final_output)
        print("Intégration de l'art de couverture, des métadonnées et des paroles...")
        try:
            subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True, encoding='utf-8')
            if lyrics_available_semantic_check == 0:
                print(f"Chanson avec art de couverture et métadonnées enregistrée sous : {final_output}")
            elif lyrics_available_semantic_check == 1:
                print(f"Chanson avec art de couverture, paroles et métadonnées enregistrée sous : {final_output}")
        except subprocess.CalledProcessError as e:
            print(f"Erreur FFmpeg : {e.stderr}")
            # Solution de repli : essayer sans paroles s'il y a un problème d'encodage
            if lyrics:
                print("Nouvel essai sans paroles en raison de problèmes d'encodage...")
                fallback_cmd = [
                    "ffmpeg",
                    "-i", downloaded_file,
                    "-i", cover_path,
                    "-map", "0:0",
                    "-map", "1:0",
                    "-c", "copy",
                    "-id3v2_version", "3",
                    # Garder les métadonnées Spotify même en solution de repli
                    "-metadata", f"title={title}",
                    "-metadata", f"artist={all_artists}",
                    "-metadata", f"album={album_name}",
                    "-metadata", f"album_artist={artist}",
                    # Métadonnées de l'art de couverture
                    "-metadata:s:v", "title=Couverture de l'album",
                    "-metadata:s:v", "comment=Couverture (avant)",
                    "-disposition:v", "attached_pic",
                    "-y",
                    final_output
                ]
                subprocess.run(fallback_cmd, check=True)
                print(f"Chanson avec art de couverture et métadonnées (SANS paroles) enregistrée sous : {final_output}")
            else:
                raise
    except subprocess.CalledProcessError as e:
        print("Échec du processus :", e.stderr)
        exit()
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        exit()
