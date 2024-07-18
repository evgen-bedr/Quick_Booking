# apps/rentals/choices/rental_choice.py
from django.db import models


class PropertyTypeChoices(models.TextChoices):
    APARTMENT = 'Apartment', 'Apartment'
    HOUSE = 'House', 'House'
    HOTEL = 'Hotel', 'Hotel'
    STUDIO = 'Studio', 'Studio'
    VILLA = 'Villa', 'Villa'
    CABIN = 'Cabin', 'Cabin'
    COTTAGE = 'Cottage', 'Cottage'


class TagChoices(models.TextChoices):
    NON_SMOKING_ROOMS = 'Non-Smoking Rooms', 'Non-Smoking Rooms'
    SPA_WELLNESS_CENTER = 'Spa and Wellness Center', 'Spa and Wellness Center'
    FITNESS_CENTER = 'Fitness Center', 'Fitness Center'
    ACCESSIBLE_FACILITIES = 'Accessible Facilities', 'Accessible Facilities'
    ROOM_SERVICE = 'Room Service', 'Room Service'
    FREE_WIFI = 'Free Wi-Fi', 'Free Wi-Fi'
    PARKING = 'Parking', 'Parking'
    AIR_CONDITIONING = 'Air Conditioning', 'Air Conditioning'
    COFFEE_TEA_MAKER = 'Coffee/Tea Maker', 'Coffee/Tea Maker'
    BAR = 'Bar', 'Bar'
    FAMILY_ROOMS = 'Family Rooms', 'Family Rooms'
    TERRACE = 'Terrace', 'Terrace'
    ELEVATOR = 'Elevator', 'Elevator'
    GARDEN = 'Garden', 'Garden'
    HEATING = 'Heating', 'Heating'
    SWIMMING_POOL = 'Swimming Pool', 'Swimming Pool'
    PET_FRIENDLY = 'Pet Friendly', 'Pet Friendly'
