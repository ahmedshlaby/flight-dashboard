
import streamlit as st

# Page configuration
st.set_page_config(page_title="About Me", page_icon="👤", layout="centered")

# Page title
st.title("👤 About Me")

# Display profile picture 
st.image("MYIMAGE_Copy.jpg", width=200)

# introduction
st.markdown("""
Hi! I'm **Ahmed Shlaby**, a passionate Data Scientist and Python developer with a strong interest in flight data analysis and visualization.

---

### 🧑‍🎓 Background
- Bachelor's degree in Information Technology and Computer Science  
- Certified Data Scientist Professional (CDSP) from Epsilon AI  
- Certified Data Analysis Professional (CDAP) from Epsilon AI  
- Experienced in data analysis, visualization, and deploying interactive dashboards using Streamlit

---

### 🛠 Skills & Tools
- Python (Pandas, NumPy, Sklearn)  
- Data Visualization (Plotly, Seaborn, Matplotlib)  
- Dashboarding with Streamlit  
- Machine Learning basics & Data Preprocessing  
- GitHub for version control

---

### 📫 Contact Me
- **Email:** [shalabyahmed299@gmail.com](mailto:shalabyahmed299@gmail.com)  
- **LinkedIn:** [linkedin.com/in/ahmedshlaby](https://linkedin.com/in/ahmedshlaby)  
- **GitHub:** [github.com/ahmedshlaby](https://github.com/ahmedshlaby)  

---

Thank you for visiting my project! Feel free to reach out for collaboration or questions.
""")

# foter
st.markdown("---")
st.markdown("""
<p style='text-align:center; font-size: 14px; color: #555;'>
    © 2025 | Developed by Ahmed Shlaby | 📧 <a href="mailto:shalabyahmed299@gmail.com">Contact Me</a>
</p>
""", unsafe_allow_html=True)
