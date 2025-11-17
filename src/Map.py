import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("🏥 England Hospitals Dashboard")
st.markdown("## Map")
#load data
df= pd.read_csv(r'C:\Users\fahed\PycharmProjects\HospitalDashboard\data\Hospital_Cleaned.csv')

df.info()
## show a quick summary
st.write(f"Total hospitals sites: {len(df)}")

#Add sidebar widgets
st.sidebar.header("Filters")
st.sidebar.write("Use these options to filter")
st.sidebar.subheader("Filter by sector")
sector_options = ["All"] + sorted(df["Sector"].unique().tolist())
sector_code = st.sidebar.selectbox("Select sector", sector_options)
st.sidebar.subheader("Filter by City/Town")
city_options = ["All"] + sorted(df["City"].dropna().unique().tolist())
city_code = st.sidebar.selectbox("Select City/Town", city_options)
# Apply the filters
filtered_df = df.copy()

if sector_code!="All":
    filtered_df = filtered_df[filtered_df['Sector']==sector_code]

if city_code!="All":
    filtered_df = filtered_df[filtered_df['City']==city_code]


#### setting colours for sector type####
colour_map= {
    "NHS Sector": [0, 128, 255], #Blue
    "Independent Sector": [255,0 ,0] #Red
}
filtered_df["sector_col"]= filtered_df['Sector'].map(colour_map)
## map view
# create viewstate- defines mapping attributes
view_state = pdk.ViewState(
    latitude= filtered_df['Latitude'].mean(),
    longitude= filtered_df['Longitude'].mean(),
    zoom = 5
)
# create layer, here the circles are put on the map
layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df,
    get_position=["Longitude", "Latitude"],  # FIXED
    get_color="sector_col",
    get_radius=800,
    pickable=True
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style=None,  # FIXED — avoids black background
    tooltip={"text": "{OrganisationName}\n{ParentName}\nAddress: {Address}"}
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
