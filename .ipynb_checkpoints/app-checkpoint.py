# # # ============================================================
# # # STREAMLIT APP
# # # Crime Mapping & Prediction System
# # # ============================================================

# # # -----------------------------
# # # 1. IMPORT REQUIRED LIBRARIES
# # # -----------------------------

# # import streamlit as st
# # import pandas as pd
# # import folium
# # import joblib

# # from streamlit_folium import folium_static

# # model = joblib.load("crime_model.pkl")
# # scaler = joblib.load("scaler.pkl")
# # encoders = joblib.load("encoders.pkl")
# # feature_order = joblib.load("feature_order.pkl")


# # # -------------------------------------------------
# # # 2. PAGE CONFIGURATION
# # # -------------------------------------------------

# # st.set_page_config(
# #     page_title="Crime Mapping & Prediction",
# #     layout="wide"
# # )

# # st.title("Crime Mapping & Prediction System")
# # st.subheader("GIS-based Spatial Analysis of Kidnapping Hotspots")


# # # -------------------------------------------------
# # # 3. LOAD DATASET
# # # -------------------------------------------------

# # # Load the crime dataset
# # data = pd.read_csv("crime.csv")

# # st.write("### Dataset Preview")
# # st.dataframe(data.head())


# # # -------------------------------------------------
# # # 4. CREATE INTERACTIVE MAP
# # # -------------------------------------------------

# # st.write("### Kidnapping Incidents Map")

# # # Create base map centered around Nigeria
# # crime_map = folium.Map(
# #     location=[9.08, 8.67],
# #     zoom_start=6
# # )

# # # Add markers for each crime location
# # for i, row in data.iterrows():

# #     folium.Marker(
# #         location=[row["Latitude"], row["Longitude"]],
# #         popup=f"""
# #         State: {row['State']} <br>
# #         LGA: {row['LGA']} <br>
# #         Victims: {row['Victims']}
# #         """,
# #         icon=folium.Icon(color="red", icon="info-sign")
# #     ).add_to(crime_map)


# # # Display map
# # folium_static(crime_map)


# # # -------------------------------------------------
# # # 5. LOAD TRAINED MODEL
# # # -------------------------------------------------

# # # This model should be saved during training
# # try:
# #     model = joblib.load("crime_model.pkl")
# #     model_loaded = True
# # except:
# #     model_loaded = False


# # # -------------------------------------------------
# # # 6. USER INPUT SECTION
# # # -------------------------------------------------

# # st.write("## Predict Kidnapping Risk")

# # col1, col2 = st.columns(2)

# # with col1:

# #     victims = st.number_input(
# #         "Number of Victims",
# #         min_value=1,
# #         max_value=50,
# #         value=5
# #     )

# #     latitude = st.number_input(
# #         "Latitude",
# #         value=9.0
# #     )

# # with col2:

# #     longitude = st.number_input(
# #         "Longitude",
# #         value=8.0
# #     )

# #     past_crime_count = st.number_input(
# #         "Past Crime Count",
# #         min_value=0,
# #         max_value=50,
# #         value=3
# #     )


# # # MAKE PREDICTION

# # if st.button("Predict Risk"):

# #     if model_loaded:

# #         input_data = pd.DataFrame({
# #             "Latitude":[latitude],
# #             "Longitude":[longitude],
# #             "Victims":[victims],
# #             "past_crime_count":[past_crime_count]
# #         })

# #         prediction = model.predict(input_data)

# #         st.success(f"Predicted Risk Level: {prediction[0]}")

# #     else:

# #         st.warning("Model file not found. Please train and save the model.")


# # # -------------------------------------------------
# # # 8. HOTSPOT VISUALIZATION
# # # -------------------------------------------------

# # st.write("## Crime Hotspots")

# # heat_map = folium.Map(
# #     location=[9.08, 8.67],
# #     zoom_start=6
# # )

# # for i, row in data.iterrows():

# #     folium.CircleMarker(
# #         location=[row["Latitude"], row["Longitude"]],
# #         radius=5,
# #         color="red",
# #         fill=True,
# #         fill_color="red"
# #     ).add_to(heat_map)

# # folium_static(heat_map)


# # # -------------------------------------------------
# # # 9. STATISTICS SECTION
# # # -------------------------------------------------

# # st.write("## Crime Statistics")

# # col1, col2, col3 = st.columns(3)

# # col1.metric("Total Incidents", len(data))
# # col2.metric("Total States", data["State"].nunique())
# # col3.metric("Total Victims", data["Victims"].sum())

# # =========================================================
# # CRIME MAPPING & PREDICTION STREAMLIT APP
# # =========================================================

# import streamlit as st
# import pandas as pd
# import joblib


# # ---------------------------------------------------------
# # 1. LOAD TRAINED MODEL AND ARTIFACTS
# # ---------------------------------------------------------

# model = joblib.load("crime_model.pkl")
# scaler = joblib.load("scaler.pkl")
# encoders = joblib.load("encoders.pkl")
# feature_order = joblib.load("feature_order.pkl")


# # ---------------------------------------------------------
# # 2. PAGE CONFIGURATION
# # ---------------------------------------------------------

# st.set_page_config(page_title="Crime Prediction System")

# st.title("Crime Mapping & Prediction System")
# st.write("Predict kidnapping risk level based on location and incident data.")


# # ---------------------------------------------------------
# # 3. USER INPUT SECTION
# # ---------------------------------------------------------

# st.subheader("Enter Incident Information")

# latitude = st.number_input("Latitude", value=7.4)
# longitude = st.number_input("Longitude", value=3.9)
# victims = st.number_input("Number of Victims", min_value=1, value=2)

# state = st.selectbox(
#     "State",
#     encoders["State"].classes_
# )

# incident_type = st.selectbox(
#     "Incident Type",
#     encoders["Incident_Type"].classes_
# )

# time_of_day = st.selectbox(
#     "Time of Day",
#     encoders["Time_of_Day"].classes_
# )

# severity = st.selectbox(
#     "Severity",
#     encoders["Severity"].classes_
# )


# # ---------------------------------------------------------
# # 4. CREATE INPUT DATAFRAME
# # ---------------------------------------------------------

# input_data = pd.DataFrame({
#     "Latitude":[latitude],
#     "Longitude":[longitude],
#     "Victims":[victims],
#     "State":[state],
#     "Incident_Type":[incident_type],
#     "Time_of_Day":[time_of_day],
#     "Severity":[severity]
# })


# # ---------------------------------------------------------
# # 5. APPLY ENCODING
# # ---------------------------------------------------------

# for col in encoders:
#     input_data[col] = encoders[col].transform(input_data[col])


# # ---------------------------------------------------------
# # 6. APPLY SCALING
# # ---------------------------------------------------------

# numerical_columns = ["Latitude","Longitude","Victims"]

# input_data[numerical_columns] = scaler.transform(
#     input_data[numerical_columns]
# )


# # ---------------------------------------------------------
# # 7. MATCH TRAINING FEATURE STRUCTURE
# # ---------------------------------------------------------

# for col in feature_order:

#     if col not in input_data.columns:
#         input_data[col] = 0

# input_data = input_data[feature_order]


# # ---------------------------------------------------------
# # 8. PREDICTION
# # ---------------------------------------------------------

# if st.button("Predict Crime Risk"):

#     prediction = model.predict(input_data)

#     st.success(f"Predicted Risk Level: {prediction[0]}")

# ============================================================
# STREAMLIT APP
# Crime Mapping & Prediction System
# ============================================================

# -------------------------------------------------
# 1. IMPORT REQUIRED LIBRARIES
# -------------------------------------------------

import streamlit as st
import pandas as pd
import folium
import joblib
from streamlit_folium import folium_static


# -------------------------------------------------
# 2. LOAD TRAINED MODEL AND ARTIFACTS
# -------------------------------------------------

model = joblib.load("crime_model.pkl")
scaler = joblib.load("scaler.pkl")
encoders = joblib.load("encoders.pkl")
feature_order = joblib.load("feature_order.pkl")


# -------------------------------------------------
# 3. PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Crime Mapping & Prediction System",
    layout="wide"
)

st.title("Crime Mapping & Prediction System")
st.subheader("GIS-Based Spatial Analysis of Kidnapping Hotspots")


# -------------------------------------------------
# 4. LOAD DATASET
# -------------------------------------------------

data = pd.read_csv("crime.csv")

st.write("### Dataset Preview")
st.dataframe(data.head())


# -------------------------------------------------
# 5. CREATE INTERACTIVE MAP
# -------------------------------------------------

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