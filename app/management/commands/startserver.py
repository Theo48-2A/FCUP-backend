from django.core.management.base import BaseCommand
from django.core.management import call_command
from app.core.config import Config
import os

class Command(BaseCommand):
    help = 'Démarre le serveur Django en fonction de l\'environnement'

    def handle(self, *args, **kwargs):
        # Récupérer l'environnement via Config
        app_env = Config.APP_ENV

        # Appliquer les migrations dans tous les cas
        self.stdout.write(self.style.SUCCESS("Appliquer les migrations..."))
        call_command(command_name='migrate', interactive=False)

        # Logique pour développement
        if app_env == 'development':
            self.stdout.write(self.style.SUCCESS("Environnement : développement"))
            self.stdout.write(self.style.SUCCESS("Démarrage du serveur de développement..."))
            call_command(command_name='runserver', interactive=False, args=f"{Config.SRV_LISTEN_ADDR}:{Config.SRV_PORT}")

        # Logique pour production
        elif app_env == 'production':
            self.stdout.write(self.style.SUCCESS("Environnement : production"))
            self.stdout.write(self.style.SUCCESS("Démarrage de Gunicorn..."))
            os.system(f"gunicorn --bind {Config.SRV_LISTEN_ADDR}:{Config.SRV_PORT} app.wsgi:application")

        # Environnement inconnu
        else:
            self.stderr.write(self.style.ERROR(f"Environnement non reconnu : {app_env}"))
            exit(1)
