class BookRequest:
    def __init__(self, request):
        self.author_id = request.json["author_id"]
        self.title = request.json["title"]
        self.year = request.json["year"]

    def __str__(self):
        return "author_id: {0}, title: {1}, year: {2}".format(self.author_id, self.title, self.year)
