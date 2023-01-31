from django.db import models


class IconChoice(models.TextChoices):
    BRIEFCASE = "BRIEFCASE", "Briefcase"
    CITY_DRIVE = "CITY_DRIVE", "City drive"
    GIVE_LOVE = "GIVE_LOVE", "Give love"
    GRADUATE_CAP = "GRADUATE_CAP", "Graduate cap"
    GROUP = "GROUP", "Group"
    HANDSHAKE = "HANDSHAKE", "Handshake"
    LIGHTBULB = "LIGHTBULB", "Light bulb"
