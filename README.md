# hflav-python-library

This repository contains a small Python helper library to fetch HFLAV data
published on Zenodo. The package `hflav_zenodo` provides a tiny `ZenodoClient`
to search for HFLAV-related records and download files from Zenodo records.

Quick usage example

```python
from hflav_zenodo import ZenodoClient

client = ZenodoClient(community="hflav")
latest = client.get_latest_hflav()
print(latest["id"], latest.get("metadata", {}).get("title"))

# download the first attached file
path = client.download_file(latest)
print("Downloaded to:", path)
```

See `requirements.txt` for dependencies.