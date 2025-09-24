import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
import helper

# --- Page Config ---
st.set_page_config(
    page_title="Marine Life Analytics",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

df = pd.read_csv("marine_dataset.csv")

# --- Custom CSS for Stylish Background & Containers ---
st.markdown("""
    <style>
    /* Full-page gradient background */
    .stApp {
        background: linear-gradient(135deg, #74ebd5, #ACB6E5);
        background-attachment: fixed;
    }

    /* Hide default Streamlit menu & footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Header styling */
    h1, h2, h3, h4 {
        color: #1E90FF;
        font-family: 'Helvetica', sans-serif;
    }

    /* KPI Card Styling */
    .metric-container {
        background: rgba(30,144,255,0.85);
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
        font-weight: bold;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.2);
        font-size: 18px;
    }

    /* Container for charts */
    .chart-container {
        background-color: rgba(255,255,255,0.85);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.15);
    }

    </style>
""", unsafe_allow_html=True)

# --- Sidebar Filters ---
st.sidebar.header("Filters")
selected_specie_1 = st.sidebar.selectbox("Specie for Yearly Abundance", helper.species_list)
selected_specie_2 = st.sidebar.selectbox("Specie for Temp vs Abundance", helper.species_list)
selected_specie_3 = st.sidebar.selectbox("Specie for Length vs Oxygen", helper.species_list)
selected_specie_4 = st.sidebar.selectbox("Specie for Location Analysis", helper.species_list)

# --- Title ---
st.markdown("<h1 style='text-align:center;'>🌊 Marine Life Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- KPI Cards ---
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f"<div class='metric-container'>Total Species<br>{len(df['Fish_Species'].unique())}</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-container'>Avg Fish Abundance<br>{round(df['Fish_Abundance'].mean(),2)}</div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metric-container'>Avg Water Temp (°C)<br>{round(df['Water_Temp_C'].mean(),2)}</div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='metric-container'>Avg Dissolved Oxygen (mg/L)<br>{round(df['Dissolved_Oxygen_mgL'].mean(),2)}</div>", unsafe_allow_html=True)

st.markdown("---")

# --- Tabs for Organized Sections ---
tabs = st.tabs(["Yearly Trends", "Distribution & Abundance", "Relationships", "Location Analysis", "Correlation"])

# --- Yearly Trends Tab ---
with tabs[0]:
    st.subheader("Yearly Fish Abundance")
    with st.container():
        fig1 = helper.yearly_fish_abundance(helper.get_specie_df(selected_specie_1), selected_specie_1)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.subheader("Yearly Trend of Average Dissolved Oxygen")
    with st.container():
        fig2 = helper.yearly_dissolved_oxygen()
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- Distribution & Abundance Tab ---
with tabs[1]:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Species Distribution")
        fig3 = helper.get_species_distribution()
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.subheader("Fish Abundance by Species")
        fig4 = px.box(df, x="Fish_Species", y="Fish_Abundance", color="Fish_Species",
                      title="Fish Abundance by Species", points="all")
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- Relationships Tab ---
with tabs[2]:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Abundance vs Water Temperature")
        fig5 = helper.abundance_vs_water_temp(helper.get_specie_df(selected_specie_2), selected_specie_2)
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.subheader("Fish Length vs Dissolved Oxygen")
        fig6 = helper.fish_length_vs_oxygen(helper.get_specie_df(selected_specie_3), selected_specie_3)
        st.plotly_chart(fig6, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- Location Analysis Tab ---
with tabs[3]:
    st.subheader("Fish Abundance Across Locations")
    fig7 = helper.abundance_vs_coord(helper.get_specie_df(selected_specie_4), selected_specie_4)
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Correlation Tab ---
with tabs[4]:
    st.subheader("Correlation Heatmap")
    corr_cols = ["Water_Temp_C","Salinity_PSU","pH","Dissolved_Oxygen_mgL","Chlorophyll_mg_m3","Fish_Abundance", "Fish_Length_cm"]
    corr = df[corr_cols].corr().values
    fig8 = ff.create_annotated_heatmap(
        z=corr,
        x=corr_cols,
        y=corr_cols,
        colorscale='RdBu',
        zmin=-1, zmax=1,
        showscale=True
    )
    fig8.update_layout(title_text="Correlation Heatmap of Ocean Parameters & Fish Abundance", title_x=0.5)
    st.plotly_chart(fig8, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("<p style='text-align:center; color: gray;'>📊 Developed by Team - BluMind</p>", unsafe_allow_html=True)
