# Détection d'objets avec Hugging Face

Script Python qui détecte les objets présents dans une image (chats, chiens, oiseaux…) en appelant l'API d'inférence Hugging Face. Par défaut, il utilise le modèle [DETR ResNet-50](https://huggingface.co/facebook/detr-resnet-50) de Meta.

## Fonctionnement

1. Le script lit l'image et l'envoie à l'API d'inférence.
2. Le modèle renvoie la liste des objets détectés, chacun avec un label, un score de confiance et une boîte englobante.
3. Le script affiche les objets dont le score dépasse un seuil (0,5 par défaut).

## Installation

```bash
git clone https://github.com/Edouardmnt/object-detection-huggingface.git
cd object-detection-huggingface
pip install -r requirements.txt
```

`requirements.txt` installe deux bibliothèques :

- `requests` pour appeler l'API Hugging Face ;
- `python-dotenv` pour lire le token depuis un fichier `.env`.

## Configuration du token

L'API Hugging Face demande un token d'accès. Il n'est jamais écrit dans le code : le script le lit dans un fichier `.env` local, que Git ignore.

1. Créez un token (droits en lecture) sur [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
2. Copiez le modèle de configuration :

   ```bash
   cp .env.example .env
   ```

3. Ouvrez `.env` et collez votre token après `HF_TOKEN=`.

Au lancement, `load_dotenv()` charge ce fichier dans les variables d'environnement, puis le script récupère le token avec `os.getenv("HF_TOKEN")`.

`.env` figure dans le `.gitignore` : il reste sur votre machine et n'est jamais commité. Seul `.env.example`, sans valeur, est versionné pour montrer les variables attendues. Si `HF_TOKEN` est absent, le script s'arrête avec un message qui explique quoi faire.

## Utilisation

```bash
python main.py cats.jpg
python main.py oiseaux.jpg --min-score 0.8
```

Exemple de sortie (à titre indicatif) :

```
Résultats de la détection pour cats.jpg :
- cat : 0.99
- cat : 0.98
```

Pour utiliser un autre modèle, renseignez `HF_API_URL` dans `.env` avec l'URL d'inférence du modèle voulu.

## Structure

```
├── main.py            # script de détection
├── requirements.txt   # dépendances (requests, python-dotenv)
├── .env.example       # modèle de configuration, sans secret
├── .gitignore         # exclut .env, les caches Python et les fichiers d'IDE
└── cats.jpg, chien.jpg, oiseaux.jpg   # images de test
```

## Stack

Python · requests · python-dotenv · API d'inférence Hugging Face · DETR (transformer de détection d'objets)
