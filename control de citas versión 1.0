import tkinter as tk
from tkinter import messagebox

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Sistema de Citas - Registro")
        self.attributes("-fullscreen")
        self.registros = []

        self.create_sidebar()
        self.create_registro_area()

    def create_sidebar(self):
        self.sidebar = tk.Frame(self, width=200, bg="#158d9b")
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="Registro", bg="#158d9b", fg="white",
                 font=("Arial", 16, "bold")).pack(pady=20)

    def create_registro_area(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(side="right", fill="both", expand=True)

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
        tk.Label(frame, text=text, bg="white", font=("Arial", 12)).grid(row=row, column=0, padx=20, sticky="w")
        entry = tk.Entry(frame, font=("Arial", 12))
        entry.grid(row=row, column=1, padx=20, pady=3, sticky="ew")
        setattr(self, f"entry_{var_name}", entry)

    def registrar(self):
        data = {
            "doctor_nombre": self.entry_doc_nombre.get().strip(),
            "doctor_especialidad": self.entry_doc_especialidad.get().strip(),
            "paciente_nombre": self.entry_pac_nombre.get().strip(),
            "paciente_apellidos": self.entry_pac_apellidos.get().strip(),
            "paciente_enfermedad": self.entry_pac_enfermedad.get().strip(),
            "paciente_seguro": self.entry_pac_seguro.get().strip()
        }

        if any(not val for val in data.values()):
            messagebox.showwarning("Campos vacíos", "Por favor, llena todos los campos.")
            return

        self.registros.append(data)
        self.limpiar_campos()
        messagebox.showinfo("Registro exitoso", "Paciente registrado correctamente.")

    def limpiar_campos(self):
        for var_name in ["doc_nombre", "doc_especialidad", "pac_nombre", "pac_apellidos", "pac_enfermedad", "pac_seguro"]:
            getattr(self, f"entry_{var_name}").delete(0, tk.END)

if __name__ == "__main__":
    app = App()
    app.mainloop()
