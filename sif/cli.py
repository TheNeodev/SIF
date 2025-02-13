import argparse
from .sif import SongInfoFinder

def main():
    parser = argparse.ArgumentParser(description='SIF: Song Information Finder')
    parser.add_argument('--title', required=True, help='Title of the song')
    parser.add_argument('--artist', required=True, help='Artist of the song')
    parser.add_argument('--compare', action='store_true', help='Compare with another song')
    parser.add_argument('--compare-title', help='Title of the song to compare with')
    parser.add_argument('--compare-artist', help='Artist of the song to compare with')

    args = parser.parse_args()
    sif = SongInfoFinder()

    song1 = sif.get_song_info(args.title, args.artist)
    if not song1:
        print(f"No data found for {args.title} by {args.artist}")
        return

    print(f"\nSong: {song1['title']} by {song1['artist']}")
    print(f"BPM: {song1['bpm']:.1f}")
    print(f"Key: {song1['key']} {song1['scale']}")

    if args.compare:
        if not args.compare_title or not args.compare_artist:
            parser.error("--compare requires --compare-title and --compare-artist")

        song2 = sif.get_song_info(args.compare_title, args.compare_artist)
        if not song2:
            print(f"\nNo data found for {args.compare_title} by {args.compare_artist}")
            return

        print(f"\nSong: {song2['title']} by {song2['artist']}")
        print(f"BPM: {song2['bpm']:.1f}")
        print(f"Key: {song2['key']} {song2['scale']}")

        compatible_bpm = sif.is_bpm_compatible(song1['bpm'], song2['bpm'])
        compatible_key = sif.is_key_compatible(song1['key'], song1['scale'], song2['key'], song2['scale'])

        print("\nCompatibility Check:")
        print(f"BPM: {'Compatible' if compatible_bpm else 'Not Compatible'}")
        print(f"Key: {'Compatible' if compatible_key else 'Not Compatible'}")
        if compatible_bpm and compatible_key:
            print("\n🎉 Perfect match for a mashup!")
        else:
            print("\n😞 Not a perfect match.")

if __name__ == '__main__':
    main()
