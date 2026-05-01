import streamlit as st
import pandas as pd
import joblib
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.express as px
from datetime import datetime

# ---------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------
st.set_page_config(
    page_title="Crime Mapping and Prediction System",
    layout="wide"
)

st.title("🛡️ Crime Mapping and Prediction Dashboard")

# ---------------------------------------------
# LOAD DATA (CACHED)
# ---------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("crime.csv")
    # Convert Date to datetime and extract useful time features
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Hour'] = pd.to_datetime(df['Time_of_Day'], format='%H:%M:%S', errors='coerce').dt.hour
    # Fallback: if Time_of_Day is categorical like "Morning", map it roughly
    time_map = {"Morning": 9, "Afternoon": 14, "Evening": 18, "Night": 22}
    df['Hour'] = df['Hour'].fillna(df['Time_of_Day'].map(time_map))
    return df

df = load_data()

# ---------------------------------------------
# LOAD MODEL (CACHED)
# ---------------------------------------------
@st.cache_resource
def load_model():
    try:
        model = joblib.load("crime_model.pkl")
        scaler = joblib.load("scaler.pkl")
        return model, scaler
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None, None

model, scaler = load_model()

# ---------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------
page = st.sidebar.selectbox(
    "Navigation",
    ["Overview", "Kidnapping Incident Map", "Crime Hotspot Map", 
     "Crime Prediction", "Crime Statistics"]
)

# =============================================
# OVERVIEW PAGE
# =============================================
if page == "Overview":
    st.header("Crime Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Crimes Recorded", len(df))
    col2.metric("Incident Types", df["Incident_Type"].nunique())
    col3.metric("States", df["State"].nunique())
    col4.metric("Average Victims", round(df["Victims"].mean(), 1))

    st.write("### Sample Dataset")
    st.dataframe(df.head(10), use_container_width=True)

# =============================================
# KIDNAPPING INCIDENT MAP  (Fixed: use Incident_Type)
# =============================================
elif page == "Kidnapping Incident Map":
    st.header("Kidnapping / High-Risk Incident Map")

    # You can change the filter to whatever makes sense (e.g. School/Church attacks are often kidnapping-related)
    high_risk_df = df[df["Incident_Type"].isin(["School", "Church"])]

    st.write(f"Showing **{len(high_risk_df)}** incidents (Schools & Churches)")

    m = folium.Map(location=[7.38, 3.95], zoom_start=8, tiles="CartoDB dark_matter")

    for _, row in high_risk_df.iterrows():
        folium.Marker(
            [row["Latitude"], row["Longitude"]],
            popup=f"{row['Incident_Type']} | Victims: {row['Victims']} | {row['Date'].date()}",
            icon=folium.Icon(color="red", icon="exclamation-triangle", prefix="fa")
        ).add_to(m)

    st_folium(m, width=900, height=600)

# =============================================
# CRIME HOTSPOT MAP
# =============================================
elif page == "Crime Hotspot Map":
    st.header("Crime Hotspot Map")

    m = folium.Map(location=[7.38, 3.95], zoom_start=8, tiles="CartoDB positron")

    heat_data = df[["Latitude", "Longitude"]].values.tolist()
    HeatMap(heat_data, radius=15, blur=10, max_zoom=13).add_to(m)

    st_folium(m, width=900, height=600)

# =============================================
# CRIME PREDICTION
# =============================================
elif page == "Crime Prediction":
    st.header("Crime Risk Prediction")

    if model is None or scaler is None:
        st.warning("Model or scaler not loaded. Prediction unavailable.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            latitude = st.number_input("Latitude", value=7.38, format="%.6f")
            longitude = st.number_input("Longitude", value=3.95, format="%.6f")
            month = st.selectbox("Month", list(range(1, 13)), index=2)

        with col2:
            day = st.selectbox("Day", list(range(1, 32)), index=14)
            # Hour input (better UX)
            hour = st.slider("Hour of Day", 0, 23, value=14)

        if st.button("🔮 Predict Crime Risk", type="primary"):
            input_data = pd.DataFrame({
                "Latitude": [latitude],
                "Longitude": [longitude],
                "Month": [month],
                "Day": [day],
                "Hour": [hour]
            })

            try:
                input_scaled = scaler.transform(input_data)
                prediction = model.predict(input_scaled)

                # Assuming your model outputs risk level or probability
                if isinstance(prediction[0], (int, float)) and prediction[0] > 1:
                    risk_text = f"High Risk (Class {int(prediction[0])})"
                    st.error(f"**Predicted Crime Risk:** {risk_text}")
                else:
                    st.success(f"**Predicted Crime Risk:** {prediction[0]}")
            except Exception as e:
                st.error(f"Prediction error: {e}. Check that input features match the trained model.")

# =============================================
# CRIME STATISTICS
# =============================================
elif page == "Crime Statistics":
    st.header("Crime Statistics")

    st.subheader("Incident Type Distribution")
    fig = px.bar(
        df["Incident_Type"].value_counts().reset_index(),
        x="Incident_Type",
        y="count",
        labels={"count": "Number of Incidents", "Incident_Type": "Incident Type"},
        color="Incident_Type"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Crime Trend")
    monthly = df.groupby("Month").size().reset_index(name="Crimes")
    fig2 = px.line(
        monthly,
        x="Month",
        y="Crimes",
        markers=True,
        labels={"Crimes": "Number of Crimes"}
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Victims by Severity")
    fig3 = px.box(df, x="Severity", y="Victims", color="Severity")
    st.plotly_chart(fig3, use_container_width=True)