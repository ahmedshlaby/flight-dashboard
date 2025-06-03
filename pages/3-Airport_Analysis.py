
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Airport Analysis", page_icon="🛫", layout="wide")
st.title("🛫 Airport Analysis")

# Load dataset
@st.cache_data
def load_data():
    url = "https://www.dropbox.com/scl/fi/cdrfwk27h6sszbqg2k82b/Flight_Canselled_Delay_C.csv?rlkey=0nnticgct444wwqqjk50ctov4&st=aazxpeja&dl=1"
    df = pd.read_csv(url, parse_dates=["fl_date"])
    return df

df = load_data()

# Sidebar - Airport selection
st.sidebar.header("✈️ Filter Airports")
airport_options = df['origin'].value_counts().head(20).index.tolist()
selected_airports = st.sidebar.multiselect("Select Origin Airports", airport_options, default=[])




if selected_airports:
    df = df[df['origin'].isin(selected_airports)]


# Tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "❌ Cancellation Analysis", "⏱️ Delay Analysis", "🔍 Compare Airports"])

with tab1:
    st.subheader("Top 10 Crowded Airports")
    origin_counts = df['origin'].value_counts().head(10).reset_index()
    origin_counts.columns = ['Origin Airport', 'Flight Count']
    st.plotly_chart(px.bar(origin_counts, x='Origin Airport', y='Flight Count', 
                    color_continuous_scale='Tealgrn', color= 'Flight Count'), use_container_width=True)


with tab2:
    st.subheader("Cancellation Rate by Airport")
    cancel_rate = df.groupby('origin')['cancelled'].mean().sort_values(ascending=False).head(10).reset_index()
    cancel_rate.columns = ['Origin Airport', 'Cancellation Rate']
    st.plotly_chart(px.bar(cancel_rate, x='Origin Airport', y='Cancellation Rate', title='Top 10 Airports by Cancellation Rate',
                     color='Cancellation Rate', color_continuous_scale='Tealgrn'), use_container_width=True)


with tab3:
    st.subheader("Top 10 Airports by Average Departure Delay")
    dep_delay = df.groupby('origin')['dep_delay'].mean().sort_values(ascending=False).head(10).reset_index()
    dep_delay.columns = ['Origin Airport', 'Average Departure Delay']
    fig_dep = px.bar(dep_delay, x='Origin Airport', y='Average Departure Delay', 
                     color='Average Departure Delay', color_continuous_scale='Tealgrn',
                     title='Top 10 Airports by Average Departure Delay')
    st.plotly_chart(fig_dep, use_container_width=True)

    st.subheader("Top 10 Airports by Average Arrival Delay")
    arr_delay = df.groupby('dest')['arr_delay'].mean().sort_values(ascending=False).head(10).reset_index()
    arr_delay.columns = ['Destination Airport', 'Average Arrival Delay']
    fig_arr = px.bar(arr_delay, x='Destination Airport', y='Average Arrival Delay',
                     color='Average Arrival Delay', color_continuous_scale='Tealgrn',
                     title='Top 10 Airports by Average Arrival Delay')
    st.plotly_chart(fig_arr, use_container_width=True)


with tab4:
    st.subheader("Compare Two Airports")
    airport_compare = st.multiselect("Select Two Airports to Compare", df['origin'].unique(), default=df['origin'].unique()[:2])

    if len(airport_compare) == 2:
        airport_df = df[df['origin'].isin(airport_compare)]
        comp_stats = airport_df.groupby('origin').agg({
            'dep_delay': 'mean',
            'arr_delay': 'mean',
            'cancelled': 'mean'}).reset_index()

        st.plotly_chart(px.bar(
            comp_stats.melt(id_vars='origin', var_name='Metric', value_name='Value'),
            x='origin', y='Value', color='Metric', barmode='group',
            title='Airport Comparison: Cancellation Rate & Delay',
            color_discrete_sequence=['#005f73', '#0a9396', '#ee9b00']), use_container_width=True)


# Footer
st.markdown("""---""")
st.markdown("""
    <p style='text-align: center; font-size: 14px;'>
        © 2025 | Developed by <strong>Ahmed Shlaby</strong> | 📧 <a href="mailto:shalabyahmed299@gmail.com">Contact</a>
    </p>
""", unsafe_allow_html=True)



