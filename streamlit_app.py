import streamlit as st
import requests
from about_f1 import display_about_f1
from about_driver import driver_info
from about_constructor import constructors_info
from about_circuit import circuit_info
from standings import ViewStanding
from datetime import datetime


# Set up the Streamlit app layout with F1 theme
st.set_page_config(page_title="F1 Data Analysis", page_icon="asset/favicon.png")

# Custom CSS for F1 theme
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f4;  /* Lighter background for better readability */
        color: #333;
    }
    h1, h2, h3 {
        color: #FF1E00;  /* F1 Red */
    }
    h1 {
        font-size: 2.5em;
    }
    h2 {
        font-size: 2em;
    }
    h3 {
        font-size: 1.5em;
    }
    .stButton>button {
        background-color: #FFFFFF; /* Button background color */
        color: black;;
        border-radius: 5px; /* Rounded corners */
        padding: 5px 10px;  /* Reduced padding for a more compact button */
        
        font-size: 1em;
        transition: background-color 0.3s, border-color 0.3s; /* Smooth transition */
        width: 100%; /* Full-width buttons */
    }
    .stButton>button:hover {
        background-color: #AE3644;  /* Darker shade of red on hover */
        border-color: #FF1E00; /* Keep border color on hover */
        color: white;

    }
    .footer {
        font-size: 0.8em;
        color: #777;
        text-align: center;  /* Center footer text */
    }
    .upcoming-race {
        background-color: #ffffff; /* White background for race cards */
        border-radius: 10px; /* Rounded corners */
        padding: 15px; /* Padding for race cards */
        box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* Subtle shadow */
        margin: 10px; /* Spacing between cards */
    }
    .sidebar .stButton {
        width: 100%; /* Full-width sidebar buttons */
        margin-bottom: 10px; /* Spacing between buttons */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for page selection
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "home"

# Navigation sidebar
st.sidebar.markdown("<h2 style='text-align: center; color: #FF1E00;font-size: 1.8em;'>F1 Navigation</h2>", unsafe_allow_html=True)

sidebar_buttons = [
    "Home",
    "About F1",
    "Drivers",
    "Constructors",
    "Circuit",
    "Standings",
    "Driver Analysis",
    "Constructor Analysis",
    "Circuit Analysis",
    "Race Analysis",
    "Predictions"
]

# Create sidebar buttons
for button in sidebar_buttons:
    if st.sidebar.button(button):
        st.session_state.selected_page = button.lower().replace(" ", "_")

# Page definitions
def home_page():
    st.markdown("<h1 style='color: red;'>F1 Data Analysis Project</h1>", unsafe_allow_html=True)
    st.markdown("""
        Welcome to the F1 Data Analysis Project, your one-stop resource for deep insights into 
        the world of Formula 1 racing. Here, you'll find everything from driver profiles and 
        team histories to in-depth race analysis, covering pit stops, lap times, and more. 
        Whether you're an F1 enthusiast or a data science fan, this site is designed to make 
        the data behind the excitement accessible and engaging.
    """)

    # F1 News Section
    st.markdown("<h2 style='color: red;'>F1 News</h2>", unsafe_allow_html=True)
    st.write("Catch up on the latest happenings in the F1 world, from race results to team changes and breaking news. This section keeps you up-to-date on all things Formula 1.")
    st.markdown("[Click here to explore the latest F1 news!](https://www.formula1.com/en/latest/all)", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<div class='footer'>&#169; 2024 F1 Data Project. All Rights and Wrong Reserved.</div>", unsafe_allow_html=True)


def driver_analysis_page():
    st.markdown("<h1 style='color: red;'>Driver Analysis</h1>", unsafe_allow_html=True)

def constructor_analysis_page():
    st.markdown("<h1 style='color: red;'>Constructor Analysis</h1>", unsafe_allow_html=True)

def circuit_analysis_page():
    st.markdown("<h1 style='color: red;'>Circuit Analysis</h1>", unsafe_allow_html=True)

def race_analysis_page():
    st.markdown("<h1 style='color: red;'>Race Analysis</h1>", unsafe_allow_html=True)


def predictions_page():
    st.markdown("<h1 style='color: red;'>Race Predictions</h1>", unsafe_allow_html=True)
    st.markdown("""
        Analyze data to make predictions about upcoming races, drivers, and team performance. 
        Use statistical models and machine learning for insights.
    """)


# Render content based on selected page
if st.session_state.selected_page == "home":
    home_page()
elif st.session_state.selected_page == "about_f1":
    display_about_f1()
elif st.session_state.selected_page == "drivers":
    driver_info()
elif st.session_state.selected_page == "constructors":
    constructors_info()
elif st.session_state.selected_page == "circuit":
    circuit_info()
elif st.session_state.selected_page == "standings":
    ViewStanding()
elif st.session_state.selected_page == "driver_analysis":
    driver_analysis_page()
elif st.session_state.selected_page == "constructor_analysis":
    constructor_analysis_page() 
elif st.session_state.selected_page == "circuit_analysis":
    circuit_analysis_page()
elif st.session_state.selected_page == "race_analysis":
    race_analysis_page()
elif st.session_state.selected_page == "predictions":
    predictions_page()

