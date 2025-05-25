import streamlit as st
from PIL import Image
import os

def load_F1_image(file_path, size=(400, 155)):
    try:
        img = Image.open(file_path)
        img = img.resize(size)  
        return img
    except FileNotFoundError:
        return None

def display_about_f1():
    """Displays a beginner's guide to Formula 1 with basic history, rules, and structure."""
    
    logo_file = os.path.join("asset/f1_red.png")
    team_logo = load_F1_image(logo_file)
    
    cols = st.columns([1, 5])
    with cols[0]:
        st.markdown("<br>", unsafe_allow_html=True)  # Adds two new lines
        st.image(team_logo, width=175)
    with cols[1]:
        st.markdown(
            "<h1 class='title' style='color: red; text-align: center; margin-bottom: 0;'>About Formula 1</h1>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)  # Adds two new lines


    st.image('asset/about_img/f1_banner.jpg', use_container_width=True)

    # History and Overview
    st.markdown("<h2 style='color: red;'>What is Formula 1 (F1)?</h2>", unsafe_allow_html=True)
    st.write(
        """
        Formula 1, also known as F1, is the most exciting and fast-paced form of motorsport in the world. It all started in 1950, 
        and since then, F1 has become a global phenomenon. It involves high-speed races, with cars designed to be as fast as possible.
        Each race is called a Grand Prix (from the French for ‘big prize’) and is held in cities around the world. At the end of the season, the best drivers and teams 
        are crowned World Champions.
        """
    )
    # using columns to center the image
    col1, col2, col3 = st.columns([1, 6, 1])  

    with col2:
        st.image('asset/about_img/f1_history.jpg', caption='The First F1 Race in 1950')

    # Basic Terminology
    st.markdown("<h2 style='color: red;'>Key F1 Terms You Should Know</h2>", unsafe_allow_html=True)
    st.write(
        """
        Here's a quick guide to some important F1 terms that will help you understand the sport better:
        
        - **Pole Position**: The front row of the starting grid, given to the fastest driver in qualifying.
        - **Grid**: The lineup of cars before the race begins.
        - **Pit Stop**: When a car pulls into the pit area during the race to change tires or fix any issues.
        - **Lap**: One full trip around the racetrack.
        - **DRS (Drag Reduction System)**: A technology that helps cars go faster by reducing air resistance, making overtaking easier.
        """
    )
    
        # using columns to center the image
    col1, col2, col3 = st.columns([1, 6, 1])  

    with col2:
        st.image('asset/about_img/pole_position.jpg', caption='Cars lining up for Pole Position')

    # Basic Race Rules
    st.markdown("<h2 style='color: red;'>How Does an F1 Weekend Work?</h2>", unsafe_allow_html=True)
    st.write(
        """
        An F1 race weekend is divided into different sessions:

        1. **Practice**: Drivers get some time to learn the track and test their cars.
        2. **Qualifying**: This determines where each driver starts the race (the fastest gets Pole Position).
        3. **The Race**: The main event where drivers compete to win.
        
        Points are awarded for finishing positions, and the top 10 drivers get points. The driver who finishes in first place gets 25 points, 
        second place gets 18 points, and so on. The driver with the most points at the end of the season wins the Drivers' Championship.
        """
    )
    
    # using columns to center the image
    col1, col2, col3 = st.columns([1, 6, 1])  

    with col2:
        st.image('asset/about_img/f1_weekend.jpg', caption='F1 Sprint Weekend Structure')

    # Tires in F1
    st.markdown("<h2 style='color: red;'>Tires: The Secret to Speed!</h2>", unsafe_allow_html=True)
    st.write(
        """
        Tires play a big role in Formula 1. Different tire types are used depending on the weather and track conditions:
        
        - **Soft**: These tires are super fast but wear out quickly.
        - **Medium**: A balance between speed and durability.
        - **Hard**: Slower but last much longer.
        - **Intermediate/Wet**: Used when the track is wet or rainy.
        """
    )
    
    # using columns to center the image
    col1, col2, col3 = st.columns([1, 6, 1])  

    with col2:
        st.image('asset/about_img/f1_tires.jpg', caption='Different tire types in F1')

    # Flags in F1 Racing
    st.markdown("<h2 style='color: red;'>What Do the Flags Mean?</h2>", unsafe_allow_html=True)
    st.write(
        """
        Flags are used to communicate important information to the drivers during the race. Here are the main flags you’ll see:

        - **Green Flag**: The track is clear, and racing can continue.
        - **Yellow Flag**: Slow down; there's something ahead on the track.
        - **Red Flag**: The race has been stopped (usually due to an accident).
        - **Blue Flag**: A faster car is behind you and needs to pass.
        - **Checkered Flag**: The race is over!
        """
    )
    
    # using columns to center the image
    col1, col2, col3 = st.columns([1, 6, 1])  

    with col2:
        st.image('asset/about_img/f1_flags.jpg', caption='F1 Race Flags')

    # Structure of F1 Teams
    st.markdown("<h2 style='color: red;'>F1 Teams: Who's Behind the Wheel?</h2>", unsafe_allow_html=True)
    st.write(
        """
        F1 teams are made up of drivers, engineers, and pit crews. Each team has two drivers who race for the team, and they compete 
        for two main championships:
        
        - **Drivers' Championship**: Awarded to the driver with the most points at the end of the season.
        - **Constructors' Championship**: Awarded to the team with the most points, based on the performance of both their drivers.
        
        Teams also have a large crew of engineers and strategists who help make decisions during the race.
        """
    )
    
    # using columns to center the image
    col1, col2, col3 = st.columns([1, 6, 1])  

    with col2:
        st.image('asset/about_img/f1_teams.jpg', caption='F1 Team Structure and Pit Crews')

    # Conclusion Section
    st.markdown("<h2 style='color: red;'>Why Formula 1 is So Exciting!</h2>", unsafe_allow_html=True)

    st.write(
        """
        Formula 1 is more than just a sport – it's a world of speed, precision, technology, and teamwork. The excitement never ends 
        as teams and drivers push the limits to be the best. F1 offers something for everyone: fast cars, dramatic races, and thrilling 
        finishes. Whether you're a casual fan or a passionate follower, F1 has a lot to offer.
        """
    )
    # using columns to center the image
    col1, col2, col3 = st.columns([1, 6, 1])  

    with col2:
        st.image('asset/about_img/f1_conclusion.jpg', caption='F1 Race action shot')

if __name__ == "__main__":
    display_about_f1()
