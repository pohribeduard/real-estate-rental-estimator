import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import numpy as np
import math

from src.models.residences import Residences


def plot_surface_and_rental_price():
    residence_table = Residences()
    residences = residence_table.get_all_residences()

    residences_df = pd.DataFrame(residences)
    residences_df = residences_df[residences_df.livable_area.notnull()]
    plt.figure()
    plt.style.use('ggplot')
    plt.scatter(residences_df['livable_area'], residences_df['price'], s=15, edgecolor="black", c="darkorange")
    plt.xlabel("Suprafața locuibilă")
    plt.ylabel("Prețului chiriei lunare")
    plt.title("Suprafața locuibilă / Prețului chiriei lunare")
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
    plt.style.use('ggplot')
    plt.scatter(livable_area, price_per_sq_meter, s=15,
                edgecolor="black", c="darkorange")
    plt.xlabel("Suprafața locuibilă")
    plt.ylabel("Prețul pe metrul pătrat")
    plt.title("Suprafața locuibilă / Suprafața locuibilă")
    plt.legend()
    plt.show()


def plot_rooms_vs_price():
    residence_table = Residences()
    residences = residence_table.get_all_residences()

    residences_df = pd.DataFrame(residences)
    residences_df = residences_df[residences_df.rooms.notnull()]
    plt.figure()
    plt.style.use('ggplot')
    plt.scatter(residences_df['rooms'], residences_df['price'], s=15, edgecolor="black", c="darkorange")
    plt.xlabel("Număr camere")
    plt.ylabel("Prețului chiriei lunare")
    plt.title("Număr camere / Prețului chiriei lunare")
    plt.legend()
    plt.show()


def normal_distribution():
    residence_table = Residences()
    # residences = residence_table.get_residences(5000)
    residences = residence_table.get_all_residences()

    residences_df = pd.DataFrame(residences)
    prices = residences_df['price']
    standard_deviation = prices.std()

    mu = prices.mean()
    variance = prices.var()
    sigma = math.sqrt(variance)
    x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 50)

    plt.style.use('ggplot')
    plt.plot(x, stats.norm.pdf(x, mu, sigma))
    plt.title('Distribuția normală a prețurilor')
    plt.xlabel('Prețul chiriei lunare')
    plt.ylabel('Probabilitatea de densitate')
    plt.suptitle('Valoarea medie: ' + str(round(mu, 2)) + '\nDeviația standard: ' + str(round(standard_deviation, 2)),
                 x=0.75, y=0.85, fontsize=10)
    plt.show()
