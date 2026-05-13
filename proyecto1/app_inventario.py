"""
Sistema de Gestión de Inventario para Refaccionaria
Desarrollado con arquitectura MVC, Clean Code y principios SOLID.
Autor: Arquitecto de Software Senior
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from typing import List, Optional, Dict

# ==========================================
# 1. MODELO (Lógica de Datos)
# ==========================================

class Product:
    """
    Clase que representa un producto (refacción).
    Usa Type Hinting para asegurar la integridad de los datos.
    """
    def __init__(self, code: str, name: str, quantity: int, price: float):
        self.code: str = code
        self.name: str = name
        self.quantity: int = quantity
        self.price: float = price

    def to_dict(self) -> Dict:
        """Convierte el objeto a diccionario para facilitar la escritura en CSV."""
        return {
            "code": self.code,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price
        }

class InventoryModel:
    """
    Gestiona la persistencia de datos en archivos locales CSV.
    Asegura que las operaciones de lectura/escritura sean seguras.
    """
    def __init__(self, filename: str = "inventario.csv"):
        self.filename: str = filename
        self.products: List[Product] = []
        self._load_from_csv()

    def _load_from_csv(self) -> None:
        """Carga los datos del archivo CSV al iniciar la aplicación."""
        if not os.path.exists(self.filename):
            # Crea el archivo con cabeceras si no existe
            self.save_to_csv()
            return
        
        try:
            with open(self.filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.products = [
                    Product(row['code'], row['name'], int(row['quantity']), float(row['price']))
                    for row in reader
                ]
        except Exception as e:
            print(f"Error al cargar datos: {e}")

    def save_to_csv(self) -> None:
        """Guarda la lista actual de productos en el archivo CSV."""
        try:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ["code", "name", "quantity", "price"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for prod in self.products:
                    writer.writerow(prod.to_dict())
        except Exception as e:
            print(f"Error al guardar datos: {e}")

    def add_product(self, product: Product) -> bool:
        """Agrega un producto si el código no existe previamente."""
        if any(p.code == product.code for p in self.products):
            return False
        self.products.append(product)
        self.save_to_csv()
        return True

    def update_product(self, updated_prod: Product) -> bool:
        """Busca un producto por código y actualiza sus valores."""
        for i, p in enumerate(self.products):
            if p.code == updated_prod.code:
                self.products[i] = updated_prod
                self.save_to_csv()
                return True
        return False

    def delete_product(self, code: str) -> bool:
        """Elimina un producto del sistema."""
        original_size = len(self.products)
        self.products = [p for p in self.products if p.code != code]
        if len(self.products) < original_size:
            self.save_to_csv()
            return True
        return False

# ==========================================
# 2. VISTA (Interfaz Gráfica de Usuario)
# ==========================================

class InventoryView(tk.Tk):
    """
    Define la estructura visual de la aplicación.
    Utiliza ttk para un aspecto moderno y profesional.
    """
    def __init__(self):
        super().__init__()
        self.title("Refaccionaria - Sistema de Control de Inventario")
        self.geometry("1100x650")
        self.configure(bg="#f4f7f6") # Fondo gris claro moderno

        # --- CONFIGURACIÓN DE ESTILOS ---
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Paleta de colores: Azul Medianoche (#1a2a6c), Gris Oscuro (#333), Blanco
        self.style.configure("TFrame", background="#f4f7f6")
        self.style.configure("Header.TLabel", font=("Helvetica", 18, "bold"), foreground="#1a2a6c", background="#f4f7f6")
        self.style.configure("Sidebar.TFrame", background="#ffffff", relief="flat")
        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#1a2a6c", foreground="white")
        self.style.map("Treeview.Heading", background=[('active', '#2a3a7c')])
        
        # Botones Personalizados
        self.style.configure("Action.TButton", font=("Helvetica", 10, "bold"), padding=8)
        self.style.configure("Delete.TButton", font=("Helvetica", 10, "bold"), background="#b21f1f", foreground="white")

        self._build_ui()

    def _build_ui(self) -> None:
        """Organiza los componentes en la ventana principal usando Grid y Pack."""
        
        # Título Superior
        header_label = ttk.Label(self, text="SISTEMA DE GESTIÓN DE REFACCIONES", style="Header.TLabel")
        header_label.pack(pady=20)

        # Contenedor Principal (Cuerpo)
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=20, pady=10)

        # --- PANEL LATERAL (FORMULARIO) ---
        self.sidebar = ttk.Frame(container, style="Sidebar.TFrame", padding=20)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        ttk.Label(self.sidebar, text="Registro de Pieza", font=("Helvetica", 12, "bold"), background="white").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Campos de Entrada
        fields = [("Código:", "code"), ("Nombre:", "name"), ("Stock:", "qty"), ("Precio ($):", "price")]
        self.entries = {}

        for i, (label_text, key) in enumerate(fields):
            ttk.Label(self.sidebar, text=label_text, background="white").grid(row=i+1, column=0, sticky="w", pady=8)
            entry = ttk.Entry(self.sidebar, font=("Helvetica", 10), width=25)
            entry.grid(row=i+1, column=1, pady=8, padx=5)
            self.entries[key] = entry

        # Botonera Lateral
        self.btn_add = ttk.Button(self.sidebar, text="✚ Agregar", style="Action.TButton")
        self.btn_add.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(20, 5))

        self.btn_update = ttk.Button(self.sidebar, text="🗘 Actualizar", style="Action.TButton")
        self.btn_update.grid(row=6, column=0, columnspan=2, sticky="ew", pady=5)

        self.btn_clear = ttk.Button(self.sidebar, text="🧹 Limpiar Campos")
        self.btn_clear.grid(row=7, column=0, columnspan=2, sticky="ew", pady=5)

        self.btn_delete = ttk.Button(self.sidebar, text="🗑 Eliminar Selección", style="Action.TButton")
        self.btn_delete.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(30, 0))

        # --- PANEL CENTRAL (TABLA Y BÚSQUEDA) ---
        right_panel = ttk.Frame(container)
        right_panel.grid(row=0, column=1, sticky="nsew")
        container.columnconfigure(1, weight=1)

        # Barra de Búsqueda
        search_frame = ttk.Frame(right_panel)
        search_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(search_frame, text="🔍 Buscar por nombre o código:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Tabla (Treeview) con Scrollbars
        table_container = ttk.Frame(right_panel)
        table_container.pack(fill="both", expand=True)

        columns = ("code", "name", "qty", "price")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="browse")
        
        # Configuración de Columnas
        self.tree.heading("code", text="CÓDIGO")
        self.tree.heading("name", text="NOMBRE DE PRODUCTO")
        self.tree.heading("qty", text="STOCK")
        self.tree.heading("price", text="PRECIO UNIT.")

        self.tree.column("code", width=120, anchor="center")
        self.tree.column("name", width=350)
        self.tree.column("qty", width=80, anchor="center")
        self.tree.column("price", width=100, anchor="center")

        # Scrollbar Vertical
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def get_form_values(self) -> Optional[Product]:
        """Extrae y valida los datos de los formularios."""
        try:
            code = self.entries["code"].get().strip()
            name = self.entries["name"].get().strip()
            qty_str = self.entries["qty"].get().strip()
            price_str = self.entries["price"].get().strip()

            if not all([code, name, qty_str, price_str]):
                messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
                return None

            qty = int(qty_str)
            price = float(price_str)

            if qty < 0 or price < 0:
                raise ValueError("Los valores numéricos deben ser positivos.")

            return Product(code, name, qty, price)

        except ValueError as e:
            messagebox.showerror("Error de Entrada", f"Datos inválidos: {e}\nAsegúrese de usar números en Stock y Precio.")
            return None

    def clear_form(self) -> None:
        """Limpia los campos del panel lateral."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.entries["code"].config(state="normal")

    def fill_form(self, product: Product) -> None:
        """Rellena el formulario con los datos de un producto seleccionado."""
        self.clear_form()
        self.entries["code"].insert(0, product.code)
        self.entries["code"].config(state="readonly")
        self.entries["name"].insert(0, product.name)
        self.entries["qty"].insert(0, product.quantity)
        self.entries["price"].insert(0, product.price)

# ==========================================
# 3. CONTROLADOR (Lógica de Interacción)
# ==========================================

class InventoryController:
    """
    Orquestador que maneja eventos de la vista y actualizaciones del modelo.
    """
    def __init__(self, model: InventoryModel, view: InventoryView):
        self.model = model
        self.view = view

        # Vinculación de Botones
        self.view.btn_add.config(command=self.handle_add)
        self.view.btn_update.config(command=self.handle_update)
        self.view.btn_delete.config(command=self.handle_delete)
        self.view.btn_clear.config(command=self.view.clear_form)

        # Eventos de Selección y Búsqueda
        self.view.tree.bind("<<TreeviewSelect>>", self.handle_row_selection)
        self.view.search_var.trace_add("write", lambda *args: self.handle_search())
        
        # Ordenamiento al hacer clic en encabezados
        for col in ("code", "name", "qty", "price"):
            self.view.tree.heading(col, command=lambda _col=col: self.sort_column(_col, False))

        self.update_table_display()

    def update_table_display(self, products_list: Optional[List[Product]] = None) -> None:
        """Refresca los datos visibles en la tabla Treeview."""
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)
        
        list_to_show = products_list if products_list is not None else self.model.products
        for p in list_to_show:
            self.view.tree.insert("", tk.END, values=(p.code, p.name, p.quantity, f"{p.price:.2f}"))

    def handle_add(self) -> None:
        product = self.view.get_form_values()
        if product:
            if self.model.add_product(product):
                messagebox.showinfo("Éxito", f"Producto {product.code} agregado correctamente.")
                self.update_table_display()
                self.view.clear_form()
            else:
                messagebox.showerror("Error", "El código de pieza ya existe en el sistema.")

    def handle_update(self) -> None:
        product = self.view.get_form_values()
        if product:
            if self.model.update_product(product):
                messagebox.showinfo("Éxito", "Información actualizada correctamente.")
                self.update_table_display()
                self.view.clear_form()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el producto.")

    def handle_delete(self) -> None:
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Selección vacía", "Por favor seleccione un producto de la tabla.")
            return

        item_data = self.view.tree.item(selected[0])
        code = item_data['values'][0]

        confirm = messagebox.askyesno("Confirmación de Seguridad", f"¿Está seguro de eliminar la pieza con código: {code}?\nEsta acción no se puede deshacer.")
        if confirm:
            if self.model.delete_product(code):
                messagebox.showinfo("Eliminado", "Producto borrado del inventario.")
                self.update_table_display()
                self.view.clear_form()

    def handle_row_selection(self, event) -> None:
        """Carga los datos de la fila seleccionada en el formulario para edición."""
        selected = self.view.tree.selection()
        if selected:
            data = self.view.tree.item(selected[0])['values']
            product = Product(str(data[0]), str(data[1]), int(data[2]), float(data[3]))
            self.view.fill_form(product)

    def handle_search(self) -> None:
        """Filtra los productos en tiempo real según el texto de búsqueda."""
        query = self.view.search_var.get().lower()
        filtered = [
            p for p in self.model.products 
            if query in p.name.lower() or query in p.code.lower()
        ]
        self.update_table_display(filtered)

    def sort_column(self, col: str, reverse: bool) -> None:
        """Ordena la tabla al hacer clic en una columna."""
        data = [(self.view.tree.set(k, col), k) for k in self.view.tree.get_children('')]
        
        if col in ("qty", "price"):
            data.sort(key=lambda t: float(t[0]), reverse=reverse)
        else:
            data.sort(reverse=reverse)

        for index, (val, k) in enumerate(data):
            self.view.tree.move(k, '', index)

        self.view.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

# ==========================================
# PUNTO DE ENTRADA
# ==========================================

if __name__ == "__main__":
    inventory_model = InventoryModel()
    inventory_view = InventoryView()
    inventory_controller = InventoryController(inventory_model, inventory_view)
    inventory_view.mainloop()
