"""
    event_cards is a list of cards. Each card is represented by a dict with description ``'de'`` and ``'en'`` in
    German and English and with ``evt``, the event change vector (same dimensions as oeko_env.V)
"""

event_card = [
    {"de": "Durch Umweltschutzgesetzgebung verstärkt Übergang auf Recycling-Methoden, die Abfallmengen reduzieren",
     "en": "Environmental protection legislation reinforces transition to recycling methods that reduce waste volumes",
     #       0   1   2   3   4   5   6    7   8   9
     #       S  Pr  Ed   Q  PG  En  Pop  Pol  R  AP
     "evt": [0,  0,  0, 1,   0, -2,  0,   0,  0,  0]
     },
    {"de": "Vereinfachte Anwendung von Verhütungsmitteln erleichtert die Geburtenkontrolle",
     "en": "Simplified use of contraceptives facilitates birth control",
     #       0   1   2   3   4   5   6    7   8   9
     #       S  Pr  Ed   Q   PG  En  Pop  Pol  R  AP
     "evt": [0,  0,  0,  0,  -3,  0,   0,   0, 0, 0]    # actually "nach eigener Wahl um bis zu 3 Schritte zurück"
     },
    {"de": "Die Wirtschaft erleidet durch Wechselkursänderungen Einbrüche auf den Exportmärkten",
     "en": "The economy suffers slumps in export markets due to exchange rate fluctuations.",
     #       0   1   2   3   4   5   6    7   8   9
     #       S  Pr  Ed   Q   PG  En  Pop  Pol  R  AP
     "evt": [0, -2,  0, -1,   0,  0,   0,   0, 0, 0]
     },
    {"de": "Eine Verschärfung der internationalen Lage hat mehr Rüstungsausgaben zur Folge",
     "en": "An escalation in the international situation leads to increased military spending.",
     #       0   1   2   3   4   5   6    7   8   9
     #       S  Pr  Ed   Q   PG  En  Pop  Pol  R  AP
     "evt": [0,  1,  0,  0,   0,  0,   0,   0, 0, -3]
     },
    # {"de": "Vereinfachte Anwendung von Verhütungsmitteln erleichtert die Geburtenkontrolle",
    #  "en": "Simplified use of contraceptives facilitates birth control",
    #  #       0   1   2   3   4   5   6    7   8   9
    #  #       S  Pr  Ed   Q   PG  En  Pop  Pol  R  AP
    #  "evt": [0,  0,  0,  0,   -3, 0,   0,   0, 0, 0]    # actually "nach eigener Wahl um bis zu 3 Schritte zurück"
    #  },
    # {"de": "Vereinfachte Anwendung von Verhütungsmitteln erleichtert die Geburtenkontrolle",
    #  "en": "Simplified use of contraceptives facilitates birth control",
    #  #       0   1   2   3   4   5   6    7   8   9
    #  #       S  Pr  Ed   Q   PG  En  Pop  Pol  R  AP
    #  "evt": [0,  0,  0,  0,   -3, 0,   0,   0, 0, 0]    # actually "nach eigener Wahl um bis zu 3 Schritte zurück"
    #  },
    # {"de": "Vereinfachte Anwendung von Verhütungsmitteln erleichtert die Geburtenkontrolle",
    #  "en": "Simplified use of contraceptives facilitates birth control",
    #  #       0   1   2   3   4   5   6    7   8   9
    #  #       S  Pr  Ed   Q   PG  En  Pop  Pol  R  AP
    #  "evt": [0,  0,  0,  0,   -3, 0,   0,   0, 0, 0]    # actually "nach eigener Wahl um bis zu 3 Schritte zurück"
    #  },
    # {"de": "Vereinfachte Anwendung von Verhütungsmitteln erleichtert die Geburtenkontrolle",
    #  "en": "Simplified use of contraceptives facilitates birth control",
    #  #       0   1   2   3   4   5   6    7   8   9
    #  #       S  Pr  Ed   Q   PG  En  Pop  Pol  R  AP
    #  "evt": [0,  0,  0,  0,   -3, 0,   0,   0, 0, 0]    # actually "nach eigener Wahl um bis zu 3 Schritte zurück"
    #  },
    # {"de": "Vereinfachte Anwendung von Verhütungsmitteln erleichtert die Geburtenkontrolle",
    #  "en": "Simplified use of contraceptives facilitates birth control",
    #  #       0   1   2   3   4   5   6    7   8   9
    #  #       S  Pr  Ed   Q   PG  En  Pop  Pol  R  AP
    #  "evt": [0,  0,  0,  0,   -3, 0,   0,   0, 0, 0]    # actually "nach eigener Wahl um bis zu 3 Schritte zurück"
    #  },
    # {"de": "Vereinfachte Anwendung von Verhütungsmitteln erleichtert die Geburtenkontrolle",
    #  "en": "Simplified use of contraceptives facilitates birth control",
    #  #       0   1   2   3   4   5   6    7   8   9
    #  #       S  Pr  Ed   Q   PG  En  Pop  Pol  R  AP
    #  "evt": [0,  0,  0,  0,   -3, 0,   0,   0, 0, 0]    # actually "nach eigener Wahl um bis zu 3 Schritte zurück"
    #  },
]