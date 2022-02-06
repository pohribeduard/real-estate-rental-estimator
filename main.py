from src.visualization.data_visualization import plot_surface_and_rental_price, plot_surface_vs_price_per_sq_meter, \
    plot_rooms_vs_price, normal_distribution
from src.visualization.result_visualization import result_visualization


# Usefull for plotting infomation about the model
if __name__ == '__main__':
    plot_surface_and_rental_price()
    plot_surface_vs_price_per_sq_meter()
    plot_rooms_vs_price()
    normal_distribution()

    result_visualization()
