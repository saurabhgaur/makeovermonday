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

# Create a sidebar for selecting the country and chart display option
selected_country = st.sidebar.selectbox("Select Country", data["Entity"].unique())
chart_display_option = st.sidebar.radio(
    "Chart Display Option", ["All Together", "Split by Metric"]
)

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

# Line chart(s) based on the chart display option
if chart_display_option == "All Together":
    # Single chart with all metrics together
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        filtered_data["Year"],
        filtered_data["Area harvested (hectares)"],
        label="Area harvested",
        color="blue",
    )
    ax.plot(
        filtered_data["Year"],
        filtered_data["Production (tonnes)"],
        label="Production",
        color="orange",
    )
    ax.plot(
        filtered_data["Year"],
        filtered_data["Yield (tonnes per hectare)"],
        label="Yield",
        color="green",
    )
    ax.plot(
        filtered_data["Year"],
        filtered_data["Population (historical estimates)"],
        label="Population",
        color="red",
    )

    ax.set_xlabel("Year")
    ax.set_ylabel("Relative Change")
    ax.set_title(f"Data for {selected_country}")
    ax.legend()

    # Display the chart using Streamlit's native `pyplot` command
    st.pyplot(fig)
else:
    # Split chart for each metric
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    axs = axs.ravel()

    axs[0].plot(
        filtered_data["Year"], filtered_data["Area harvested (hectares)"], color="blue"
    )
    axs[0].set_xlabel("Year")
    axs[0].set_ylabel("Relative Change")
    axs[0].set_title("Area harvested")

    axs[1].plot(
        filtered_data["Year"], filtered_data["Production (tonnes)"], color="orange"
    )
    axs[1].set_xlabel("Year")
    axs[1].set_ylabel("Relative Change")
    axs[1].set_title("Production")

    axs[2].plot(
        filtered_data["Year"],
        filtered_data["Yield (tonnes per hectare)"],
        color="green",
    )
    axs[2].set_xlabel("Year")
    axs[2].set_ylabel("Relative Change")
    axs[2].set_title("Yield")

    axs[3].plot(
        filtered_data["Year"],
        filtered_data["Population (historical estimates)"],
        color="red",
    )
    axs[3].set_xlabel("Year")
    axs[3].set_ylabel("Relative Change")
    axs[3].set_title("Population")

    # Adjust spacing between subplots
    fig.tight_layout()

    # Display the charts using Streamlit's native `pyplot` command
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
