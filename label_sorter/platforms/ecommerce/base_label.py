

class BaseLabel:
    def __init__(self, page_text, page_table):
        self.page_debrief_dict = {
            "order_id" : None, "sorting_key" : None, "qty" : None
        }
        self.page_text = page_text
        self.page_table = page_table
    