from pathlib import Path

def get_default_log_path(file_name):
    current_dir = Path(__file__).parent.absolute()
    default_log_path = current_dir / file_name
    return default_log_path

    
