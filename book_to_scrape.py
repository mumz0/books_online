import time
from bs4 import BeautifulSoup
import requests
import os
import csv

from book import Book
import utils


class BookToScrape:

    def scan_everything(self):
        build_folder_path = self.create_folder_to_store_data()
        base_url = "http://books.toscrape.com/"
        category_url_dict_lst = self.get_category_links(base_url)
        for category_url_dict in category_url_dict_lst:
            book_objs_lst = self.get_category_book_objs(category_url_dict, base_url)
            self.load_data_to_csv_and_download_images(book_objs_lst, build_folder_path)
    

    def create_folder_to_store_data(self):
        path = os.path.abspath(os.path.join(os.getcwd(), "_build"))
        build_folder_path = utils.create_folder_with_date_time(path)
        return build_folder_path


    def load_data_to_csv_and_download_images(self, book_objs_lst, build_folder_path):
        category_directory = utils.create_folder(build_folder_path, book_objs_lst[0].category)
        images_folder = utils.create_folder(category_directory, "images")
        self.create_books_csv_file(book_objs_lst, category_directory)          
        for book_obj in book_objs_lst:
            img_data = requests.get(book_obj.image_url)
            if img_data.status_code == 200:
                image_path = os.path.join(images_folder, book_obj.universal_product_code) + ".jpg"
                with open(image_path, 'wb') as handler:
                    handler.write(img_data.content) 



    def create_books_csv_file(self, lst, directory):
        header_dict = {"image_url": "image url", "product_page_url": "product page url", "category": "category", "title": "title", "review_rating": "review rating", "product_description": "product description", "universal_product_code": "universal product code", "price_excl_tax": "price excl tax", "price_incl_tax": "price incl tax", "availability": "availability"}
        csv_path = os.path.join(directory, "books") + ".csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL)
            self.add_headers(header_dict, writer)
            for row in lst:
                writer.writerow(vars(row).values())
        csvfile.close()


    def get_category_book_objs(self, category_url_dict, base_url):
        book_obj_lst = []
        book_url_lst = self.parse_books_url_per_page(category_url_dict["category_url"])
        for book_url in book_url_lst:
            book_data = self.get_book_data(book_url, base_url, category_url_dict["category"])
            book_obj = self.transform_data(book_data)
            book_obj_lst.append(book_obj)
        return book_obj_lst

    
    def get_category_links(self, base_url):
        dict_lst = []
        soup = self.parse_page(base_url)
        elems = soup.find_all(class_ = "nav nav-list")
        for elem in elems:
            ul_tag = elem.find("ul")
            a_links = ul_tag.find_all('a')
            for a_link in a_links:
                link = a_link.get("href")
                new_url = utils.create_url(base_url, link)
                category = a_link.get_text()
                _dict = {"category": category, "category_url": new_url}
                dict_lst.append(_dict)
        return dict_lst


    def get_book_data(self, book_url, base_url, category):
        book_data_dict={}
        soup = self.parse_page(book_url)
        book_data_dict["product_page_url"] = book_url
        try:
                book_data_dict["title"] = soup.find("h1").text

        except AttributeError:
                book_data_dict["title"] = "Non renseigné"
        try:
            book_data_dict["product_description"] = soup.find(id="product_description").find_next_sibling('p').text
        except AttributeError:
            book_data_dict["product_description"] = "Non renseigné"

        try:
            book_data_dict["universal_product_code"] = soup.find("th", text="UPC").find_next_sibling("td").text
        except AttributeError:
            book_data_dict["universal_product_code"] = "Non renseigné"

        try:
            book_data_dict["price_excl_tax"] = soup.find("th", text="Price (excl. tax)").find_next_sibling("td").text
        except AttributeError:
            book_data_dict["price_excl_tax"] = "Non renseigné"

        try:
            book_data_dict["price_incl_tax"] = soup.find("th", text="Price (incl. tax)").find_next_sibling("td").text
        except AttributeError:
            book_data_dict["price_incl_tax"] = "Non renseigné"

        try:
            book_data_dict["availability"] = soup.find("th", text="Availability").find_next_sibling("td").text
        except AttributeError:
            book_data_dict["availability"] = "Non renseigné"

        try:
            book_data_dict["review_rating"] = soup.find("th", text="Number of reviews").find_next_sibling("td").text
        except AttributeError:
            book_data_dict["review_rating"] = "Non renseigné"
        try:  
            relative_image_url = soup.find(class_ = "item active").find('img', alt = book_data_dict["title"]).get("src")
            book_data_dict["image_url"] = utils.create_absolute_link(base_url, relative_image_url)
        except AttributeError:
            book_data_dict["image_url"] = "Non renseigné"
        
        book_data_dict["category"] = category

        return book_data_dict  


    def transform_data(self, book_data_dict):
        book_data_dict = utils.format_book_data(book_data_dict)
        book_obj = Book.create_book_obj(book_data_dict)
        return book_obj


    def parse_books_url_per_page(self, url):
        book_link_lst = []
        soup = self.parse_page(url)

        books_elems = soup.find_all("h3")
        for book_elem in books_elems:
            book_link = book_elem.find("a").get("href")
            absolute_link = utils.create_absolute_link(url, book_link)
            book_link_lst.append(absolute_link)

        next_page_link = self.check_next_page(soup)
        if next_page_link:
            next_page_url = utils.modify_url(url, next_page_link)  
            book_link_lst += self.parse_books_url_per_page(next_page_url)

        return book_link_lst

                            
    def parse_page(self, url):
        max_retries = 2
        for index in range(max_retries):
            try:
                response = requests.get(url)
                if response.ok:
                    soup = BeautifulSoup(response.text, "html.parser")
                    return soup
            except requests.ConnectTimeout:
                print("La connexion a l'adresse : ", url, " à expiré. Essai ", index + 1)


    def check_next_page(self, soup):
        if soup.find(class_ = "next"):
            next_page_link = soup.find(class_ = "next").find("a").get("href")
            return next_page_link


    def add_headers(self, headers, writer):
        writer.writerow(headers.values())