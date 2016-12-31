class Message:
    def __init__(self, user, id, title, date, detail, author):
        self.title = title.strip()
        self.date = date
        self.user = user
        self.id = id
        self.detail = detail
        self.author = author
