import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("🏥 UK Hospitals Map")
#load data
df= pd.read_csv(r'C:\Users\fahed\PycharmProjects\HospitalDashboard\data\Hospital_Cleaned.csv')

## show a quick sumary
st.write(f"Total hospitals sites: {len(df)}")


#### setting colours for sector type####
colour_map= {
    "NHS Sector": [0, 128, 255], #Blue
    "Independent Sector": [255,0 ,0] #Red
}
df["sector_col"]= df['Sector'].map(colour_map)
## map view
# create viewstate- defines mapping attributes
view_state = pdk.ViewState(
    latitude= df['Latitude'].mean(),
    longitude= df['Longitude'].mean(),
    zoom = 5
)
# create layer, here the circles are put on the map
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[Longitude, Latitude]",
    get_color='sector_col',  #points colours
    get_radius=800,
    pickable=True,
)
deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{OrganisationName}\n{ParentName}"}
)

st.pydeck_chart(deck)

### make a small table to represent legend

st.markdown("""
**Legend**

<div>
    <div>
        <span style="background-color: blue; padding: 5px 12px; display: inline-block;"></span>
        &nbsp; NHS sector
    </div>
    <div style="margin-top: 6px;">
        <span style="background-color: red; padding: 5px 12px; display: inline-block;"></span>
        &nbsp; Independent sector
    </div>
</div>
""", unsafe_allow_html=True)