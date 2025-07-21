import pandas as pd

from helpers import Model


class Stats:

    STATS = "../connections_stats.csv"
    def __init__(self):
        self.sheet = pd.read_csv("../connections_stats.csv")


        #MODEL, GUESS -> GUESS -> CORRECT/GUESSES


    # def write_model(self):







