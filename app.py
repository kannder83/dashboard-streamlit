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
    st.write(
        "Vehiculos Registrados en Colombia por Municipios - Electricos e Hibridos")


# Cargar datos en el dataframe

df_cars = pd.read_csv("./data/electric_cars.csv")

# st.write(df_cars)

# Contenedor Imagen:
with st.container():
    st.image("./data/car_image.webp",
             caption='Electric cars', use_column_width="auto")

# contenedor principal
with st.container():
    # titulo
    st.title(
        "Vehiculos Registrados en Colombia por Municipios - Electricos e Hibridos")

# Filtros
with st.container():
    # Multiselect
    filter_municipio, filter_year = st.columns(2)

    with filter_municipio:
        # Filtro por Municipio
        list_municipio = df_cars["MUNICIPIO"].unique()
        list_municipio.sort()

        all_cities = st.radio(
            "Seleccione la forma de visualizar las ciudades:",
            ('Por ciudades', 'Todas las ciudades'))

        if all_cities == 'Todas las ciudades':
            view_municipio = list_municipio
        else:
            view_municipio = st.multiselect(
                "Municipio", list_municipio, "BOGOTA")

    with filter_year:
        # Filtro por año de registro
        list_years = df_cars["ANIO_REGISTRO"].unique()
        list_years.sort()

        all_years = st.radio(
            "Seleccione la forma de visualizar los años:",
            ('Por año', 'Todos los años'))

        if all_years == 'Todos los años':
            view_year = list_years
        else:
            view_year = st.multiselect(
                "Año de Registro", list_years, 2022)


# Dataframe filtrado
cars_filter = df_cars[
    (df_cars["MUNICIPIO"].isin(view_municipio)) &
    (df_cars["ANIO_REGISTRO"].isin(view_year))
]


# Total de Vehiculos registrados
with st.container():
    # Creación de KPI
    kpi1, kpi2 = st.columns(2)
    # Creación de KPI con st.metric
    with kpi1:
        st.metric(label=f"Total Vehiculos Registrados",
                  value=f"{cars_filter['CANTIDAD'].sum():,.0f}")

    with kpi2:
        st.metric(label='Total de Marcas Registradas',
                  value=f"{(cars_filter['MARCA']).nunique():,.0f}")


# Configuración graficios
with st.container():
    st.header("Clasificación de Vehiculos")

    data_line = pd.DataFrame(cars_filter.groupby(
        ["ANIO_REGISTRO", "MUNICIPIO", "COMBUSTIBLE", "SERVICIO"]).size().reset_index(name='COUNT'))

    left_chart, right_chart = st.columns(2)

    with left_chart:
        line_chart = alt.Chart(data_line).mark_arc(innerRadius=50).encode(
            theta="sum(COUNT)",
            color=alt.Color("COMBUSTIBLE", title="Tipo de Motor",
                            scale=alt.Scale(scheme="tableau10"))
        )
        st.altair_chart(line_chart, use_container_width=True)

    with right_chart:
        line_chart = alt.Chart(data_line).mark_arc(innerRadius=50).encode(
            theta="sum(COUNT)",
            color=alt.Color("SERVICIO", title="Tipo de Servicio",
                            scale=alt.Scale(scheme="category10"))
        )
        st.altair_chart(line_chart, use_container_width=True)


# Configuración graficios
with st.container():
    st.header("Marcas de Vehiculos")
    st.write("Marcas de vehiculos registrados por año.")

    # Datos
    data_line = pd.DataFrame(cars_filter.groupby(
        ['ANIO_REGISTRO', "MARCA"]).size().reset_index(name='COUNT'))

    sort_df = pd.DataFrame(data_line.sort_values(
        by="COUNT", ascending=False)).reset_index(drop=True)

    list_marca = pd.DataFrame(sort_df["MARCA"].unique(), columns=["MARCA"])

    number_marca = st.slider('Cantidad de Marcas para visualizar: ', 1,
                             list_marca["MARCA"].nunique(), 1)

    list_marca = list_marca.head(number_marca)

    sort_df = sort_df[sort_df["MARCA"].isin(list_marca["MARCA"])]

    line_chart = alt.Chart(sort_df).mark_bar(opacity=0.8).encode(
        y=alt.Y("MARCA:N", title=""),
        x=alt.X("sum(COUNT):Q", title="Vehiculos Registrados"),
        color=alt.Color("ANIO_REGISTRO:N", title="Año de Registro",
                        scale=alt.Scale(scheme="tableau20")),
        order=alt.Order(
            'COUNT:N',
            sort="descending"
        )
    )

    st.altair_chart(line_chart, use_container_width=True)


# Configuración graficios
with st.container():
    st.header("Clase de Vehiculos")
    st.write("Vehiculos registrados por año")
    data_line = pd.DataFrame(cars_filter.groupby(
        ['ANIO_REGISTRO', 'CLASE']).size().reset_index(name='COUNT'))

    data_line = data_line.sort_values(by='COUNT', ascending=False)

    line_chart = alt.Chart(data_line).mark_bar().encode(
        x=alt.X("sum(COUNT):Q", title="Cantidad de Vehiculos"),
        y=alt.Y("ANIO_REGISTRO:N", title=""),
        color="CLASE:N",
        order=alt.Order(
              'COUNT:N',
              sort="descending"
        )
    )

    st.altair_chart(line_chart, use_container_width=True)

with st.container():
    st.header("Información del Dashboard")
    st.write("Repositorio: https://github/kannder83/dashboard-streamlit")
    st.write("Datos: https://www.datos.gov.co/Transporte/Numero-de-Veh-culos-El-ctricos-Hibridos/7qfh-tkr3")
