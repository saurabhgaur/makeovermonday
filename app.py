import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
data = pd.read_csv("cereal_production_data.csv")

# Set page title and layout using Tailwind CSS
st.set_page_config(page_title="Cereal Production Dashboard", layout="wide")

# Set the title and description of the dashboard
st.title("Cereal Production Dashboard")
st.markdown("This dashboard visualizes cereal production data.")

# Create a sidebar for selecting the country
selected_country = st.sidebar.selectbox("Select Country", data["Entity"].unique())

# Filter the data based on the selected country
filtered_data = data[data["Entity"] == selected_country]

# Calculate the relative change for each series compared to the first year
first_year = filtered_data["Year"].min()

filtered_data["Area harvested (hectares)"] = (
    filtered_data["Area harvested (hectares)"]
    / filtered_data.loc[
        filtered_data["Year"] == first_year, "Area harvested (hectares)"
    ].values[0]
)

filtered_data["Production (tonnes)"] = (
    filtered_data["Production (tonnes)"]
    / filtered_data.loc[
        filtered_data["Year"] == first_year, "Production (tonnes)"
    ].values[0]
)

filtered_data["Yield (tonnes per hectare)"] = (
    filtered_data["Yield (tonnes per hectare)"]
    / filtered_data.loc[
        filtered_data["Year"] == first_year, "Yield (tonnes per hectare)"
    ].values[0]
)

filtered_data["Population (historical estimates)"] = (
    filtered_data["Population (historical estimates)"]
    / filtered_data.loc[
        filtered_data["Year"] == first_year, "Population (historical estimates)"
    ].values[0]
)

# Line chart with years on the x-axis and different lines for each metric
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(
    filtered_data["Year"],
    filtered_data["Area harvested (hectares)"],
    label="Area harvested",
)
ax.plot(filtered_data["Year"], filtered_data["Production (tonnes)"], label="Production")
ax.plot(
    filtered_data["Year"], filtered_data["Yield (tonnes per hectare)"], label="Yield"
)
ax.plot(
    filtered_data["Year"],
    filtered_data["Population (historical estimates)"],
    label="Population",
)

ax.set_xlabel("Year")
ax.set_ylabel("Relative Change")
ax.set_title(f"Data for {selected_country}")
ax.legend()

# Display the chart using Streamlit's native `pyplot` command
st.pyplot(fig)

# Show the data table
st.subheader("Data Table")
st.dataframe(filtered_data)

# Show the description of the columns
st.subheader("Column Descriptions")
st.markdown(
    """
- Area harvested (hectares): The relative change in the total area of land used for cereal production compared to the first year present in the data.
- Production (tonnes): The relative change in the total production of cereals compared to the first year present in the data.
- Yield (tonnes per hectare): The relative change in the average yield of cereals per hectare compared to the first year present in the data.
- Population (historical estimates): The relative change in the historical population estimates compared to the first year present in the data.
"""
)
