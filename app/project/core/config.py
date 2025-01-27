import os

class ConfigError(Exception):
    """Exception personnalisée pour les erreurs de configuration."""
    pass


class Config:
    @staticmethod
    def get_env_var(var_name):
        """Récupérer une variable d'environnement ou lever une exception."""
        value = os.getenv(var_name)
        if value is None:
            raise ConfigError(f"La variable d'environnement '{var_name}' est manquante.")
        return value

    # Environnement de l'application
    APP_ENV = get_env_var.__func__('APP_ENV')

    # Serveur
    SRV_PROTOCOL = get_env_var.__func__('SRV_PROTOCOL')
    SRV_IP = get_env_var.__func__('SRV_IP')
    SRV_PORT = get_env_var.__func__('SRV_PORT')
    SRV_LISTEN_ADDR = get_env_var.__func__('SRV_LISTEN_ADDR')

    # Base de données
    DB_USER = get_env_var.__func__('DB_USER')
    DB_PASSWORD = get_env_var.__func__('DB_PASSWORD')
    DB_IP = get_env_var.__func__('DB_IP')
    DB_PORT = get_env_var.__func__('DB_PORT')
    DB_NAME = get_env_var.__func__('DB_NAME')

    # Clé API pour SendGrid
    SENDGRID_API_KEY = get_env_var.__func__('SENDGRID_API_KEY')

    # Secrets et autres variables critiques
    SECRET_KEY = get_env_var.__func__('SECRET_KEY')
