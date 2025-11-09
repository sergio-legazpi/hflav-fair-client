from dotenv import load_dotenv
from zenodo_client import Zenodo

from hflav_zenodo.app import HFLAVApp

from source.source_zenodo import ZenodoClient

load_dotenv()

average = HFLAVApp()
client = Zenodo()
path = average.get_json(
    client=client, record_id=13989054, name="hflav-tau-lifetime.json"
)
new_try = ZenodoClient()
new_try.get_files_by_name(query="tau lifetime")
new_try.get_file_by_id(id=13989054, filename="hflav-tau-mass.json")
print("Downloaded file to:", path)
inst = average.from_json(path)
print("Instantiated average from JSON:", inst)
inst2 = average.from_zenodo(
    client=client, record_id=13989054, name="hflav-tau-br-uc.json"
)
print("Instantiated average from Zenodo:", inst2)
json_str = average.to_json()
print("Serialized average to JSON string:", json_str)
