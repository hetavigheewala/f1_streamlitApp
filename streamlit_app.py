import streamlit as st
import requests
from about_f1 import display_about_f1
from about_driver import driverInfo
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
    "Track Info",
    "Constructors",
    "Drivers",
    "Race Calendar",
    "Predictions",
    "Standings",
    "Analysis",
    "Contact"
]

# Create sidebar buttons
for button in sidebar_buttons:
    if st.sidebar.button(button):
        st.session_state.selected_page = button.lower().replace(" ", "_")

# Page definitions
def home_page():
    st.title("F1 Data Analysis Project")
    st.markdown("""
        Welcome to the F1 Data Analysis Project, your one-stop resource for deep insights into 
        the world of Formula 1 racing. Here, you'll find everything from driver profiles and 
        team histories to in-depth race analyses, covering pit stops, lap times, and more. 
        Whether you're an F1 enthusiast or a data science fan, this site is designed to make 
        the data behind the excitement accessible and engaging.
    """)

    # F1 News Section
    st.header("F1 News")
    st.write("Catch up on the latest happenings in the F1 world, from race results to team changes and breaking news. This section keeps you up-to-date on all things Formula 1.")


    # Fetch and display upcoming races
    st.header("Upcoming Races")


    # Footer
    st.markdown("---")
    st.markdown("<div class='footer'>&#169; 2024 F1 Data Project. All Rights Reserved.</div>", unsafe_allow_html=True)


def track_info_page():
    st.title("Track Information")
    st.markdown("""
        Here you can find detailed information about various F1 tracks, including 
        their characteristics, history, and notable events.
    """)

def constructors():
    st.title("Constructors")
    st.markdown("""
        Explore the profiles of constructors, including their histories, statistics, 
        and achievements throughout the seasons.
    """)

def drivers():
    st.title("Drivers")
    st.markdown("""
        Explore the profiles of drivers, including their histories, statistics, 
        and achievements throughout the seasons.
    """)
def predictions_page():
    st.title("Race Predictions")
    st.markdown("""
        Analyze data to make predictions about upcoming races, drivers, and team performance. 
        Use statistical models and machine learning for insights.
    """)

def analysis_page():
    st.title("Race Analysis")
    st.markdown("""
        Dive deep into race analyses, including lap times, pit stops, and team strategies. 
        Understand the factors that influence race outcomes.
    """)

def contact_page():
    st.title("Contact Me")
    st.markdown("""
        For inquiries, feedback, or suggestions, please reach out to us via the provided 
        contact form or through our social media channels.
    """)

# Render content based on selected page
if st.session_state.selected_page == "home":
    home_page()
elif st.session_state.selected_page == "about_f1":
    display_about_f1()
elif st.session_state.selected_page == "track_info":
    track_info_page()
elif st.session_state.selected_page == "constructors":
    constructors()
elif st.session_state.selected_page == "drivers":
    driverInfo()
elif st.session_state.selected_page == "predictions":
    predictions_page()
elif st.session_state.selected_page == "standings":
    ViewStanding()
elif st.session_state.selected_page == "analysis":
    analysis_page()
elif st.session_state.selected_page == "contact":
    contact_page()
