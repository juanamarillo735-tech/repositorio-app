import streamlit as st
import pulp

# Título y descripción de la App
st.title("Optimización de Servidores Cloud")
st.write("Esta aplicación resuelve el modelo de programación lineal para maximizar los ingresos de un Data Center.")

# Parámetros (Permite al usuario interactuar)
st.sidebar.header("Capacidad del Clúster")
max_cpu = st.sidebar.slider("Núcleos de CPU disponibles", 50, 200, 120)
max_ram = st.sidebar.slider("GB de RAM disponibles", 100, 500, 320)
max_ssd = st.sidebar.slider("GB de SSD disponibles", 500, 2000, 1000)

if st.button("Calcular Solución Óptima"):
    # Inicializar modelo
    modelo = pulp.LpProblem("Maximizacion_Cloud", pulp.LpMaximize)

    # Variables de decisión
    x1 = pulp.LpVariable("VM_Basica", lowBound=0, cat='Integer')
    x2 = pulp.LpVariable("VM_Pro", lowBound=5, cat='Integer') # Minimo 5 por contrato
    x3 = pulp.LpVariable("VM_Enterprise", lowBound=0, cat='Integer')

    # Función Objetivo
    modelo += 20 * x1 + 50 * x2 + 120 * x3, "Ingreso_Total"

    # Restricciones basadas en los sliders interactivos
    modelo += 2 * x1 + 4 * x2 + 8 * x3 <= max_cpu, "Limite_CPU"
    modelo += 4 * x1 + 16 * x2 + 32 * x3 <= max_ram, "Limite_RAM"
    modelo += 50 * x1 + 100 * x2 + 250 * x3 <= max_ssd, "Limite_SSD"

    # Resolver
    modelo.solve()

    # Mostrar Resultados en la interfaz web
    if pulp.LpStatus[modelo.status] == 'Optimal':
        st.success("¡Solución óptima encontrada!")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("VM Básicas", int(x1.varValue))
        col2.metric("VM Pro", int(x2.varValue))
        col3.metric("VM Enterprise", int(x3.varValue))
        
        st.header(f"Ingreso Mensual Máximo: ${int(pulp.value(modelo.objective))} USD")
    else:
        st.error("No se encontró una solución óptima con estos parámetros.")