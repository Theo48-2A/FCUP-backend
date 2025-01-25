import os
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Démarre le serveur Django en fonction de l\'environnement'

    def handle(self, *args, **kwargs):
        # Détection de l'environnement via les variables d'environnement
        app_env = os.getenv('APP_ENV', 'development')

        # Appliquer les migrations dans tous les cas
        self.stdout.write(self.style.SUCCESS("Appliquer les migrations..."))
        call_command('migrate', interactive=False)

        # Logique pour développement
        if app_env == 'development':
            self.stdout.write(self.style.SUCCESS("Environnement : développement"))
            self.stdout.write(self.style.SUCCESS("Démarrage du serveur de développement..."))
            call_command('runserver', '0.0.0.0:8000')

        # Logique pour production
        elif app_env == 'production':
            self.stdout.write(self.style.SUCCESS("Environnement : production"))
            self.stdout.write(self.style.SUCCESS("Démarrage de Gunicorn..."))
            os.system('gunicorn --bind 0.0.0.0:8000 app.wsgi:application')

        # Environnement inconnu
        else:
            self.stderr.write(self.style.ERROR("Environnement non reconnu : {}".format(app_env)))
            exit(1)
