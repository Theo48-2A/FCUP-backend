# Utiliser l'image officielle Nginx
FROM nginx:alpine

# Définir le répertoire de configuration
WORKDIR /etc/nginx/

# Copier le fichier de configuration template dans le conteneur
COPY nginx.conf.template /etc/nginx/templates/nginx.conf.template

# Script d'entrée pour générer le nginx.conf avec les bonnes variables d'environnement
CMD envsubst '$NGINX_INTERNAL_PORT' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf && \
    nginx -g 'daemon off;'
