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
- SQLLite: SQLite est un système de base de données qui a la particularité de fonctionner sans serveur, l'intérêt c'est que c'est très léger et rapide à mettre en place. On a donc mis en place SQLLite afin de stocker des données structurer ailleurs que dans des variables, comme ça lorsqu'on relance notre script de zéro les urls sont persisté, cela évite de surcharger la mémoire de notre programme.
