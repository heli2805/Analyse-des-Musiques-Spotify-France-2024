import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from datetime import datetime

# Vos identifiants Spotify
CLIENT_ID = '315c5c5eb8144cfd8aa4c035063d6e91'
CLIENT_SECRET = 'eb5c0d3330b645edba43e437524bed90'

# Configuration de l'authentification
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Fonction pour récupérer les chansons d'une année donnée avec une gestion correcte de l'offset
def get_tracks_by_year(year, market='FR'):
    query = f'year:{year}'
    tracks = []
    limit = 50
    offset = 0
    
    while offset < 1000:  # Ne pas dépasser un offset de 1000
        try:
            # Requête vers l'API avec un marché valide
            results = sp.search(q=query, type='track', limit=limit, offset=offset, market=market)
            if not results['tracks']['items']:
                break

            for item in results['tracks']['items']:
                track_info = {
                    'track_name': item['name'],
                    'track_id': item['id'],
                    'artist_name': item['artists'][0]['name'],
                    'artist_id': item['artists'][0]['id'],
                    'album_name': item['album']['name'],
                    'album_id': item['album']['id'],
                    'release_date': item['album']['release_date'],
                    'popularity': item['popularity'],
                    'duration_ms': item['duration_ms'],
                    'explicit': item['explicit'],
                    'external_url': item['external_urls']['spotify'],
                    'artist_image_url': item['artists'][0]['images'][0]['url'] if item['artists'][0].get('images') else None,
                    'album_cover_url': item['album']['images'][0]['url'] if item['album'].get('images') else None
                }
                tracks.append(track_info)
            offset += limit
        except spotipy.exceptions.SpotifyException as e:
            print(f"Une erreur s'est produite : {e}")
            break  # Sortir de la boucle en cas d'erreur

    return tracks

# Fonction pour filtrer les chansons de janvier à avril 2024
def filter_tracks_jan_to_april(tracks):
    filtered_tracks = []
    
    for track in tracks:
        release_date = track['release_date']
        try:
            release_date_obj = datetime.strptime(release_date, '%Y-%m-%d')
        except ValueError:
            continue
        
        if release_date_obj.year == 2024 and 1 <= release_date_obj.month <= 4:
            filtered_tracks.append(track)
    
    return filtered_tracks

# Récupération des chansons de 2024 avec gestion de l'offset
all_tracks_2024 = get_tracks_by_year(2024, market='FR')

# Filtrage pour les mois de janvier à avril 2024
tracks_jan_to_april = filter_tracks_jan_to_april(all_tracks_2024)

# Sauvegarder les résultats dans un fichier JSON
with open('tracks_2024_jan_to_april.json', 'w', encoding='utf-8') as f:
    json.dump(tracks_jan_to_april, f, ensure_ascii=False, indent=4)

print(f"Total des morceaux récupérés de janvier à avril 2024 : {len(tracks_jan_to_april)}")
