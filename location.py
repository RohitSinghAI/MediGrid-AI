import urllib.parse


def get_location(location_data):

    if not location_data:
        return "Not Available"

    latitude = location_data.get("latitude")
    longitude = location_data.get("longitude")

    if latitude is None or longitude is None:
        return "Not Available"

    query = urllib.parse.quote("nearby pharmacies")

    return (
        f"https://www.google.com/maps/search/{query}"
        f"/@{latitude},{longitude},15z"
    )