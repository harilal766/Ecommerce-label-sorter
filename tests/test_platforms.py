from label_sorter.platforms.ecommerce.base_label import BaseLabel
from label_sorter.platforms.ecommerce.amazon import AmazonLabel


class TestBaseLabel:
    base_label_inst = BaseLabel()
    def test_page():
        pass
    
    def get_pages_for_testing():
        pass

class TestAmazonLabel:
    amazon_pages = 0
    single_item_page = 0
    mixed_items_page = 0
    amzn_label_instance = AmazonLabel()


