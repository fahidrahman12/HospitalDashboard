
import streamlit as st
import pandas as pd
import plotly.express as px
import os
st.markdown("## Plots")

## READ DATA
main_dir= os.path.dirname(os.path.abspath(__file__))
df_path= os.path.join(main_dir, '..','..','data','Hospital_Cleaned.csv')
data= pd.read_csv(df_path
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
