import matplotlib.pyplot as plt
import pandas as pd

from src.models.residences import Residences


def plot_surface_and_rental_price():
    residence_table = Residences()
    residences = residence_table.get_all_residences()

    residences_df = pd.DataFrame(residences)
    residences_df = residences_df[residences_df.livable_area.notnull()]
    plt.figure()
    plt.scatter(residences_df['livable_area'], residences_df['price'], s=15, edgecolor="black", c="darkorange",
                label="surface")
    plt.xlabel("Suprafata locuibila")
    plt.ylabel("Pretului chiriei lunare")
    plt.title("Suprafata locuibila vs. Pretului chiriei lunare")
    plt.legend()
    plt.show()


def plot_surface_vs_price_per_sq_meter():
    residence_table = Residences()
    residences = residence_table.get_all_residences()

    residences_df = pd.DataFrame(residences)
    residences_df = residences_df[residences_df.livable_area.notnull()]
    residences_df = residences_df[residences_df.livable_area > 0]
    livable_area = residences_df['livable_area']
    price_per_sq_meter = residences_df['price']/residences_df['livable_area']

    plt.figure()
    plt.scatter(livable_area, price_per_sq_meter, s=15,
                edgecolor="black", c="darkorange", label="surface")
    plt.xlabel("Suprafata locuibila")
    plt.ylabel("Pretul pe metru patrat")
    plt.title("Suprafata locuibila vs. Pretul pe metru patrat")
    plt.legend()
    plt.show()


def plot_rooms_vs_price():
    residence_table = Residences()
    residences = residence_table.get_all_residences()

    residences_df = pd.DataFrame(residences)
    residences_df = residences_df[residences_df.rooms.notnull()]
    plt.figure()
    plt.scatter(residences_df['rooms'], residences_df['price'], s=15, edgecolor="black", c="darkorange",
                label="bedrooms")
    plt.xlabel("Numar camere")
    plt.ylabel("Pretului chiriei lunare")
    plt.title("Numar camere vs. Pretului chiriei lunare")
    plt.legend()
    plt.show()
