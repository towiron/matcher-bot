from geopy.geocoders import Nominatim
from geopy.adapters import URLLibAdapter
import certifi
import ssl


def get_coordinates(city_name: str, timeout: int = 10) -> list | None:
    """Возвращает координаты переданного в city_name города"""
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    def adapter_factory(**kwargs):
        kwargs.pop('ssl_context', None)  # удаляем, если есть
        return URLLibAdapter(ssl_context=ssl_context, **kwargs)

    geolocator = Nominatim(
        user_agent="matcher_bot",
        timeout=timeout,
        adapter_factory=adapter_factory
    )

    location = geolocator.geocode(city_name)
    return (location.latitude, location.longitude) if location else None

def get_city_name(latitude: float, longitude: float, timeout: int = 10) -> str | None:
    """Возвращает название города по координатам"""
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    def adapter_factory(**kwargs):
        kwargs.pop('ssl_context', None)
        return URLLibAdapter(ssl_context=ssl_context, **kwargs)

    geolocator = Nominatim(
        user_agent="matcher_bot",
        timeout=timeout,
        adapter_factory=adapter_factory
    )

    location = geolocator.reverse((latitude, longitude), language="en")  # можно поменять язык на "ru"
    if not location:
        return None

    address = location.raw.get("address", {})
    return address.get("city") or address.get("town") or address.get("village") or address.get("state")
