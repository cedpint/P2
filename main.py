import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin
import string


def get_all_categories():
    """
    Retrieves all books categories from the website.

    Returns:
        list: A list containing all categories of books.
    """
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    categories = []
    category_tags = soup.find("ul", class_="nav-list").find("ul").find_all("a", href=True)
    for category_tag in category_tags:
        category = category_tag.text.strip()
        """categories.append((category, category_tag["href"]))"""
        categories.append((category, urljoin(url, category_tag["href"])))
        
    # Vérifier si le dossier "data" existe, sinon le créer
    if not os.path.exists("data"):
        os.makedirs("data")    

    # Write categories to a CSV file
    """with open("categories.csv", "w", newline="", encoding="utf-8") as file:"""
    file_path_categories = os.path.join("data", "categories.csv")
    with open(file_path_categories, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Category"])
        for item in categories:
            writer.writerow([item[0]])

    return categories


def get_books_from_page(soup, cat_url):
    """
    Fetches all books from a specific page

    Args:
        soup (BeautifulSoup): The BeautifulSoup object representing the page.
        cat_url (str): The URL of the book category.

    Returns:
        list: A list containing all book URLs from the page.
    """
    books = []
    product_pod_tags = soup.find_all("article", class_="product_pod")
    for product_pod_tag in product_pod_tags:
        book_url = urljoin(cat_url, product_pod_tag.find("h3").find("a")["href"])
        book_title = product_pod_tag.find("h3").find("a")["title"]
        book_image_url = urljoin(cat_url, product_pod_tag.find("img")["src"])
        download_book_image(book_image_url, book_title)
        books.append(book_url)

    return books


def get_all_books_from_one_category(cat_url):
    """
    Fetches all books from a specific category based on the provided URL.

    Args:
        cat_url (str): The URL of the book category.

    Returns:
        list: A list containing all book titles from the category.
    """
    response = requests.get(cat_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    category = soup.find("h1").text.strip()
    books = get_books_from_page(soup, cat_url)  # Call the new function
    next_page = soup.find("li", class_="next")

    while next_page:
        next_url = urljoin(cat_url, next_page.find("a")["href"]) 
        response = requests.get(next_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        books += get_books_from_page(soup, next_url)  # Append books from the next page
        next_page = soup.find("li", class_="next")    

    # Nettoyer le nom de la catégorie pour le nom du fichier
    cleaned_category_name = ''.join(c if c in string.ascii_letters + string.digits + " _-" else '_' for c in category.strip())

    # Création du nom de fichier en fonction de la catégorie du livre
    file_name = cleaned_category_name.lower() + ".csv"
    file_path_books_category = os.path.join("data", file_name)
    
    with open(file_path_books_category, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Product Page URL', 'Category', 'Image URL', 'Product Description', 'Review Rating', 'UPC', 'Price (excl. tax)', 'Price (incl. tax)', 'Availability'])
        writer.writeheader()
        for book_url in books:
            book_infos = get_book_infos(book_url)
            writer.writerow(book_infos)

    return books


def get_book_infos(url_book):
    """
    Retrieve the information of a book from his URL and save the details in a CSV file.

    Args:
        url_book (str): The URL of the book.

    Returns:
        dict: A dictionary containing the book information.
    """
    # Insert the url of the book
    
    response = requests.get(url_book)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the book title
    title_book = soup.find('h1').text

    # Get the category of the book
    ul_category = soup.find('ul', class_='breadcrumb')
    category_book = ul_category.find_all('li')[2].text.strip()

    # Get the image of the book
    image_book = soup.find('img')
    """image_src = url_book + image_book['src'].strip('../../')"""
    image_src = "http://books.toscrape.com/" + image_book['src'].strip('../../')
    # Get the product description
    product_description = soup.find('article').find('p').text

    # Get the review rating, number of stars
    review_rating = soup.find('p', class_='star-rating')['class'][1] + ' stars'

    # Get the book details
    product_info = soup.find('table', class_='table')
    rows = product_info.find_all('tr')
    universal_product_code = rows[0].find('td').text
    price_no_tax = rows[2].find('td').text
    price_with_tax = rows[3].find('td').text
    availability_book = rows[5].find('td').text

    book_details = {
        'Product Page URL': url_book,
        'Title': title_book,
        'Category': category_book,
        'Image URL': image_src,
        'Product Description': product_description,
        'Review Rating': review_rating,
        'UPC': universal_product_code,
        'Price (excl. tax)': price_no_tax,
        'Price (incl. tax)': price_with_tax,
        'Availability': availability_book
    }
    
    return book_details


def download_book_image(book_image_url, book_title):
    """
    Downloads the image of a book from its URL and saves it locally.

    Args:
        url_book (str): The URL of the book image.
        book_title (str): The title of the book.

    Returns:
        str: The filename of the saved image.
    """
    response = requests.get(book_image_url)
    image_content = response.content

    # Create the "images" directory if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")

    # Create the filename by replacing characters that might cause issues
    cleaned_book_title = ''.join(c if c.isalnum() or c in " _.-" else '_' for c in book_title)
    filename = f"images/{cleaned_book_title}.jpg"

    # Save the image locally
    with open(filename, "wb") as image_file:
        image_file.write(image_content)

    return filename

if __name__ == "__main__":
    # call function get_all_categories()
    categories = get_all_categories()
    print("All categories:", categories)

    # URL of the books category
    for category in categories:
        books = get_all_books_from_one_category(category[1])
        print("All books:", books)

    # Book URL 
    # book_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    # book_info = get_book_infos(book_url)
    # print("Book information:", book_info)
