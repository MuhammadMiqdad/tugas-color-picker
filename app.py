import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import streamlit as st
from io import BytesIO

def get_dominant_colors(image, k=5, random_state=42):
    # Ensure image is in RGB format
    image = image.convert('RGB')
    
    # Resize image to speed up processing but retain detail
    width, height = image.size
    aspect_ratio = height / width
    new_width = 400
    new_height = int(new_width * aspect_ratio)
    image = image.resize((new_width, new_height))
    image_np = np.array(image)
    
    # Reshape image to be a list of pixels
    pixels = image_np.reshape(-1, 3)
    
    # Perform KMeans clustering to find the dominant colors
    kmeans = KMeans(n_clusters=k, random_state=random_state)
    kmeans.fit(pixels)
    
    # Get the colors
    colors = kmeans.cluster_centers_.astype(int)
    return colors

def display_palette(colors):
    # Create an image with the color palette
    palette = Image.new('RGB', (300, 50 * len(colors)))
    for i, color in enumerate(colors):
        color_block = Image.new('RGB', (300, 50), tuple(color))
        palette.paste(color_block, (0, i * 50))
    return palette

def color_to_hex(color):
    return '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])

st.title('Dominant Color Palette Generator')

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    st.write("Generating palette...")
    colors = get_dominant_colors(image)
    palette = display_palette(colors)
    
    st.image(palette, caption='Color Palette', use_column_width=True)
    
    st.write('Dominant Colors:')
    cols = st.columns(len(colors))
    for i, color in enumerate(colors):
        with cols[i]:
            hex_color = color_to_hex(color)
            st.markdown(f"""
                <div class="color-block" style="background-color: {hex_color};">
                    <p>{hex_color}</p>
                </div>
            """, unsafe_allow_html=True)

# Optionally, add CSS for better styling
def local_css():
    css = """
    <style>
body {
    background-color: #f4f4f9;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
    color: #333;
    text-align: center;
    margin-bottom: 1.5rem;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.stButton>button:hover {
    background-color: #45a049;
}

.uploaded-image {
    margin-top: 2rem;
    text-align: center;
}

.color-block {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 120px;
    height: 120px;
    margin: 10px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transition: transform 0.3s ease;
    border: 3px solid #fff; /* Menambahkan bingkai putih */
}

.color-block:hover {
    transform: scale(1.1);
}

.color-block p {
    text-align: center;
    margin-top: 10px;
    font-size: 0.9rem;
    color: #555;
}
</style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Apply the custom CSS
local_css()
