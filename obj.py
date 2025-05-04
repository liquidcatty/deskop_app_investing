### create in this file objects for use like labels, buttons etd ###
from read_stoq import StoqInfo
import tkinter as tk


class TableWithInfoAboutStoq:
    def __init__(self, stock_code="AAPL", start="2020-01-01", end="2024-12-31"):
        stoq = StoqInfo()