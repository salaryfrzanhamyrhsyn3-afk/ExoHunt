
import csv
import io
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

QUERY = """
SELECT pl_name, hostname, disc_year, discoverymethod,
       pl_orbper, pl_rade, pl_bmasse, sy_dist
FROM pscomppars
ORDER BY pl_name
"""

def fetch_exoplanets():
    params = urllib.parse.urlencode({
        "query": QUERY,
        "format": "csv"
    })

    url = f"{API_URL}?{params}"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ExoHunt/0.1"}
    )

    print("Connecting to NASA Exoplanet Archive...")

    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read().decode("utf-8-sig")

    reader = csv.DictReader(io.StringIO(data))
    planets = list(reader)

    if not planets or not reader.fieldnames:
        raise ValueError("No planet data received from NASA.")

    output_file = Path("data/confirmed_exoplanets.csv")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(planets)

    print(f"Planets downloaded: {len(planets)}")
    print(f"Saved to: {output_file}")
    print("Data source: NASA Exoplanet Archive")
    print("Retrieved at:", datetime.now(timezone.utc).isoformat())


if __name__ == "__main__":
    try:
        fetch_exoplanets()
    except Exception as error:
        print("Download failed:", error)
