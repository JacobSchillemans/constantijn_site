import streamlit as st
import base64
import os
import datetime

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

def calculate_age(dob: datetime.datetime, current_time: datetime.datetime):
    """
    Calculate age in years with decimal precision based on the date of birth and current time.
    """
    delta = current_time - dob
    age_in_days = delta.days + delta.seconds / 86400  # including fraction of day
    age_in_years = age_in_days / 365.25  # Approximate, accounting for leap years
    return age_in_years

def main():
    # Configure the page title & layout
    st.set_page_config(
        page_title="Co’s starting point",
        page_icon=":dog:",
        layout="wide"
    )

    # Hide default Streamlit elements & set black background
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

        /* Remove margins/padding to ensure content is centered vertically */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Red title on black background, centered
    st.markdown(
        "<h1 style='color: red; text-align: center;'>Welcome Co, I've been expecting you</h1>",
        unsafe_allow_html=True
    )

    # Add optional subtitle or remove as per user: User previously added an h2
    #st.markdown(
    #    "<h2 style='color: white; text-align: center;'>Choose your starting point</h2>",
    #    unsafe_allow_html=True
    #)

    # First row of 2 images
    row1col1, row1col2 = st.columns(2)

    with row1col1:
        # Sjoe page link (formerly "Anouk")
        anouk_img_html = embed_local_image("static/images/anouk.jpg")
        st.markdown(
            f"""
            <div style='text-align: right;'>
                <a href="Sjoe" style='text-decoration: none;'>{anouk_img_html}</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    with row1col2:
        # Liégois page link (formerly "Standard de Liège")
        liegeois_img_html = embed_local_image("static/images/standard.png")
        st.markdown(
            f"""
            <div style='text-align: left;'>
                <a href="Liégois" style='text-decoration: none;'>{liegeois_img_html}</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Second row of 2 images
    row2col1, row2col2 = st.columns(2)

    with row2col1:
        # "Can I drive?" page link (formerly "Breathalyzer")
        can_i_drive_img_html = embed_local_image("static/images/beer.jpg")
        st.markdown(
            f"""
            <div style='text-align: right;'>
                <a href="Breathalyzer" style='text-decoration: none;'>{can_i_drive_img_html}</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    with row2col2:
        # "stockfish" page link (formerly "Extras")
        stockfish_img_html = embed_local_image("static/images/stockfish.jpeg")
        st.markdown(
            f"""
            <div style='text-align: left;'>
                <a href="Stockfish" style='text-decoration: none;'>{stockfish_img_html}</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Calculate Co's age
    dob = datetime.datetime(2000, 10, 6)
    now = datetime.datetime.now()
    age_in_years = calculate_age(dob, now)
    age_str = f"{age_in_years:.10f}"

    st.write("---")

    # Show Co's age in white text, centered, below the images with larger font size
    st.markdown(
        f"<p style='color: white; text-align: center; font-size: 28px;'>"
        f"Btw, you're currently {age_str} years old</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
