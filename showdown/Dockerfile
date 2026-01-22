# Utilisation de la version LTS (Long Term Support) actuelle de Node sur Alpine Linux (très léger)
FROM node:18-alpine

# Installation de git pour cloner le repo
RUN apk add --no-cache git

# Création du répertoire de travail
WORKDIR /app

# Clonage de la dernière version de Pokémon Showdown
# On clone dans le dossier courant (.)
RUN git clone https://github.com/smogon/pokemon-showdown.git .

# Installation des dépendances
RUN npm install

# Configuration : Showdown a besoin d'un fichier config.js.
# On copie l'exemple fourni par défaut qui fonctionne très bien pour un serveur privé.
RUN cp config/config-example.js config/config.js

# Le port par défaut de Showdown est 8000
EXPOSE 8000

# Commande de lancement
CMD mkdir -p logs/repl && \
    node pokemon-showdown