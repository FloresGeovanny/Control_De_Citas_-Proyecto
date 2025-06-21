import tkinter as tk
from tkinter import ttk, messagebox


class Persona:
    def __init__(self, nombre, edad=None):
        self.nombre = nombre
        self.edad = edad

class Doctor:
    def __init__(self, nombre, especialidad="General"):
        self.nombre = nombre
        self.especialidad = especialidad

class Paciente(Persona):
    def __init__(self, nombre, edad, enfermedad=None, seguro_social=None, doctor_asignado=None, camilla_asignada="Sin asignar"):
        super().__init__(nombre, edad)
        self.enfermedad = enfermedad
        self.seguro_social = seguro_social
        self.doctor_asignado = doctor_asignado 
        self.camilla_asignada = camilla_asignada 

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Sistema de Citas de un Hospital - V3 (OOP en Registro + Camilla Simple)")
        self.attributes("-fullscreen", True)
        
        
        self.registros = []  

        
        self.doctores_disponibles = [
            Doctor("Dr. Pérez", "Cardiología"),
            Doctor("Dr. Gómez", "Pediatría"),
            Doctor("Dra. Ruiz", "Medicina General")
        ]

        self.create_sidebar()
        self.create_main_area()

    def create_sidebar(self):
        
        self.sidebar = tk.Frame(self, width=200, bg="#158d9b")
        self.sidebar.pack(side="left", fill="y")

        
        buttons = ["Inicio", "Registro de paciente y doctor", "Asignar camilla"]

        for name in buttons:
            btn = tk.Button(self.sidebar, text=name, bg="#34495e", fg="white",
                             relief="flat", command=lambda n=name: self.show_frame(n))
            btn.pack(fill="x", pady=2, padx=5)

    def create_main_area(self):
        
        self.frames = {}
        container = tk.Frame(self, bg="white")
        container.pack(side="right", fill="both", expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for name in ["Inicio", "Registro de paciente y doctor", "Asignar camilla"]:
            frame = tk.Frame(container, bg="white")
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame

        self.create_inicio_frame(self.frames["Inicio"])
        self.create_registro_frame(self.frames["Registro de paciente y doctor"])
        self.create_asignar_camilla_frame(self.frames["Asignar camilla"])

        self.show_frame("Inicio")

    def create_inicio_frame(self, frame):
        
        tk.Label(frame, text="Bienvenido al Sistema de Gestión Hospitalaria",
                 bg="white", font=("Arial", 24, "bold"), fg="#158d9b").pack(pady=50)
        tk.Label(frame, text="Utilice el menú lateral para navegar por las opciones.",
                 bg="white", font=("Arial", 16)).pack(pady=20)
        tk.Label(frame, text="Fecha actual: 20 de junio de 2025",
                 bg="white", font=("Arial", 12)).pack(pady=10)


    def create_registro_frame(self, frame):
        
        frame.columnconfigure(1, weight=1) 

        tk.Label(frame, text="Registro de Paciente y Doctor", bg="white", font=("Arial", 18, "bold"), fg="#34495e").grid(row=0, column=0, columnspan=2, pady=(20, 15))

        
        self.create_label_entry(frame, "Nombre del Paciente:", "pac_nombre", 1)
        self.create_label_entry(frame, "Apellidos del Paciente:", "pac_apellidos", 2)
        self.create_label_entry(frame, "Edad:", "pac_edad", 3)
        self.create_label_entry(frame, "Enfermedad:", "pac_enfermedad", 4)
        self.create_label_entry(frame, "No. Seguro Social:", "pac_seguro", 5)

        
        tk.Label(frame, text="Doctor Asignado:", bg="white", font=("Arial", 12)).grid(row=6, column=0, padx=20, sticky="w")
        self.combo_doctor_registro = ttk.Combobox(frame, 
                                                 values=[d.nombre for d in self.doctores_disponibles], 
                                                 state="readonly", 
                                                 font=("Arial", 12))
        self.combo_doctor_registro.grid(row=6, column=1, padx=20, pady=5, sticky="ew")
        if self.doctores_disponibles:
            self.combo_doctor_registro.set(self.doctores_disponibles[0].nombre) 

        btn_registrar = tk.Button(frame, text="Registrar", bg="#158d9b", fg="white",
                                     font=("Arial", 12), command=self.registrar)
        btn_registrar.grid(row=7, column=0, columnspan=2, pady=15) 

    def create_label_entry(self, frame, text, var_name, row):
        
        tk.Label(frame, text=text, bg="white", font=("Arial", 12)).grid(row=row, column=0, padx=20, sticky="w")
        entry = tk.Entry(frame, font=("Arial", 12))
        entry.grid(row=row, column=1, padx=20, pady=3, sticky="ew")
        setattr(self, f"entry_{var_name}", entry)

    def registrar(self):
        
        nombre = self.entry_pac_nombre.get().strip()
        apellidos = self.entry_pac_apellidos.get().strip()
        edad_str = self.entry_pac_edad.get().strip()
        enfermedad = self.entry_pac_enfermedad.get().strip()
        seguro = self.entry_pac_seguro.get().strip()
        doctor_nombre_seleccionado = self.combo_doctor_registro.get().strip()

        if not all([nombre, apellidos, edad_str, enfermedad, seguro, doctor_nombre_seleccionado]):
            messagebox.showwarning("Campos vacíos", "Por favor, llena todos los campos.")
            return

        try:
            edad = int(edad_str)
            if edad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error de entrada", "La edad debe ser un número entero positivo.")
            return

        doctor_obj = next((d for d in self.doctores_disponibles if d.nombre == doctor_nombre_seleccionado), None)
        if not doctor_obj:
            messagebox.showerror("Error", "Doctor seleccionado no válido.")
            return
            
        
        nuevo_paciente = Paciente(f"{nombre} {apellidos}", edad, enfermedad, seguro, doctor_obj)
        self.registros.append(nuevo_paciente)

        self.limpiar_campos_registro()
        self.actualizar_tabla_pacientes()
        messagebox.showinfo("Registro exitoso", f"Paciente {nombre} {apellidos} registrado correctamente.")

    def limpiar_campos_registro(self):
        
        for var_name in ["pac_nombre", "pac_apellidos", "pac_edad", "pac_enfermedad", "pac_seguro"]:
            getattr(self, f"entry_{var_name}").delete(0, tk.END)
        if self.doctores_disponibles:
            self.combo_doctor_registro.set(self.doctores_disponibles[0].nombre)


    def create_asignar_camilla_frame(self, frame):
        
        tk.Label(frame, text="Asignar Camilla a Paciente", bg="white", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(frame, text="Seleccione paciente:", bg="white", font=("Arial", 12)).pack(pady=5)

        self.combo_pacientes_camilla = ttk.Combobox(frame, state="readonly", font=("Arial", 12))
        self.combo_pacientes_camilla.pack(pady=5, padx=20, fill="x")

        tk.Label(frame, text="Ingrese Camilla (Ej. C1, C2):", bg="white", font=("Arial", 12)).pack(pady=5)
        self.entry_camilla = tk.Entry(frame, font=("Arial", 12))
        self.entry_camilla.pack(pady=5, padx=20, fill="x")

        btn_asignar = tk.Button(frame, text="Asignar Camilla", bg="#158d9b", fg="white",
                                 font=("Arial", 12), command=self.asignar_camilla)
        btn_asignar.pack(pady=20)

        
        self.table_camillas = ttk.Treeview(frame, columns=("Paciente", "Doctor", "Enfermedad", "Camilla"), show="headings")
        self.table_camillas.heading("Paciente", text="Paciente")
        self.table_camillas.heading("Doctor", text="Doctor Asignado")
        self.table_camillas.heading("Enfermedad", text="Enfermedad")
        self.table_camillas.heading("Camilla", text="Camilla")
        
        self.table_camillas.column("Paciente", width=150)
        self.table_camillas.column("Doctor", width=150)
        self.table_camillas.column("Enfermedad", width=150)
        self.table_camillas.column("Camilla", width=100)

        self.table_camillas.pack(pady=20, padx=20, fill="both", expand=True)

        self.actualizar_tabla_pacientes() 

    def asignar_camilla(self):
        
        paciente_seleccionado_nombre = self.combo_pacientes_camilla.get().strip()
        camilla_asignada_id = self.entry_camilla.get().strip()

        if not paciente_seleccionado_nombre or not camilla_asignada_id:
            messagebox.showwarning("Error", "Seleccione un paciente e ingrese una camilla.")
            return

        paciente_encontrado = None
        for p in self.registros:
            
            if p.nombre == paciente_seleccionado_nombre:
                paciente_encontrado = p
                break

        if paciente_encontrado:
            paciente_encontrado.camilla_asignada = camilla_asignada_id
            messagebox.showinfo("Asignación Exitosa", f"Camilla {camilla_asignada_id} asignada a {paciente_encontrado.nombre}.")
            self.entry_camilla.delete(0, tk.END) 
        else:
            messagebox.showerror("Error", "Paciente no encontrado.")

        self.actualizar_tabla_pacientes()

    def actualizar_tabla_pacientes(self):
        
        self.table_camillas.delete(*self.table_camillas.get_children())
        
        
        paciente_nombres_para_combo = []

        for paciente in self.registros:
            self.table_camillas.insert("", "end", values=(
                paciente.nombre, 
                paciente.doctor_asignado.nombre if paciente.doctor_asignado else "N/A",
                paciente.enfermedad, 
                paciente.camilla_asignada
            ))
            
            if paciente.camilla_asignada == "Sin asignar":
                paciente_nombres_para_combo.append(paciente.nombre)

        self.combo_pacientes_camilla["values"] = paciente_nombres_para_combo
        if paciente_nombres_para_combo:
            self.combo_pacientes_camilla.set(paciente_nombres_para_combo[0]) 
        else:
            self.combo_pacientes_camilla.set("") 


    def show_frame(self, name):
        
        frame = self.frames[name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
