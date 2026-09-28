import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Oferta No Cubierta",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("📊 Análisis de Oferta de Flota No Cubierta")
st.markdown("---")

# Carga de datos con cache para mejor rendimiento
@st.cache_data
def cargar_datos():
    df = pd.read_excel(
        'OfertaFlotaNoCubierta.xlsx',
        sheet_name='ConsolidadoNoCumplidos'
    )
    return df

# Cargar datos
try:
    df = cargar_datos()
    st.caption(f"Datos disponibles: {len(df)} registros")
except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.stop()

columnas_requeridas = [
    'Year', 'Trimestre', 'Mes', 'Nombre del mes', 'COD RUTA', 'RUTA',
    'TIPO DE VEHICULO', 'EMPRESAS', 'MATERIAL PLAN', 'FECHA', 'PARTNER'
]
columnas_faltantes = [columna for columna in columnas_requeridas if columna not in df.columns]
if columnas_faltantes:
    st.error(f"Faltan columnas requeridas en el Excel: {', '.join(columnas_faltantes)}")
    st.stop()

# Sidebar con filtros
st.sidebar.header("🔍 Filtros")

# Filtro por Year
anios = sorted(df['Year'].unique())
anio_seleccionado = st.sidebar.multiselect(
    "Año",
    options=anios,
    default=anios
)

# Filtro por Trimestre
trimestres = sorted(df['Trimestre'].unique())
trimestre_seleccionado = st.sidebar.multiselect(
    "Trimestre",
    options=trimestres,
    default=trimestres
)

# Filtro por Mes
meses = df[['Mes', 'Nombre del mes']].drop_duplicates().sort_values('Mes')
mes_seleccionado = st.sidebar.multiselect(
    "Mes",
    options=meses['Nombre del mes'].tolist(),
    default=meses['Nombre del mes'].tolist()
)

# Filtro por Empresa (TODAS las empresas)
todas_empresas = sorted(df['EMPRESAS'].unique().tolist())
empresa_seleccionado = st.sidebar.multiselect(
    "Empresa",
    options=todas_empresas,
    default=todas_empresas
)

# Filtro por Ruta (TODAS las rutas)
todas_rutas = sorted(df['COD RUTA'].unique().tolist())
ruta_seleccionado = st.sidebar.multiselect(
    "Ruta",
    options=todas_rutas,
    default=todas_rutas
)

# Filtro por Material (TODOS los materiales)
todos_materiales = sorted(df['MATERIAL PLAN'].unique().tolist())
material_seleccionado = st.sidebar.multiselect(
    "Material",
    options=todos_materiales,
    default=todos_materiales
)

# Filtro por Tipo de Vehículo (último filtro)
tipos_vehiculo = sorted(df['TIPO DE VEHICULO'].unique().tolist())
tipo_vehiculo_seleccionado = st.sidebar.multiselect(
    "Tipo de Vehículo",
    options=tipos_vehiculo,
    default=tipos_vehiculo
)

# Aplicar filtros
df_filtrado = df[
    (df['Year'].isin(anio_seleccionado)) &
    (df['Trimestre'].isin(trimestre_seleccionado)) &
    (df['Nombre del mes'].isin(mes_seleccionado)) &
    (df['TIPO DE VEHICULO'].isin(tipo_vehiculo_seleccionado)) &
    (df['EMPRESAS'].isin(empresa_seleccionado)) &
    (df['COD RUTA'].isin(ruta_seleccionado)) &
    (df['MATERIAL PLAN'].isin(material_seleccionado))
].copy()

st.sidebar.markdown("---")
st.sidebar.info(f"**Registros filtrados:** {len(df_filtrado)}")

if df_filtrado.empty:
    st.warning("No hay registros para los filtros seleccionados. Ajusta los filtros para ver el análisis.")
    st.stop()

# Métricas principales (KPIs)
st.header("📈 Métricas Principales")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Servicios No Cumplidos",
        value=len(df_filtrado)
    )

with col2:
    empresas_unicas = df_filtrado['EMPRESAS'].nunique()
    st.metric(
        label="Empresas Afectadas",
        value=empresas_unicas
    )

with col3:
    rutas_unicas = df_filtrado['COD RUTA'].nunique()
    st.metric(
        label="Rutas Afectadas",
        value=rutas_unicas
    )

with col4:
    materiales_unicos = df_filtrado['MATERIAL PLAN'].nunique()
    st.metric(
        label="Materiales Diferentes",
        value=materiales_unicos
    )

with col5:
    tipos_vehiculo_count = df_filtrado['TIPO DE VEHICULO'].nunique()
    st.metric(
        label="Tipos de Vehículo",
        value=tipos_vehiculo_count
    )

st.markdown("---")

# Análisis temporal
st.header("📅 Análisis Temporal")

col_temporal1, col_temporal2 = st.columns(2)

with col_temporal1:
    # Servicios por mes
    servicios_por_mes = df_filtrado.groupby(['Mes', 'Nombre del mes']).size().reset_index(name='Cantidad')
    servicios_por_mes = servicios_por_mes.sort_values('Mes')
    
    fig_mes = px.bar(
        servicios_por_mes,
        x='Nombre del mes',
        y='Cantidad',
        title='Servicios No Cumplidos por Mes',
        labels={'Nombre del mes': 'Mes', 'Cantidad': 'Cantidad de Servicios'},
        color='Nombre del mes',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_mes.update_layout(showlegend=False)
    st.plotly_chart(fig_mes, width='stretch')

with col_temporal2:
    # Servicios por trimestre
    servicios_por_trimestre = df_filtrado.groupby(['Year', 'Trimestre']).size().reset_index(name='Cantidad')
    servicios_por_trimestre['Periodo'] = servicios_por_trimestre['Year'].astype(str) + ' - T' + servicios_por_trimestre['Trimestre'].astype(str)
    
    fig_trimestre = px.bar(
        servicios_por_trimestre,
        x='Periodo',
        y='Cantidad',
        title='Servicios No Cumplidos por Trimestre',
        labels={'Periodo': 'Periodo', 'Cantidad': 'Cantidad de Servicios'},
        color='Periodo',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_trimestre.update_layout(showlegend=False)
    st.plotly_chart(fig_trimestre, width='stretch')

st.markdown("---")

# Análisis por Empresa
st.header("🏢 Análisis por Empresa")

col_empresa1, col_empresa2 = st.columns(2)

with col_empresa1:
    # Top 10 empresas con más servicios no cumplidos
    top_empresas_df = df_filtrado['EMPRESAS'].value_counts().head(10).reset_index()
    top_empresas_df.columns = ['Empresa', 'Cantidad']
    
    fig_empresas = px.bar(
        top_empresas_df,
        x='Cantidad',
        y='Empresa',
        orientation='h',
        title='Top 10 Empresas con Más Servicios No Cumplidos',
        labels={'Empresa': 'Empresa', 'Cantidad': 'Cantidad de Servicios'},
        color='Empresa',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_empresas.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_empresas, width='stretch')

with col_empresa2:
    # Mantener legible la distribución al agrupar las rutas menos frecuentes.
    conteo_rutas = df_filtrado['COD RUTA'].value_counts()
    servicios_por_ruta = conteo_rutas.head(10).rename_axis('COD RUTA').reset_index(name='Cantidad')
    otras_rutas = int(conteo_rutas.iloc[10:].sum())
    if otras_rutas:
        servicios_por_ruta = pd.concat([
            servicios_por_ruta,
            pd.DataFrame([{'COD RUTA': 'Otras rutas', 'Cantidad': otras_rutas}])
        ], ignore_index=True)
    
    fig_ruta_empresa = px.bar(
        servicios_por_ruta,
        x='Cantidad',
        y='COD RUTA',
        orientation='h',
        title='Distribución por Ruta (Top 10 + otras)',
        labels={'COD RUTA': 'Código de Ruta', 'Cantidad': 'Servicios'},
        color='COD RUTA',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_ruta_empresa.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)
    st.plotly_chart(fig_ruta_empresa, width='stretch')

st.markdown("---")

# Análisis por Ruta
st.header("🛣️ Análisis por Ruta")

# Top 15 rutas con más servicios no cumplidos
top_rutas = df_filtrado.groupby(['COD RUTA', 'RUTA']).size().reset_index(name='Cantidad')
top_rutas = top_rutas.sort_values('Cantidad', ascending=False).head(15)

fig_rutas = px.bar(
    top_rutas,
    x='COD RUTA',
    y='Cantidad',
    title='Top 15 Rutas con Más Servicios No Cumplidos',
    labels={'COD RUTA': 'Código de Ruta', 'Cantidad': 'Cantidad de Servicios'},
    color='COD RUTA',
    color_discrete_sequence=px.colors.qualitative.Set2,
    hover_data=['RUTA']
)
st.plotly_chart(fig_rutas, width='stretch')

st.markdown("---")

# Análisis de Oportunidades
st.header("💡 Análisis de Oportunidades")

col_oportunidad1, col_oportunidad2 = st.columns(2)

with col_oportunidad1:
    # Ranking de combinaciones empresa y tipo de vehículo.
    oportunidades = df_filtrado.groupby(['EMPRESAS', 'TIPO DE VEHICULO']).size().reset_index(name='Cantidad')
    oportunidades = oportunidades.sort_values('Cantidad', ascending=False).head(10)
    oportunidades['Oportunidad'] = oportunidades['EMPRESAS'].astype(str) + ' - ' + oportunidades['TIPO DE VEHICULO'].astype(str)
    
    fig_oportunidades = px.bar(
        oportunidades,
        x='Cantidad',
        y='Oportunidad',
        orientation='h',
        color='TIPO DE VEHICULO',
        title='Top 10 Combinaciones Empresa y Vehículo',
        labels={'Oportunidad': 'Empresa y tipo de vehículo', 'Cantidad': 'Servicios', 'TIPO DE VEHICULO': 'Tipo de vehículo'},
        hover_data=['EMPRESAS', 'TIPO DE VEHICULO'],
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_oportunidades.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_oportunidades, width='stretch')

with col_oportunidad2:
    # Barras horizontales: Empresas vs Meses
    empresa_mes = df_filtrado.groupby(['EMPRESAS', 'Nombre del mes']).size().reset_index(name='Cantidad')
    # Top 10 empresas
    top_10_empresas = df_filtrado['EMPRESAS'].value_counts().head(10).index
    empresa_mes = empresa_mes[empresa_mes['EMPRESAS'].isin(top_10_empresas)]
    
    fig_empresa_mes = px.bar(
        empresa_mes,
        x='Cantidad',
        y='EMPRESAS',
        color='Nombre del mes',
        orientation='h',
        title='Top 10 Empresas: Servicios por Mes',
        labels={'EMPRESAS': 'Empresa', 'Cantidad': 'Cantidad', 'Nombre del mes': 'Mes'},
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_empresa_mes, width='stretch')

st.markdown("---")

# =============================================================================
# CRUCES ENTRE EMPRESA, RUTA Y MATERIAL
# =============================================================================

st.header("🔀 Cruzes: Empresa × Ruta × Material")

# Pestañas para diferentes tipos de cruce
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Resumen de Cruces",
    "🏢 Empresa × Ruta",
    "📦 Empresa × Material",
    "🛣️ Ruta × Material"
])

# Tab 1: Resumen de Cruces
with tab1:
    st.subheader("Resumen de Combinaciones Únicas")
    
    # Crear el resumen con columnas separadas correctamente
    resumen_cruces = df_filtrado.groupby(['EMPRESAS', 'COD RUTA', 'RUTA', 'MATERIAL PLAN']).size().reset_index(name='Cantidad')
    resumen_cruces = resumen_cruces.sort_values('Cantidad', ascending=False).head(20)
    
    st.dataframe(
        resumen_cruces[['EMPRESAS', 'COD RUTA', 'RUTA', 'MATERIAL PLAN', 'Cantidad']].head(20),
        width='stretch'
    )
    
    # Gráfico de barras horizontales para las combinaciones
    resumen_cruces['Combinacion'] = (
        resumen_cruces['EMPRESAS'].str[:30] + '... | ' + 
        resumen_cruces['COD RUTA'] + ' | ' + 
        resumen_cruces['MATERIAL PLAN'].str[:40]
    )
    
    fig_combinaciones = px.bar(
        resumen_cruces.head(15),
        x='Cantidad',
        y='Combinacion',
        orientation='h',
        title='Top 15 Combinaciones (Empresa + Ruta + Material)',
        labels={'Combinacion': 'Combinación', 'Cantidad': 'Cantidad de Servicios'},
        color='COD RUTA',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_combinaciones.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_combinaciones, width='stretch')

# Tab 2: Empresa × Ruta
with tab2:
    st.subheader("Cruces entre Empresa y Ruta")
    
    # Barras horizontales: Empresa × Ruta
    empresa_ruta = df_filtrado.groupby(['EMPRESAS', 'COD RUTA']).size().reset_index(name='Cantidad')
    # Top 10 empresas y rutas
    top_empresas_list = df_filtrado['EMPRESAS'].value_counts().head(10).index
    top_rutas_list = df_filtrado['COD RUTA'].value_counts().head(10).index
    empresa_ruta_filtrado = empresa_ruta[
        (empresa_ruta['EMPRESAS'].isin(top_empresas_list)) &
        (empresa_ruta['COD RUTA'].isin(top_rutas_list))
    ]
    
    fig_empresa_ruta = px.bar(
        empresa_ruta_filtrado,
        x='Cantidad',
        y='EMPRESAS',
        color='COD RUTA',
        orientation='h',
        title='Empresa × Ruta (Top 10 de cada uno)',
        labels={'EMPRESAS': 'Empresa', 'Cantidad': 'Cantidad', 'COD RUTA': 'Ruta'},
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_empresa_ruta, width='stretch')
    
    # Tabla de detalle
    st.subheader("Detalle de Servicios por Empresa y Ruta")
    detalle_empresa_ruta = df_filtrado.groupby(['EMPRESAS', 'COD RUTA', 'RUTA']).size().reset_index(name='Total Servicios')
    detalle_empresa_ruta = detalle_empresa_ruta.sort_values('Total Servicios', ascending=False).head(20)
    st.dataframe(detalle_empresa_ruta, width='stretch')

# Tab 3: Empresa × Material
with tab3:
    st.subheader("Cruces entre Empresa y Material")
    
    # Barras horizontales: Empresa × Material
    empresa_material = df_filtrado.groupby(['EMPRESAS', 'MATERIAL PLAN']).size().reset_index(name='Cantidad')
    empresa_material_filtrado = empresa_material[
        empresa_material['EMPRESAS'].isin(top_empresas_list)
    ]
    
    fig_empresa_material = px.bar(
        empresa_material_filtrado,
        x='Cantidad',
        y='EMPRESAS',
        color='MATERIAL PLAN',
        orientation='h',
        title='Empresa × Material (Top 10 Empresas)',
        labels={'EMPRESAS': 'Empresa', 'Cantidad': 'Cantidad', 'MATERIAL PLAN': 'Material'},
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_empresa_material, width='stretch')

# Tab 4: Ruta × Material
with tab4:
    st.subheader("Cruces entre Ruta y Material")
    
    # Barras horizontales: Ruta × Material
    ruta_material = df_filtrado.groupby(['COD RUTA', 'MATERIAL PLAN']).size().reset_index(name='Cantidad')
    ruta_material_filtrado = ruta_material[
        ruta_material['COD RUTA'].isin(top_rutas_list)
    ]
    
    fig_ruta_material = px.bar(
        ruta_material_filtrado,
        x='Cantidad',
        y='COD RUTA',
        color='MATERIAL PLAN',
        orientation='h',
        title='Ruta × Material (Top 10 Rutas)',
        labels={'COD RUTA': 'Ruta', 'Cantidad': 'Cantidad', 'MATERIAL PLAN': 'Material'},
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_ruta_material, width='stretch')

st.markdown("---")

# Análisis de Oportunidades con Cruces
st.header("🎯 Oportunidades Específicas por Cruces")

# Crear métricas de oportunidad
st.subheader("Identificación de Oportunidades de Mejora")

# Oportunidades por empresa con múltiples rutas
oportunidad_multi_ruta = df_filtrado.groupby('EMPRESAS').agg({
    'COD RUTA': 'nunique',
    'MATERIAL PLAN': 'nunique',
    'PARTNER': 'count'
}).reset_index()
oportunidad_multi_ruta.columns = ['Empresa', 'Rutas Diferentes', 'Materiales Diferentes', 'Total Servicios']
oportunidad_multi_ruta = oportunidad_multi_ruta.sort_values('Total Servicios', ascending=False).head(10)

col_opp1, col_opp2 = st.columns(2)

with col_opp1:
    st.markdown("**Empresas con mayor diversidad de rutas afectadas**")
    st.dataframe(oportunidad_multi_ruta, width='stretch')

with col_opp2:
    # Tasa de concentración
    concentracion = df_filtrado.groupby('EMPRESAS')['COD RUTA'].nunique().reset_index(name='Rutas')
    concentracion = concentracion.sort_values('Rutas', ascending=False).head(10)
    
    fig_concentracion = px.bar(
        concentracion,
        x='Rutas',
        y='EMPRESAS',
        orientation='h',
        title='Número de Rutas Diferentes por Empresa',
        labels={'EMPRESAS': 'Empresa', 'Rutas': 'Cantidad de Rutas'},
        color='EMPRESAS',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_concentracion.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_concentracion, width='stretch', key='concentracion_por_empresa')

st.markdown("---")

# Tabla de datos detallados
st.header("📋 Datos Detallados")

# Selector de columnas para mostrar
columnas_disponibles = df_filtrado.columns.tolist()
columnas_seleccionadas = st.multiselect(
    "Selecciona las columnas a mostrar",
    options=columnas_disponibles,
    default=['COD RUTA', 'RUTA', 'TIPO DE VEHICULO', 'EMPRESAS', 'FECHA', 'PARTNER', 'MATERIAL PLAN']
)

# Mostrar tabla
st.dataframe(
    df_filtrado.sort_values('FECHA', ascending=False)[columnas_seleccionadas],
    width='stretch',
    height=400
)

# Botón de descarga
csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Descargar datos filtrados (CSV)",
    data=csv,
    file_name='oferta_no_cubierta_filtrada.csv',
    mime='text/csv'
)

st.markdown("---")

# =============================================================================
# SECCIÓN FINAL: OBSERVACIONES Y RECOMENDACIONES
# =============================================================================

st.header("📝 Observaciones y Recomendaciones")

# Crear pestañas para organizar la información
tab_obs, tab_rec, tab_opor = st.tabs([
    "🔍 Observaciones del Análisis",
    "💡 Recomendaciones",
    "🎯 Oportunidades Detectadas"
])

# Tab 1: Observaciones
with tab_obs:
    st.subheader("Hallazgos Principales")
    
    # Calcular métricas clave para las observaciones
    total_servicios = len(df_filtrado)
    empresas_afectadas = df_filtrado['EMPRESAS'].nunique()
    rutas_afectadas = df_filtrado['COD RUTA'].nunique()
    materiales_diferentes = df_filtrado['MATERIAL PLAN'].nunique()
    
    # Empresa con más servicios
    top_empresa = df_filtrado['EMPRESAS'].value_counts().index[0]
    top_empresa_count = df_filtrado['EMPRESAS'].value_counts().iloc[0]
    
    # Ruta con más servicios
    top_ruta = df_filtrado['COD RUTA'].value_counts().index[0]
    top_ruta_count = df_filtrado['COD RUTA'].value_counts().iloc[0]
    
    # Mes con más servicios
    top_mes = df_filtrado['Nombre del mes'].value_counts().index[0]
    top_mes_count = df_filtrado['Nombre del mes'].value_counts().iloc[0]
    concentracion_rutas = df_filtrado['COD RUTA'].value_counts().head(5).sum() / total_servicios * 100
    
    st.markdown(f"""
    ### 📊 Resumen Ejecutivo
    
    | Métrica | Valor |
    |---------|-------|
    | Total de servicios no cumplidos | **{total_servicios}** |
    | Empresas afectadas | **{empresas_afectadas}** |
    | Rutas afectadas | **{rutas_afectadas}** |
    | Materiales diferentes | **{materiales_diferentes}** |
    
    ### 🔎 Hallazgos Clave
    
    1. **Empresa más afectada:** `{top_empresa}` con **{top_empresa_count}** servicios no cumplidos
    
    2. **Ruta más crítica:** `{top_ruta}` con **{top_ruta_count}** servicios no cumplidos
    
    3. **Mes con mayor incidencia:** `{top_mes}` con **{top_mes_count}** servicios
    
    4. **Concentración:** El top 5 de empresas concentra el **{df_filtrado['EMPRESAS'].value_counts().head(5).sum() / total_servicios * 100:.1f}%** de los servicios no cumplidos

    5. **Concentración por ruta:** Las 5 rutas más frecuentes reúnen el **{concentracion_rutas:.1f}%** de los servicios no cumplidos
    """)
    
    st.markdown("---")
    st.plotly_chart(fig_concentracion, width='stretch')
    st.markdown("""
    ### ⚠️ Contexto Nacional Relevante
    
    #### 1. Orden Público y Seguridad Vial
    
    Colombia enfrenta una **crisis de orden público** que afecta directamente las operaciones de transporte:
    
    - **100+ bloqueos viales** registrados en los primeros meses de 2026 (Colfecar)
    - **Zonas críticas:** Bajo Cauca antioqueño, Cauca, Nariño, Putumayo, Chocó, Arauca
    - **Vías afectadas:** Panamericana (Ipiales-Cali), Troncal de Occidente, Ruta del Sol
    - **Pérdidas estimadas:** Más de **$250 mil millones** por bloqueos en 2026
    - **Incidentes:** Quema de vehículos, extorsiones, retenciones ilegales
    
    #### 2. Estado de la Infraestructura Vial
    
    La red vial colombiana presenta deficiencias estructurales:
    
    - **142,284 km** de vías terciarias (69% del total), solo **6% pavimentadas**
    - **40%** de las vías terciarias están en **mal estado** (DNP 2025)
    - **Ejecución presupuestal:** Solo 46.3% del presupuesto de transporte ejecutado en 2025
    - **Regiones más afectadas:** Pacífico, Chocó, Putumayo, Arauca, La Guajira
    
    #### 3. Estado del Parque Automotor
    
    La flota de carga colombiana es una de las más antiguas de América Latina:
    
    - **Edad promedio:** 21-22.8 años (Colfecar 2025)
    - **360,000 vehículos** de carga en operación
    - **97.4%** de los transportadores poseen entre 1-3 vehículos
    - **28.4%** de camiones de dos ejes tienen más de 35 años
    - **Impacto:** Mayores costos de mantenimiento, menor eficiencia, riesgos de seguridad
    """)

# Tab 2: Recomendaciones
with tab_rec:
    st.subheader("Plan de Acción Recomendado")
    
    st.markdown("""
    ### 🎯 Estrategias Inmediatas (0-3 meses)
    
    | Acción | Descripción | Responsable |
    |--------|-------------|-------------|
    | **Monitoreo de vías** | Implementar sistema de alertas tempranas para corredores críticos (Bajo Cauca, Panamericana, Chocó) | Operaciones |
    | **Rutas alternas** | Establecer protocolos de desvío para zonas con alto riesgo de bloqueos | Logística |
    | **Comunicación** | Crear canal directo con autoridades de seguridad vial (Policía de Carreteras) | Gerencia |
    | **Seguros** | Verificar cobertura de pólizas de terrorismo y seguridad para flota | Administración |
    
    ### 📈 Estrategias de Mediano Plazo (3-12 meses)
    
    | Acción | Descripción | Beneficio |
    |--------|-------------|-----------|
    | **Diversificación de flota** | Evaluar renovación de vehículos con más de 20 años | Reducción de costos de mantenimiento |
    | **Telemática** | Implementar sistemas de monitoreo GPS y gestión de flota | Optimización de rutas y seguridad |
    | **Alianzas estratégicas** | Establecer acuerdos con empresas locales en zonas críticas | Continuidad operativa |
    | **Capacitación** | Entrenar conductores en protocolos de seguridad y atención de emergencias | Reducción de riesgos |
    
    ### 🚀 Estrategias de Largo Plazo (1-3 años)
    
    | Acción | Descripción | Impacto |
    |--------|-------------|---------|
    | **Renovación de flota** | Programa de chatarrización y adquisición de vehículos modernos | Eficiencia y sostenibilidad |
    | **Infraestructura** | Participar en programas de vías terciarias (Caminos Comunitarios) | Mejora de conectividad |
    | **Tecnología** | Implementar plataforma integral de gestión de transporte | Competitividad |
    | **Sostenibilidad** | Evaluar migración a vehículos eléctricos o híbridos | Cumplimiento normativo |
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 📋 Recomendaciones Específicas por Tipo de Ruta
    
    #### Rutas en Zonas de Alto Riesgo (Bajo Cauca, Chocó, Putumayo)
    
    - **Evitar horarios nocturnos** en corredores con presencia de grupos armados
    - **Coordinar con autoridades** militares y de policía para movilización segura
    - **Establecer corredores humanitarios** previamente acordados
    - **Considerar transporte fluvial o aéreo** como alternativa en zonas críticas
    
    #### Rutas con Infraestructura Deficiente (Vías Terciarias)
    
    - **Reducir velocidad** y aumentar distancia de seguridad
    - **Mantenimiento preventivo** más frecuente por desgaste de vehículos
    - **Evaluar costos adicionales** por combustible y tiempo en vías no pavimentadas
    - **Planificar tiempos de entrega** más amplios por condiciones de vía
    
    #### Rutas con Materiales Específicos
    
    - **Verificar compatibilidad** del vehículo con el material a transportar
    - **Capacitar conductores** en manejo de materiales peligrosos o especiales
    - **Contar con equipo de seguridad** adecuado para cada tipo de carga
    """)

# Tab 3: Oportunidades Detectadas
with tab_opor:
    st.subheader("Oportunidades de Mejora Identificadas")
    
    # Calcular oportunidades basadas en los datos
    # 1. Empresas con múltiples rutas afectadas
    empresa_rutas = df_filtrado.groupby('EMPRESAS')['COD RUTA'].nunique().reset_index(name='Rutas')
    empresa_rutas = empresa_rutas.sort_values('Rutas', ascending=False).head(5)
    
    # 2. Rutas con múltiples empresas afectadas
    ruta_empresas = df_filtrado.groupby('COD RUTA')['EMPRESAS'].nunique().reset_index(name='Empresas')
    ruta_empresas = ruta_empresas.sort_values('Empresas', ascending=False).head(5)
    
    # 3. Materiales con más incidencias
    material_incidencias = df_filtrado['MATERIAL PLAN'].value_counts().head(5)
    
    col_opor1, col_opor2 = st.columns(2)
    
    with col_opor1:
        st.markdown("""
        ### 🏢 Oportunidad 1: Consolidación de Empresas
        
        Las empresas con mayor número de rutas afectadas representan una oportunidad para:
        
        - **Negociar acuerdos marco** con condiciones preferenciales
        - **Establecer programas de mejora continua** conjuntos
        - **Optimizar recursos** compartiendo flota en rutas comunes
        - **Reducir costos** por economías de escala
        
        **Empresas prioritarias:**
        """)
        
        for idx, row in empresa_rutas.iterrows():
            st.markdown(f"- **{row['EMPRESAS']}**: {row['Rutas']} rutas afectadas")
    
    with col_opor2:
        st.markdown("""
        ### 🛣️ Oportunidad 2: Optimización de Rutas
        
        Las rutas con mayor concentración de empresas afectadas requieren:
        
        - **Análisis de capacidad** de la vía y puntos críticos
        - **Coordinación entre empresas** para evitar saturación
        - **Inversión en infraestructura** vial prioritaria
        - **Monitoreo constante** de condiciones de seguridad
        
        **Rutas prioritarias:**
        """)
        
        for idx, row in ruta_empresas.iterrows():
            st.markdown(f"- **{row['COD RUTA']}**: {row['Empresas']} empresas afectadas")
    
    st.markdown("---")
    
    st.markdown("""
    ### 📦 Oportunidad 3: Gestión de Materiales
    
    Los materiales con mayor incidencia de incumplimiento requieren:
    
    - **Revisión de procesos** de carga y descarga
    - **Estandarización de protocolos** de transporte
    - **Evaluación de proveedores** alternativos
    - **Implementación de controles** de calidad más estrictos
    
    **Materiales con mayor incidencia:**
    """)
    
    for material, count in material_incidencias.items():
        st.markdown(f"- **{material}**: {count} servicios no cumplidos")
    
    st.markdown("---")
    
    st.markdown("""
    ### 💰 Impacto Económico Estimado
    
    Basado en los datos del sector:
    
    | Concepto | Valor Estimado |
    |----------|----------------|
    | Costo por servicio no cumplido | $2-5 millones COP |
    | Pérdida mensual estimada | $500 millones - $1.500 millones COP |
    | Costo anual proyectado | $6.000 - $18.000 millones COP |
    | Ahorro potencial con optimización | 20-30% |
    
    *Nota: Los valores son estimaciones basadas en promedios del sector transporte de carga en Colombia.*
    """)

st.markdown("---")
st.caption(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
