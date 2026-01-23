# Pokestral-V2

## Poke-env

### Actions

L'IA doit être capable, durant un match, d'effectuer les actions suivantes :

#### Analyse

- Voir son équipe. Pour chaque pokémon, cela inclus :
    - Attaques + PP restants ;
    - Objet tenu **actuellement** ;
    - Talent du Pokémon (actuel + de base) ;
    - Statistiques (+ changements de stats/HP actuels) ;
    - Status du pokémon (paralysie, empoisonnement (normal ou grave), confusion, attraction, ...) ;
    - Type(s) du pokémon (actuel, de base, téracrystallisation) ;
    - Niveau du pokémon (permet notamment d'ajuster les calculs de stats) ;
- Voir ses options. Cela inclus :
    - Attaques possibles (utile pour les objets "*choix*", certains talents, ...) ;
    - Actions possibles (switch, méga-évolution, téracrystallisation, ...) ;
- Voir son adversaire. Cela inclus à peu près les mêmes informations que pour sa propre équipe, mais en rajoutant des inconnus et/ou des ranges de valeurs ;
- Voir l'état actuel de la partie (pokémons présents sur le terrain, tours joués jusqu'à maintenant, ...) ;
- Voir les informations de la partie (ex. le type de match), ainsi que les règles du match.

### Actions

- Effectuer une attaque ;
- Changer de pokémon ;
- Effectuer une action spéciale (méga-évolution, téracrystallisation, ...) avant d'attaquer ;
- Parler dans le chat (2 versions : une entraînée sur le chat de Showdown, une sans entraînement supplémentaire) ;
- Forfeit (activable/désactivable) ;