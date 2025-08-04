
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import datetime

st.set_page_config(page_title="Oasis Re Hurricane Simulator", layout="centered")

st.title("🌀 Oasis Re: Hurricane Loss Simulator")
st.markdown("""
Welcome to the Oasis Re catastrophe simulator. This tool allows institutional users, DAO treasuries, and LPs
to model hurricane-driven loss scenarios and capital-at-risk profiles in real time.

Use the sliders to simulate a season and visualize your Probable Maximum Loss (PML) curve.
""")

st.sidebar.header("Simulation Controls")
num_simulations = st.sidebar.slider("Number of Simulations", 100, 5000, 1000, step=100)
max_exposure = st.sidebar.slider("Max Exposure per Location (Billion USD)", 1.0, 10.0, 5.0, step=0.5)
storm_intensity_max = st.sidebar.slider("Max Storm Intensity (Category)", 1, 5, 5)

st.sidebar.markdown("---")
st.sidebar.markdown("**Live NOAA Feed Placeholder**")
st.sidebar.markdown("Last Update: " + str(datetime.datetime.utcnow()) + " UTC")
st.sidebar.markdown("_Live storm data integration coming soon._")

# Exposure setup (mock)
exposure_coords = [(-80, 26), (-77, 30), (-74, 35), (-71, 40)]
exposure_values = np.linspace(1.0, max_exposure, len(exposure_coords))

# Simulation function
def simulate_storm_loss():
    total_loss = 0
    landfall_lon = np.random.uniform(-82, -70)
    landfall_lat = np.random.uniform(25, 40)
    intensity = np.random.randint(1, storm_intensity_max + 1)
    for (lon, lat), value in zip(exposure_coords, exposure_values):
        dist = np.sqrt((lon - landfall_lon)**2 + (lat - landfall_lat)**2)
        if dist < 10:
            loss = (intensity**2) / (dist + 1) * value * 0.05
            total_loss += min(loss, value)
    return total_loss

# Run simulations
losses = [simulate_storm_loss() for _ in range(num_simulations)]
sorted_losses = np.sort(losses)[::-1]
exceedance_prob = np.arange(1, num_simulations + 1) / (num_simulations + 1)

# Plot PML Curve
fig, ax = plt.subplots()
ax.plot(exceedance_prob * 100, sorted_losses, label='PML Curve')
ax.set_xlabel("Exceedance Probability (%)")
ax.set_ylabel("Total Loss (Billion USD)")
ax.set_title("Simulated PML Curve for Hurricane Season")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Summary stats
st.subheader("Loss Summary")
st.write(f"**Average Annual Loss (AAL):** ${np.mean(losses):.2f}B")
st.write(f"**Worst Case Loss (1-in-100):** ${np.percentile(losses, 1):.2f}B")
st.write(f"**Best Case Loss:** ${np.min(losses):.2f}B")

# Footer
st.markdown("""---\n_Oasis Re © 2025. All rights reserved. For institutional use only._""")
