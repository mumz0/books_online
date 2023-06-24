class Book :
    
    def __init__(
            self, 
            _image_url: str,
            _product_page_url: str, 
            _category: str, 
            _title: str, 
            _product_description: str, 
            _universal_product_code: str, 
            _price_excl_tax: int,
            _price_incl_tax: int,
            _availability: int,
            _review_rating: int,
            ):

        self.image_url = _image_url
        self.id = _product_page_url
        self.category = _category
        self.title = _title
        self.review_rating = _review_rating
        self.product_description = _product_description
        self.universal_product_code = _universal_product_code, 
        self.price_excl_tax = _price_excl_tax
        self.price_incl_tax = _price_incl_tax
        self.availability = _availability
    

    def create_book_obj(dict):
        book_obj = Book(
            _image_url = dict["image_url"],
            _product_page_url = dict["product_page_url"], 
            _category = dict["category"], 
            _title = dict["title"], 
            _review_rating = dict["review_rating"], 
            _product_description = dict["product_description"], 
            _universal_product_code = dict["universal_product_code"], 
            _price_excl_tax = dict["price_excl_tax"], 
            _price_incl_tax = dict["price_incl_tax"],
            _availability = dict["availability"],
            )
        return book_obj
