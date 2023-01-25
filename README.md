# SMA - Projet noté Prey-predators

Superprédateurs: rouges\
Carnivores: oranges\
Herbivores: verts\
Decomposeurs: bleus en théorie (mais concrètement on ne voit que le trait du vecteur d'accélération)\
Végétaux: verts (mais petits)\
Cadavres: rouges (mais très petits)\

# Détail des spécificités:
Appuyez sur I dans la fenêtre pour avoir les informations concernant les population dans la console

Les agents ne cherchent pas à manger tant que leur faim n'a pas atteint un certain seuil (qui est un paramètre soumis à mutation). Par contre, la symbiose peut les pousser à se rapprocher de leurs cibles (même si en soit on ne peut pas vraiment parler de symbiose dans ce cas). La symbiose avec les différentes espèces est soumise à mutation et peut être modifié dans scenario.json

Lorsqu'un agent commence à manger, il reste immobile, et sa jauge de faim diminue tant qu'il a à manger. S'il bouge(pour fuir par exemple), il arrête de manger
