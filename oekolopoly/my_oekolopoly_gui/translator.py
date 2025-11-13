def dict_translate(args):
    """
    :param args: contains attribute ``language = "de"|"en"``
    :return: translation dictionary for all GUI elements
    """
    if args.language == "de":
        dtl = {"Help Mode": "Hilfemodus",
               "Exit": "Verlassen",
               "Forward": "Weiter ->",
               "Back": "<- Zurück",
               "Page": "Seite: ",
               "Special Case": "Spezialfall",
               "Points": "Aktionspunkte",
               "MoreInfoPoints": "Einfluss, Geld, Arbeit,\n"
                                 "Energie, Güter, Nahrung",
               "Production": "Produktion",
               "MoreInfoProduction": "Industrie, Handwerk,\n"
                                     "Landwirtschaft,\n"
                                     "Dienstleistungen",
               "Redevelop": "Sanierung",
               "MoreInfoRedevelop": "Umweltschutz, Recycling,\n"
                                    "Biotechnik, sanfte Energie,\n"
                                    "Landschaftserhaltung,\n"
                                    "Humanisierung der\n"
                                    "Arbeitswelt",
               "EnvirDamage": "Umweltbelastung",
               "MoreInfoEnvirDamage": "Abgase, Abwässer,\n"
                                      "Abwärme, Lärm, Raubbau,\n"
                                      "Landschaftszerstörung,\n"
                                      "Trennung natürlicher Kreisläufe,\n"
                                      "Verkehrschaos, Städtezerfall",
               "ClearActions": "Entferne verteilte Punkte",
               "ExecuteStep": "Zug ausführen",
               "CloseGame": "Spiel beenden",
               "Reset": "Neues Spiel",
               "BestMoveAI": "Bester Zug (KI)",
               "PreviewMode": "Vorschaumodus",
               "Help": "Hilfe?",
               "GameInstructions": "Spielanleitung",
               "GameHistory": "Spielhistorie",
               "ActionPointsLeft": "Aktionspunkte übrig: ",
               "DistributedPoints": "Verteilte Punkte: ",
               "Round": "Runde: ",
               "GameOver": "Game over",
               }
        return dtl
    if args.language == "en":
        dtl = {"Help Mode": "Help Mode",
               "Exit": "Exit",
               "Forward": "Forward ->",
               "Back": "<- Back",
               "Page": "Page: ",
               "Special Case": "SpecialCase",
               "Points": "Action Points",
               "MoreInfoPoints": "Influence, money, work,\n"
                                 "energy, goods, food",
               "Production": "Production",
               "MoreInfoProduction": "Industry, crafts,\n"
                                     "agriculture,\n"
                                     "services",
               "Redevelop": "Redevelop",
               "MoreInfoRedevelop": "Environmental protection,\n"
                                    "recycling, biotechnology,\n"
                                    "landscape conservation,\n"
                                    "humane working\n"
                                    "environment",
               "EnvirDamage": "Environ. Damage",
               "MoreInfoEnvirDamage": "Waste gases, wastewater,\n"
                                      "waste heat, noise, exploitation,\n"
                                      "landscape destruction,\n"
                                      "disconnection of natural cycles,\n"
                                      "traffic chaos, urban decay",
               "ClearActions": "Clear points",
               "ExecuteStep": "Execute step",
               "CloseGame": "Exit",
               "Reset": "New game",
               "BestMoveAI": "Best move (AI)",
               "PreviewMode": "Preview mode",
               "Help": "Help?",
               "GameInstructions": "Game instructions",
               "GameHistory": "Game history",
               "ActionPointsLeft": "Action points left: ",
               "DistributedPoints": "Distributed points: ",
               "Round": "Round: ",
               "GameOver": "Game over",
               }
        return dtl
    raise RuntimeError(f"[dict_translate] args.language = {args.language} is not supported!")