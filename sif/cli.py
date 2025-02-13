import argparse
from .sif import SongInfoFinder

# sif/cli.py (updated output handling)
def main():
    parser = argparse.ArgumentParser(description='SIF: Song Information Finder')
    # ... existing arguments ...
    
    args = parser.parse_args()
    sif = SongInfoFinder()

    song1 = sif.get_song_info(args.title, args.artist)
    print(f"\nSong: {song1['title']} by {song1['artist']}")
    
    if song1['bpm'] > 0:
        print(f"BPM: {song1['bpm']:.1f}")
    else:
        print("BPM: Not available")
    
    if song1['key'] != 'N/A':
        print(f"Key: {song1['key']} {song1['scale']}")
    else:
        print("Key: Not available")

    
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
