
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Airline Insights", page_icon="📈", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    url = "https://www.dropbox.com/scl/fi/cdrfwk27h6sszbqg2k82b/Flight_Canselled_Delay_C.csv?rlkey=0nnticgct444wwqqjk50ctov4&st=aazxpeja&dl=1"
    df = pd.read_csv(url, parse_dates=["fl_date"])
    return df

df = load_data()

# Sidebar filters
st.sidebar.markdown("## ✈️ Airline Insights Filters")
st.sidebar.markdown("---")

min_date = df['fl_date'].min().date()
max_date = df['fl_date'].max().date()

start_date, end_date = st.sidebar.date_input("📅 Select Date Range:", value=(min_date, max_date), min_value=min_date, max_value=max_date)

selected_airline = st.sidebar.multiselect("Select Airline(s):", options=sorted(df['airline'].unique()), default=[])
selected_status = st.sidebar.multiselect("Select Flight Status:", options=sorted(df['flight_status'].unique()), default=[])

# Filter data
df_filtered = df[(df['fl_date'] >= pd.to_datetime(start_date)) & (df['fl_date'] <= pd.to_datetime(end_date))]

if selected_airline:
    df_filtered = df_filtered[df_filtered['airline'].isin(selected_airline)]
if selected_status:
    df_filtered = df_filtered[df_filtered['flight_status'].isin(selected_status)]


# tabs for choise
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "❌ Cancellation Analysis", "🕒 Delay Analysis", "🔁 Compare Airlines"])


# Top Airlines by Count (overview tab)
with tab1:
    st.markdown("## 🏆 Top 10 Airlines by Flight Count")
    top_airlines = df_filtered['airline'].value_counts().nlargest(10).reset_index()
    top_airlines.columns = ['Airline', 'Flights']

    st.plotly_chart(px.bar(top_airlines, x='Airline', y='Flights',
                title="Top 10 Airlines by Number of Flights",
                color='Flights', color_continuous_scale='Tealgrn',
                template='plotly_white'), use_container_width=True)

    # Flights Distribution by Time of Day
    st.markdown("## ☀️ Flights Distribution by Time of Day")

    dep_period_counts = df_filtered.groupby(['airline', 'dep_time_Period']).size().reset_index(name='flight_count').sort_values(by= 'flight_count', ascending= False)

    st.plotly_chart(px.bar(dep_period_counts,
                x='airline',
                y='flight_count',
                color='dep_time_Period',
                title='Flights by Time of Day and Airline',
                barmode='group',
                labels={'flight_count': 'Number of Flights', 'dep_time_Period': 'Time Period'},
                template='plotly_white',
                color_discrete_sequence=px.colors.sequential.Tealgrn), use_container_width=True)

    

# Cancellation Rate by Airline
with tab2:
    st.markdown("## ❌ Cancellation Rate by Airline")
    tab1, tab2 = st.tabs(["🥧 Pie Chart", "📊 Bar Chart"])

    cancel_data = df_filtered.groupby("airline").agg(
        total_flights=('flight_status', 'count'),
        cancelled_flights=('flight_status', lambda x: (x == 'Cancelled').sum())).reset_index()

    cancel_data['cancellation_rate'] = (cancel_data['cancelled_flights'] / cancel_data['total_flights']) * 100

    # Monthly Cancellation Rate per Airline
    st.markdown("## 📉 Monthly Cancellation Rate per Airline")

    df_filtered['month'] = df_filtered['fl_date'].dt.to_period('M').astype(str)
    monthly_cancel = df_filtered.groupby(['month', 'airline'])['cancelled'].mean().reset_index()

    st.plotly_chart(px.line(monthly_cancel, x='month', y='cancelled', color='airline',
                title='Monthly Cancellation Rate per Airline',
                labels={'cancelled': 'Cancellation Rate'},
                template='plotly_white', color_discrete_sequence=px.colors.sequential.Tealgrn), use_container_width=True)


    with tab1:  # Pie Chart
        st.plotly_chart(
            px.pie(cancel_data, names="airline", values="cancellation_rate",
                title="Pie Chart: Cancellation Rate Distribution",
                color_discrete_sequence=px.colors.sequential.Tealgrn), use_container_width=True)


    with tab2:  # Bar Chart
        st.plotly_chart(
            px.bar(cancel_data.sort_values(by="cancellation_rate", ascending=False),
                x="airline", y="cancellation_rate",
                title="Bar Chart: Cancellation Rate by Airline (%)",
                labels={"airline": "Airline", "cancellation_rate": "Cancellation Rate (%)"},
                color="cancellation_rate", color_continuous_scale='Tealgrn',
                template="plotly_white"), use_container_width=True)




# Average Delay by Airline
with tab3:
    st.markdown("## 🕒 Average Departure Delay by Airline")

    avg_delay = df_filtered.groupby('airline')['dep_delay'].mean().reset_index().sort_values(by='dep_delay', ascending=False)

    st.plotly_chart(px.bar(avg_delay, x='airline', y='dep_delay',
                title='Average Departure Delay (in minutes)',
                labels={'airline': 'Airline', 'dep_delay': 'Avg Departure Delay'},
                color='dep_delay', color_continuous_scale='Tealgrn',
                template='plotly_white'), use_container_width=True)
    
    # for arr delay
    st.markdown("## 🕒 Average Arrival Delay by Airline")

    avg_delay = df_filtered.groupby('airline')['arr_delay'].mean().reset_index().sort_values(by='arr_delay', ascending=False)

    st.plotly_chart(px.bar(avg_delay, x='airline', y='arr_delay',
                title='Average Departure Delay (in minutes)',
                labels={'airline': 'Airline', 'arr_delay': 'Avg Departure Delay'},
                color='arr_delay', color_continuous_scale='Tealgrn',
                template='plotly_white'), use_container_width=True)


# compare between 2 Airline
with tab4:
    st.markdown("## ✈️ Compare Airlines")

    airlines_to_compare = st.multiselect(
        "Select up to 2 Airlines to Compare:",
        options=df_filtered['airline'].unique(),
        default=df_filtered['airline'].unique()[:2],
        max_selections=2
    )

    if len(airlines_to_compare) == 2:
        compare_df = df_filtered[df_filtered['airline'].isin(airlines_to_compare)]

        # Total per airlinee
        compare_grouped = compare_df.groupby('airline').agg(
            total_flights=('flight_status', 'count'),
            cancelled_flights=('flight_status', lambda x: (x == 'Cancelled').sum()),
            avg_delay=('dep_delay', 'mean')
        ).reset_index()

        compare_grouped['cancellation_rate'] = (compare_grouped['cancelled_flights'] / compare_grouped['total_flights']) * 100

        # Kpis
        st.markdown("### 📌 Key Metrics")
        col1, col2 = st.columns(2)

        with col1:
            st.metric(label=f"{airlines_to_compare[0]} - Total Flights", value=compare_grouped.loc[0, 'total_flights'])
            st.metric(label=f"{airlines_to_compare[0]} - Cancellation Rate", value=f"{compare_grouped.loc[0, 'cancellation_rate']:.2f}%")
            st.metric(label=f"{airlines_to_compare[0]} - Avg Delay", value=f"{compare_grouped.loc[0, 'avg_delay']:.2f} min")

        with col2:
            st.metric(label=f"{airlines_to_compare[1]} - Total Flights", value=compare_grouped.loc[1, 'total_flights'])
            st.metric(label=f"{airlines_to_compare[1]} - Cancellation Rate", value=f"{compare_grouped.loc[1, 'cancellation_rate']:.2f}%")
            st.metric(label=f"{airlines_to_compare[1]} - Avg Delay", value=f"{compare_grouped.loc[1, 'avg_delay']:.2f} min")

        # Comparison Table
        st.markdown("### 📊 Comparison Table")
        st.dataframe(compare_grouped)

        # charts
        st.markdown("### 📈 Comparison Charts")
        st.plotly_chart(
            px.bar(compare_grouped, x='airline', y='total_flights',
                title="Total Flights per Airline", color='total_flights',
                color_continuous_scale='Tealgrn', template='plotly_white',
                labels = {'airline' : 'AirLine', 'total_flights': 'Number Of Flights'},
                text_auto=True),
            use_container_width=True)

        st.plotly_chart(
            px.bar(compare_grouped, x='airline', y='cancellation_rate',
                title="Cancellation Rate (%) per Airline", color='cancellation_rate',
                color_continuous_scale='Tealgrn', template='plotly_white',
                labels = {'airline' : 'AirLine', 'cancellation_rate': 'Cancellation Rate'},
                text_auto='.2f'),
            use_container_width=True)

        st.plotly_chart(
            px.bar(compare_grouped, x='airline', y='avg_delay',
                title="Average Delay (minutes) per Airline", color='avg_delay',
                color_continuous_scale='Tealgrn', template='plotly_white',
                labels = {'airline' : 'AirLine', 'avg_delay': 'Avg Delay (min)'},
                text_auto='.2f'),
            use_container_width=True)

        # Monthly Comparison
        st.markdown("### 🗓️ Monthly Comparison")

        monthly_compare = compare_df.copy()
        monthly_compare['month'] = monthly_compare['fl_date'].dt.to_period('M').astype(str)

        monthly_summary = monthly_compare.groupby(['month', 'airline']).agg(
            total_flights=('flight_status', 'count'),
            cancelled_flights=('flight_status', lambda x: (x == 'Cancelled').sum()),
            avg_delay=('dep_delay', 'mean')
        ).reset_index()

        monthly_summary['cancellation_rate'] = (monthly_summary['cancelled_flights'] / monthly_summary['total_flights']) * 100

        st.plotly_chart(px.line(monthly_summary, x='month', y='total_flights', color='airline',
                      title='Monthly Flight Count per Airline',
                      labels = {'month' : 'Month (year)', 'total_flights': 'Total Flights'},
                      template='plotly_white'), use_container_width=True)
        
        
        # Analysis insight 
        st.markdown("### 🧠 Insight")

        if compare_grouped.loc[0, 'avg_delay'] > compare_grouped.loc[1, 'avg_delay']:
            worst_airline = compare_grouped.loc[0, 'airline']
        else:
            worst_airline = compare_grouped.loc[1, 'airline']

        st.info(f"📌 Based on the current data, **{worst_airline}** has a higher average delay.")




# Footer
st.markdown("""---""")
st.markdown("""
    <p style='text-align: center; font-size: 14px;'>
        © 2025 | Developed by <strong>Ahmed Shlaby</strong> | 📧 <a href="mailto:shalabyahmed299@gmail.com">Contact</a>
    </p>
""", unsafe_allow_html=True)

