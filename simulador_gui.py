import tkinter as tk
from tkinter import ttk
import customtkinter
import ejercicio_286
from time import perf_counter
from functools import lru_cache
import cProfile
import pstats
import csv


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "dark-blue"
)  # Themes: "blue" (standard), "green", "dark-blue"

FILENAME = "data_table.csv"


class Table(tk.Frame):
    def __init__(self, parent, columns):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.columns = columns
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        # Add columns to the treeview
        for col in columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=100, anchor=tk.CENTER)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.pack(expand=True, fill="both")

    def insert_row(self, row):
        self.tree.insert("", "end", values=row)

    # def insert_multiple_rows(self, rows):
    #     for row in rows:
    #         self.tree.insert("", "end", values=row)

    def insert_multiple_rows(self):
        with open(FILENAME, "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader[1:]:
                self.tree.insert("", "end", values=row)

    def clear_table(self):
        self.tree.delete(*self.tree.get_children())


class EditableMatrix2(tk.Toplevel):
    def __init__(self, parent, matrix, update_callback, matrix_num):
        super().__init__(parent)
        self.title("Pr Condición de Alta")

        self.matrix = matrix
        self.update_callback = update_callback
        self.matrix_num = matrix_num
        self.entries = []

        # Add labels for column names
        for j, col_name in enumerate(["Buena", "Regular", "Crítica"]):
            col_label = customtkinter.CTkLabel(
                self,
                text=col_name,
                text_color="black",
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )
            col_label.grid(row=0, column=j + 1, padx=5, pady=5)

        # Add labels for row names and entry widgets
        for i, row_name in enumerate(["Mejorada", "No Mejorada", "Muerto"]):
            row_label = customtkinter.CTkLabel(
                self,
                text=row_name,
                text_color="black",
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )
            row_label.grid(row=i + 1, column=0, padx=5, pady=5)

            row_entries = []
            for j in range(len(matrix[0])):
                entry = customtkinter.CTkEntry(self)
                entry.grid(row=i + 1, column=j + 1, padx=5, pady=5)
                entry.insert(0, matrix[i][j])
                row_entries.append(entry)
            self.entries.append(row_entries)

        apply_button = customtkinter.CTkButton(
            self, text="Apply", command=self.apply_changes
        )
        apply_button.grid(
            row=len(matrix) + 1, columnspan=len(matrix[0]) + 1, padx=5, pady=10
        )

    def apply_changes(self):
        try:
            updated_matrix = [
                [float(entry.get()) for entry in row] for row in self.entries
            ]
            self.update_callback(updated_matrix, self.matrix_num)
            self.destroy()
        except ValueError:
            tk.messagebox.showerror(
                "Error", "Invalid input. Please enter numeric values."
            )


class MatrixInput(tk.Toplevel):
    def __init__(self, parent, matrix, update_callback, matrix_num):
        super().__init__(parent)
        self.title("Modificar Probabilidades")

        self.matrix = matrix
        self.update_callback = update_callback
        self.matrix_num = matrix_num
        self.entries = []

        # Add column names
        for j, col_name in enumerate(["Buena", "Regular", "Crítica", "Alta"]):
            col_label = customtkinter.CTkLabel(
                self,
                text=col_name,
                text_color="black",
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )
            col_label.grid(row=0, column=j + 1, padx=5, pady=5)

        # Add row names and entry widgets
        for i, row_name in enumerate(["Buena", "Regular", "Crítica"]):
            row_label = customtkinter.CTkLabel(
                self,
                text=row_name,
                text_color="black",
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )
            row_label.grid(row=i + 1, column=0, padx=5, pady=5)

            row_entries = []
            for j in range(len(matrix[0])):
                entry = customtkinter.CTkEntry(self)
                entry.grid(row=i + 1, column=j + 1, padx=5, pady=5)
                entry.insert(0, matrix[i][j])
                row_entries.append(entry)
            self.entries.append(row_entries)

        apply_button = customtkinter.CTkButton(
            self, text="Apply", command=self.apply_changes
        )
        apply_button.grid(
            row=len(matrix) + 1, columnspan=len(matrix[0]) + 1, padx=5, pady=10
        )

    def apply_changes(self):
        try:
            updated_matrix = [
                [float(entry.get()) for entry in row] for row in self.entries
            ]
            self.update_callback(updated_matrix, self.matrix_num)
            self.destroy()
        except ValueError:
            tk.messagebox.showerror(
                "Error", "Invalid input. Please enter numeric values."
            )


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simulador - Ejercicio 286")
        self.geometry(f"{1100}x{750}")

        self.grid_columnconfigure((0), weight=0)
        self.grid_columnconfigure((1, 2, 3, 4, 5), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((3, 4, 5), weight=0)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=250, corner_radius=5)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, columnspan=2, sticky="nsew")

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Probabilidades",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=(80, 50), pady=(10, 0))

        self.main_frame = customtkinter.CTkFrame(self.sidebar_frame)
        self.main_frame.grid(
            row=1, column=0, padx=(20, 0), columnspan=4, pady=(10, 0), sticky="nsew"
        )
        self.matrix = [
            [0.2, 0.2, 0.05, 0.1],
            [0.7, 0.5, 0.6, 0.4],
            [0.2, 0.25, 0.2, 0.04],
        ]

        self.create_static_matrix()

        edit_button = customtkinter.CTkButton(
            self.main_frame,
            text="Editar Probabilidades",
            command=self.open_matrix_input,
        )
        edit_button.grid(padx=10, pady=10, columnspan=2)
        self.matrix2 = [
            [round(6 / 22, 3), round(3 / 22, 3), round(1 / 22, 3)],
            [round(3 / 22, 3), round(2 / 22, 3), round(1 / 22, 3)],
            [round(1 / 22, 3), round(3 / 22, 3), round(2 / 22, 3)],
        ]
        # self.matrix2 = [
        #     [1, 2, 3],
        #     [4, 5, 6],
        #     [7, 8, 9],
        # ]
        self.static_matrix_frame = customtkinter.CTkFrame(self.sidebar_frame)
        self.static_matrix_frame.grid(
            row=4, column=0, padx=(20, 0), columnspan=4, pady=(20, 0), sticky="nsew"
        )
        self.create_static_matrix2()

        # FRAME DE ITERACIONES
        self.iteraciones_frame = customtkinter.CTkFrame(
            self.sidebar_frame, fg_color="transparent"
        )
        self.iteraciones_frame.grid(
            row=5, column=0, padx=(0, 0), columnspan=4, pady=(20, 0), sticky="nsew"
        )

        self.iteraciones_label = customtkinter.CTkLabel(
            self.iteraciones_frame, text="Iteraciones:", text_color="white"
        )
        self.iteraciones_label.grid(row=1, column=0, padx=(40, 20), pady=20)

        self.entry = customtkinter.CTkEntry(
            self.iteraciones_frame,
            textvariable=tk.StringVar(self.iteraciones_frame, value=10),
        )
        self.entry.grid(row=1, column=2)

        self.start_simulation_button = customtkinter.CTkButton(
            master=self.iteraciones_frame,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            text="Simular",
            command=self.run_simulation,
        )
        self.start_simulation_button.grid(row=2, column=2)

        # TABLA DE DATOS
        columns = [
            "Día",
            "RND",
            "Condición",
            "Condición Siguiente",
            "RND Alta",
            "Condición Alta",
        ]

        self.table_frame = customtkinter.CTkFrame(self)
        self.table_frame.grid(
            row=0, column=2, columnspan=4, rowspan=6, padx=(20, 0), sticky="nsew"
        )
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_label = customtkinter.CTkLabel(
            self.table_frame, text="Tabla de Simulación"
        )
        self.table_label.pack()

        self.simulation_table = Table(self.table_frame, columns)
        self.simulation_table.pack(expand=True, fill="both")

        self.vector_temp = [0, 0, "", "", 0, ""]
        self.simulation_table.insert_row(self.vector_temp)

    def create_static_matrix(self):
        # Add column names
        for j, col_name in enumerate(["Buena", "Regular", "Crítica", "Alta"]):
            col_label = customtkinter.CTkLabel(self.main_frame, text=col_name)
            col_label.grid(row=0, column=j + 1, padx=5, pady=5)

        # Add row names and entry widgets
        for i, row_name in enumerate(["Buena", "Regular", "Crítica"]):
            row_label = customtkinter.CTkLabel(self.main_frame, text=row_name)
            row_label.grid(row=i + 1, column=0, padx=5, pady=5)

        for i, row in enumerate(self.matrix):
            for j, value in enumerate(row):
                label = customtkinter.CTkLabel(self.main_frame, text=value)
                label.grid(row=i + 1, column=j + 1, padx=15, pady=5)

    def open_matrix_input(self):
        matrix_input_window = MatrixInput(
            self, self.matrix, self.update_matrix, matrix_num=1
        )

    def update_matrix(self, new_matrix, matrix_num):
        if matrix_num == 1:
            self.matrix = new_matrix
            self.clear_static_matrix()
            self.create_static_matrix()
        elif matrix_num == 2:
            self.matrix2 = new_matrix
            self.clear_static_matrix2()
            self.create_static_matrix2()

    def clear_static_matrix(self):
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, customtkinter.CTkLabel):
                widget.grid_forget()

    def create_static_matrix2(self):

        # Add labels for column names
        for j, col_name in enumerate(["Buena", "Regular", "Crítica"]):
            col_label = customtkinter.CTkLabel(self.static_matrix_frame, text=col_name)
            col_label.grid(row=0, column=j + 1, padx=5, pady=5)

        # Add labels for row names and matrix values
        for i, row_name in enumerate(["Mejorada", "No Mejorada", "Muerto"]):
            row_label = customtkinter.CTkLabel(self.static_matrix_frame, text=row_name)
            row_label.grid(row=i + 1, column=0, padx=5, pady=5)

            for j, value in enumerate(self.matrix2[i]):
                value_label = customtkinter.CTkLabel(
                    self.static_matrix_frame, text=value
                )
                value_label.grid(row=i + 1, column=j + 1, padx=5, pady=5)

        edit_button2 = customtkinter.CTkButton(
            self.static_matrix_frame,
            text="Editar Pr de Alta",
            command=self.open_matrix_input2,
        )
        edit_button2.grid(padx=10, pady=10, columnspan=2)

    def open_matrix_input2(self):
        matrix_input_window2 = EditableMatrix2(
            self, self.matrix2, self.update_matrix, matrix_num=2
        )

    def clear_static_matrix2(self):
        for widget in self.static_matrix_frame.winfo_children():
            widget.grid_forget()

    def run_simulation(self):
        start = perf_counter()
        self.simulation_table.clear_table()
        # pr_tuple_1 = tuple(tuple(lst) for lst in self.matrix)
        # pr_tuple_2 = tuple(tuple(lst) for lst in self.matrix2)
        ejercicio_286.start_simulation(
            pr_en_hospital=self.matrix,
            pr_cond_alta=self.matrix2,
            iter=int(self.entry.get()),
        )
        self.simulation_table.insert_multiple_rows()

        end = perf_counter()
        print(f"Esta funcion demora {end-start} segundos")


if __name__ == "__main__":
    app = App()
    cProfile.run("app.mainloop()", "profile_results", sort={"cumulative"})
    profile_data = pstats.Stats("profile_results")
    profile_data.strip_dirs().sort_stats("cumulative").print_stats(20)
