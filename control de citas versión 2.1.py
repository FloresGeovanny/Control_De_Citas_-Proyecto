import tkinter as tk
from tkinter import ttk, messagebox

class Persona:
    def __init__(self, nombre, edad=None):
        self.nombre = nombre
        self.edad = edad

class PersonalHospital:
    def __init__(self, nombre, area):
        self.nombre = nombre
        self.area = area
        self.ocupado = False

class Doctor(PersonalHospital):
    def __init__(self, nombre, area, especialidad="General"):
        super().__init__(nombre, area)
        self.especialidad = especialidad

class Enfermero(PersonalHospital):
    pass

class Paciente(Persona):
    def __init__(self, nombre, edad, area, camilla=None, doctor=None, enfermero=None, enfermedad=None, seguro_social=None):
        super().__init__(nombre, edad)
        self.area = area
        self.camilla = camilla
        self.doctor = doctor
        self.enfermero = enfermero
        self.enfermedad = enfermedad
        self.seguro_social = seguro_social

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Citas de un Hospital")
        self.attributes("-fullscreen", True)

        self.doctores = [
            Doctor("Dr. Pérez", "Urgencias", "Cardiología"),
            Doctor("Dr. Gómez", "Hospitalización", "Pediatría"),
            Doctor("Dra. Ruiz", "Urgencias", "Medicina General")
        ]

        self.enfermeros = [
            Enfermero("Enf. Martínez", "Urgencias"),
            Enfermero("Enf. López", "Hospitalización"),
            Enfermero("Enf. García", "Urgencias")
        ]

        self.camillas = {
            "Urgencias": [{"ocupada": False, "id": i + 1} for i in range(5)],
            "Hospitalización": [{"ocupada": False, "id": i + 1} for i in range(10)],
            "UCI": [{"ocupada": False, "id": i + 1} for i in range(3)]
        }

        self.areas_disponibles = list(self.camillas.keys())

        self.pacientes = []

        self.create_sidebar()
        self.create_main_area()
        self.actualizar_tablas_display()

    def create_sidebar(self):
        self.sidebar = tk.Frame(self, width=200, bg="#158d9b")
        self.sidebar.pack(side="left", fill="y")

        buttons = [
            "Inicio",
            "Registro de Paciente",
            "Administrar Personal",
            "Ver Camillas y Asignaciones",
            "Salir"
        ]

        for name in buttons:
            if name == "Salir":
                btn = tk.Button(self.sidebar, text=name, bg="#e74c3c", fg="white",
                                 relief="flat", command=self.exit_app)
            else:
                btn = tk.Button(self.sidebar, text=name, bg="#34495e", fg="white",
                                 relief="flat", command=lambda n=name: self.show_frame(n))
            btn.pack(fill="x", pady=5, padx=10, ipady=5)

    def exit_app(self):
        self.destroy()

    def create_main_area(self):
        self.frames = {}
        container = tk.Frame(self, bg="white")
        container.pack(side="right", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for name in ["Inicio", "Registro de Paciente", "Administrar Personal", "Ver Camillas y Asignaciones"]:
            frame = tk.Frame(container, bg="white")
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame

        self.create_inicio_frame(self.frames["Inicio"])
        self.create_registro_paciente_frame(self.frames["Registro de Paciente"])
        self.create_administrar_personal_frame(self.frames["Administrar Personal"])
        self.create_ver_camillas_frame(self.frames["Ver Camillas y Asignaciones"])

        self.show_frame("Inicio")

    def create_inicio_frame(self, frame):
        tk.Label(frame, text="Bienvenido al Sistema de Gestión Hospitalaria",
                 bg="white", font=("Arial", 24, "bold"), fg="#158d9b").pack(pady=50)
        tk.Label(frame, text="Utilice el menú lateral para navegar por las opciones.",
                 bg="white", font=("Arial", 16)).pack(pady=20)
        tk.Label(frame, text="Fecha actual: 11 de junio de 2025",
                 bg="white", font=("Arial", 12)).pack(pady=10)
        

    def create_registro_paciente_frame(self, frame):
        frame.columnconfigure(1, weight=1)

        tk.Label(frame, text="Registro de Paciente", bg="white", font=("Arial", 18, "bold"), fg="#34495e").grid(row=0, column=0, columnspan=2, pady=(20, 15))

        self.create_label_entry(frame, "Nombre:", "pac_nombre", 1)
        self.create_label_entry(frame, "Edad:", "pac_edad", 2)
        self.create_label_entry(frame, "Enfermedad:", "pac_enfermedad", 3)
        self.create_label_entry(frame, "No. Seguro Social:", "pac_seguro_social", 4)

        tk.Label(frame, text="Área Requerida:", bg="white", font=("Arial", 12)).grid(row=5, column=0, padx=20, sticky="w")
        self.combo_registro_area = ttk.Combobox(frame, values=self.areas_disponibles, state="readonly", font=("Arial", 12))
        self.combo_registro_area.grid(row=5, column=1, padx=20, pady=5, sticky="ew")
        if self.areas_disponibles:
            self.combo_registro_area.set(self.areas_disponibles[0])
            
        self.combo_registro_area.bind("<<ComboboxSelected>>", self.update_personnel_comboboxes)

        tk.Label(frame, text="Doctor Asignado:", bg="white", font=("Arial", 12)).grid(row=6, column=0, padx=20, sticky="w")
        self.combo_doctor_registro = ttk.Combobox(frame, values=[], state="readonly", font=("Arial", 12))
        self.combo_doctor_registro.grid(row=6, column=1, padx=20, pady=5, sticky="ew")

        tk.Label(frame, text="Enfermero Asignado:", bg="white", font=("Arial", 12)).grid(row=7, column=0, padx=20, sticky="w")
        self.combo_enfermero_registro = ttk.Combobox(frame, values=[], state="readonly", font=("Arial", 12))
        self.combo_enfermero_registro.grid(row=7, column=1, padx=20, pady=5, sticky="ew")

        btn_registrar = tk.Button(frame, text="Registrar Paciente", bg="#158d9b", fg="white",
                                     font=("Arial", 12, "bold"), command=self.registrar_paciente_logic,
                                     relief="raised", bd=2, highlightbackground="#158d9b", highlightthickness=1)
        btn_registrar.grid(row=8, column=0, columnspan=2, pady=20, ipadx=10, ipady=5)

        self.update_personnel_comboboxes()

    def create_label_entry(self, parent_frame, text, var_name, row):
        tk.Label(parent_frame, text=text, bg="white", font=("Arial", 12)).grid(row=row, column=0, padx=20, sticky="w")
        entry = tk.Entry(parent_frame, font=("Arial", 12), bd=2, relief="groove")
        entry.grid(row=row, column=1, padx=20, pady=5, sticky="ew")
        setattr(self, f"entry_{var_name}", entry)

    def update_personnel_comboboxes(self, event=None):
        selected_area = self.combo_registro_area.get()

        available_doctors = [
            d.nombre for d in self.doctores
            if d.area == selected_area and not d.ocupado
        ]
        self.combo_doctor_registro["values"] = available_doctors
        if available_doctors:
            self.combo_doctor_registro.set(available_doctors[0])
        else:
            self.combo_doctor_registro.set("")

        available_nurses = [
            e.nombre for e in self.enfermeros
            if e.area == selected_area and not e.ocupado
        ]
        self.combo_enfermero_registro["values"] = available_nurses
        if available_nurses:
            self.combo_enfermero_registro.set(available_nurses[0])
        else:
            self.combo_enfermero_registro.set("")

    def registrar_paciente_logic(self):
        nombre = self.entry_pac_nombre.get().strip()
        edad_str = self.entry_pac_edad.get().strip()
        enfermedad = self.entry_pac_enfermedad.get().strip()
        seguro_social = self.entry_pac_seguro_social.get().strip()
        area = self.combo_registro_area.get().strip()
        selected_doctor_name = self.combo_doctor_registro.get().strip()
        selected_enfermero_name = self.combo_enfermero_registro.get().strip()

        if not all([nombre, edad_str, enfermedad, seguro_social, area, selected_doctor_name, selected_enfermero_name]):
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos para registrar al paciente.")
            return

        try:
            edad = int(edad_str)
            if edad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error de entrada", "La edad debe ser un número entero positivo.")
            return

        camilla_info = None
        for c_data in self.camillas.get(area, []):
            if not c_data["ocupada"]:
                camilla_info = c_data
                break

        if camilla_info is None:
            messagebox.showerror("Error de asignación", f"No hay camillas disponibles en el área de '{area}'.")
            return

        doc_asignado = next((d for d in self.doctores if d.nombre == selected_doctor_name), None)
        enf_asignado = next((e for e in self.enfermeros if e.nombre == selected_enfermero_name), None)

        if not doc_asignado or doc_asignado.area != area or doc_asignado.ocupado:
            messagebox.showerror("Error de asignación", f"El doctor '{selected_doctor_name}' no está disponible, no pertenece a '{area}' o está ocupado.")
            return

        if not enf_asignado or enf_asignado.area != area or enf_asignado.ocupado:
            messagebox.showerror("Error de asignación", f"El enfermero/a '{selected_enfermero_name}' no está disponible, no pertenece a '{area}' o está ocupado.")
            return

        camilla_info["ocupada"] = True
        doc_asignado.ocupado = True
        enf_asignado.ocupado = True

        paciente = Paciente(nombre, edad, area, camilla_info["id"], doc_asignado, enf_asignado, enfermedad, seguro_social)
        self.pacientes.append(paciente)

        self.limpiar_campos_registro_paciente()
        self.actualizar_tablas_display()
        self.update_personnel_comboboxes()
        messagebox.showinfo("Registro Exitoso", f"Paciente {nombre} registrado en camilla {camilla_info['id']} de {area} con Dr. {doc_asignado.nombre} y Enf. {enf_asignado.nombre}.")

    def limpiar_campos_registro_paciente(self):
        self.entry_pac_nombre.delete(0, tk.END)
        self.entry_pac_edad.delete(0, tk.END)
        self.entry_pac_enfermedad.delete(0, tk.END)
        self.entry_pac_seguro_social.delete(0, tk.END)
        if self.areas_disponibles:
            self.combo_registro_area.set(self.areas_disponibles[0])
        self.combo_doctor_registro.set("")
        self.combo_enfermero_registro.set("")

    def create_administrar_personal_frame(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        tk.Label(frame, text="Administrar Personal", bg="white", font=("Arial", 18, "bold"), fg="#34495e").pack(pady=(20, 10))

        button_frame = tk.Frame(frame, bg="white")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Registrar Doctor", command=self.registrar_doctor_popup,
                   bg="#158d9b", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Registrar Enfermero", command=self.registrar_enfermero_popup,
                   bg="#158d9b", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=0, column=1, padx=5)

        self.personal_table = ttk.Treeview(frame, columns=("Nombre", "Tipo", "Área", "Especialidad/Ocupado"), show="headings")
        self.personal_table.heading("Nombre", text="Nombre")
        self.personal_table.heading("Tipo", text="Tipo")
        self.personal_table.heading("Área", text="Área")
        self.personal_table.heading("Especialidad/Ocupado", text="Especialidad (Doctor) / Ocupado (Enfermero)")
        self.personal_table.pack(pady=15, padx=20, fill="both", expand=True)

        action_button_frame = tk.Frame(frame, bg="white")
        action_button_frame.pack(pady=10)
        tk.Button(action_button_frame, text="Editar Personal Seleccionado", command=self.editar_personal,
                   bg="#34495e", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=0, column=0, padx=5)
        tk.Button(action_button_frame, text="Eliminar Personal Seleccionado", command=self.eliminar_personal,
                   bg="#b30000", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=0, column=1, padx=5)

        self.actualizar_tabla_personal()

    def actualizar_tabla_personal(self):
        for item in self.personal_table.get_children():
            self.personal_table.delete(item)

        for d in self.doctores:
            self.personal_table.insert("", tk.END, values=(d.nombre, "Doctor", d.area, d.especialidad))
        for e in self.enfermeros:
            self.personal_table.insert("", tk.END, values=(e.nombre, "Enfermero", e.area, "Sí" if e.ocupado else "No"))

    def registrar_doctor_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Registrar Doctor")
        popup.transient(self)
        popup.grab_set()

        tk.Label(popup, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
        entry_nombre = tk.Entry(popup, font=("Arial", 10))
        entry_nombre.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(popup, text="Área:").grid(row=1, column=0, padx=10, pady=5)
        combo_area = ttk.Combobox(popup, values=self.areas_disponibles, state="readonly", font=("Arial", 10))
        combo_area.grid(row=1, column=1, padx=10, pady=5)
        if self.areas_disponibles:
            combo_area.set(self.areas_disponibles[0])

        tk.Label(popup, text="Especialidad:").grid(row=2, column=0, padx=10, pady=5)
        entry_especialidad = tk.Entry(popup, font=("Arial", 10))
        entry_especialidad.grid(row=2, column=1, padx=10, pady=5)

        def guardar():
            nombre = entry_nombre.get().strip()
            area = combo_area.get().strip()
            especialidad = entry_especialidad.get().strip()
            if not all([nombre, area, especialidad]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=popup)
                return
            self.doctores.append(Doctor(nombre, area, especialidad))
            messagebox.showinfo("Éxito", f"Doctor {nombre} registrado.", parent=popup)
            self.actualizar_tabla_personal()
            self.update_personnel_comboboxes()
            popup.destroy()

        tk.Button(popup, text="Guardar", command=guardar, bg="#158d9b", fg="white", font=("Arial", 10, "bold")).grid(row=3, column=0, columnspan=2, pady=10)

    def registrar_enfermero_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Registrar Enfermero")
        popup.transient(self)
        popup.grab_set()

        tk.Label(popup, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
        entry_nombre = tk.Entry(popup, font=("Arial", 10))
        entry_nombre.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(popup, text="Área:").grid(row=1, column=0, padx=10, pady=5)
        combo_area = ttk.Combobox(popup, values=self.areas_disponibles, state="readonly", font=("Arial", 10))
        combo_area.grid(row=1, column=1, padx=10, pady=5)
        if self.areas_disponibles:
            combo_area.set(self.areas_disponibles[0])

        def guardar():
            nombre = entry_nombre.get().strip()
            area = combo_area.get().strip()
            if not all([nombre, area]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=popup)
                return
            self.enfermeros.append(Enfermero(nombre, area))
            messagebox.showinfo("Éxito", f"Enfermero/a {nombre} registrado/a.", parent=popup)
            self.actualizar_tabla_personal()
            self.update_personnel_comboboxes()
            popup.destroy()

        tk.Button(popup, text="Guardar", command=guardar, bg="#158d9b", fg="white", font=("Arial", 10, "bold")).grid(row=2, column=0, columnspan=2, pady=10)

    def editar_personal(self):
        try:
            item_id = self.personal_table.selection()[0]
            values = self.personal_table.item(item_id, 'values')
            nombre_actual = values[0]
            tipo_personal = values[1]

            personal_obj = None
            if tipo_personal == "Doctor":
                personal_obj = next((d for d in self.doctores if d.nombre == nombre_actual), None)
            elif tipo_personal == "Enfermero":
                personal_obj = next((e for e in self.enfermeros if e.nombre == nombre_actual), None)

            if not personal_obj:
                messagebox.showwarning("Error", "No se encontró el personal para editar.")
                return

            popup = tk.Toplevel(self)
            popup.title(f"Editar {tipo_personal}")
            popup.transient(self)
            popup.grab_set()

            tk.Label(popup, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
            entry_nombre_ed = tk.Entry(popup, font=("Arial", 10))
            entry_nombre_ed.insert(0, personal_obj.nombre)
            entry_nombre_ed.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(popup, text="Área:").grid(row=1, column=0, padx=10, pady=5)
            combo_area_ed = ttk.Combobox(popup, values=self.areas_disponibles, state="readonly", font=("Arial", 10))
            combo_area_ed.set(personal_obj.area)
            combo_area_ed.grid(row=1, column=1, padx=10, pady=5)

            entry_especialidad_ed = None
            if tipo_personal == "Doctor":
                tk.Label(popup, text="Especialidad:").grid(row=2, column=0, padx=10, pady=5)
                entry_especialidad_ed = tk.Entry(popup, font=("Arial", 10))
                entry_especialidad_ed.insert(0, personal_obj.especialidad)
                entry_especialidad_ed.grid(row=2, column=1, padx=10, pady=5)

            def guardar_edicion():
                personal_obj.nombre = entry_nombre_ed.get().strip()
                personal_obj.area = combo_area_ed.get().strip()
                if tipo_personal == "Doctor" and entry_especialidad_ed:
                    personal_obj.especialidad = entry_especialidad_ed.get().strip()

                messagebox.showinfo("Éxito", f"{tipo_personal} actualizado correctamente.", parent=popup)
                self.actualizar_tabla_personal()
                self.update_personnel_comboboxes()
                popup.destroy()

            row_offset = 1 if tipo_personal == "Doctor" else 0
            tk.Button(popup, text="Guardar Cambios", command=guardar_edicion,
                       bg="#158d9b", fg="white", font=("Arial", 10, "bold")).grid(row=3 + row_offset, column=0, columnspan=2, pady=10)

        except IndexError:
            messagebox.showwarning("Advertencia", "Seleccione un personal de la tabla para editar.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al editar: {e}")

    def eliminar_personal(self):
        try:
            item_id = self.personal_table.selection()[0]
            values = self.personal_table.item(item_id, 'values')
            nombre_a_eliminar = values[0]
            tipo_personal = values[1]

            if tipo_personal == "Doctor":
                self.doctores[:] = [d for d in self.doctores if d.nombre != nombre_a_eliminar]
            elif tipo_personal == "Enfermero":
                self.enfermeros[:] = [e for e in self.enfermeros if e.nombre != nombre_a_eliminar]
            else:
                messagebox.showwarning("Error", "Tipo de personal no reconocido para eliminar.")
                return

            messagebox.showinfo("Éxito", f"{tipo_personal} {nombre_a_eliminar} eliminado correctamente.")
            self.actualizar_tabla_personal()
            self.actualizar_tablas_display()
            self.update_personnel_comboboxes()
        except IndexError:
            messagebox.showwarning("Advertencia", "Seleccione un personal de la tabla para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al eliminar: {e}")

    def create_ver_camillas_frame(self, frame):
        tk.Label(frame, text="Estado de Camillas y Asignaciones", bg="white", font=("Arial", 18, "bold"), fg="#34495e").pack(pady=(20, 10))

        self.camillas_table = ttk.Treeview(frame, columns=("Paciente", "Edad", "Enfermedad", "Área", "Camilla", "Doctor Asignado", "Especialidad Doctor", "Enfermero Asignado"), show="headings")
        self.camillas_table.heading("Paciente", text="Paciente")
        self.camillas_table.heading("Edad", text="Edad")
        self.camillas_table.heading("Enfermedad", text="Enfermedad")
        self.camillas_table.heading("Área", text="Área")
        self.camillas_table.heading("Camilla", text="Camilla")
        self.camillas_table.heading("Doctor Asignado", text="Doctor Asignado")
        self.camillas_table.heading("Especialidad Doctor", text="Especialidad Doctor")
        self.camillas_table.heading("Enfermero Asignado", text="Enfermero Asignado")

        self.camillas_table.column("Paciente", width=120)
        self.camillas_table.column("Edad", width=50)
        self.camillas_table.column("Enfermedad", width=100)
        self.camillas_table.column("Área", width=80)
        self.camillas_table.column("Camilla", width=70)
        self.camillas_table.column("Doctor Asignado", width=120)
        self.camillas_table.column("Especialidad Doctor", width=120)
        self.camillas_table.column("Enfermero Asignado", width=120)

        self.camillas_table.pack(pady=15, padx=20, fill="both", expand=True)

        liberar_frame = tk.Frame(frame, bg="white")
        liberar_frame.pack(pady=10)

        tk.Label(liberar_frame, text="Liberar Camilla:", bg="white", font=("Arial", 12)).pack(side="left", padx=10)
        self.combo_liberar_camilla = ttk.Combobox(liberar_frame, state="readonly", font=("Arial", 12))
        self.combo_liberar_camilla.pack(side="left", padx=10)

        btn_liberar = tk.Button(liberar_frame, text="Liberar", command=self.liberar_camilla_logic,
                                 bg="#b30000", fg="white", font=("Arial", 10, "bold"))
        btn_liberar.pack(side="left", padx=10)

        self.actualizar_tabla_camillas()

    def actualizar_tabla_camillas(self):
        for item in self.camillas_table.get_children():
            self.camillas_table.delete(item)

        self.combo_liberar_camilla["values"] = []
        liberar_options = []

        for paciente in self.pacientes:
            doc_nombre = paciente.doctor.nombre if paciente.doctor else "N/A"
            doc_especialidad = paciente.doctor.especialidad if paciente.doctor else "N/A"
            enf_nombre = paciente.enfermero.nombre if paciente.enfermero else "N/A"
            camilla_id = paciente.camilla if paciente.camilla else "N/A"

            self.camillas_table.insert("", tk.END, values=(
                paciente.nombre,
                paciente.edad,
                paciente.enfermedad,
                paciente.area,
                camilla_id,
                doc_nombre,
                doc_especialidad,
                enf_nombre
            ))
            if paciente.camilla != "N/A":
                liberar_options.append(f"{paciente.nombre} (Camilla: {camilla_id}, Área: {paciente.area})")

        self.combo_liberar_camilla["values"] = liberar_options
        if liberar_options:
            self.combo_liberar_camilla.set("")

    def liberar_camilla_logic(self):
        selected_text = self.combo_liberar_camilla.get()
        if not selected_text:
            messagebox.showwarning("Advertencia", "Seleccione un paciente para liberar la camilla.")
            return

        try:
            parts = selected_text.split(" (Camilla: ")
            if len(parts) < 2:
                raise ValueError("Formato de selección incorrecto.")
            paciente_nombre_str = parts[0]
            camilla_info_str = parts[1].replace(")", "")
            camilla_id = int(camilla_info_str.split(",")[0].strip())
            area = camilla_info_str.split("Área: ")[1].strip()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al procesar la selección: {e}\nFormato esperado: 'Nombre (Camilla: X, Área: Y)'")
            return

        paciente_a_liberar = None
        for p in self.pacientes:
            if p.nombre == paciente_nombre_str and p.camilla == camilla_id and p.area == area:
                paciente_a_liberar = p
                break

        if not paciente_a_liberar:
            messagebox.showerror("Error", "No se encontró el paciente o la asignación de camilla.")
            return

        for camilla_data in self.camillas.get(paciente_a_liberar.area, []):
            if camilla_data["id"] == paciente_a_liberar.camilla and camilla_data["ocupada"]:
                camilla_data["ocupada"] = False
                break

        if paciente_a_liberar.doctor:
            is_doctor_still_needed = any(p for p in self.pacientes if p != paciente_a_liberar and p.doctor == paciente_a_liberar.doctor)
            if not is_doctor_still_needed:
                paciente_a_liberar.doctor.ocupado = False

        if paciente_a_liberar.enfermero:
            is_nurse_still_needed = any(p for p in self.pacientes if p != paciente_a_liberar and p.enfermero == paciente_a_liberar.enfermero)
            if not is_nurse_still_needed:
                paciente_a_liberar.enfermero.ocupado = False

        self.pacientes.remove(paciente_a_liberar)

        messagebox.showinfo("Éxito", f"Camilla {camilla_id} del paciente {paciente_a_liberar.nombre} liberada.")
        self.actualizar_tablas_display()
        self.update_personnel_comboboxes()

    def actualizar_tablas_display(self):
        self.actualizar_tabla_personal()
        self.actualizar_tabla_camillas()

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
