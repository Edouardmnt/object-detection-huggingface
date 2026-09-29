import requests
import os


def query(filename):
    """Envoie une image à l'API Hugging Face pour la détection d'objets."""
    # Vérifie si le fichier existe
    if not os.path.exists(filename):
        print(f"Erreur : Le fichier {filename} n'existe pas.")
        return None

    # Lecture et envoi de l'image à l'API
    with open(filename, "rb") as f:
        data = f.read()

    response = requests.post(API_URL, headers=headers, data=data)

    # Vérifie si la requête a été réussie
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur API : {response.status_code} - {response.text}")
        return None

# Nom du fichier image à analyser
filename = "C:/Users/edoua/PycharmProjects/projet_IA/cats.jpg"

# Appel de l'API et récupération des résultats
output = query(filename)

# Traitement et affichage des résultats
if output:
    print("Résultats de la détection :")
    for detection in output:
        label = detection.get("label", "Inconnu")  # Récupère le label (ou 'Inconnu' si absent)
        score = detection.get("score", 0)         # Récupère le score (ou 0 si absent)
        print(f"- Objet détecté : {label}, Score : {score:.2f}")
else:
    print("Aucun résultat à afficher.")
