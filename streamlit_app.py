import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set page title
st.set_page_config(page_title="Cereal Production Analysis")

# Add a title to the sidebar section
st.sidebar.title("Settings")

# Add a title to the main section
st.title("Cereal Production Analysis")


@st.cache_data
def get_data():
    # Load the data
    data = pd.read_csv("cereal_production_data.csv")

    # Get the unique country names from the data
    countries = data["Entity"].unique()

    return data, countries


# Call the function to get the data and countries
data, countries = get_data()


# Add a selectbox to choose the country
selected_country = st.sidebar.selectbox(
    "Select Country",
    countries.tolist(),
    index=int(np.where(countries == "World")[0][0]),
)

# Add a subtitle for the data section
# Add a title to the line chart
st.subheader(f"Cereal Production Metrics for {selected_country}")
# Filter the data for the selected country
filtered_data = data[data["Entity"] == selected_country].copy()

# Add a slider for setting the starting year
start_year = st.sidebar.slider(
    "Starting Year",
    min_value=int(filtered_data["Year"].min()),
    max_value=int(filtered_data["Year"].max()),
)

# Calculate the relative change based on the starting year
filtered_data.loc[:, "Area harvested (hectares)"] = (
    filtered_data["Area harvested (hectares)"]
    / filtered_data.loc[
        filtered_data["Year"] == start_year, "Area harvested (hectares)"
    ].values[0]
) * 100
filtered_data.loc[:, "Production (tonnes)"] = (
    filtered_data["Production (tonnes)"]
    / filtered_data.loc[
        filtered_data["Year"] == start_year, "Production (tonnes)"
    ].values[0]
) * 100
filtered_data.loc[:, "Yield (tonnes per hectare)"] = (
    filtered_data["Yield (tonnes per hectare)"]
    / filtered_data.loc[
        filtered_data["Year"] == start_year, "Yield (tonnes per hectare)"
    ].values[0]
) * 100
filtered_data.loc[:, "Population (historical estimates)"] = (
    filtered_data["Population (historical estimates)"]
    / filtered_data.loc[
        filtered_data["Year"] == start_year, "Population (historical estimates)"
    ].values[0]
) * 100


# Add a button for selecting the chart display option
chart_display_option = st.sidebar.radio(
    "Chart Display Option", ["All Together", "Split by Metric"]
)

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

    # Set x-axis limits
    ax.set_xlim(start_year, filtered_data["Year"].max())

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
    axs[0].set_xlim(start_year, filtered_data["Year"].max())  # Set x-axis limits

    axs[1].plot(
        filtered_data["Year"], filtered_data["Production (tonnes)"], color="orange"
    )
    axs[1].set_xlabel("Year")
    axs[1].set_ylabel("Relative Change")
    axs[1].set_title("Production")
    axs[1].set_xlim(start_year, filtered_data["Year"].max())  # Set x-axis limits

    axs[2].plot(
        filtered_data["Year"],
        filtered_data["Yield (tonnes per hectare)"],
        color="green",
    )
    axs[2].set_xlabel("Year")
    axs[2].set_ylabel("Relative Change")
    axs[2].set_title("Yield")
    axs[2].set_xlim(start_year, filtered_data["Year"].max())  # Set x-axis limits

    axs[3].plot(
        filtered_data["Year"],
        filtered_data["Population (historical estimates)"],
        color="red",
    )
    axs[3].set_xlabel("Year")
    axs[3].set_ylabel("Relative Change")
    axs[3].set_title("Population")
    axs[3].set_xlim(start_year, filtered_data["Year"].max())  # Set x-axis limits

    # Adjust spacing between subplots
    fig.tight_layout()

    # Display the charts using Streamlit's native `pyplot` command
    st.pyplot(fig)

# Display the filtered data table
st.write(filtered_data)
