from dotenv import load_dotenv
from zenodo_client import Zenodo

load_dotenv()

client = Zenodo()
path = client.download(record_id=13989054, name="hflav-tau-br-uc.json")
file_path = client.get_record(record_id=12696548)
print("Downloaded file to:", path)
