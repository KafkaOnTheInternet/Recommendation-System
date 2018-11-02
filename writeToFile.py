import pandas as pd
import numpy as np
from random import randint

excel_file = "movies1.xlsx"
movies = pd.read_excel(excel_file, sheet_name = "scores")

