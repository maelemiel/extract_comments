#!/usr/bin/env python3
"""
Application d'exemple démontrant les annotations commentaires.
"""

class User:
    """Classe représentant un utilisateur."""
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        # TODO: Ajouter validation d'email @pierre P2 DUE:2023-12-31
        self.is_active = True

    def authenticate(self, password):
        # FIXME: Implémenter la vérification de mot de passe @alice P1 #42
        return True
    
    def send_welcome_email(self):
        # REVIEW: Évaluer si nous devrions utiliser un template @bob
        message = f"Bienvenue {self.name}!"
        # BUG: Le message n'est pas encodé correctement pour les caractères spéciaux P1 DUE:2023-11-15
        return self._send_email(message)
    
    def _send_email(self, message):
        # TEMP: Implémentation temporaire, sera remplacée par un service réel
        print(f"Email envoyé à {self.email}: {message}")
        return True


# HACK: Contournement temporaire pour la connexion à la base de données @pierre
DB_CONNECTION = {
    'host': 'localhost',
    'user': 'admin'
    # NOTE: Le mot de passe est stocké dans les variables d'environnement
}

def process_data(data):
    """Traite les données utilisateur."""
    # OPTIMIZE: Cette fonction est lente avec de grandes quantités de données @alice P3 DUE:2024-01-15
    result = []
    for item in data:
        # QUESTION: Devrions-nous filtrer les valeurs nulles? @bob
        processed = item * 2
        result.append(processed)
    return result

# TODO: Implémenter l'endpoint API REST pour la création d'utilisateurs @pierre P2
def create_user_api():
    pass

# IDEA: Ajouter une fonctionnalité d'export PDF des rapports @alice P3 CREATED:2023-10-01
def generate_report():
    # IN PROGRESS: Développement du système de rapports @bob P2 DUE:2023-12-25
    pass
