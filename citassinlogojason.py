import streamlit as st
from datetime import datetime, timedelta
import json
import os

# Nombre de los archivos de datos
PACIENTES_FILE = 'pacientes_data.json'
CITAS_FILE = 'citas_data.json'

# Función para cargar los datos desde un archivo
def cargar_datos(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

# Función para guardar los datos en un archivo
def guardar_datos(filename, datos):
    with open(filename, 'w') as file:
        json.dump(datos, file)

# Cargar los datos de pacientes y citas
pacientes = cargar_datos(PACIENTES_FILE)
citas = cargar_datos(CITAS_FILE)

def agregar_paciente():
    st.title("Agregar Paciente")
    nombre = st.text_input("Nombre del Paciente")
    if st.button("Agregar Paciente"):
        if nombre in pacientes:
            st.error("El paciente ya existe")
        else:
            pacientes[nombre] = {"nombre": nombre}
            guardar_datos(PACIENTES_FILE, pacientes)
            st.success(f"Paciente {nombre} agregado exitosamente")

def borrar_paciente():
    st.title("Borrar Paciente")
    nombre = st.text_input("Nombre del Paciente")
    if st.button("Borrar Paciente"):
        if nombre in pacientes:
            del pacientes[nombre]
            guardar_datos(PACIENTES_FILE, pacientes)
            st.success(f"Paciente {nombre} borrado exitosamente")
        else:
            st.error("El paciente no existe")

def consultar_pacientes():
    st.title("Consultar Pacientes")
    if not pacientes:
        st.write("No hay pacientes registrados.")
    for nombre in pacientes:
        st.write(f"Nombre: {nombre}")

def registrar_cita():
    st.title("Registrar Cita")
    if not pacientes:
        st.warning("No hay pacientes registrados. Registra un paciente primero.")
        return
    paciente_nombre = st.selectbox("Selecciona el Paciente", list(pacientes.keys()))
    fecha = st.date_input("Selecciona la Fecha")
    hora_inicio = st.selectbox("Selecciona la Hora de Inicio", [f"{h}:00" for h in range(8, 16)])
    hora_inicio_dt = datetime.strptime(f"{fecha} {hora_inicio}", "%Y-%m-%d %H:%M")
    hora_fin_dt = hora_inicio_dt + timedelta(hours=1)
    hora_inicio_str = hora_inicio_dt.strftime("%H:%M")
    hora_fin_str = hora_fin_dt.strftime("%H:%M")

    if st.button("Registrar Cita"):
        cita_id = f"{paciente_nombre}-{fecha}-{hora_inicio_str}"
        if cita_id in citas:
            st.error("El paciente ya tiene una cita en ese horario")
        else:
            citas[cita_id] = {
                "paciente": paciente_nombre,
                "fecha": fecha.strftime("%Y-%m-%d"),
                "hora_inicio": hora_inicio_str,
                "hora_fin": hora_fin_str
            }
            guardar_datos(CITAS_FILE, citas)
            st.success(f"Cita registrada para {paciente_nombre} el {fecha} de {hora_inicio_str} a {hora_fin_str}")

def borrar_cita():
    st.title("Borrar Cita")
    if not pacientes:
        st.warning("No hay pacientes registrados. Registra un paciente primero.")
        return
    paciente_nombre = st.selectbox("Selecciona el Paciente", list(pacientes.keys()))
    fecha = st.date_input("Selecciona la Fecha")
    hora_inicio = st.selectbox("Selecciona la Hora de Inicio", [f"{h}:00" for h in range(8, 16)])
    hora_inicio_str = datetime.strptime(f"{fecha} {hora_inicio}", "%Y-%m-%d %H:%M").strftime("%H:%M")

    if st.button("Borrar Cita"):
        cita_id = f"{paciente_nombre}-{fecha}-{hora_inicio_str}"
        if cita_id in citas:
            del citas[cita_id]
            guardar_datos(CITAS_FILE, citas)
            st.success(f"Cita para {paciente_nombre} el {fecha} a las {hora_inicio_str} borrada exitosamente")
        else:
            st.error("No se encontró una cita para ese paciente en ese horario")

def consultar_citas():
    st.title("Consultar Citas")
    if not citas:
        st.write("No hay citas registradas.")
    for cita_id, datos in citas.items():
        st.write(f"Paciente: {datos['paciente']}, Fecha: {datos['fecha']}, Hora: {datos['hora_inicio']} - {datos['hora_fin']}")

st.sidebar.title("Menú Principal")

menu_principal = st.sidebar.radio("Selecciona una opción", ["Ninguna", "Pacientes", "Citas"], index=0)

if menu_principal == "Pacientes":
    password = st.sidebar.text_input("Introduce la contraseña", type="password")
    if password:
        if password == "Tt3plco4$":
            st.sidebar.title("Opciones de Pacientes")
            opcion = st.sidebar.radio("Selecciona una opción", ["Agregar Paciente", "Borrar Paciente", "Consultar Pacientes"], index=0)
            if opcion == "Agregar Paciente":
                agregar_paciente()
            elif opcion == "Borrar Paciente":
                borrar_paciente()
            elif opcion == "Consultar Pacientes":
                consultar_pacientes()
        else:
            st.sidebar.error("Contraseña incorrecta")
elif menu_principal == "Citas":
    st.sidebar.title("Opciones de Citas")
    opcion = st.sidebar.radio("Selecciona una opción", ["Registrar Cita", "Borrar Cita", "Consultar Citas"], index=0)
    if opcion == "Registrar Cita":
        registrar_cita()
    elif opcion == "Borrar Cita":
        borrar_cita()
    elif opcion == "Consultar Citas":
        consultar_citas()
