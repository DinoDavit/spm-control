import tkinter as tk
import ttkbootstrap as ttk

def add_range_input(parent, name):
    row = ttk.Frame(parent, text = 'name')
    row.pack()

    row.pack_propagate(False)

def add_single_entry(parent, name):
    row = ttk.Frame(parent)
    row.pack()

    row.pack_propogate(False)