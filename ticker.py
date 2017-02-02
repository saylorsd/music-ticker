import time
import requests
from led_matrix_ticker import LEDMatrixTicker as Ticker

from settings import API_KEY, SECRET, APP_NAME, ACCT

EIGHTH_NOTES = chr(0x0E)

ticker = Ticker(width=4, brightness=0, rotated=True)

url = "http://ws.audioscrobbler.com/2.0/"

params = {
    'method': 'user.getrecenttracks',
    'user': ACCT,
    'api_key': API_KEY,
    'format': 'json'
}


def get_curr_track():
    r = requests.get(url, params=params)
    if r.status_code == 200:
        data = r.json()
        for track in data['recenttracks']['track']:
            if '@attr' in track and 'nowplaying' in track['@attr'] and track['@attr']['nowplaying'] =='true':
                artist = track['artist']['#text']
                title = track['name']
                return artist, title

try:
    artist, track = get_curr_track()
    message = EIGHTH_NOTES + " {} - {}    ".format(artist, track) + EIGHTH_NOTES
    ticker.scroll_message(message, speed=6, repeats=1)

    while(True):
        new_artist, new_track = get_curr_track()
        print(new_artist, new_track)
        if new_artist != artist or new_track != track:
            message = EIGHTH_NOTES + " {} - {}    ".format(new_artist, new_track) + EIGHTH_NOTES
            print(message)
            ticker.scroll_message(message, speed=6, repeats=1)
            artist = new_artist
            track = new_track
        else:
            print('sleepin\'')
            time.sleep(1)

finally:
    ticker.clear_all()
