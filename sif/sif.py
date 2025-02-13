import requests
from difflib import SequenceMatcher

class SongInfoFinder:
    def __init__(self):
        self.headers = {
            'User-Agent': 'SIF/1.0 (https://github.com/yourusername/sif)'
        }

    def _best_match(self, query, items, threshold=0.6):
        matches = []
        for item in items:
            ratio = SequenceMatcher(None, query.lower(), item.lower()).ratio()
            if ratio >= threshold:
                matches.append((ratio, item))
        return sorted(matches, reverse=True)[0][1] if matches else None

    def _search_musicbrainz(self, title, artist):
        url = "https://musicbrainz.org/ws/2/recording/"
        params = {
            'query': f'recording:"{title}" AND artist:"{artist}"',
            'fmt': 'json',
            'limit': 10
        }
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            for recording in data.get('recordings', []):
                mbid = recording.get('id')
                if not mbid:
                    continue
                
                # Try to get acoustic data first
                if self._get_acoustic_data(mbid):
                    return (
                        mbid,
                        recording.get('title', title),
                        recording.get('artist-credit', [{}])[0].get('name', artist)
                    )
            
            # Fallback to first recording if no acoustic data found
            if data.get('recordings'):
                first_rec = data['recordings'][0]
                return (
                    first_rec.get('id'),
                    first_rec.get('title', title),
                    first_rec.get('artist-credit', [{}])[0].get('name', artist)
                )
                
        except requests.exceptions.RequestException:
            pass
        return (None, None, None)

    def _get_acoustic_data(self, mbid):
        try:
            response = requests.get(
                f"https://acousticbrainz.org/api/v1/{mbid}/low-level",
                headers=self.headers,
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if 'rhythm' in data and 'tonal' in data:
                    return data
            return None
        except (requests.exceptions.RequestException, ValueError):
            return None

    def _get_fallback_bpm(self, title, artist):
        try:
            response = requests.get(
                "https://api.getsongbpm.com/search/",
                params={'q': f'{title} {artist}'},
                headers={'X-API-KEY': 'public'}  # Public demo key
            )
            data = response.json()
            if data.get('search'):
                return data['search'][0].get('tempo')
        except requests.exceptions.RequestException:
            return None

    def get_song_info(self, title, artist):
        # Try MusicBrainz first
        mbid, found_title, found_artist = self._search_musicbrainz(title, artist)
        acoustic_data = self._get_acoustic_data(mbid) if mbid else None
        
        # Fallback to getsongbpm if no acoustic data
        bpm = None
        if acoustic_data:
            try:
                bpm = acoustic_data['rhythm']['bpm']
                key = acoustic_data['tonal']['key_key']
                scale = acoustic_data['tonal']['key_scale']
            except KeyError:
                pass
        else:
            bpm = self._get_fallback_bpm(found_title or title, found_artist or artist)

        # Final fallback values
        return {
            'title': found_title or title,
            'artist': found_artist or artist,
            'bpm': bpm or 0,
            'key': (acoustic_data or {}).get('tonal', {}).get('key_key', 'N/A'),
            'scale': (acoustic_data or {}).get('tonal', {}).get('key_scale', 'N/A').lower()
        }

    # ... keep existing compatibility methods ...

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
