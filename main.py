"""Détection d'objets dans une image via l'API d'inférence Hugging Face."""

import argparse
import os
import sys

import requests
from dotenv import load_dotenv

# Charge les variables définies dans le fichier .env (ignoré par Git)
load_dotenv()

DEFAULT_API_URL = "https://router.huggingface.co/hf-inference/models/facebook/detr-resnet-50"
API_URL = os.getenv("HF_API_URL", DEFAULT_API_URL)
HF_TOKEN = os.getenv("HF_TOKEN")


def query(filename: str):
    """Envoie une image à l'API et renvoie la liste des objets détectés."""
    if not os.path.exists(filename):
        print(f"Erreur : le fichier {filename} n'existe pas.")
        return None

    with open(filename, "rb") as f:
        data = f.read()

    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "image/jpeg"}
    response = requests.post(API_URL, headers=headers, data=data, timeout=60)

    if response.status_code == 200:
        return response.json()
    print(f"Erreur API : {response.status_code} - {response.text}")
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Détecte les objets présents dans une image.")
    parser.add_argument("image", nargs="?", default="cats.jpg", help="chemin de l'image (défaut : cats.jpg)")
    parser.add_argument("--min-score", type=float, default=0.5, help="score minimal affiché (défaut : 0.5)")
    args = parser.parse_args()

    if not HF_TOKEN:
        sys.exit("HF_TOKEN introuvable : copiez .env.example en .env et renseignez votre token Hugging Face.")

    output = query(args.image)
    if not output:
        print("Aucun résultat à afficher.")
        return

    print(f"Résultats de la détection pour {args.image} :")
    for detection in output:
        score = detection.get("score", 0)
        if score >= args.min_score:
            print(f"- {detection.get('label', 'inconnu')} : {score:.2f}")


if __name__ == "__main__":
    main()
