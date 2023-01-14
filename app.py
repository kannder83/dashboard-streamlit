import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

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
    filter_fuel, filter_year = st.columns(2)

    with filter_fuel:
        # Filtro por combustible
        list_fuel = df_cars["COMBUSTIBLE"].unique()
        list_fuel.sort()
        view_fuel = st.multiselect(
            "COMBUSTIBLE", list_fuel, list_fuel[1])

    with filter_year:
        # Filtro por año de registro
        list_years = df_cars["ANIO_REGISTRO"].unique()
        list_years.sort()
        view_year = st.multiselect("ANIO_REGISTRO", list_years, list_years[-1])


# Dataframe filtrado
cars_filter = df_cars[
    (df_cars["COMBUSTIBLE"].isin(view_fuel)) &
    (df_cars["MODELO"].isin(view_year))
]


# Total de Vehiculos registrados
with st.container():
    # Creación de KPI
    kpi1, kpi2 = st.columns(2)
    # Creación de KPI con st.metric
    with kpi1:
        st.metric(label='Total Vehiculos Registrados Nacional',
                  value=f"{cars_filter['CANTIDAD'].sum():,.0f}")

    with kpi2:
        st.metric(label='Total Vehiculos Registrados en Bogota',
                  value=f"{(cars_filter['MUNICIPIO']=='BOGOTA').sum():,.0f}")


# Para graficar
# Titulo
st.header("Graficos Vehiculos")
# Configuración graficios
with st.container():
    # Se crean 2 columnas para el grafico de lineas y el de pie
    # Calcular el DF que se va a graficar
    data_line = pd.DataFrame(cars_filter.groupby(
        "MUNICIPIO")["CANTIDAD"].count())
    data_line.reset_index(inplace=True)
# df_ciudades = pd.DataFrame(df_cars.groupby("MUNICIPIO")["CANTIDAD"].count())
# df_ciudades.reset_index(inplace=True)
# df_ciudades

    # data_line = data_line.reset_index(inplace=True)

    st.write(data_line.head(10))
    # Cargar configurar el grafico
    # line_chart = px.line(
    #     data_line,
    #     x="MUNICIPIO",
    #     y="CANTIDAD",
    #     title="Vehiculos por ciudad"
    # )
    # line_chart.update_layout(
    #     height=600,
    #     width=1000
    # )
    # st.plotly_chart(line_chart)

    data_line = data_line.sort_values(by='CANTIDAD', ascending=False).head(10)
    line_chart = alt.Chart(data_line).mark_circle().encode(
        y="MUNICIPIO",
        x="CANTIDAD",
        size="CANTIDAD"
    )
    st.altair_chart(line_chart)
