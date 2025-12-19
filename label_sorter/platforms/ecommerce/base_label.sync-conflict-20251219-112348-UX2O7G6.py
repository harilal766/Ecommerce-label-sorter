

class BaseLabel:
    def __init__(self, page_text, page_table, page_num = None):
        self.page_debrief_dict = {
            "order_id" : None, "items" : []
        }
        self.page_text = page_text
        self.page_table = page_table
        self.page_number = page_num
    