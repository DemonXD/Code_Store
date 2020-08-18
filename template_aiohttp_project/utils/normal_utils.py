import asyncio

def row2dict(item):
    """
        for sqlalchemy model instance
        return a {column name:value } dict 
    """
    d = {}
    for column in item.__table__.columns:
        d[column.name] = str(getattr(item, column.name))
    return d


class PubSubChannel:
    def __init__(self):
        self.list = []

    def add(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
        else:
            print(f"{observer} Existed!")
    def remove(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            print(f"Failed to remove {observer}")
    def notify(self):
        pass
