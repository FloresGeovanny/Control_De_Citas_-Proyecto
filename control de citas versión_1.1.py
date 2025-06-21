import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Sistema de Citas de un Hospital")
        self.attributes("-fullscreen")
        self.registros = []  # Lista de registros guardados

        self.create_sidebar()
        self.create_main_area()

    def create_sidebar(self):
        """ Crea la barra lateral con botones de navegación. """
        self.sidebar = tk.Frame(self, width=200, bg="#158d9b")
        self.sidebar.pack(side="left", fill="y")

        buttons = ["Inicio", "Registro de paciente y doctor", "Asignar camilla"]

        for name in buttons:
            btn = tk.Button(self.sidebar, text=name, bg="#34495e", fg="white",
                            relief="flat", command=lambda n=name: self.show_frame(n))
            btn.pack(fill="x", pady=2, padx=5)

    def create_main_area(self):
        """ Crea el área principal con diferentes vistas. """
        self.frames = {}
        container = tk.Frame(self, bg="white")
        container.pack(side="right", fill="both", expand=True)

        for name in ["Inicio", "Registro de paciente y doctor", "Asignar camilla"]:
            frame = tk.Frame(container, bg="white")
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame

        self.create_registro_frame(self.frames["Registro de paciente y doctor"])
        self.create_asignar_camilla_frame(self.frames["Asignar camilla"])

        self.show_frame("Inicio")

    def create_registro_frame(self, frame):
        """ Crea la vista de registro de pacientes y médicos. """
        tk.Label(frame, text="Datos del Doctor", bg="white", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 5))
        self.create_label_entry(frame, "Nombre del Doctor:", "doc_nombre", 1)
        self.create_label_entry(frame, "Especialidad:", "doc_especialidad", 2)

        tk.Label(frame, text="Datos del Paciente", bg="white", font=("Arial", 14, "bold")).grid(row=3, column=0, columnspan=2, pady=(15, 5))
        self.create_label_entry(frame, "Nombre:", "pac_nombre", 4)
        self.create_label_entry(frame, "Apellidos:", "pac_apellidos", 5)
        self.create_label_entry(frame, "Enfermedad:", "pac_enfermedad", 6)
        self.create_label_entry(frame, "No. Seguro Social:", "pac_seguro", 7)

        btn_registrar = tk.Button(frame, text="Registrar", bg="#158d9b", fg="white",
                                  font=("Arial", 12), command=self.registrar)
        btn_registrar.grid(row=8, column=0, columnspan=2, pady=15)

    def create_label_entry(self, frame, text, var_name, row):
        """ Crea etiquetas y campos de entrada. """
        tk.Label(frame, text=text, bg="white", font=("Arial", 12)).grid(row=row, column=0, padx=20, sticky="w")
        entry = tk.Entry(frame, font=("Arial", 12))
        entry.grid(row=row, column=1, padx=20, pady=3, sticky="ew")
        setattr(self, f"entry_{var_name}", entry)

    def registrar(self):
        """ Registra los datos de un paciente con su doctor. """
        data = {
            "doctor_nombre": self.entry_doc_nombre.get().strip(),
            "doctor_especialidad": self.entry_doc_especialidad.get().strip(),
            "paciente_nombre": self.entry_pac_nombre.get().strip(),
            "paciente_apellidos": self.entry_pac_apellidos.get().strip(),
            "paciente_enfermedad": self.entry_pac_enfermedad.get().strip(),
            "paciente_seguro": self.entry_pac_seguro.get().strip(),
            "camilla": "Sin asignar"
        }

        if any(not val for val in data.values()):
            messagebox.showwarning("Campos vacíos", "Por favor, llena todos los campos.")
            return

        self.registros.append(data)
        self.limpiar_campos_registro()
        self.actualizar_tabla_pacientes()
        messagebox.showinfo("Registro exitoso", "Paciente registrado correctamente.")

    def limpiar_campos_registro(self):
        """ Limpia los campos tras registrar. """
        for var_name in ["doc_nombre", "doc_especialidad", "pac_nombre", "pac_apellidos", "pac_enfermedad", "pac_seguro"]:
            getattr(self, f"entry_{var_name}").delete(0, tk.END)

    def create_asignar_camilla_frame(self, frame):
        """ Vista para asignar camilla y mostrar tabla. """
        tk.Label(frame, text="Asignar Camilla a Paciente", bg="white", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(frame, text="Seleccione paciente:", bg="white", font=("Arial", 12)).pack(pady=5)

        self.combo_pacientes = ttk.Combobox(frame, state="readonly", font=("Arial", 12))
        self.combo_pacientes.pack(pady=5, padx=20, fill="x")

        self.entry_camilla = tk.Entry(frame, font=("Arial", 12))
        self.entry_camilla.pack(pady=5, padx=20, fill="x")

        btn_asignar = tk.Button(frame, text="Asignar Camilla", bg="#158d9b", fg="white",
                                font=("Arial", 12), command=self.asignar_camilla)
        btn_asignar.pack(pady=20)

        self.table = ttk.Treeview(frame, columns=("Doctor", "Especialidad", "Nombre", "Apellidos", "Enfermedad", "Camilla"), show="headings")
        for col in ("Doctor", "Especialidad", "Nombre", "Apellidos", "Enfermedad", "Camilla"):
            self.table.heading(col, text=col)
        self.table.pack(pady=20, padx=20, fill="both", expand=True)

        self.actualizar_tabla_pacientes()

    def asignar_camilla(self):
        """ Asigna camilla a un paciente. """
        paciente_seleccionado = self.combo_pacientes.get()
        camilla_asignada = self.entry_camilla.get().strip()

        if not paciente_seleccionado or not camilla_asignada:
            messagebox.showwarning("Error", "Seleccione un paciente e ingrese una camilla.")
            return

        for r in self.registros:
            if f"{r['paciente_nombre']} {r['paciente_apellidos']}" == paciente_seleccionado:
                r["camilla"] = camilla_asignada

        self.actualizar_tabla_pacientes()

    def actualizar_tabla_pacientes(self):
        """ Actualiza la tabla con registros. """
        self.table.delete(*self.table.get_children())
        self.combo_pacientes["values"] = []

        for r in self.registros:
            self.table.insert("", "end", values=(
                r["doctor_nombre"], r["doctor_especialidad"], r["paciente_nombre"],
                r["paciente_apellidos"], r["paciente_enfermedad"], r["camilla"]
            ))

        self.combo_pacientes["values"] = [
            f"{r['paciente_nombre']} {r['paciente_apellidos']}" for r in self.registros
        ]

    def show_frame(self, name):
        self.frames[name].tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
