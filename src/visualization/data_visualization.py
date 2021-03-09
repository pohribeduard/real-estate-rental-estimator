import matplotlib.pyplot as plt
import pandas as pd

from src.models.residences import Residences


def plot_surface_and_rental_price():
    residence_table = Residences()
    residences = residence_table.get_residences(100000)

    residences_df = pd.DataFrame(residences)
    plt.figure()
    plt.scatter(residences_df['livable_area'], residences_df['price'], s=15, edgecolor="black", c="darkorange",
                label="surface")
    plt.xlabel("Surface Area")
    plt.ylabel("Rental Price")
    plt.title("Surface Area vs. Rental Price")
    plt.legend()
    plt.show()


def plot_surface_vs_price_per_sq_meter():
    residence_table = Residences()
    residences = residence_table.get_residences(100000)

    residences_df = pd.DataFrame(residences)
    plt.figure()
    plt.scatter(residences_df['livable_area'], residences_df['price']/residences_df['livable_area'], s=15,
                edgecolor="black", c="darkorange", label="surface")
    plt.xlabel("Surface Area")
    plt.ylabel("Rental Price Per Sq Meter")
    plt.title("Surface Area vs. Rental Price Per Sq Meter")
    plt.legend()
    plt.show()


def plot_rooms_vs_price():
    residence_table = Residences()
    residences = residence_table.get_residences(100000)

    residences_df = pd.DataFrame(residences)
    residences_df = residences_df[residences_df.rooms.notnull()]
    plt.figure()
    plt.scatter(residences_df['rooms'], residences_df['price'], s=15, edgecolor="black", c="darkorange",
                label="bedrooms")
    plt.xlabel("Bedrooms")
    plt.ylabel("Rental Price")
    plt.title("Bedrooms vs. House Price")
    plt.legend()
    plt.show()
