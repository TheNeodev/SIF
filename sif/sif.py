import requests

class SongInfoFinder:
    def _search_musicbrainz(self, title, artist):
        url = "http://musicbrainz.org/ws/2/recording/"
        params = {
            'query': f'artist:"{artist}" AND recording:"{title}"',
            'fmt': 'json'
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if 'recordings' in data and data['recordings']:
                recording = data['recordings'][0]
                mbid = recording['id']
                title = recording['title']
                artist_name = recording['artist-credit'][0]['name'] if recording.get('artist-credit') else artist
                return (mbid, title, artist_name)
        except requests.exceptions.RequestException:
            pass
        return (None, None, None)

    def _get_acoustic_data(self, mbid):
        url = f"https://acousticbrainz.org/api/v1/{mbid}/low-level"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def get_song_info(self, title, artist):
        mbid, found_title, found_artist = self._search_musicbrainz(title, artist)
        if not mbid:
            return None

        acoustic_data = self._get_acoustic_data(mbid)
        if not acoustic_data:
            return None

        try:
            bpm = acoustic_data['rhythm']['bpm']
            key = acoustic_data['tonal']['key_key']
            scale = acoustic_data['tonal']['key_scale']
        except KeyError:
            return None

        return {
            'title': found_title,
            'artist': found_artist,
            'bpm': bpm,
            'key': key,
            'scale': scale.lower()
        }

    def is_bpm_compatible(self, bpm1, bpm2, tolerance=0.02):
        if bpm1 <= 0 or bpm2 <= 0:
            return False
        ratio = bpm1 / bpm2
        return any(abs(ratio - target) <= tolerance for target in [0.5, 1, 2])

    def is_key_compatible(self, key1, scale1, key2, scale2):
        relative_keys = {
            'C major': 'A minor',
            'C# major': 'A# minor',
            'D major': 'B minor',
            'D# major': 'C minor',
            'E major': 'C# minor',
            'F major': 'D minor',
            'F# major': 'D# minor',
            'G major': 'E minor',
            'G# major': 'F minor',
            'A major': 'F# minor',
            'A# major': 'G minor',
            'B major': 'G# minor',
            'A minor': 'C major',
            'A# minor': 'C# major',
            'B minor': 'D major',
            'C minor': 'D# major',
            'C# minor': 'E major',
            'D minor': 'F major',
            'D# minor': 'F# major',
            'E minor': 'G major',
            'F minor': 'G# major',
            'F# minor': 'A major',
            'G minor': 'A# major',
            'G# minor': 'B major',
        }
        key_scale1 = f"{key1} {scale1}"
        key_scale2 = f"{key2} {scale2}"
        return (key_scale1 == key_scale2) or (relative_keys.get(key_scale1) == key_scale2) or (relative_keys.get(key_scale2) == key_scale1)
