# pages/1_Anouk.py

import streamlit as st
from datetime import datetime, timedelta
import pytz
import folium
from streamlit_folium import st_folium
import os
import json

# Define the path for the cache file
CACHE_DIR = "static/data"
CACHE_FILE = os.path.join(CACHE_DIR, "sjoe_cache.json")

def get_cache():
    """
    Reads the cache file and returns the cached data.
    If the cache doesn't exist or is corrupted, initialize with default values.
    """
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    if os.path.isfile(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
                if 'last_text_time' in cache:
                    # Parse the datetime string back to a datetime object
                    cache['last_text_time'] = datetime.fromisoformat(cache['last_text_time'])
                    return cache
        except (json.JSONDecodeError, KeyError, ValueError):
            st.warning("Cache file is corrupted. Resetting cache.")

    # Initialize default cache (set to current time)
    default_time = datetime.now(pytz.timezone('Europe/Brussels'))
    default_cache = {
        "last_text_time": default_time.isoformat()
    }
    save_cache(default_cache)
    # Convert 'last_text_time' to datetime object
    default_cache['last_text_time'] = default_time
    return default_cache

def save_cache(cache):
    """
    Saves the cache data to the cache file.
    The 'last_text_time' is stored as an ISO-formatted string.
    """
    cache_to_save = cache.copy()
    # Ensure 'last_text_time' is a datetime object before calling .isoformat()
    if isinstance(cache_to_save.get('last_text_time'), datetime):
        cache_to_save['last_text_time'] = cache_to_save['last_text_time'].isoformat()
    elif isinstance(cache_to_save.get('last_text_time'), str):
        try:
            dt = datetime.fromisoformat(cache_to_save['last_text_time'])
            cache_to_save['last_text_time'] = dt.isoformat()
        except ValueError:
            # If parsing fails, set to current time
            cache_to_save['last_text_time'] = datetime.now(pytz.timezone('Europe/Brussels')).isoformat()
    else:
        # Set to current time if not datetime or string
        cache_to_save['last_text_time'] = datetime.now(pytz.timezone('Europe/Brussels')).isoformat()

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache_to_save, f, ensure_ascii=False, indent=2)

def time_since_last_text(last_text_time):
    """
    Calculate the time elapsed since the last text.
    Returns a timedelta object.
    """
    now = datetime.now(pytz.timezone('Europe/Brussels'))
    delta = now - last_text_time
    return delta

def create_map(latitude, longitude):
    """
    Create a Folium map centered at the given latitude and longitude.
    Adds a marker indicating Anouk's location.
    """
    my_map = folium.Map(location=[latitude, longitude], zoom_start=12)
    folium.Marker(
        [latitude, longitude],
        tooltip="Anouk is here!",
        popup="Anouk's Location in Limburg"
    ).add_to(my_map)
    return my_map

def main():
    # Configure the page title & layout
    st.set_page_config(
        page_title="Sjoe",
        page_icon=":heart:",
        layout="wide"
    )

    st.title("Sjoe :heart:")
    st.write("## Should I text Anouk?")

    # Initialize session state for auto-refresh control
    if 'last_rerun' not in st.session_state:
        st.session_state['last_rerun'] = datetime.now(pytz.timezone('Europe/Brussels'))

    # Load cache
    cache = get_cache()
    last_text_time = cache['last_text_time']

    # Button to reset the counter
    if st.button("I've texted Sjoe"):
        new_time = datetime.now(pytz.timezone('Europe/Brussels'))
        st.session_state['last_text_time'] = new_time
        cache['last_text_time'] = new_time
        save_cache(cache)
        st.success("You've successfully texted Anouk!")
        st.rerun()

    # Calculate time since last text
    delta = time_since_last_text(last_text_time)

    # Display the counter
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        time_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    else:
        time_str = f"{hours} hours, {minutes} minutes, {seconds} seconds"

    st.write(f"**You've not texted Sjoe for:** {time_str}")

    # Display timed messages based on elapsed time with emojis
    if delta >= timedelta(minutes=60):
        st.error(":broken_heart: \"We're so done\"")
    elif delta >= timedelta(minutes=15):
        st.warning(":rose: \"You better buy me flowers\" ~Anouk")
    elif delta >= timedelta(minutes=2):
        st.warning(":exclamation: You're in the danger zone")

    # Optional: Display countdown until the next message
    if delta < timedelta(seconds=30):
        remaining = timedelta(seconds=30) - delta
        st.info(f"You're safe for now. {remaining.seconds} seconds until the next message")
    elif timedelta(seconds=30) <= delta < timedelta(minutes=2):
        remaining = timedelta(minutes=2) - delta
        #st.info(f"**Time until flower warning:** {remaining.seconds} seconds")
    elif timedelta(minutes=2) <= delta < timedelta(minutes=10):
        remaining = timedelta(minutes=10) - delta
        #st.info(f"**Time until relationship ends:** {remaining.seconds} seconds")

    st.write("---")
    st.write("## Where is she now?")

    # Coordinates for Limburg, Belgium (e.g., Hasselt)
    lat = 50.9352
    lon = 5.3249

    # Create and display the map
    my_map = create_map(lat, lon)
    st_folium(my_map, width=700, height=500)

    # Auto-refresh every 10 seconds
    if datetime.now(pytz.timezone('Europe/Brussels')) - st.session_state['last_rerun'] > timedelta(seconds=10):
        st.session_state['last_rerun'] = datetime.now(pytz.timezone('Europe/Brussels'))
        st.rerun()

if __name__ == "__main__":
    main()
