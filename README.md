CONTROL DE CITAS DE UN HSOPITAL
 1. Datos o información que hace valido el trabajo o área de la persona
 Usuario(nombre)
 Contraseña
 Cargo(Medico, Enfermería, Recepcionista, Limpieza)
 Fecha de ingreso 
  

2. Datos o base dependiendo del área
Agenda de citas por paciente
visualización de las citas correspondientes
lugares de aseo y horarios
Ingreso de nuevo medicamento
 
3. Gestión de citas por usuario o paciente
 Fecha y hora de la cita
 Paciente 
 Tipo de cita

4. control de citas y tareas
Registro de actividades por cargo
Asignación de citas y tareas dependiendo su cargo
Notificación y recordatorios
  

6. Informes y estadísticas 
Generar una estadística sobre cantidad de citas y tareas realizadas (semana)
Información sobre la cantidad de pacientes atendidos y su calidad de atención (valoracion)


USUARIO Y CONTRASEÑA 1.0
1. Botón Iniciar Sesión (self.login_btn)
Ubicación: Ventana principal (login).

Función: Ejecuta el método iniciar_sesion cuando se presiona.

Qué hace en iniciar_sesion:

Lee los valores ingresados en los campos de usuario y contraseña.

Verifica si el usuario existe en el archivo JSON y si la contraseña coincide.

Si la autenticación es correcta:

Muestra un mensaje de bienvenida con el rol del usuario.

Llama a mostrar_interfaz_por_rol para mostrar la interfaz o funcionalidad según el rol.

Si no coincide, muestra un mensaje de error.

2. Botón Registrarse (self.registro_btn)
Ubicación: Ventana principal (login), debajo del texto "¿No tienes cuenta? Regístrate abajo".

Función: Ejecuta el método abrir_registro cuando se presiona.

Qué hace en abrir_registro:

Oculta la ventana principal de login (self.root.withdraw()).

Abre una nueva ventana para registrar un usuario nuevo, creando una instancia de la clase RegistroWindow.

3. Botón Registrar (self.registrar_btn)
Ubicación: Ventana de registro (nueva ventana RegistroWindow).

Función: Ejecuta el método registrar_usuario cuando se presiona.

Qué hace en registrar_usuario:

Toma los datos ingresados (usuario, contraseña y rol).

Verifica que el usuario no exista ya en el archivo.

Valida que los campos usuario y contraseña no estén vacíos.

Si todo es correcto:

Añade el nuevo usuario al diccionario de usuarios.

Guarda los datos actualizados en el archivo JSON.

Muestra un mensaje confirmando el registro.

Cierra la ventana de registro.

Si hay errores, muestra mensajes de advertencia o error.

Resumen de cómo interactúan los botones
Primero, el usuario puede iniciar sesión con Iniciar Sesión si ya tiene cuenta.

Si no tiene cuenta, puede abrir el formulario de registro con Registrarse.

En la ventana de registro, completa sus datos y pulsa Registrar para crear su cuenta.

Los datos se guardan en un archivo JSON local y luego puede iniciar sesión con esos datos.

Según el rol, se mostraría una interfaz específica (en el código actual solo hay mensajes de ejemplo).

Breve explicación del flujo general
Ventana Login:

Usuario ingresa credenciales.

Presiona Iniciar Sesión.

Se valida usuario y contraseña.

Si correcto, se muestra mensaje y se abre interfaz según rol.

Si incorrecto, error.

Ventana Registro (al presionar Registrarse):

Usuario llena formulario.

Presiona Registrar.

Se valida que el usuario no exista y que los campos no estén vacíos.

Se guarda el nuevo usuario.

Se cierra esta ventana y puede volver a login para iniciar sesión.


Clases en el código
1. Clase LoginApp
Qué es:
La clase principal que maneja la ventana de inicio de sesión (login).

Responsabilidades:

Crear la ventana de login con campos para usuario y contraseña.

Cargar los usuarios desde el archivo JSON.

Manejar el proceso de inicio de sesión.

Abrir la ventana de registro si el usuario quiere crear una cuenta nueva.

Mostrar mensajes según el rol del usuario después del login exitoso.

Atributos importantes:

self.root: la ventana principal de Tkinter.

self.usuarios: diccionario que contiene los usuarios cargados desde el archivo.

Widgets de la interfaz (entry para usuario y contraseña, botones).

Métodos principales:

iniciar_sesion(): valida las credenciales ingresadas.

abrir_registro(): oculta la ventana actual y abre la ventana de registro.

mostrar_interfaz_por_rol(rol): método placeholder que muestra un mensaje según el rol.

2. Clase RegistroWindow
Qué es:
Ventana secundaria que permite crear nuevos usuarios.

Responsabilidades:

Mostrar formulario para crear un nuevo usuario (usuario, contraseña, rol).

Validar que el usuario no exista y que los campos estén completos.

Guardar el nuevo usuario en el archivo JSON.

Cerrar la ventana después de registrar.

Atributos importantes:

self.root: ventana secundaria de Tkinter (Toplevel) que se abre encima de la principal.

self.usuarios: diccionario que contiene los usuarios actuales para validar y guardar nuevos.

Widgets para entrada de datos y selección de rol.

Métodos principales:

registrar_usuario(): maneja la lógica de validación y almacenamiento del nuevo usuario.

¿Cómo trabajan juntas estas clases?
La clase LoginApp inicia la aplicación con la ventana de login.

Si el usuario no existe, la clase LoginApp abre la ventana RegistroWindow.

La clase RegistroWindow registra un nuevo usuario y actualiza el archivo JSON.

Después de registrar, el usuario puede cerrar la ventana de registro y volver a la ventana de login para iniciar sesión.


INTERFAZ DE MEDICO (Vista de citas) 1.1
se agrego parte del codigo una nueva interfaz en el codigo donde puede mostrar citas (aun no programar y que se guarden pero la ventana ya funciona si te registras como medico)
Una nueva ventana (Toplevel) que simula una agenda de citas con un área de texto editable. linea de la 118-132
Al iniciar sesión como “Médico”, se abra directamente la ventana con las citas( antes dando un mensaje sobre la ventana ahora ya se puede ejcutar y ver, no solo dando un mensaje por messagebox.showinfo). linea 64 y 65 






