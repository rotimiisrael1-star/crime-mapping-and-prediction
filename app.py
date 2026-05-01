# STREAMLIT APP
# Crime Mapping & Prediction System

# IMPORT REQUIRED LIBRARIES

import streamlit as st
import pandas as pd
import folium
import joblib
from streamlit_folium import folium_static


# LOAD TRAINED MODEL AND ARTIFACTS

model = joblib.load("crime_model.pkl")
scaler = joblib.load("scaler.pkl")
encoders = joblib.load("encoders.pkl")
feature_order = joblib.load("feature_order.pkl")

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Crime Mapping & Prediction System",
    layout="wide"
)

st.title("Crime Mapping & Prediction System")
st.subheader("GIS-Based Spatial Analysis of Kidnapping Hotspots")

# LOAD DATASET

data = pd.read_csv("combined.csv")

st.write("### Dataset Preview")
st.dataframe(data.head())


# CREATE INTERACTIVE MAP
st.write("### Kidnapping Incidents Map")

crime_map = folium.Map(
    location=[9.08, 8.67],   # Nigeria center
    zoom_start=6
)

for i, row in data.iterrows():

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"""
        State: {row['State']} <br>
        LGA: {row['LGA']} <br>
        Victims: {row['Victims']}
        """,
        icon=folium.Icon(color="red")
    ).add_to(crime_map)

folium_static(crime_map)


# USER INPUT SECTION
st.write("## Predict Kidnapping Risk")

col1, col2 = st.columns(2)

with col1:

    latitude = st.number_input(
        "Latitude",
        value=7.4
    )

    victims = st.number_input(
        "Number of Victims",
        min_value=1,
        value=2
    )

    state = st.selectbox(
        "State",
        encoders["State"].classes_
    )

    incident_type = st.selectbox(
        "Incident Type",
        encoders["Incident_Type"].classes_
    )

with col2:

    longitude = st.number_input(
        "Longitude",
        value=3.9
    )

    time_of_day = st.selectbox(
        "Time of Day",
        encoders["Time_of_Day"].classes_
    )

    severity = st.selectbox(
        "Severity",
        encoders["Severity"].classes_
    )

# CREATE INPUT DATAFRAME

input_data = pd.DataFrame({

    "Latitude":[latitude],
    "Longitude":[longitude],
    "Victims":[victims],
    "State":[state],
    "Incident_Type":[incident_type],
    "Time_of_Day":[time_of_day],
    "Severity":[severity]
})


# APPLY LABEL ENCODING

for col in encoders:

    input_data[col] = encoders[col].transform(input_data[col])


# APPLY SCALING

numerical_columns = ["Latitude","Longitude","Victims"]

input_data[numerical_columns] = scaler.transform(
    input_data[numerical_columns]
)


# MATCH TRAINING FEATURE STRUCTURE

for col in feature_order:

    if col not in input_data.columns:
        input_data[col] = 0

input_data = input_data[feature_order]


# MAKE PREDICTION

if st.button("Predict Crime Risk"):

    prediction = model.predict(input_data)

    st.success(f"Predicted Risk Level: {prediction[0]}")


# HOTSPOT VISUALIZATION

st.write("## Crime Hotspots")

heat_map = folium.Map(
    location=[9.08, 8.67],
    zoom_start=6
)

for i, row in data.iterrows():

    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=5,
        color="red",
        fill=True
    ).add_to(heat_map)

folium_static(heat_map)


# CRIME STATISTICS

st.write("## Crime Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Incidents", len(data))
col2.metric("Total States", data["State"].nunique())
col3.metric("Total Victims", data["Victims"].sum())
