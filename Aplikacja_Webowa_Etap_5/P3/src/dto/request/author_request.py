class AuthorRequest:
    def __init__(self, request):
        self.name = request.json["name"]
        self.surname = request.json["surname"]

    def __str__(self):
        return "name: {0}, surname: {1}".format(self.name, self.surname)
