# ameli-crawler
 
### Développeurs
- Romain Paturet
- Nathan Podesta
 
### Outils
- Python
- Redis
- SQLite
- RedisInsight v2
- DB Browser for SQLite
 
 
## Objectif du projet
 
Le but de ce projet est de permettre la recherche par nom, prénom ou spécialité d'un médecin.
Pour cela nous allons indexer les pages et representer les donnees extraites du site http://annuairesante.ameli.fr/trouver-un-professionnel-de-sante/.
Ce site permet de rechercher des médecins  grâce à leur nom, prénom, spécialité ou encore leur localisation.
 
Ce site a la particularité d'être mis à jour à chaque fois qu'une feuille de soins est générée par un médecin et est donc toujours à jour. Malheureusement aucune API n'est exposée et aucune extraction n'est proposée. Pour remédier à ça nous allons automatiser l’extraction de ses données , par expérience le site prend plusieurs jours à être entièrement lu. Le problème majeur est que le premier lien découvert ne sera pas relu avant que le site ne le soit entièrement.
 
L'approche par le crawling permettra de découvrir au fur et à mesure le site et de maniere aleatoire.
 
# Technique
 
La majeure partie du temps le programme attend le retour des appels web, les performances du langages n'auront que peu d'impact sur la vitesse d'exécution. Nous avons donc choisi Python pour sa simplicité de syntaxe et d'exécution. C'est aussi le langage le plus utilisé pour le web scraping/crawling. De plus, il possède de nombreuses librairies compatibles qui vont nous permettre de nous connecter à une base ou encore de générer des graphes.
Afin de stocker nos données temporairement, nous avons utilisé SQLite, c'est un système de base de données qui a la particularité de fonctionner sans serveur, l'intérêt c'est que c'est très léger et rapide à mettre en place. Dans notre cas nous allons y stocker les données intermédiaires de chacune de nos étapes de manière structurée. Le principal avantage est de repartir de l'état dans lequel le programme s’est arrêté. Cela évite aussi de surcharger des variables qui vont ralentir l'exécution. C'est une mémoire persistante en quelque sorte.
Récupérer des information et les stocker c'est bien mais savoir les représenter c'est encore mieux. Pour cela nous allons utiliser Redis Graph,  Redis est un serveur de cache de données et Redis Graph permet de stocker des graph dans un cache.
 
 ### Description de l'algorithme
Nous avons implémenté un surfeur aléatoire dans notre crawler. Cet algorithme est basé sur la notion de probabilité. En effet, nous avons une probabilité de 0.5 de choisir une URL dans la liste des URLs à crawler. Si nous avons une probabilité de 0.5, alors nous avons une chance sur deux de choisir une URL dans la liste des URLs à crawler.
Après avoir construit notre corpus, nous avons décidé à chaque tour de boucle de choisir un nombre aléatoirement entre 0 et 1. Si ce nombre est égal à 1, alors nous allons choisir une URL dans la liste des URLs des docteurs de la spécialité et de la région qu'on est en train de crawler. Si ce nombre est égal à 0, alors nous allons choisir une URL au hasard dans la liste des URLs des spécialités puis de la même manière chosir un département puis une ville puis un docteur aléatoirement afin de stocker en base le nom du docteur.

Plus grossièrement :
    - Tirer un nombre aléatoire entre 0 et 1
    - Si c'est égal à 1, alors on choisit une URL au hasard dans la liste des URLs des docteurs (de la spécialité et de la région qu'on est en train de crawler)
    - Si c'est égal à 0, alors on choisit une URL au hasard dans la liste des URLs des spécialités puis de la même manière on choisit un département puis une ville puis un docteur aléatoirement afin de stocker en base le nom du docteur
    - Si la page a été crawlée, on va sur le cas 0

## Generation du corpus
 
 
## Représentation des données par un graph
 
Pour la démonstration nous allons créer un graph qui représentera la distribution des médecins par départements.
# Todo
 
- Check if url already exists
- Generate the graph
- Add Redis Search

