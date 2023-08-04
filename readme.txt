# Projet BookstoScrape

## Introduction

Ce projet est une application Python qui extrait des informations sur les livres à partir du site "http://books.toscrape.com/".

## Installation

1. Cloner ce dépôt vers votre machine locale en utilisant la commande suivante :
   
   git clone <URL_DU_REPO>


2. Accéder au répertoire du projet :

   cd BookstoScrape


3. Créer un nouvel environnement virtuel en utilisant la commande suivante :

   python -m venv venv


4. Activer l'environnement virtuel (venv) :

   - Sur Windows : venv\Scripts\activate
   - Sur macOS et Linux : source venv/bin/activate


5. Installer les dépendances en utilisant la commande suivante :

   pip install -r requirements.txt


## Exécution

Une fois que vous avez activé l'environnement virtuel et installé les dépendances, vous pouvez exécuter l'application en utilisant la commande suivante :

   python main.py


L'application commencera à extraire les informations sur les livres à partir du site "http://books.toscrape.com/" et stockera les données dans des fichiers CSV dans le dossier "data".

## Note

Assurez-vous de ne pas inclure les données/images extraites dans le dépôt Git. Le dossier "data" et le dossier "images" sont déjà exclus du suivi Git grâce au fichier .gitignore.


*****EXPLICATIONS DES FONCTIONS ET LEUR UTILITE*****

Projet BookstoScrape - Fonctions et Utilité

Ce projet est une application Python qui extrait des informations sur les livres à partir du site "http://books.toscrape.com/". 
Vous trouverez ci-dessous une description détaillée de chaque fonction du projet et de son utilité :

**Fonction get_all_categories()
Cette fonction récupère toutes les catégories de livres disponibles sur le site "http://books.toscrape.com/".

Utilité :

Elle permet de créer une liste contenant toutes les catégories de livres, ainsi que leurs URL respectives.
Les informations sont ensuite écrites dans un fichier CSV appelé "categories.csv" dans le dossier "data".

**Fonction get_books_from_page(soup, cat_url)
Cette fonction extrait les informations de tous les livres présents sur une page spécifique du site.

Paramètres :

soup : L'objet BeautifulSoup représentant la page web.
cat_url : L'URL de la catégorie de livres.

Utilité :

Elle récupère les détails de chaque livre (URL, titre et URL de l'image de couverture).
Elle télécharge les images de couverture des livres et les enregistre dans le dossier "images".
La fonction renvoie une liste contenant toutes les URLs des livres présents sur la page.

**Fonction get_all_books_from_one_category(cat_url)
Cette fonction récupère tous les livres d'une catégorie donnée et de toutes ses pages.

Paramètre :

cat_url : L'URL de la catégorie de livres.

Utilité :

Elle appelle la fonction get_books_from_page() pour récupérer les livres de la page actuelle.
Elle recherche la pagination pour récupérer les livres des pages suivantes.
Les informations de chaque livre sont enregistrées dans un fichier CSV spécifique à la catégorie dans le dossier "data".

**Fonction get_book_infos(url_book)
Cette fonction extrait les informations détaillées d'un livre spécifique à partir de son URL.

Paramètre :

url_book : L'URL du livre.
Utilité :

Elle récupère des informations telles que le titre du livre, la catégorie, l'URL de l'image de couverture, la description du produit, la note de l'évaluation, le code UPC, les prix et la disponibilité.
Les informations sont renvoyées sous forme de dictionnaire.

**Fonction download_book_image(book_image_url, book_title)
Cette fonction télécharge l'image de couverture d'un livre à partir de son URL et l'enregistre localement.

Paramètres :

book_image_url : L'URL de l'image de couverture du livre.
book_title : Le titre du livre.

Utilité :

Elle télécharge l'image de couverture du livre et l'enregistre dans le dossier "images" avec un nom de fichier approprié.

**Fonction main()
Cette fonction est le point d'entrée du programme.

Utilité :

Elle appelle les différentes fonctions pour exécuter le processus d'extraction des données.

Ces fonctions travaillent ensemble pour extraire les informations sur les livres du site "http://books.toscrape.com/" et les enregistrer dans des fichiers CSV dans le dossier "data". 
Les images de couverture des livres sont également téléchargées et stockées dans le dossier "images". 
Vous pouvez exécuter l'application en utilisant la commande python main.py après avoir activé l'environnement virtuel et installé les dépendances.