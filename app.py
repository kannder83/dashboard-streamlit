import streamlit as st
import pandas as pd
import plotly.express as px

# configuracion de la pagina

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.title("Dashboard")
    st.write("Dashboard de Ejemplo")


# Cargar datos en el dataframe

df_cars = pd.read_csv("./data/electric_cars.csv")

st.write(df_cars)

# contenedor principal
with st.container():
    # titulo
    st.title("Vehiculos Electricos e Hibridos")

# Filtros
with st.container():
    # Multiselect
    filter_fuel, filter_year, filter_service = st.columns(3)

    with filter_fuel:
        # Filtro por combustible
        list_fuel = df_cars["COMBUSTIBLE"].unique()
        list_fuel.sort()
        view_fuel = st.multiselect("COMBUSTIBLE", list_fuel, list_fuel[0])

    with filter_year:
        # Filtro por año
        list_years = df_cars["MODELO"].unique()
        list_years.sort()
        view_year = st.multiselect("MODELO", list_years, list_years[0])

    with filter_service:
        # Filtro por combustible
        list_service = df_cars["SERVICIO"].unique()
        list_service.sort()
        view_service = st.multiselect(
            "SERVICIO", list_service, list_service[0])

# Dataframe filtrado
cars_filter = df_cars[
    (df_cars["COMBUSTIBLE"].isin(view_fuel)) &
    (df_cars["MODELO"].isin(view_year)) &
    (df_cars["SERVICIO"].isin(view_service))
]


# Total de Vehiculos registrados
with st.container():
    # Creación de KPI
    kpi1, kpi2 = st.columns(2)
    # Creación de KPI con st.metric
    with kpi1:
        st.metric(label='Total Vehiculos Registrados',
                  value=f"{df_cars['CANTIDAD'].sum():,.0f}")

    with kpi2:
        st.metric(label='Total Vehiculos Registrados en Bogota',
                  value=f"{df_cars['MUNICIPIO'].value_counts()['BOGOTA']:,.0f}")


# Para graficar
# Titulo
st.header("Graficos Vehiculos")
# Configuración graficios
with st.container():
    # Se crean 2 columnas para el grafico de lineas y el de pie
    # Calcular el DF que se va a graficar
    # data_line = df_cars.groupby("MUNICIPIO")["CANTIDAD"].count()
    data_line = cars_filter
    st.write(data_line)
    # # Cargar configurar el grafico
    # line_chart = px.line(
    #     data_line,
    #     x="CANTIDAD",
    #     y="CANTIDAD",
    #     title="Vehiculos por ciudad"
    # )
    # line_chart.update_layout(
    #     height=600,
    #     width=1000
    # )
    # st.plotly_chart(line_chart)
