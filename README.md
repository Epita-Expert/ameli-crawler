# Ameli-Crawler
 
## Auteurs
- Romain Paturet
- Nathan Podesta
 
## Outils
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

## Generation du corpus

Pour la génération du corpus, nous allons commencer par récupérer toutes les spécialités présente sur ce lien http://annuairesante.ameli.fr/trouver-un-professionnel-de-sante/.

```python
html = get(f'{base_url}/trouver-un-professionnel-de-sante/')
list_url_speciality = re.findall('<a href=\"(/trouver-un-professionnel-de-sante/(.*?))\">', html)[:-1]
specialities = [Speciality(url_speciality[1], url_speciality[0]) for url_speciality in list_url_speciality
```

Ensuite le crawler suivra un des liens, qui lui donner une liste de departement pui une liste de ville est enfin la liste des medecins exercant dans cette ville.

## Description de l'algorithme
Nous avons implémenté un surfeur aléatoire dans notre crawler. Cet algorithme est basé sur la notion de probabilité. En effet, nous avons une probabilité de 0.5 de choisir une URL dans la liste des URLs à crawler. Si nous avons une probabilité de 0.5, alors nous avons une chance sur deux de choisir une URL dans la liste des URLs à crawler.

Après avoir construit notre corpus, nous avons décidé à chaque tour de boucle de choisir un nombre aléatoirement entre 0 et 1. Si ce nombre est égal à 1, alors nous allons choisir une URL dans la liste des URLs des docteurs de la spécialité et de la région qu'on est en train de crawler. Si ce nombre est égal à 0, alors nous allons choisir une URL au hasard dans la liste des URLs des spécialités puis de la même manière chosir un département puis une ville puis un docteur aléatoirement afin de stocker en base le nom du docteur.

Plus grossièrement :
    - Tirer un nombre aléatoire entre 0 et 1
    - Si c'est égal à 1, alors on choisit une URL au hasard dans la liste des URLs des docteurs (de la spécialité et de la région qu'on est en train de crawler)
    - Si c'est égal à 0, alors on choisit une URL au hasard dans la liste des URLs des spécialités puis de la même manière on choisit un département puis une ville puis un docteur aléatoirement afin de stocker en base le nom du docteur
    - Si la page a été crawlée, on va sur le cas 0

## Description de la données
Nous avons créer plusieurs table: 'doctor', 'speciality', 'city', 'department'.

### Speciality :

| Link | Name |
| :---: | :---: |
/trouver-un-professionnel-de-sante/masseur-kinesitherapeute | masseur-kinesitherapeute
/trouver-un-professionnel-de-sante/gynecologues-obstetricien | gynecologues-obstetricien
/trouver-un-professionnel-de-sante/infirmier | infirmier
/trouver-un-professionnel-de-sante/ophtalmologiste | ophtalmologiste
/trouver-un-professionnel-de-sante/chirurgiens-dentistes | chirurgiens-dentistes
/trouver-un-professionnel-de-sante/medecin-generaliste | medecin-generaliste
/trouver-un-professionnel-de-sante/acupuncteur | acupuncteur
/trouver-un-professionnel-de-sante/allergologue | allergologue
/trouver-un-professionnel-de-sante/allergologue | allergologue

Ces données récupérées vont nous permettre ensuite d'aller récupérer les départements dans lesquels nous pouvons trouver des personnels de santé de la spécialité choisie.

### Departement :

| Link | Name | Speciality |
| :---: | :---: | :---: |
/trouver-un-professionnel-de-sante/psychiatres/49-maine-et-loire | 49-maine-et-loire | psychiatres
/trouver-un-professionnel-de-sante/pediatre/65-hautes-pyrenees | 65-hautes-pyrenees | pediatre

Ces données récupérées vont nous permettre ensuite d'aller récupérer les villes dans lesquels nous pouvons trouver des personnels de santé de la spécialité choisie de ce département.

### City :
| Link | Name | department_link |
| :---: | :---: | :---: |
/trouver-un-professionnel-de-sante/psychiatres/49-maine-et-loire-les-ponts-de-ce | les-ponts-de-ce | /trouver-un-professionnel-de-sante/psychiatres/49-maine-et-loire
/trouver-un-professionnel-de-sante/pediatre/65-hautes-pyrenees-tarbes | tarbes | /trouver-un-professionnel-de-sante/pediatre/65-hautes-pyrenees
/trouver-un-professionnel-de-sante/oto-rhino-laryngologue-%28orl%29-et-chirurgien-cervico-facial/972-martinique-fort-de-france	 | fort-de-france | /trouver-un-professionnel-de-sante/oto-rhino-laryngologue-%28orl%29-et-chirurgien-cervico-facial/972-martinique

Ces données récupérées vont nous permettre ensuite d'aller récupérer les noms des docteurs.

### Doctor :
| Link | Name | city_link |
| :---: | :---: | :---: |
/professionnels-de-sante/fiche-detaillee-planson-jennifer-BLs1kjc4MzGx | PLANSON JENNIFER | /trouver-un-professionnel-de-sante/psychiatres/49-maine-et-loire-les-ponts-de-ce
/professionnels-de-sante/fiche-detaillee-laporte-eve-Brc1mzU1MzG7 | LAPORTE EVE | /trouver-un-professionnel-de-sante/pediatre/65-hautes-pyrenees-tarbes
/professionnels-de-sante/fiche-detaillee-brafine-eddy-CbU1kDMxMDC0 | BRAFINE EDDY | /trouver-un-professionnel-de-sante/oto-rhino-laryngologue-%28orl%29-et-chirurgien-cervico-facial/972-martinique-fort-de-france

Grâce à notre crawler nous allons donc pouvoir récupérer tous les noms des docteurs de chaque spécialité de manière aléatoire.
## Représentation des données par un graph
 
Pour la démonstration nous allons créer un graph qui représentera le lien entre les spécialités et un département (Ain).

![image](https://user-images.githubusercontent.com/45274627/176322566-5e4056b3-3ee2-410c-804e-4cf81e290f5b.png)


## Todo:
- [x] Check if url already exists
- [ ] Generate the graph live
- [ ] Add Redis Search

