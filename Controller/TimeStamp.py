from datetime import datetime

def get_timestamp():
    """Renvoie l'horodatage actuel au format 'dd-mm-yyyy-hh:mm:ss'."""
    return datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
