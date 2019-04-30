from eztv_extract import eztv_extract
from tmdb_extract_watchlist import extract_watchlist_series


shows = extract_watchlist_series()

for show in shows:
    # eztv_extract(show)
    print(show)
