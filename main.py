from book_to_scrape import BookToScrape


def run():
    book_to_scrape_obj = BookToScrape()
    return book_to_scrape_obj

if __name__ == "__main__":
    book_to_scrape_obj = run()
    book_to_scrape_obj.scan_everything()