
import streamlit as st

st.set_page_config(page_title="Flight Delay Dashboard", layout="wide", page_icon="✈️")

# Title
st.markdown("""<h1 style='text-align: center; color: #003049; font-size: 50px;'>
                    ✈️ Flight Delay and Cancellation Analysis
                    <h1 style='text-align: center; color: #003049; 'font-size: 50px; color: #003049;'>
                        (2019 - 2023)
                    </h1>
                </h1>""", unsafe_allow_html=True)

# Description
st.markdown("""
    <div style='background-color: #c7d9be; padding: 25px; border-radius: 12px;'>
        <p style='font-size: 18px; color: #264653;'>
            Welcome to the <strong>Flight Delay and Cancellation Analysis Dashboard</strong>.<br>
            This dashboard explores U.S. Flight data from 2019 to 2023 to cover insights related to:
        </p>
        <ul style='font-size: 17px; color: #2a9d8f;'>
            <li>🛫 Airport activity</li>
            <li>⏱️ Flight delays</li>
            <li>❌ Cancellations</li>
            <li>📊 Airline performance</li>
            <li>📌 And more...</li>
        </ul>
        <p style='font-size: 16px; color: #264653;'>
            Use the sidebar to explore interactive visualizations and uncover insights that help understand U.S. flight trends and challenges.
        </p>
    </div>
""", unsafe_allow_html=True)

# Navigation Links 
st.markdown("### 📂 Explore the Dashboard")
st.page_link("pages/1-Flight_Overview.py", label="📈 Flight Overview")
st.page_link("pages/2-Airline_Analysis.py", label="🛩️ Airline Analysis")
st.page_link("pages/3-Airport_Analysis.py", label="🛬 Airport Analysis")
st.page_link("pages/4-Project_Presentation.py", label="🗂️ Project Presentation")
st.page_link("pages/5-About.py", label="👤 About Me")

# About Me Section
st.markdown("---")
st.markdown("### 👨‍💻 About the Developer")
st.markdown("""
            - **Name:** Ahmed Shlaby  
            - **GitHub:** [github.com/ahmedshlaby](https://github.com/ahmedshlaby)  
            - **LinkedIn:** [linkedin.com/in/ahmedshlaby](https://linkedin.com/in/ahmedshlaby)  
            - **Email:** [shalabyahmed299@gmail.com](mailto:shalabyahmed299@gmail.com)
            """)


# Footer
st.markdown("""---""")
st.markdown("""
                <p style='text-align: center; font-size: 14px;'>
                    © 2025 | Developed by <strong>Ahmed Shlaby</strong> | 📧 <a href="mailto:shalabyahmed299@gmail.com">Contact</a>
                </p>
            """, unsafe_allow_html=True)
