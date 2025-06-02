

import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# Function to format large numbers
def format_number(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    else:
        return str(n)


# Page configuration
st.set_page_config(page_title="Flight Analysis Dashboard", page_icon="✈️", layout="wide", initial_sidebar_state="expanded")


# CSS style f
st.markdown("""
    <style>
    .kpi-card {
        background-color: #c7d9be;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease-in-out;
        margin: 10px;
    }
    .kpi-card:hover {
        transform: scale(1.02);
        background-color: #5e8d83;
        color: #fff;
    }
    .kpi-label {
        font-size: 16px;
        font-weight: 600;
        color: #2f3e46;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 34px;
        font-weight: 800;
        color: #1b4332;
        margin-bottom: 5px;
    }
    .kpi-delta {
        font-size: 14px;
        font-weight: 500;
        color: #6c757d;
    }
    .kpi-card:hover .kpi-delta {
        color: #e6f4ea;
    }
    </style>
""", unsafe_allow_html=True)


# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Flight_Canselled_Delay_C.csv", parse_dates=["fl_date"])
    return df

df = load_data()

# Sidebar filters
st.sidebar.markdown("## 🧭 Filters")
st.sidebar.markdown("---")

# Date Range Selector
min_date = df['fl_date'].min().date()
max_date = df['fl_date'].max().date()

start_date, end_date = st.sidebar.date_input("📅 Select Date Range:", value=(min_date, max_date), min_value=min_date, max_value=max_date)

selected_airline = st.sidebar.multiselect("Select Airline(s):", options=sorted(df['airline'].unique()), default=[])
selected_origin = st.sidebar.multiselect("Select Origin City:", options=sorted(df['origin_city'].unique()), default=[])
selected_dest = st.sidebar.multiselect("Select Destination City:", options=sorted(df['dest_city'].unique()), default=[])
selected_status = st.sidebar.multiselect("Select Flight Status:", options=sorted(df['flight_status'].unique()), default=[])

# Apply filters
df_filtered = df[(df['fl_date'] >= pd.to_datetime(start_date)) & (df['fl_date'] <= pd.to_datetime(end_date))]

if selected_airline:
    df_filtered = df_filtered[df_filtered['airline'].isin(selected_airline)]
if selected_origin:
    df_filtered = df_filtered[df_filtered['origin_city'].isin(selected_origin)]
if selected_dest:
    df_filtered = df_filtered[df_filtered['dest_city'].isin(selected_dest)]
if selected_status:
    df_filtered = df_filtered[df_filtered['flight_status'].isin(selected_status)]

# Overview 
st.markdown("## 📊 Overview Dashboard")

# KPIs
col1, col2, col3, col4 = st.columns(4)

total_flights = df_filtered.shape[0]
delayed_flights = df_filtered[df_filtered['dep_delay'] > 15].shape[0]
cancelled_flights = df_filtered[df_filtered['flight_status'] == 'Cancelled'].shape[0]
on_time_flights = total_flights - delayed_flights - cancelled_flights

delay_percent = (delayed_flights / total_flights) * 100 if total_flights > 0 else 0
cancel_percent = (cancelled_flights / total_flights) * 100 if total_flights > 0 else 0


with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">✈️ Total Flights</div>
            <div class="kpi-value">{format_number(total_flights)}</div>
        </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">🕒 Delayed Flights</div>
            <div class="kpi-value">{format_number(delayed_flights)}</div>
            
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">❌ Cancelled Flights</div>
            <div class="kpi-value">{format_number(cancelled_flights)}</div>
            
        </div>
    """, unsafe_allow_html=True)


with col4:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">✅ On-Time Flights</div>
            <div class="kpi-value">{format_number(on_time_flights)}</div>
        </div>
    """, unsafe_allow_html=True)


st.markdown("---")


# Color Palette 
custom_colors = ["#114538", "#5e8d83", "#d2e1cc", "#161d23"]

# Flights Over Time
st.markdown("## 📅 Flights Over Time")
chart_type = st.radio("Select Chart Type:", ["Line Chart", "Bar Chart"], horizontal=True)

df_filtered["year"] = df_filtered["fl_date"].dt.year
flights_over_time = df_filtered.groupby("year").size().reset_index(name="count")

if chart_type == "Line Chart":
    st.plotly_chart(px.line(flights_over_time, x="year", y="count", markers=True,
                  title="Flights Count Over Time",
                  labels={"year": "Year", "count": "Number of Flights"},
                  template="plotly_white", color_discrete_sequence=custom_colors), use_container_width=True)
else:
    st.plotly_chart(px.bar(flights_over_time, x="year", y="count",
                 title="Flights Count Over Time",
                 labels={"year": "Year", "count": "Number of Flights"},
                 template="plotly_white", color_discrete_sequence=custom_colors), use_container_width=True)

# Flight Status Distribution
st.markdown("## 📌 Flight Status Distribution")

status_counts = df_filtered['flight_status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']

st.plotly_chart(px.pie(status_counts, names='Status', values='Count',
              title="Flight Status Breakdown", hole = 0.5,
              color_discrete_sequence=['#114538', '#5e8d83', '#d2e1cc']), use_container_width=True)



# Footer
st.markdown("""---""")
st.markdown("""
    <p style='text-align: center; font-size: 14px;'>
        © 2025 | Developed by <strong>Ahmed Shlaby</strong> | 📧 <a href="mailto:shalabyahmed299@gmail.com">Contact</a>
    </p>
""", unsafe_allow_html=True)
