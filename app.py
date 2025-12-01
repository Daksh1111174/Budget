import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="India Budget Analysis 2014–2025", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("Budget 2014-2025.csv")

df = load_data()

st.title("📊 India Budget Explorer (2014–2025)")

# Show raw data
if st.checkbox("Show Dataset"):
    st.dataframe(df, use_container_width=True)

# Select ministry
ministry = st.selectbox("Select Ministry", sorted(df["Ministry Name"].unique()))

filtered = df[df["Ministry Name"] == ministry]

st.subheader(f"📌 Budget Trend for: {ministry}")

fig = px.bar(
    filtered,
    x="Year",
    y="Total Plan & Non-Plan",
    title=f"Total Budget Over Time — {ministry}",
    labels={"Total Plan & Non-Plan": "Total Budget (₹ Crores)"},
)
st.plotly_chart(fig, use_container_width=True)


# Compare multiple ministries
st.subheader("📌 Compare Budgets Between Ministries")

ministries = st.multiselect(
    "Select Ministries to Compare",
    sorted(df["Ministry Name"].unique()),
    default=[ministry]
)

compare_df = df[df["Ministry Name"].isin(ministries)]

fig2 = px.line(
    compare_df,
    x="Year",
    y="Total Plan & Non-Plan",
    color="Ministry Name",
    markers=True,
    title="Comparative Budget of Ministries",
)
st.plotly_chart(fig2, use_container_width=True)

# Summary statistics
st.subheader("📌 Budget Statistics")

st.write(compare_df.groupby("Ministry Name")["Total Plan & Non-Plan"].describe())

st.success("App Loaded Successfully ✔")
