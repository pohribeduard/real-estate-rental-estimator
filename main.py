from src.models.ad_locations import AdLocations
from src.models.ad_metadata import AdMetadata
from src.models.ads import Ads
from src.models.cities import Cities
from src.models.counties import Counties
from src.models.residences import Residences
from src.models.zones import Zones

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

# or

# row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}


ads = Ads()
smth = ads.test_query()
print()