from urllib.parse import urlsplit


def row_to_dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


def get_url_base(url: str) -> str:

    scheme, netlock, _, _, _ = urlsplit(url)

    return '{}://{}'.format(scheme, netlock)
