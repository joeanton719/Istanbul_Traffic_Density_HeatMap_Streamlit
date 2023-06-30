import zipfile

import folium
import folium.plugins as plugins
import pandas as pd
import ujson as json
from streamlit_folium import folium_static

import streamlit as st

# Set Wide mode
st.set_page_config(layout="wide")


# read data
zf = zipfile.ZipFile('gh_td.zip') 
gh_td = pd.read_csv(zf.open("gh_td.csv"))


# Loading Json data
@st.cache_data()
def load_json():
    # Open the zip file in read mode
    with zipfile.ZipFile("td_data.zip", "r") as zip_file:

        # Read the JSON file as bytes
        json_data = zip_file.read("td_data.json")

        # Decode the bytes to string
        json_str = json_data.decode("utf-8")

        # Parse the JSON string
        return json.loads(json_str)


data=load_json()

# Display the map using folium_static
with st.spinner('🚦 Hang tight! The heatmap is navigating through the traffic jam of data, almost there!\n'\
                '🚦 Beklemede kal! Isı haritası, veri trafiğinde ilerliyor, neredeyse tamamlandı!'):

        #Title
        st.title('Daily Traffic Density in Istanbul')

        st.text("With this heat map, you can see the average daily traffic density in all parts of Istanbul between January 2020 and April 2023. \n"\
                "The busiest points and important traffic corridors can be observed through this map.")

        st.text("Ocak 2020 ve Nisan 2023 tarihleri arasında İstanbul'un her yerindeki günlük ortalama trafik yoğunluğunu bu ısı haritası ile "\
                "görebilirsiniz. \nEn yoğun noktalar ve önemli trafik koridorları bu harita aracılığıyla gözlemlenebilir.")


# Create a Folium map object
        map = folium.Map(location=[gh_td['LATITUDE'].mean(), gh_td['LONGITUDE'].mean()], zoom_start=10)

        # Add the HeatMapWithTime layer to the map
        hm = plugins.HeatMapWithTime(data, 
                                auto_play=True,
                                index=list(gh_td['DATE_TIME'].unique()),
                                min_opacity=0.05, 
                                max_opacity=0.9,  
                                min_speed=5.5,
                                max_speed=10,
                                speed_step=0.5)

        hm.add_to(map)


        folium_static(map, width=1200, height=500)
