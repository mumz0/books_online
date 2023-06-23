from urllib.parse import urljoin
import os
from datetime import datetime



def create_url(url, link):
    new_link = url + link
    return new_link
    

def create_absolute_link(base_url, relative_url):
    absolute_link = urljoin(base_url, relative_url)
    return absolute_link  


def modify_url(url, path_to_add):
    new_url = urljoin(url, path_to_add)
    return new_url


def formate_book_data(book_dict):
    for key, value in book_dict.items():
        book_dict[key] = value.encode('Latin-1').decode('utf-8', 'ignore')
        if key == "category":
            book_dict[key] = value.strip()
        if key == "title":
            illegal_chars = r',<>:"/\|?*'
            for char in illegal_chars:
                filename = book_dict[key].replace(char, '')
                new_filename = ' '.join(filename.split()[:20])
                book_dict[key] = new_filename
    return book_dict


def create_folder_with_date_time(path):
    folder_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if not folder_name in path:
        new_directory = os.path.join(path, folder_name)
        os.makedirs(new_directory)

        print("Le dossier ", folder_name, " a été créé avec succès.")
    else:
        print("Le dossier ", folder_name, " existe déjà.")
    return new_directory


def create_folder(path, folder_name):
    if not os.path.exists(folder_name):
        new_directory = os.path.join(path, folder_name)
        os.mkdir(new_directory)
        print("Le dossier ", folder_name, " a été créé avec succès.")
    else:
        print("Le dossier ", folder_name, " existe déjà.")
    return new_directory