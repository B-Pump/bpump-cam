# bpump-cam

Documentation only in French for the moment !

Calculateur d'angles pour le projet B-Pump, coach robotique 100% connecté !

Ce programme utilise les bibliothèques [Mediapipe](https://pypi.org/project/mediapipe/) et [OpenCV](https://pypi.org/project/opencv-python/) pour calculer les angles entre les liaisons du corps, offrant ainsi une solution robuste pour vérifier la précision des mouvements. L'objectif est d'assurer que l'utilisateur effectue correctement les exercices en mesurant les angles formés par différentes parties du corps.

# Fonctionnalités

- Utilisation de [Mediapipe](https://pypi.org/project/mediapipe/) pour la détection des points clés du corps.
- Intégration d'[OpenCV](https://pypi.org/project/opencv-python/) pour le traitement d'image et le calcul des angles entre les liaisons.
- Prise en charge de plusieurs exercices grâce à la flexibilité du calcul des angles.
- Interface dans la console pour tester avec plusieurs vidéos via le fichier [input](./input.py)

# Utilisation

1. Vérifier que vous possèdez une version de python entre la [3.7](https://www.python.org/downloads/release/python-370/) et la [3.10](https://www.python.org/downloads/release/python-3100/).
2. Installer les dépendances via le fichier [requirements](./requirements.txt)

```
pip install -r requirements.txt
```

3. Exécuter le programme [input.py](./input.py)
4. Admirer le robot calculer les angles du corps sur différents exercices

# Contributions

Les contributions sous forme de suggestions, rapports de bugs, ou demandes de fonctionnalités sont les bienvenues. N'hésitez pas à ouvrir une [issue](https://github.com/wiizzl/bpump-app/issues) ou à faire un [PR](https://github.com/wiizzl/bpump-app/pulls).

# Auteurs
- [Arkitect](https://github.com/Arkhitecte)
- [wiizz](https://github.com/wiizzl)
- [Siphastar83](https://github.com/Siphastar83)

# License

Ce projet est sous license MIT. Vous pouvez consulter le fichier [LICENSE](./LICENSE.md) pour plus d'infos.