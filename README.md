# ameli-crawler

### Développeurs
- Romain Paturet
- Nathan Podesta

### Outils
- Python
- Redis
- SQLLite
- RedisInsight v2
- DB Browser for SQLLite

### Pourquoi ces outils ?
- Python: Avec ses performances optimales et ses innombrables modules, Python est tout simplement le langage le plus utilisé pour le web scraping/crawling. Python est généralement considéré comme étant un langage facile à apprendre car sa syntaxe est simple et lisible. C'est pour cela qu'on l'a choisi.
- Redis: On utilise Redis afin de générer des graphs.
- SQLLite: SQLite est un système de base de données qui a la particularité de fonctionner sans serveur, l'intérêt c'est que c'est très léger et rapide à mettre en place. On a donc mis en place SQLLite afin de stocker des données structurer ailleurs que dans des variables, comme ça lorsqu'on relance notre script de zéro les URLs sont persisté, cela évite de surcharger la mémoire de notre programme.


### Description de l'algorithme
Nous avons implémenté un surfeur aléatoire dans notre crawler. Cet algorithme est basé sur la notion de probabilité. En effet, nous avons une probabilité de 0.5 de choisir une URL dans la liste des URLs à crawler. Si nous avons une probabilité de 0.5, alors nous avons une chance sur deux de choisir une URL dans la liste des URLs à crawler.
Après avoir construit notre corpus, nous avons décidé à chaque tour de boucle de choisir un nombre aléatoirement entre 0 et 1. Si ce nombre est égal à 1, alors nous allons choisir une URL dans la liste des URLs des docteurs de la spécialité et de la région qu'on est en train de crawler. Si ce nombre est égal à 0, alors nous allons choisir une URL au hasard dans la liste des URLs des spécialités puis de la même manière chosir un département puis une ville puis un docteur aléatoirement afin de stocker en base le nom du docteur.

Plus grossièrement :
    - Tirer un nombre aléatoire entre 0 et 1
    - Si c'est égal à 1, alors on choisit une URL au hasard dans la liste des URLs des docteurs (de la spécialité et de la région qu'on est en train de crawler)
    - Si c'est égal à 0, alors on choisit une URL au hasard dans la liste des URLs des spécialités puis de la même manière on choisit un département puis une ville puis un docteur aléatoirement afin de stocker en base le nom du docteur
    - Si la page a été crawlée, on va sur le cas 0


