# app.py

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tankexport-Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("tanks_data.csv")
    df["Order Year"] = df["Order Year"].astype(int)
    df["Total Contract Year"] = df["Total Contract Year"].astype(int)
    df["Delivery Year"] = df["Delivery Year"].fillna(0).astype(int)
    return df

df = load_data()

st.markdown(
    """
    <style>
    .centered-container {
        max-width: 30%;
        margin: 0 auto;
    }
    </style>
    <div class="centered-container">
    """,
    unsafe_allow_html=True
)

st.title("Tankexport-Dashboard")

top_exporters = (
    df.groupby("Exporter")["Delivery Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .index.tolist()
)
all_exporters = sorted(set(df["Exporter"]) - set(top_exporters))
ordered_exporters = top_exporters + all_exporters

selected_exporter = st.selectbox("Wähle ein Exportland:", ordered_exporters)
filtered_df = df[df["Exporter"] == selected_exporter]

# === Diagramm 1: Gelieferte Panzer nach Importland ===
st.subheader("Verteilung der gelieferten Panzer nach Importland")
delivery_summary = (
    filtered_df.groupby("Importer")["Delivery Quantity"]
    .sum()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots(figsize=(10, 4))
delivery_summary.plot(kind="bar", ax=ax1)
ax1.set_ylabel("Anzahl der Panzer")
ax1.set_xlabel("Importland")
ax1.set_title(f"Panzerlieferungen von {selected_exporter}")
st.pyplot(fig1)

# === Diagramm 2: Bestellte Panzer nach Jahr ===
st.subheader("Bestellte Panzer nach Jahr")
yearly_summary = (
    filtered_df.groupby("Order Year")["Order Quantity"]
    .sum()
    .sort_index()
)

fig2, ax2 = plt.subplots(figsize=(10, 4))
yearly_summary.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Bestellte Panzer")
ax2.set_xlabel("Jahr")
ax2.set_title(f"Panzerbestellungen aus {selected_exporter} nach Jahr")
st.pyplot(fig2)

st.subheader(f"Alle Panzerlieferungen aus {selected_exporter}")

display_df = filtered_df.copy()
display_df["Order Year"] = display_df["Order Year"].astype(str)
display_df["Delivery Year"] = display_df["Delivery Year"].replace(0, "").astype(str)

st.dataframe(display_df[[
    "Importer", "Tank Type", "Order Quantity",
    "Order Year", "Delivery Quantity", "Delivery Year"
]])

st.markdown("</div>", unsafe_allow_html=True)
