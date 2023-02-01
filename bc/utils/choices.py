from django.db import models


class IconChoice(models.TextChoices):
    BRIEFCASE = "briefcase", "Briefcase"
    CITY_DRIVE = "city-drive", "City drive"
    GIVE_LOVE = "give-love", "Give love"
    GRADUATE_HAT = "graduate-hat", "Graduate hat"
    GROUP = "group", "Group"
    HANDSHAKE = "handshake", "Handshake"
    LIGHTBULB = "light-bulb", "Light bulb"
