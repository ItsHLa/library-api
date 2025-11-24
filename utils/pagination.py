class Paginator:
    def __init__(self, page_size, items, page= 1) -> None:

        self.page = int(page)
        self.page_size = int(page_size)
        self.items = items
        self.len = items.count()
        print(round(self.len / self.page_size))
        self.total_page = max(round(self.len / self.page_size), 1)
        self.start = (self.page - 1) * self.page_size
        self.end = self.start +self.page_size
        
    def paginate(self):
        query = self.items[self.start:self.end]
        data = {
            'total_pages' : self.total_page,
            'current_page' : self.page,
            # 'offset' : self.start,
            'limit' : self.page_size,
            'remain' : max(self.total_page - self.page, 0),
            'count' : self.len }
        return query, data