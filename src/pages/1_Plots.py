
import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("## Plots")

## READ DATA
data = pd.read_csv(
    r'C:\Users\fahed\PycharmProjects\HospitalDashboard\data\Hospital.csv'
)

#count Hospitals per sector
sector_counts= data['Sector'].value_counts().reset_index()
sector_counts.columns= ["Sector", "Count"]

print(sector_counts)
fig_sector= px.pie(sector_counts, values='Count', names='Sector', color= 'Sector',
                   color_discrete_map={
                       'Independent Sector': 'rgb(255, 0, 0)',
                       'NHS Sector': 'rgb(0, 128, 255)'
                   })

st.plotly_chart(fig_sector)
