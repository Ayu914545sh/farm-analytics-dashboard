from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="Smart Farm Analytics Dashboard",
    page_icon="🌱",
    layout="wide"
)


# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():

    df = pd.read_csv(
        "Farm_Analytics_Project/data/cleaned/cleaned_farm_data.csv"
    )

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    return df


df = load_data()


# =====================================================
# TITLE
# =====================================================

st.title("🌱 Smart Farm Analytics Dashboard")

st.write(
    "Analysis of farm production, crop performance "
    "and resource utilization."
)

st.divider()


# =====================================================
# FILTERS
# =====================================================

st.sidebar.header("🔍 Filters")


farm_list = sorted(
    df["farm_name"]
    .dropna()
    .unique()
)

selected_farms = st.sidebar.multiselect(
    "Select Farm",
    farm_list,
    default=farm_list
)


crop_list = sorted(
    df["crop_name"]
    .dropna()
    .unique()
)

selected_crops = st.sidebar.multiselect(
    "Select Crop",
    crop_list,
    default=crop_list
)


filtered_df = df[
    (df["farm_name"].isin(selected_farms))
    &
    (df["crop_name"].isin(selected_crops))
].copy()


if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()


# =====================================================
# KPI CARDS
# =====================================================

st.header("📌 Overall Farm Performance")


total_yield = filtered_df["yield_kg"].sum()

total_water = filtered_df["water_used_l"].sum()

total_energy = filtered_df["energy_used_kwh"].sum()

avg_temperature = filtered_df["temperature_c"].mean()


c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Total Yield",
    f"{total_yield:,.0f} kg"
)


c2.metric(
    "Water Used",
    f"{total_water:,.0f} L"
)


c3.metric(
    "Energy Used",
    f"{total_energy:,.1f} kWh"
)


c4.metric(
    "Avg Temperature",
    f"{avg_temperature:.2f} °C"
)


st.divider()


# =====================================================
# INSIGHT 1
# FARM-WISE YIELD
# =====================================================

st.header("🌾 Insight 1: Farm-wise Yield")

farm_yield = (
    filtered_df
    .groupby("farm_name", as_index=False)["yield_kg"]
    .sum()
    .sort_values("yield_kg", ascending=False)
)


fig1 = px.bar(
    farm_yield,
    x="farm_name",
    y="yield_kg",
    text="yield_kg",
    title="Total Yield by Farm",
    labels={
        "farm_name": "Farm",
        "yield_kg": "Yield (kg)"
    }
)


fig1.update_traces(
    texttemplate="<b>%{text:,.0f} kg</b>",
    textposition="outside",
    textfont_size=16,
    cliponaxis=False
)


fig1.update_layout(
    yaxis_range=[
        0,
        farm_yield["yield_kg"].max() * 1.20
    ]
)


st.plotly_chart(
    fig1,
    use_container_width=True
)


st.divider()


# =====================================================
# INSIGHT 2
# CROP-WISE YIELD
# =====================================================

st.header("🥬 Insight 2: Crop-wise Yield")

crop_yield = (
    filtered_df
    .groupby("crop_name", as_index=False)["yield_kg"]
    .sum()
    .sort_values("yield_kg", ascending=False)
)


fig2 = px.bar(
    crop_yield,
    x="crop_name",
    y="yield_kg",
    text="yield_kg",
    title="Total Yield by Crop",
    labels={
        "crop_name": "Crop",
        "yield_kg": "Yield (kg)"
    }
)


fig2.update_traces(
    texttemplate="<b>%{text:,.0f} kg</b>",
    textposition="outside",
    textfont_size=16,
    cliponaxis=False
)


fig2.update_layout(
    yaxis_range=[
        0,
        crop_yield["yield_kg"].max() * 1.20
    ]
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


st.divider()


# =====================================================
# INSIGHT 3
# MONTHLY YIELD TREND
# =====================================================

st.header("📈 Insight 3: Monthly Yield Trend")

monthly_yield = (
    filtered_df
    .groupby("month", as_index=False)["yield_kg"]
    .sum()
    .sort_values("month")
)


fig3 = px.line(
    monthly_yield,
    x="month",
    y="yield_kg",
    markers=True,
    text="yield_kg",
    title="Monthly Yield Trend",
    labels={
        "month": "Month",
        "yield_kg": "Yield (kg)"
    }
)


fig3.update_traces(
    texttemplate="<b>%{text:,.0f}</b>",
    textposition="top center",
    textfont_size=14
)


fig3.update_layout(
    yaxis_range=[
        0,
        monthly_yield["yield_kg"].max() * 1.25
    ]
)


st.plotly_chart(
    fig3,
    use_container_width=True
)


st.divider()


# =====================================================
# INSIGHT 4
# ACTIVITY STATUS
# =====================================================

st.header("✅ Insight 4: Activity Status")

status_data = (
    filtered_df["status"]
    .value_counts()
    .reset_index()
)

status_data.columns = [
    "Status",
    "Count"
]


fig4 = px.pie(
    status_data,
    names="Status",
    values="Count",
    hole=0.4,
    title="Activity Status Distribution"
)


fig4.update_traces(
    textposition="inside",
    textinfo="label+value+percent",
    textfont_size=14
)


st.plotly_chart(
    fig4,
    use_container_width=True
)


st.divider()


# =====================================================
# INSIGHT 5
# WATER EFFICIENCY
# =====================================================

st.header("💧 Insight 5: Water Use Efficiency")

water_data = (
    filtered_df
    .groupby("farm_name", as_index=False)["water_efficiency"]
    .mean()
)


fig5 = px.bar(
    water_data,
    x="farm_name",
    y="water_efficiency",
    text="water_efficiency",
    title="Average Yield per 100 Litres of Water",
    labels={
        "farm_name": "Farm",
        "water_efficiency": "Yield per 100 L Water (kg)"
    }
)


fig5.update_traces(
    texttemplate="<b>%{text:.2f} kg</b>",
    textposition="outside",
    textfont_size=16,
    cliponaxis=False
)


fig5.update_layout(
    yaxis_range=[
        0,
        water_data["water_efficiency"].max() * 1.25
    ]
)


st.plotly_chart(
    fig5,
    use_container_width=True
)


st.divider()


# =====================================================
# INSIGHT 6
# FARM-WISE ENERGY USAGE
# =====================================================

st.header("⚡ Insight 6: Farm-wise Energy Consumption")

energy_data = (
    filtered_df
    .groupby("farm_name", as_index=False)["energy_used_kwh"]
    .sum()
)


fig6 = px.bar(
    energy_data,
    x="farm_name",
    y="energy_used_kwh",
    text="energy_used_kwh",
    title="Total Energy Consumption by Farm",
    labels={
        "farm_name": "Farm",
        "energy_used_kwh": "Energy Used (kWh)"
    }
)


fig6.update_traces(
    texttemplate="<b>%{text:,.1f} kWh</b>",
    textposition="outside",
    textfont_size=16,
    cliponaxis=False
)


fig6.update_layout(
    yaxis_range=[
        0,
        energy_data["energy_used_kwh"].max() * 1.20
    ]
)


st.plotly_chart(
    fig6,
    use_container_width=True
)


st.divider()

# =====================================================
# INSIGHT 7
# FARM EFFICIENCY SCORE
# =====================================================

st.header("🏆 Insight 7: Overall Farm Efficiency Score")

st.write(
    "This custom efficiency score combines water efficiency "
    "and energy efficiency to compare overall resource utilization."
)


efficiency_data = (
    filtered_df
    .groupby("farm_name", as_index=False)
    .agg(
        total_yield=("yield_kg", "sum"),
        total_water=("water_used_l", "sum"),
        total_energy=("energy_used_kwh", "sum")
    )
)


efficiency_data["water_efficiency"] = (
    efficiency_data["total_yield"]
    / efficiency_data["total_water"]
) * 100


efficiency_data["energy_efficiency"] = (
    efficiency_data["total_yield"]
    / efficiency_data["total_energy"]
)


# Normalize values between 0 and 100
def normalize(series):

    if series.max() == series.min():
        return pd.Series(
            [100] * len(series),
            index=series.index
        )

    return (
        (series - series.min())
        /
        (series.max() - series.min())
    ) * 100


efficiency_data["water_score"] = normalize(
    efficiency_data["water_efficiency"]
)

efficiency_data["energy_score"] = normalize(
    efficiency_data["energy_efficiency"]
)


# Combined custom score
efficiency_data["efficiency_score"] = (
    efficiency_data["water_score"]
    +
    efficiency_data["energy_score"]
) / 2


efficiency_data = efficiency_data.sort_values(
    "efficiency_score",
    ascending=False
)


fig7 = px.bar(
    efficiency_data,
    x="farm_name",
    y="efficiency_score",
    text="efficiency_score",
    title="Farm Resource Efficiency Score",
    labels={
        "farm_name": "Farm",
        "efficiency_score": "Efficiency Score"
    }
)


fig7.update_traces(
    texttemplate="<b>%{text:.1f}</b>",
    textposition="outside",
    textfont_size=16,
    cliponaxis=False
)


fig7.update_layout(
    yaxis_range=[0, 110]
)


st.plotly_chart(
    fig7,
    use_container_width=True
)


st.caption(
    "Note: This is a custom project metric combining "
    "water efficiency and energy efficiency equally."
)


st.divider()


# =====================================================
# INSIGHT 8
# YIELD CONSISTENCY
# =====================================================

st.header("📊 Insight 8: Yield Consistency by Farm")

st.write(
    "A farm with a lower coefficient of variation has "
    "more stable and consistent yield across its records."
)


consistency = (
    filtered_df
    .groupby("farm_name")["yield_kg"]
    .agg(["mean", "std"])
    .reset_index()
)


consistency["variation_percent"] = (
    consistency["std"]
    /
    consistency["mean"]
) * 100


consistency = consistency.sort_values(
    "variation_percent"
)


fig8 = px.bar(
    consistency,
    x="farm_name",
    y="variation_percent",
    text="variation_percent",
    title="Yield Variation by Farm",
    labels={
        "farm_name": "Farm",
        "variation_percent": "Yield Variation (%)"
    }
)


fig8.update_traces(
    texttemplate="<b>%{text:.1f}%</b>",
    textposition="outside",
    textfont_size=16,
    cliponaxis=False
)


fig8.update_layout(
    yaxis_range=[
        0,
        consistency["variation_percent"].max() * 1.25
    ]
)


st.plotly_chart(
    fig8,
    use_container_width=True
)


st.caption(
    "Lower variation indicates more consistent production."
)


st.divider()


# =====================================================
# INSIGHT 9
# CROP RESOURCE EFFICIENCY
# =====================================================

st.header("🌿 Insight 9: Crop Resource Efficiency")

st.write(
    "This insight compares how much water and energy "
    "are required to generate crop yield."
)


crop_efficiency = (
    filtered_df
    .groupby("crop_name", as_index=False)
    .agg(
        yield_kg=("yield_kg", "sum"),
        water_used_l=("water_used_l", "sum"),
        energy_used_kwh=("energy_used_kwh", "sum")
    )
)


crop_efficiency = crop_efficiency[
    crop_efficiency["yield_kg"] > 0
].copy()


crop_efficiency["water_per_kg"] = (
    crop_efficiency["water_used_l"]
    /
    crop_efficiency["yield_kg"]
)


crop_efficiency["energy_per_kg"] = (
    crop_efficiency["energy_used_kwh"]
    /
    crop_efficiency["yield_kg"]
)


fig9 = px.scatter(
    crop_efficiency,
    x="water_per_kg",
    y="energy_per_kg",
    text="crop_name",
    size="yield_kg",
    title="Crop Water vs Energy Requirement",
    labels={
        "water_per_kg": "Water Required per kg Yield (L)",
        "energy_per_kg": "Energy Required per kg Yield (kWh)",
        "crop_name": "Crop",
        "yield_kg": "Total Yield"
    }
)


fig9.update_traces(
    textposition="top center"
)


st.plotly_chart(
    fig9,
    use_container_width=True
)


st.caption(
    "Crops closer to the bottom-left use relatively less "
    "water and energy per kilogram of yield."
)


st.divider()


# =====================================================
# INSIGHT 10
# STATUS VS YIELD
# =====================================================

st.header("🚦 Insight 10: Operational Status vs Yield")

st.write(
    "This insight compares average yield across different "
    "operational statuses."
)


status_yield = (
    filtered_df
    .groupby("status", as_index=False)["yield_kg"]
    .mean()
    .sort_values(
        "yield_kg",
        ascending=False
    )
)


fig10 = px.bar(
    status_yield,
    x="status",
    y="yield_kg",
    text="yield_kg",
    title="Average Yield by Activity Status",
    labels={
        "status": "Activity Status",
        "yield_kg": "Average Yield (kg)"
    }
)


fig10.update_traces(
    texttemplate="<b>%{text:.1f} kg</b>",
    textposition="outside",
    textfont_size=16,
    cliponaxis=False
)


fig10.update_layout(
    yaxis_range=[
        0,
        status_yield["yield_kg"].max() * 1.25
    ]
)


st.plotly_chart(
    fig10,
    use_container_width=True
)


st.caption(
    "This is an association in the dataset and does not "
    "by itself prove that activity status causes yield changes."
)


st.divider()


# =====================================================
# INSIGHT 11
# TEMPERATURE PERFORMANCE
# =====================================================

st.header("🌡 Insight 11: Temperature Range vs Yield")

st.write(
    "This insight compares average crop yield under "
    "different temperature ranges."
)


temperature_data = filtered_df.copy()


temperature_data["temperature_range"] = pd.cut(
    temperature_data["temperature_c"],
    bins=[
        0,
        24,
        25,
        26,
        100
    ],
    labels=[
        "Below 24°C",
        "24–25°C",
        "25–26°C",
        "Above 26°C"
    ]
)


temperature_yield = (
    temperature_data
    .groupby(
        "temperature_range",
        observed=False
    )["yield_kg"]
    .mean()
    .reset_index()
)


temperature_yield = temperature_yield.dropna()


fig11 = px.bar(
    temperature_yield,
    x="temperature_range",
    y="yield_kg",
    text="yield_kg",
    title="Average Yield Across Temperature Ranges",
    labels={
        "temperature_range": "Temperature Range",
        "yield_kg": "Average Yield (kg)"
    }
)


fig11.update_traces(
    texttemplate="<b>%{text:.1f} kg</b>",
    textposition="outside",
    textfont_size=16,
    cliponaxis=False
)


fig11.update_layout(
    yaxis_range=[
        0,
        temperature_yield["yield_kg"].max() * 1.25
    ]
)


st.plotly_chart(
    fig11,
    use_container_width=True
)


st.divider()


# =====================================================
# EXECUTIVE SMART INSIGHTS
# =====================================================

st.header("💡 Executive Insights")


# Highest total yield farm
farm_summary = (
    filtered_df
    .groupby("farm_name")["yield_kg"]
    .sum()
)


best_yield_farm = farm_summary.idxmax()

best_yield_value = farm_summary.max()


# Highest yield crop
crop_summary = (
    filtered_df
    .groupby("crop_name")["yield_kg"]
    .sum()
)


best_crop = crop_summary.idxmax()

best_crop_value = crop_summary.max()


# Most water-efficient farm
water_summary = (
    filtered_df
    .groupby("farm_name")
    .agg({
        "yield_kg": "sum",
        "water_used_l": "sum"
    })
)


water_summary["efficiency"] = (
    water_summary["yield_kg"]
    /
    water_summary["water_used_l"]
) * 100


best_water_farm = (
    water_summary["efficiency"]
    .idxmax()
)


best_water_value = (
    water_summary["efficiency"]
    .max()
)


# Completed percentage
done_count = (
    filtered_df["status"]
    .str.lower()
    .eq("done")
    .sum()
)


completion_rate = (
    done_count
    /
    len(filtered_df)
) * 100


a, b = st.columns(2)


with a:

    st.success(
        f"🌾 Highest total yield: "
        f"{best_yield_farm} "
        f"({best_yield_value:,.0f} kg)"
    )

    st.info(
        f"🥬 Highest-yield crop: "
        f"{best_crop} "
        f"({best_crop_value:,.0f} kg)"
    )


with b:

    st.success(
        f"💧 Highest water efficiency: "
        f"{best_water_farm} "
        f"({best_water_value:.2f} kg per 100 L)"
    )

    st.info(
        f"✅ Activity completion rate: "
        f"{completion_rate:.1f}%"
    )


st.caption(
    "Executive insights automatically update when "
    "dashboard filters are changed."
)


st.divider()


# =====================================================
# CLEAN DATA TABLE
# =====================================================

st.header("📋 Cleaned Farm Dataset")

st.write(
    f"Total filtered records: {len(filtered_df)}"
)


st.dataframe(
    filtered_df,
    use_container_width=True
)
