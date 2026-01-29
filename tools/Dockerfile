# Utilisation d'une image légère
FROM node:18-slim

# Créer le répertoire de travail
WORKDIR /usr/src/app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installation propre (production)
RUN npm install --only=production

# Copier le reste du code source
COPY . .

# Exposer le port
EXPOSE 3000

# Lancer l'application
CMD [ "node", "src/index.js" ]