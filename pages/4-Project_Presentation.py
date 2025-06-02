
import streamlit as st

st.set_page_config(page_title="Project Presentation", layout="wide")

# Title
st.markdown("""
    <h1 style='text-align: center; color: #003049; font-size: 42px; margin-bottom: 20px;'>
        📊 Flight Delay & Cancellation Project Presentation
    </h1>
""", unsafe_allow_html=True)

# Section 1: Data Understanding
st.header("1. Data Understanding")
st.markdown("""
- Loaded flight data from CSV containing records from 2019 to 2023.
- Data includes features such as flight date, origin, destination, delays, cancellation status, and airline info.
- Main goal: Analyze flight delay and cancellation patterns across US airports and airlines.
""")

# Section 2: Data Cleaning
st.header("2. Data Cleaning & Preparation")
st.markdown("""
- Converted `fl_date` column to datetime format.
- Extracted new features: `month` and `day_of_week` from the flight date.
- Removed irrelevant columns that do not contribute to prediction or cause data leakage, e.g., actual delay times, flight status, and city names.
- Removed duplicate rows.
- Dropped rows with missing values in important columns like `crs_elapsed_time`.
""")

# Section 3: Exploratory Data Analysis (EDA)
st.header("3. Exploratory Data Analysis (EDA)")
st.markdown("""
- Visualized key trends using interactive charts:
  - Top 10 busiest airports by number of flights.
  - Airports with highest cancellation rates.
  - Average departure and arrival delays by airports.
- Used bar charts, pie charts, and line charts for clear insights.
- This analysis helped to understand the data distribution and focus areas.
""")

# Section 4: Streamlit Dashboard
st.header("4. Interactive Dashboard with Streamlit")
st.markdown("""
- Built a multi-page Streamlit app to display analysis results.
- Pages include:
  - **Home:** Project overview and contact info.
  - **Flight Overview:** KPIs and overall flight trends.
  - **Airline Analysis:** Performance metrics by airline.
  - **Airport Analysis:** Deep dive into airport delays and cancellations.
- Used Plotly for dynamic and responsive visualizations.
- Applied consistent color schemes and user-friendly layout.
""")

# Section 5: Data Preprocessing for Modeling
st.header("5. Data Preprocessing for Machine Learning")
st.markdown("""
- Split data into features (`X`) and target (`y`) where target is `cancelled` (flight cancellation status).
- Performed train-test split (80% train, 20% test) with stratification to maintain class distribution.
- For numerical features:
  - Applied `RobustScaler` to normalize data and reduce the impact of outliers.
- For categorical features:
  - Used `BinaryEncoder` to convert categorical variables into numeric format.
""")

# Section 6: Handling Imbalanced Data
st.header("6. Handling Class Imbalance")
st.markdown("""
- The dataset is imbalanced: fewer cancelled flights compared to non-cancelled.
- Used **SMOTE (Synthetic Minority Oversampling Technique)** to generate synthetic samples for the minority class.
- This helps improve model training by balancing the classes and preventing bias toward the majority class.
""")

# foter
st.markdown("---")
st.markdown("""
<p style='text-align:center; font-size: 14px; color: #555;'>
    © 2025 | Developed by Ahmed Shlaby | 📧 <a href="mailto:shalabyahmed299@gmail.com">Contact Me</a>
</p>
""", unsafe_allow_html=True)


