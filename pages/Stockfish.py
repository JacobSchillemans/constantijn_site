# pages/4_stockfish.py

import streamlit as st
import os
import base64

##################
# Helper Functions
##################

def embed_local_image(image_path: str, width=300, height=250, border_color="red"):
    """
    Reads an image file from disk, encodes it to base64, 
    and returns an HTML img tag string for embedding.
    Automatically detects MIME type based on file extension.
    """
    if not os.path.isfile(image_path):
        return f"<p style='color: white;'>Image not found: {image_path}</p>"

    with open(image_path, "rb") as file:
        data = file.read()
    base64_data = base64.b64encode(data).decode("utf-8")
    
    # Determine the image's MIME type based on its extension
    ext = os.path.splitext(image_path)[1].lower()
    if ext == '.png':
        mime = 'image/png'
    elif ext in ['.jpg', '.jpeg']:
        mime = 'image/jpeg'
    elif ext == '.gif':
        mime = 'image/gif'
    else:
        mime = 'image/png'  # default to PNG if unknown
    
    # Return the image tag without additional text
    html_img = f"""
    <img src="data:{mime};base64,{base64_data}"
         style="cursor: pointer; border: 3px solid {border_color}; 
                width: {width}px; height: {height}px;" />
    """
    return html_img

def main():
    # Configure the page title & layout
    st.set_page_config(
        page_title="The Only 4 Sites You Need",
        page_icon=":fish:",
        layout="wide"
    )

    ##############
    # Page Styling
    ##############
    st.markdown("""
        <style>
        /* Hide hamburger menu & footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Hide the entire sidebar */
        [data-testid="stSidebar"] {
            display: none !important;
        }

        /* Make the background black */
        .stApp {
            background-color: black !important;
        }

        /* Remove default padding/margins */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Style for the "Back to Main Page" button */
        .back-button {
            background-color: red;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin-top: 30px;
            border-radius: 5px;
            cursor: pointer;
        }

        .back-button:hover {
            background-color: darkred;
        }
        </style>
    """, unsafe_allow_html=True)

    ################
    # Page Content
    ################
    # Title
    st.markdown(
        "<h1 style='color: white; text-align: center;'>4 Sites 4 You</h1>",
        unsafe_allow_html=True
    )

    # Description (Optional)
    #st.write("## :fish: Explore These Essential Sites")

    # Create a 2x2 grid of images, each linking to its respective URL
    row1col1, row1col2 = st.columns(2)
    row2col1, row2col2 = st.columns(2)

    #########################
    # 1) Local Weather Ixelles
    #########################
    with row1col1:
        weather_img_html = embed_local_image("static/images/weather.webp")
        st.markdown(
            f"""
            <div style='text-align: right;'>
                <a href="https://www.buienradar.be/weer/etterbeek/be/2798578" target="_blank"
                   style='text-decoration: none;'>{weather_img_html}</a>
            </div>
            """,
            unsafe_allow_html=True
        )
        #st.markdown("<p style='color: white; text-align: center;'>Local Weather Ixelles</p>", unsafe_allow_html=True)

    ################
    # 2) Chess Site
    ################
    with row1col2:
        chess_img_html = embed_local_image("static/images/chess.jpg")
        st.markdown(
            f"""
            <div style='text-align: left;'>
                <a href="https://lichess.org/" target="_blank"
                   style='text-decoration: none;'>{chess_img_html}</a>
            </div>
            """,
            unsafe_allow_html=True
        )
        #st.markdown("<p style='color: white; text-align: center;'>Lichess</p>", unsafe_allow_html=True)

    ################
    # 3) Palantir Stock
    ################
    with row2col1:
        palantir_img_html = embed_local_image("static/images/palantir.png")
        st.markdown(
            f"""
            <div style='text-align: right;'>
                <a href="https://www.google.com/search?q=palantir+stock" target="_blank"
                   style='text-decoration: none;'>{palantir_img_html}</a>
            </div>
            """,
            unsafe_allow_html=True
        )
        #st.markdown("<p style='color: white; text-align: center;'>Palantir Stock</p>", unsafe_allow_html=True)

    ###################
    # 4) Fishing Forecast
    ###################
    with row2col2:
        fishing_img_html = embed_local_image("static/images/fish.jpeg")
        st.markdown(
            f"""
            <div style='text-align: left;'>
                <a href="https://www.accuweather.com/en/be/brussels/27581/fishing-weather/27581" target="_blank"
                   style='text-decoration: none;'>{fishing_img_html}</a>
            </div>
            """,
            unsafe_allow_html=True
        )
        #st.markdown("<p style='color: white; text-align: center;'>Fishing Forecast</p>", unsafe_allow_html=True)

    #############################
    # "Back to Main Page" Button
    #############################
    # Add a horizontal rule for separation
    st.write("---")

    # Center the button using HTML/CSS
    st.markdown(
        """
        <div style='text-align: center;'>
            <a href="/" class="back-button">Back to Main Page</a>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
