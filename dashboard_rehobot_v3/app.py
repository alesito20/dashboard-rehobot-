
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Corporación Rehobot | GEESOP",page_icon="🏭",layout="wide")
COLORS={"Objetivo 1":"#2878D0","Objetivo 2":"#159A83","Objetivo 3":"#E58A32","Objetivo 4":"#8257C5"}
DARK="#14263D"

# Información base tomada de las hojas de desarrollo y Resultados-Indicadores.
OBJ={
"Objetivo 1":{
"title":"Optimización del flujo de preparación y despacho",
"problem":"Tiempos improductivos por búsqueda, preparación y traslado de materiales y herramientas.",
"tools":[
 {"name":"Clasificación ABC","purpose":"Priorizar materiales y recursos según su importancia y movimiento.","actions":["Identificar los ítems utilizados en la preparación de servicios","Organizar la información para distinguir categorías A, B y C","Priorizar el control y la ubicación de los recursos de mayor importancia"],"visual":"abc"},
 {"name":"Redistribución / Slotting + Espagueti","purpose":"Ubicar los recursos de mayor rotación cerca de la zona de preparación y despacho y reducir recorridos cruzados.","actions":["Revisar la distribución física y las ubicaciones actuales","Reubicar los recursos de mayor rotación cerca del despacho","Comparar el recorrido y tiempo de preparación antes y después"],"visual":"route"},
 {"name":"Kanban","purpose":"Facilitar la identificación visual de disponibilidad y necesidad de reposición.","actions":["Definir señales visuales para los recursos que requieren reposición","Establecer el punto de aviso y responsable de reposición","Verificar la disponibilidad antes de preparar el servicio"],"visual":"kanban"}],
"metrics":[["Tiempo de preparación y despacho por solicitud",85,60,"min","reduction"],["Distancia recorrida por ciclo de preparación",120,78,"m","reduction"]],
"econ":[1632,1152,480,434,0,46],
"route":["Diagnóstico del almacén","Clasificación ABC","Redistribución / Slotting","Señalización Kanban","Preparación y despacho optimizados"]},
"Objetivo 2":{
"title":"Estandarización de procedimientos operativos",
"problem":"Sobreprocesamiento y variabilidad en la ejecución de las actividades del servicio.",
"tools":[
 {"name":"Análisis de operaciones","purpose":"Descomponer la actividad para distinguir VA, NVA y NVAN e identificar oportunidades de simplificación.","actions":["Levantar la secuencia actual del servicio","Clasificar las actividades en VA, NVA y NVAN","Identificar esperas, consultas y reprocesos que pueden eliminarse"],"visual":"operations"},
 {"name":"Procedimiento Operativo Estándar (POE)","purpose":"Documentar una secuencia uniforme con responsables, tiempos, criterios de calidad y seguridad.","actions":["Definir la secuencia estándar de 15 pasos","Incorporar orden de trabajo, checklist, herramientas verificadas y protocolo LOTO","Establecer controles y pruebas de funcionamiento"],"visual":"poe"},
 {"name":"Metodología 5S","purpose":"Mantener clasificación, orden, limpieza, estandarización y disciplina en el almacén y zona de trabajo.","actions":["Seiri: retirar objetos innecesarios","Seiton: definir ubicaciones y rotulación","Seiso: limpiar el área y los recursos","Seiketsu: establecer estándares visibles","Shitsuke: realizar auditorías y seguimiento"],"visual":"5s"}],
"metrics":[["Tiempo de ciclo del servicio",371.25,288,"min","reduction"],["Cumplimiento general 5S",14,78,"%","increase"],["Costo de actividades NVA",71.25,3,"S/ por servicio","reduction"]],
"econ":[371.25,288,1665,290,0,1375],
"route":["Diagnóstico del servicio","Análisis de operaciones","Diseño del POE","Aplicación de 5S","Ejecución estandarizada"]},
"Objetivo 3":{
"title":"Evaluación y mejora ergonómica de las actividades",
"problem":"Exposición a posturas desfavorables y movimientos innecesarios durante instalación y mantenimiento.",
"tools":[
 {"name":"Evaluación OWAS","purpose":"Codificar espalda, brazos, piernas y carga para clasificar las posturas y priorizar acciones.","actions":["Observar las fases de trabajo y registrar posturas cada 30 segundos","Codificar espalda, brazos, piernas y carga","Clasificar las combinaciones en categorías de acción OWAS 1 a 4","Priorizar las operaciones críticas"],"visual":"owas"},
 {"name":"Estudio de tiempos","purpose":"Medir tiempos observados, calcular tiempo normal y determinar el tiempo estándar.","actions":["Registrar 10 ciclos por operación","Calcular el tiempo promedio observado","Aplicar valoración y suplementos para determinar el tiempo estándar","Comparar los tiempos iniciales y mejorados"],"visual":"times"},
 {"name":"Estudio de movimientos","purpose":"Examinar desplazamientos, reposicionamientos y acciones innecesarias para mejorar la secuencia de trabajo.","actions":["Identificar movimientos y alcances innecesarios","Organizar herramientas según la operación","Mejorar el posicionamiento de componentes","Estandarizar la secuencia y verificar el resultado"],"visual":"motion"}],
"metrics":[["Tiempo estándar por servicio",72.94,56.47,"min","reduction"],["Tiempo de ejecución por servicio",72.94,56.47,"min","reduction"]],
"econ":[13785.66,10672.83,3112.83,2250,150,712.83],
"route":["Diagnóstico postural","Evaluación OWAS","Priorización de posturas","Estudio de tiempos y movimientos","Adecuación y estándar de trabajo"]},
"Objetivo 4":{
"title":"Control y exactitud del inventario",
"problem":"Dificultad para conocer qué hay, cuánto hay, dónde está y quién tiene los equipos y herramientas.",
"tools":[
 {"name":"Kardex","purpose":"Registrar entradas, salidas y saldos por código, fecha, documento y destino.","actions":["Asignar códigos únicos a los ítems","Registrar cada entrada y salida por movimiento","Controlar saldo por ítem y documento","Mantener trazabilidad por obra o proveedor"],"visual":"kardex"},
 {"name":"Ubicaciones codificadas","purpose":"Identificar la ubicación física mediante zona, estante, nivel y posición.","actions":["Definir zonas A, B, C y herramientas","Asignar códigos Estante-Nivel-Posición","Rotular estantes, niveles y posiciones","Registrar ubicación en el Kardex"],"visual":"locations"},
 {"name":"Clasificación ABC","purpose":"Priorizar el control del inventario de acuerdo con el valor y la importancia de los ítems.","actions":["Calcular el valor de inventario por ítem","Ordenar los ítems según su participación","Asignar categoría A, B o C","Definir frecuencia de control según categoría"],"visual":"abc_inventory"},
 {"name":"Conteo cíclico","purpose":"Verificar periódicamente el inventario físico frente al registro y corregir diferencias.","actions":["Programar conteos periódicos","Comparar saldo físico con saldo del Kardex","Registrar diferencias y causas","Actualizar los registros y dar seguimiento a la exactitud"],"visual":"cycle"}],
"metrics":[["Exactitud del registro de inventario (ERI)",58.33,100,"%","increase"],["Herramientas devueltas a tiempo",33.33,70,"%","increase"]],
"econ":[1980,6.5,1973.5,204,216,1553.5],
"route":["Diagnóstico del cuaderno","Kardex","Ubicaciones codificadas","Clasificación ABC","Conteo cíclico y verificación"]}}

# Datos operativos que sí aparecen cuantificados en el libro de trabajo.
OWAS=pd.DataFrame({"Categoría OWAS":[1,2,3,4],"Frecuencia":[2,2,0,1],"Acción":["Mantener","Programar corrección","Corrección próxima","Intervención inmediata"]})
BACK=pd.DataFrame({"Posición de espalda":["Recta","Doblada","Con giro","Doblada y girada"],"Frecuencia":[140,140,80,40]})
ARMS=pd.DataFrame({"Posición de brazos":["Ambos bajos","Un brazo elevado","Ambos elevados"],"Frecuencia":[280,100,20]})
LEGS=pd.DataFrame({"Posición de piernas":["De pie, ambas rectas","Una recta y otra flexionada","Ambas flexionadas","Ambas flexionadas y desequilibradas","Arrodillado","Caminando"],"Frecuencia":[180,40,60,20,80,20]})
FIVE_S=pd.DataFrame({"S":["Seiri","Seiso"],"Antes":[20,30],"Después":[85,65]})
ABC_INV=pd.DataFrame({"Código":["EB-01","EB-02","HI-01","HI-02","HI-03","HI-04","EL-01","EL-02","EL-03"],
"Ítem":["Electrobomba sumergible","Electrobomba centrífuga","Tubería HDPE","Válvula check","Perno galvanizado","Codo PVC","Cable sumergible","Tablero de control","Kit de empalme"],
"Valor inventario (S/)":[4700,620,1428,405,325,487.5,2364,950,70],
"Clase ABC":["A","C","B","B","C","C","A","A","A"]})
KARDEX=pd.DataFrame({"Fecha":["01/10/2026","01/10/2026","01/10/2026","07/10/2026","07/10/2026"],
"Código":["EB-01","HI-01","EL-01","HI-01","EL-01"],"Documento":["OS-101","OS-101","OS-101","F001-0318","F002-1127"],
"Entrada":[1,0,0,100,150],"Salida":[0,60,70,0,0],"Saldo":[1,90,130,190,280]})
METRICS={}
for key,d in OBJ.items():
    METRICS[key]=pd.DataFrame([{"Indicador":m[0],"Antes":m[1],"Después":m[2],"Unidad":m[3]} for m in d["metrics"]])

def money(x): return f"S/ {x:,.2f}"
def fmt(x,u):
    if u=="%": return f"{x:.2f}%"
    if u=="min": return f"{x:.2f} min"
    if u=="m": return f"{x:.2f} m"
    return money(x)
def pct(a,b,kind):
    return (a-b)/a*100 if kind=="reduction" else b-a

st.markdown("""<style>
.stApp{background:#F4F7FB}.block-container{padding-top:1.2rem;max-width:1600px}
.hero{padding:24px 28px;border-radius:18px;background:linear-gradient(115deg,#14263D,#2B4C70);color:white;margin-bottom:18px}
.hero h1{color:white;margin:0;font-size:2rem}.hero p{color:#D8E6F3;margin:6px 0 0}
div[data-testid="stMetric"]{background:white;border:1px solid #DFE7F0;border-radius:14px;padding:13px 16px}
.card{background:white;border:1px solid #DFE7F0;border-radius:14px;padding:15px;margin-bottom:8px}
</style>""",unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>Corporación Rehobot</h1><p>Dashboard dinámico de mejora operativa · Proyecto GEESOP</p></div>',unsafe_allow_html=True)

page=st.sidebar.radio("Panel de navegación",["Resumen general","Objetivo 1","Objetivo 2","Objetivo 3","Objetivo 4","Comparativa general","Impacto económico","Flujo de caja"])
st.sidebar.caption("Selecciona un objetivo y luego una herramienta para recorrer su implementación paso a paso.")

def route_chart(steps,color):
    n=len(steps)
    fig=go.Figure()
    for i,s in enumerate(steps):
        fig.add_trace(go.Scatter(x=[i],y=[0],mode="markers+text",text=[s],textposition="bottom center",
          marker=dict(size=34,color=color,line=dict(color="white",width=3)),showlegend=False,
          hovertemplate=f"Etapa {i+1}: {s}<extra></extra>"))
        if i<n-1:
            fig.add_annotation(x=i+0.5,y=0,ax=i+0.08,ay=0,axref="x",ayref="y",xref="x",yref="y",
              text="➜",showarrow=False,font=dict(size=24,color="#64748B"))
    fig.update_layout(template="plotly_white",height=220,xaxis=dict(visible=False,range=[-0.5,n-.5]),
      yaxis=dict(visible=False,range=[-0.6,.6]),margin=dict(l=10,r=10,t=20,b=60))
    return fig

def tool_visual(key,tool):
    vis=tool["visual"]
    if vis=="abc":
        df=pd.DataFrame({"Categoría":["A","B","C"],"Prioridad de control":[3,2,1]})
        fig=px.funnel(df,x="Prioridad de control",y="Categoría",color="Categoría",
          color_discrete_map={"A":COLORS[key],"B":"#75A9DF","C":"#C9D8E8"},title="Secuencia de priorización ABC")
        st.plotly_chart(fig,use_container_width=True)
        st.caption("La distribución cuantitativa ABC debe vincularse al registro de materiales clasificados de esta herramienta.")
    elif vis=="route":
        stages=pd.DataFrame({"Punto":["Almacén","Zona de selección","Preparación","Despacho"],"Orden":[1,2,3,4]})
        fig=px.line(stages,x="Orden",y="Punto",markers=True,title="Ruta de preparación y despacho")
        fig.update_traces(line_color=COLORS[key],marker_size=14)
        fig.update_layout(template="plotly_white",height=330,xaxis_visible=False)
        st.plotly_chart(fig,use_container_width=True)
        st.info("El plano de recorrido Spaghetti puede sustituirse por el plano real del almacén cuando se incorpore la distribución física.")
    elif vis=="kanban":
        cols=st.columns(3)
        for c,(h,t) in zip(cols,[("Disponible","Material listo para preparar"),("Reponer","Alerta de stock mínimo"),("En preparación","Recurso reservado para servicio")]):
            c.markdown(f'<div class="card"><h3>{h}</h3><p>{t}</p></div>',unsafe_allow_html=True)
        st.caption("Tablero visual de estados Kanban. Los registros se pueden editar en la tabla de seguimiento.")
    elif vis=="operations":
        df=pd.DataFrame({"Tipo de actividad":["VA","NVA","NVAN"],"Antes (min)":[180,71.25,120],"Después (min)":[168,3,117]})
        fig=go.Figure()
        for c in ["Antes (min)","Después (min)"]:
            fig.add_trace(go.Bar(name=c,x=df["Tipo de actividad"],y=df[c]))
        fig.update_layout(barmode="group",template="plotly_white",title="Composición del tiempo del servicio",height=350)
        st.plotly_chart(fig,use_container_width=True)
    elif vis=="poe":
        df=pd.DataFrame({"Fase":["Orden de trabajo","Preparación","Seguridad / LOTO","Ejecución","Verificación y cierre"],"Control":[1,1,1,1,1]})
        fig=px.scatter(df,x="Control",y="Fase",size="Control",color="Fase",title="Puntos de control del POE")
        fig.update_layout(template="plotly_white",height=330,showlegend=False,xaxis_visible=False)
        st.plotly_chart(fig,use_container_width=True)
        st.metric("Pasos del POE","15")
    elif vis=="5s":
        edited=st.data_editor(FIVE_S,key="five_s_editor",use_container_width=True,num_rows="fixed")
        fig=go.Figure()
        fig.add_trace(go.Scatterpolar(r=edited["Antes"],theta=edited["S"],fill="toself",name="Antes",line_color="#94A3B8"))
        fig.add_trace(go.Scatterpolar(r=edited["Después"],theta=edited["S"],fill="toself",name="Después",line_color=COLORS[key]))
        fig.update_layout(template="plotly_white",title="Radar de auditoría 5S (escala 0–100)",polar=dict(radialaxis=dict(range=[0,100])),height=420)
        st.plotly_chart(fig,use_container_width=True)
    elif vis=="owas":
        a,b=st.columns(2)
        with a:
            fig=px.bar(OWAS,x="Categoría OWAS",y="Frecuencia",color="Categoría OWAS",
              color_discrete_sequence=["#2E8B57","#E4B84A","#E67E22","#C0392B"],title="Frecuencia por categoría OWAS")
            fig.update_layout(template="plotly_white",height=340)
            st.plotly_chart(fig,use_container_width=True)
        with b:
            fig=px.bar(BACK,x="Posición de espalda",y="Frecuencia",color_discrete_sequence=[COLORS[key]],title="Distribución de posturas de espalda")
            fig.update_layout(template="plotly_white",height=340,xaxis_tickangle=-25)
            st.plotly_chart(fig,use_container_width=True)
        st.markdown("**Registros de evaluación OWAS (editable)**")
        ed=st.data_editor(OWAS,key="owas_editor",use_container_width=True,num_rows="dynamic")
        st.download_button("Descargar registros OWAS editados",ed.to_csv(index=False).encode("utf-8"),"registros_owas.csv","text/csv")
    elif vis=="times":
        df=pd.DataFrame({"Actividad":["Preparación","Manipulación","Ajuste","Fijación"],"Inicial":[9.41,14.12,11.76,16.47],"Mejorado":[8.24,14.12,9.41,12.94]})
        fig=go.Figure()
        fig.add_trace(go.Bar(x=df["Actividad"],y=df["Inicial"],name="Inicial",marker_color="#9AA8B8"))
        fig.add_trace(go.Bar(x=df["Actividad"],y=df["Mejorado"],name="Mejorado",marker_color=COLORS[key]))
        fig.update_layout(barmode="group",template="plotly_white",title="Tiempo estándar por actividad",height=360)
        st.plotly_chart(fig,use_container_width=True)
        st.caption("Los tiempos por actividad se muestran como componentes del estudio. El total del indicador principal se toma de Resultados-Indicadores.")
    elif vis=="motion":
        steps=["Preparar herramientas","Manipular equipos","Ajustar componentes","Fijar y verificar"]
        fig=go.Figure(go.Sankey(node=dict(label=steps,pad=22,thickness=20,color=[COLORS[key]]*4),
          link=dict(source=[0,1,2],target=[1,2,3],value=[1,1,1],color="rgba(130,87,197,.25)")))
        fig.update_layout(title="Secuencia de movimientos del trabajo",height=320,template="plotly_white")
        st.plotly_chart(fig,use_container_width=True)
    elif vis=="kardex":
        ed=st.data_editor(KARDEX,key="kardex_editor",use_container_width=True,num_rows="dynamic")
        fig=px.line(ed,x="Fecha",y="Saldo",color="Código",markers=True,title="Evolución de saldos registrados")
        fig.update_layout(template="plotly_white",height=350)
        st.plotly_chart(fig,use_container_width=True)
        st.download_button("Descargar Kardex editado",ed.to_csv(index=False).encode("utf-8"),"kardex_editado.csv","text/csv")
    elif vis=="locations":
        grid=pd.DataFrame({"Zona":["A","B","C","Herramientas"],"Ubicación":["E01","E02","E03","E04"],"Uso":["Alta rotación","Rotación media","Baja rotación","Equipos reutilizables"]})
        st.dataframe(grid,use_container_width=True,hide_index=True)
        fig=px.treemap(grid,path=["Zona","Ubicación"],values=[1,1,1,1],color="Zona",title="Mapa lógico de zonas del almacén")
        fig.update_layout(template="plotly_white",height=350)
        st.plotly_chart(fig,use_container_width=True)
    elif vis=="abc_inventory":
        ed=st.data_editor(ABC_INV,key="abc_inv_editor",use_container_width=True,num_rows="dynamic")
        fig=px.treemap(ed,path=["Clase ABC","Código"],values="Valor inventario (S/)",color="Clase ABC",
          color_discrete_map={"A":COLORS[key],"B":"#A58AD5","C":"#DCCFF0"},title="Composición del valor de inventario por ABC")
        fig.update_layout(template="plotly_white",height=390)
        st.plotly_chart(fig,use_container_width=True)
        st.download_button("Descargar clasificación ABC editada",ed.to_csv(index=False).encode("utf-8"),"clasificacion_abc.csv","text/csv")
    elif vis=="cycle":
        df=pd.DataFrame({"Control":["Exactitud ERI","Devolución oportuna"],"Antes":[58.33,33.33],"Después":[100,70],"Meta":[90,70]})
        fig=go.Figure()
        for c in ["Antes","Después","Meta"]:
            fig.add_trace(go.Bar(name=c,x=df["Control"],y=df[c]))
        fig.update_layout(barmode="group",template="plotly_white",title="Verificación del control de inventario (%)",height=350,yaxis_range=[0,110])
        st.plotly_chart(fig,use_container_width=True)

def objective_page(key):
    d=OBJ[key]; color=COLORS[key]
    st.markdown(f'<div style="background:{color};padding:17px 22px;border-radius:14px;color:white"><h2 style="color:white;margin:0">{key} · {d["title"]}</h2><p style="margin:5px 0 0">Ruta de herramientas e implementación interactiva</p></div>',unsafe_allow_html=True)
    st.markdown("**Problema:** "+d["problem"])
    st.subheader("Ruta completa del objetivo")
    st.plotly_chart(route_chart(d["route"],color),use_container_width=True)
    names=[t["name"] for t in d["tools"]]
    selected=st.selectbox("Selecciona la herramienta para explorar su desarrollo",names,key=f"tool_{key}")
    idx=names.index(selected); tool=d["tools"][idx]
    st.markdown(f'<div class="card" style="border-left:6px solid {color}"><h3>{idx+1}. {tool["name"]}</h3><p>{tool["purpose"]}</p></div>',unsafe_allow_html=True)
    left,right=st.columns([1,1.25])
    with left:
        st.markdown("#### Secuencia de trabajo")
        for n,action in enumerate(tool["actions"],1):
            st.markdown(f"**{n}.** {action}")
        st.markdown("#### Avance en la ruta")
        st.progress((idx+1)/len(names),text=f"Herramienta {idx+1} de {len(names)}")
    with right:
        st.markdown("#### Visualización de la herramienta")
        tool_visual(key,tool)
    st.markdown("---")
    st.subheader("Indicadores editables del objetivo")
    st.caption("Puedes modificar los valores Antes y Después. Las tarjetas y la gráfica se actualizan con los valores editados durante esta sesión.")
    if key not in st.session_state:
        st.session_state[key]=METRICS[key].copy()
    edited=st.data_editor(st.session_state[key],key=f"metrics_{key}",use_container_width=True,num_rows="fixed",
       column_config={"Antes":st.column_config.NumberColumn(format="%.2f"),"Después":st.column_config.NumberColumn(format="%.2f")})
    st.session_state[key]=edited
    cols=st.columns(len(edited))
    for col,(_,r) in zip(cols,edited.iterrows()):
        kind=next((m[4] for m in d["metrics"] if m[0]==r["Indicador"]),"reduction")
        delta=pct(r["Antes"],r["Después"],kind)
        label=f"{delta:.2f}% reducción" if kind=="reduction" else f"+{delta:.2f} puntos"
        col.metric(r["Indicador"],fmt(r["Después"],r["Unidad"]),label,help=f"Antes: {fmt(r['Antes'],r['Unidad'])}")
    fig=go.Figure()
    for _,r in edited.iterrows():
        fig.add_trace(go.Scatter(x=[r["Antes"],r["Después"]],y=[r["Indicador"]]*2,mode="lines+markers+text",
          text=["Antes","Después"],textposition=["top center","bottom center"],line=dict(color=color,width=6),
          marker=dict(size=14,color=["#8998A9",color]),name=r["Indicador"]))
    fig.update_layout(template="plotly_white",title="Comparación dinámica AS-IS / TO-BE",height=350,xaxis_title="Valor del indicador")
    st.plotly_chart(fig,use_container_width=True)
    st.download_button("Descargar indicadores editados",edited.to_csv(index=False).encode("utf-8"),f"{key.lower().replace(' ','_')}_indicadores.csv","text/csv")
    st.subheader("Impacto económico individual")
    before,after,gross,investment,recurring,net=d["econ"]
    a,b,c,e=st.columns(4)
    a.metric("Ahorro / beneficio bruto",money(gross))
    b.metric("Inversión inicial",money(investment))
    c.metric("Costo recurrente",money(recurring))
    e.metric("Beneficio neto primer año",money(net))
    wf=go.Figure(go.Waterfall(x=["Beneficio bruto","Inversión","Recurrentes","Neto primer año"],measure=["relative","relative","relative","total"],
      y=[gross,-investment,-recurring,0],text=[money(gross),money(-investment),money(-recurring),money(net)],textposition="outside",
      increasing={"marker":{"color":color}},decreasing={"marker":{"color":"#D66B5D"}},totals={"marker":{"color":DARK}}))
    wf.update_layout(template="plotly_white",title="Puente económico del objetivo",height=360)
    st.plotly_chart(wf,use_container_width=True)
    st.caption("Los cambios en las tablas editables son temporales durante la sesión. Descarga el CSV si deseas conservarlos.")

if page=="Resumen general":
    st.subheader("Resumen ejecutivo")
    inv=sum(d["econ"][3] for d in OBJ.values()); gross=sum(d["econ"][2] for d in OBJ.values())
    rec=sum(d["econ"][4] for d in OBJ.values()); net=gross-inv-rec
    cols=st.columns(4)
    cols[0].metric("Objetivos",4); cols[1].metric("Inversión total",money(inv))
    cols[2].metric("Beneficio bruto anual",money(gross)); cols[3].metric("Beneficio neto primer año",money(net))
    st.subheader("Mapa de herramientas y rutas")
    cards=st.columns(4)
    for col,(key,d) in zip(cards,OBJ.items()):
        with col:
            st.markdown(f'<div class="card" style="border-top:6px solid {COLORS[key]}"><b>{key}</b><p>{d["title"]}</p><b>{len(d["tools"])} herramientas / etapas</b></div>',unsafe_allow_html=True)
    st.subheader("Flujo integrado de los cuatro objetivos")
    for key,d in OBJ.items():
        st.markdown(f"**{key}**")
        st.plotly_chart(route_chart(d["route"],COLORS[key]),use_container_width=True)
    econ=pd.DataFrame({"Objetivo":list(OBJ.keys()),"Beneficio bruto":[d["econ"][2] for d in OBJ.values()],"Inversión":[d["econ"][3] for d in OBJ.values()]})
    fig=px.bar(econ,x="Objetivo",y=["Beneficio bruto","Inversión"],barmode="group",title="Beneficio e inversión por objetivo")
    fig.update_layout(template="plotly_white",height=380)
    st.plotly_chart(fig,use_container_width=True)

elif page in OBJ:
    objective_page(page)

elif page=="Comparativa general":
    st.subheader("Comparativa general AS-IS / TO-BE")
    rows=[]
    for key,d in OBJ.items():
        for m in d["metrics"]:
            change=pct(m[1],m[2],m[4])
            rows.append({"Objetivo":key,"Indicador":m[0],"Antes":m[1],"Después":m[2],"Unidad":m[3],"Variación":change})
    df=pd.DataFrame(rows)
    st.dataframe(df,use_container_width=True,hide_index=True)
    fig=px.bar(df,x="Variación",y="Indicador",color="Objetivo",orientation="h",color_discrete_map=COLORS,
      title="Magnitud de la mejora por indicador")
    fig.update_layout(template="plotly_white",height=600)
    st.plotly_chart(fig,use_container_width=True)
    heat=df.pivot_table(index="Objetivo",columns="Indicador",values="Variación")
    fig=px.imshow(heat,text_auto=".1f",aspect="auto",color_continuous_scale="Tealgrn",title="Mapa de calor de las variaciones")
    fig.update_layout(template="plotly_white",height=420)
    st.plotly_chart(fig,use_container_width=True)

elif page=="Impacto económico":
    st.subheader("Impacto económico consolidado")
    df=pd.DataFrame([{"Objetivo":k,"Beneficio bruto":d["econ"][2],"Inversión":d["econ"][3],"Costos recurrentes":d["econ"][4],"Beneficio neto primer año":d["econ"][5]} for k,d in OBJ.items()])
    st.dataframe(df.style.format({c:"S/ {:,.2f}" for c in df.columns if c!="Objetivo"}),use_container_width=True,hide_index=True)
    fig=px.bar(df,x="Objetivo",y=["Beneficio bruto","Inversión","Costos recurrentes"],barmode="group",title="Componentes económicos por objetivo")
    fig.update_layout(template="plotly_white",height=420)
    st.plotly_chart(fig,use_container_width=True)
    fig=go.Figure(go.Waterfall(x=["Beneficio bruto O1","O2","O3","O4","Inversión total","Costos recurrentes"],measure=["relative"]*6,
      y=[d["econ"][2] for d in OBJ.values()]+[-sum(d["econ"][3] for d in OBJ.values()),-sum(d["econ"][4] for d in OBJ.values())]))
    fig.update_layout(template="plotly_white",title="Waterfall consolidado",height=420)
    st.plotly_chart(fig,use_container_width=True)

elif page=="Flujo de caja":
    st.subheader("Flujo de caja consolidado")
    inv=sum(d["econ"][3] for d in OBJ.values()); gross=sum(d["econ"][2] for d in OBJ.values()); rec=sum(d["econ"][4] for d in OBJ.values())
    cok=0.12; n=5; flows=[-inv]+[gross-rec]*n; cum=np.cumsum(flows)
    df=pd.DataFrame({"Periodo":["Año 0"]+[f"Año {i}" for i in range(1,n+1)],"Inversión":[-inv]+[0]*n,
      "Beneficio bruto":[0]+[gross]*n,"Costos recurrentes":[0]+[-rec]*n,"Flujo neto":flows,"Flujo acumulado":cum})
    st.dataframe(df.style.format({c:"S/ {:,.2f}" for c in df.columns if c!="Periodo"}),use_container_width=True,hide_index=True)
    van=sum(flows[t]/((1+cok)**t) for t in range(len(flows)))
    try:
        import numpy_financial as npf
        tir=npf.irr(flows)
    except Exception: tir=None
    c=st.columns(3); c[0].metric("VAN (COK 12%)",money(van)); c[1].metric("TIR",f"{tir:.2%}" if tir is not None else "No calculada"); c[2].metric("Flujo neto anual",money(gross-rec))
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df["Periodo"],y=df["Flujo neto"],mode="lines+markers",name="Flujo neto",line=dict(color="#2878D0",width=4)))
    fig.add_trace(go.Scatter(x=df["Periodo"],y=df["Flujo acumulado"],mode="lines+markers",name="Flujo acumulado",line=dict(color="#159A83",width=4,dash="dash")))
    fig.add_hline(y=0,line_dash="dot",line_color="#64748B")
    fig.update_layout(template="plotly_white",title="Evolución del flujo neto y acumulado",height=430,yaxis_title="Soles (S/)")
    st.plotly_chart(fig,use_container_width=True)
    st.warning("Proyección constante a cinco años con COK de 12%. Validar los flujos individuales del libro antes de usar la evaluación como resultado definitivo.")

st.markdown("---")
st.caption("Los módulos de edición permiten ajustar datos durante la sesión y descargar CSV. Los cambios no modifican automáticamente el Excel original.")
