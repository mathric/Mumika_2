from pathlib import Path
import json

def get_default_credential_path():
    # Get default credential path
    current_dir = Path(__file__).parent.absolute()
    default_credential_path = current_dir / 'env.json'
    return default_credential_path

def load_credential(path=None):
    credential_path = path
    if credential_path is None:
        credential_path = get_default_credential_path()
    with open(credential_path) as f:
        credential = json.load(f)
    return credential