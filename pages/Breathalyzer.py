# pages/3_Breathalyzer.py

import streamlit as st
import time
import os
import json
from datetime import datetime

# Path to the drinks data file
DATA_FILE = "static/data/drinks.json"

def initialize_data_file():
    """
    Ensure that the data file exists. If not, create an empty list.
    """
    if not os.path.exists(DATA_FILE):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

def load_drinks():
    """
    Load the list of drinks from the JSON file.
    Returns:
        List of drinks, where each drink is a dict with 'timestamp', 'name', 'volume_ml', 'abv'.
    """
    initialize_data_file()
    with open(DATA_FILE, 'r') as f:
        try:
            drinks = json.load(f)
            # Validate that drinks is a list
            if not isinstance(drinks, list):
                drinks = []
        except json.JSONDecodeError:
            drinks = []
    return drinks

def save_drinks(drinks):
    """
    Save the list of drinks to the JSON file.
    """
    with open(DATA_FILE, 'w') as f:
        json.dump(drinks, f)

def add_drink(drink_info):
    """
    Add a new drink to the drinks list and save it.
    Args:
        drink_info: dict with 'name', 'volume_ml', 'abv', 'image'.
    """
    drinks = load_drinks()
    drink_entry = {
        "timestamp": time.time(),
        "name": drink_info["name"],
        "volume_ml": drink_info["volume_ml"],
        "abv": drink_info["abv"],
        "image": drink_info["image"]
    }
    drinks.append(drink_entry)
    save_drinks(drinks)

def reset_drinks():
    """
    Reset the drinks list by clearing the JSON file.
    """
    save_drinks([])

def calculate_bac(drinks, user_weight=80.0, distribution_ratio=0.68):
    """
    Widmark formula to calculate total Blood Alcohol Content (g/L or ‰) over time
    for each consumed drink.
    """
    now = time.time()
    metabolism_rate = 0.15  # g/L/hour (typical average)

    total_bac = 0.0

    for drink in drinks:
        drink_time = drink["timestamp"]
        volume_ml = drink["volume_ml"]
        abv = drink["abv"]

        # Time difference in hours since that drink
        hours_elapsed = (now - drink_time) / 3600.0

        # Grams of pure alcohol in this drink
        grams_alcohol = volume_ml * abv * 0.8

        # Widmark formula (g/L or promille)
        eBAC_drink = (grams_alcohol / (user_weight * distribution_ratio)) - (metabolism_rate * hours_elapsed)

        if eBAC_drink < 0:
            eBAC_drink = 0.0

        total_bac += eBAC_drink

    # Floor at 0 if negative
    if total_bac < 0:
        total_bac = 0.0

    return total_bac

def main():
    # Configure the page title & layout
    st.set_page_config(
        page_title="Can I Drive?",
        page_icon=":beer:",
        layout="wide"
    )

    st.title("Breathalyzer :beer:")
    st.write(
        """
        Hi Co, here you can track your Blood Alcohol Content over time.  
        """
    )
    st.write("(Yes, it is based on your weight. No, I don't know your weight).")
    st.write("Just select the drinks you're having.")

    # Define drinks with volume, ABV fraction, and image path
    # Adjust image paths to match your actual files in static/images
    drinks_info = {
        "Beer (25cl ~5%)": {
            "name": "Beer (25cl ~5%)",
            "volume_ml": 250,
            "abv": 0.05,
            "image": "static/images/beer_light.jpg"
        },
        "Strong Beer (33cl ~8%)": {
            "name": "Strong Beer (33cl ~8%)",
            "volume_ml": 330,
            "abv": 0.08,
            "image": "static/images/beer_strong.jpg"
        },
        "Wine (20cl ~12%)": {
            "name": "Wine (20cl ~12%)",
            "volume_ml": 200,
            "abv": 0.12,
            "image": "static/images/wine.jpg"
        },
        "Shot (4cl ~40%)": {
            "name": "Shot (4cl ~40%)",
            "volume_ml": 40,
            "abv": 0.40,
            "image": "static/images/shot.jpg"
        },
        "Cocktail (~25cl)": {
            "name": "Cocktail (~25cl)",
            "volume_ml": 250,
            "abv": 0.20,  # approximate
            "image": "static/images/cocktail.jpg"
        }
    }

    # Display drink options with images
    st.subheader("Choose a drink:")

    for drink_name, info in drinks_info.items():
        # Create a row with image and button
        cols = st.columns([1, 3])  # left column for image, right column for button
        with cols[0]:
            if os.path.isfile(info["image"]):
                st.image(info["image"], width=70)
            else:
                st.warning(f"Image not found: {info['image']}")
        with cols[1]:
            if st.button(drink_name):
                # Add the drink to the JSON file
                add_drink(info)
                st.success(f"Added: {drink_name}")

                # Load current drinks to count
                drinks = load_drinks()
                beer_count = sum(1 for d in drinks if d["name"] == "Beer (25cl ~5%)")
                strong_beer_count = sum(1 for d in drinks if d["name"] == "Strong Beer (33cl ~8%)")
                wine_count = sum(1 for d in drinks if d["name"] == "Wine (20cl ~12%)")
                shot_count = sum(1 for d in drinks if d["name"] == "Shot (4cl ~40%)")
                cocktail_count = sum(1 for d in drinks if d["name"] == "Cocktail (~25cl)")

                # Unlock messages based on counts
                unlocked = False
                if beer_count == 3:
                    with st.spinner("Unlocking your reward..."):
                        time.sleep(1)
                        st.balloons()
                        st.success("You've unlocked: car keys! 🚗🔑")
                        unlocked = True
                if strong_beer_count == 2:
                    with st.spinner("Unlocking your reward..."):
                        time.sleep(1)
                        st.snow()
                        st.success("You've unlocked: car keys! 🚗🔑")
                        unlocked = True
                if shot_count == 3:
                    with st.spinner("Unlocking your reward..."):
                        time.sleep(1)
                        st.toast("You've unlocked: Flight to Mexico! 🛫🏖️")
                        unlocked = True
                if wine_count == 3:
                    with st.spinner("Unlocking your reward..."):
                        time.sleep(1)
                        st.image("static/images/wine_glass.gif", width=200)  # Ensure this GIF exists
                        st.success("You've unlocked: The closet! 🍷👩‍🎓")
                        unlocked = True
                if cocktail_count == 2:
                    with st.spinner("Unlocking your reward..."):
                        time.sleep(1)
                        st.image("static/images/cocktail_party.gif", width=200)  # Ensure this GIF exists
                        st.success("You've unlocked: The closet! 🍹👨‍🎓")
                        unlocked = True

        st.write("---")  # Separator line for clarity

    # Load drinks from the JSON file
    drinks = load_drinks()

    # Calculate BAC in promille
    bac = calculate_bac(drinks, user_weight=80.0, distribution_ratio=0.68)
    st.markdown(f"**Your alcohol level is:** `{bac:.5f} ‰`")

    # Provide feedback based on BAC (Belgian legal limit is 0.5‰)
    if bac >= 0.5:
        st.error("You are above the legal driving limit (0.5‰).")
    elif bac > 0.0:
        st.info("You are below the Belgian limit... for now.")
    else:
        st.success("You have no alcohol in your blood.")

    # Display counts of each drink type
    st.write("---")
    st.subheader("Your Drink Counts:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Beer (25cl ~5%)**: {sum(1 for d in drinks if d['name'] == 'Beer (25cl ~5%)')}")
    with col2:
        st.markdown(f"**Strong Beer (33cl ~8%)**: {sum(1 for d in drinks if d['name'] == 'Strong Beer (33cl ~8%)')}")
    with col3:
        st.markdown(f"**Wine (20cl ~12%)**: {sum(1 for d in drinks if d['name'] == 'Wine (20cl ~12%)')}")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(f"**Shot (4cl ~40%)**: {sum(1 for d in drinks if d['name'] == 'Shot (4cl ~40%)')}")
    with col5:
        st.markdown(f"**Cocktail (~25cl)**: {sum(1 for d in drinks if d['name'] == 'Cocktail (~25cl)')}")

    # Option to reset drink log
    st.write("---")
    if st.button("Reset Drink Log"):
        reset_drinks()
        st.success("Drink log has been reset.")

if __name__ == "__main__":
    main()
