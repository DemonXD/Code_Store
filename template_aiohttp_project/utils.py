def row2dict(item):
    d = {}
    for column in item.__table__.columns:
        d[column.name] = str(getattr(item, column.name))
    return d