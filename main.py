from src.models.ad_locations import AdLocations
from src.models.residences import Residences
from src.visualization.data_visualization import plot_surface_and_rental_price, plot_rooms_vs_price, \
    plot_surface_vs_price_per_sq_meter

# plot_surface_and_rental_price()
# plot_surface_vs_price_per_sq_meter()
# plot_rooms_vs_price()


residence_table = Residences()
residences = residence_table.test_query()
print()