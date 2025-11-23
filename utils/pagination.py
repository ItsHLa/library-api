class Paginator:
    def __init__(self, page_size, items, page= 1) -> None:

        self.page = int(page)
        self.page_size = int(page_size)
        self.items = items
        self.len = items.count()
        self.total_page = self.len / self.page_size
        self.start = (self.page - 1) * self.page_size
        self.end = self.start +self.page_size
        
    def paginate(self):
        query = self.items[self.start:self.end]
        data = {
            'total_pages' : self.total_page,
            'current_page' : self.page,
            # 'offset' : self.start,
            'limit' : self.page_size,
            'remain' : self.total_page - self.page,
            'count' : self.len }
        return query, data