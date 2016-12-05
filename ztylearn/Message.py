class Message:
    def __init__(self, user, id, title, date, detail):
        self.title = title.strip()
        self.date = date
        self.user = user
        self.id = id
        self.detail = detail


    @property
    async def dict(self):
        d = self.__dict__.copy()
        d["detail"] = await self.detail
        del d['user']
        return d