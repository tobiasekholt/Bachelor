import requests

BASE_URL = "https://ws.geonorge.no/transformering/v1/"


def get_available_projections(kategori=None, system=None):
    """Fetches a list of available projections from the API."""
    params = {}
    if kategori:
        params["kategori"] = kategori
    if system:
        params["system"] = system
    response = requests.get(f"{BASE_URL}/transformering/v1/projeksjoner", params=params)
    return response.json()


def transform_coord(x, y, fra, til, z=None, t=None):
    """Transforms a single coordinate from one coordinate system to another."""
    params = {"x": x, "y": y, "fra": fra, "til": til}
    if z:
        params["z"] = z
    if t:
        params["t"] = t
    response = requests.get(f"{BASE_URL}/transformering/v1/transformer", params=params)
    return response.json()


def transform_coords(coords, fra, til):
    """Transforms a list of coordinates from one coordinate system to another."""
    data = {"fra": fra, "til": til, "punkter": coords}
    response = requests.post(f"{BASE_URL}/transformering/v1/transformer", json=data)
    return response.json()
