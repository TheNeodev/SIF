# SIF: Song Information Finder

Get song information (BPM, key) and check mashup compatibility between two songs.

## Installation

```bash
pip install sif-song-info-finder
```

## Usage

### Get Song Info
```bash
sif --title "Billie Jean" --artist "Michael Jackson"
```

### Compare Two Songs
```bash
sif --title "Song1" --artist "Artist1" --compare --compare-title "Song2" --compare-artist "Artist2"
```

## Features
- Fetch BPM and key from AcousticBrainz
- Check BPM compatibility (exact, double, or half)
- Check key compatibility (same or relative)
