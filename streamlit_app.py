# streamlit_app.py
"""
Image Processing Streamlit App (Final version with dynamic titles & no warnings)
"""

from io import BytesIO
import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
import numpy as np

st.set_page_config(page_title="Image Processing Project", layout="wide")

st.markdown("""
# 🖼️ Image Processing Web App
Upload an image from the sidebar, choose a filter and adjust parameters. Then download the processed image.
""")

# Sidebar: uploader and filter selection
with st.sidebar:
    st.header("Upload & Filters")
    uploaded_file = st.file_uploader("Browse image (PNG / JPG / JPEG)", type=["png", "jpg", "jpeg"])
    st.markdown("---")
    filter_choice = st.selectbox(
        "Choose a filter",
        ["None", "Brightness", "Contrast", "Invert", "Enhancement (Auto Equalize)", "Grayscale"]
    )
    st.markdown("**Filter options**")

    # safe defaults
    brightness_factor = 1.0
    contrast_factor = 1.0

    # sliders for brightness/contrast
    if filter_choice == "Brightness":
        brightness_factor = st.slider(
            "Brightness factor", 0.1, 3.0, 1.0, 0.05,
            help="1.0 = original, <1 darker, >1 brighter"
        )
    elif filter_choice == "Contrast":
        contrast_factor = st.slider(
            "Contrast factor", 0.1, 3.0, 1.0, 0.05,
            help="1.0 = original, >1 more contrast, <1 less contrast"
        )

    st.markdown("---")
    st.write("Tip: You can re-upload or change filter to see different results.")
    st.markdown("---")
    st.write("Made for college project. Ready to deploy on Streamlit Cloud or locally.")


def load_image(file) -> Image.Image:
    # Ensure image is RGB so ImageOps.invert works properly
    img = Image.open(file).convert("RGB")
    return img


def apply_filter(img: Image.Image, choice: str, brightness_factor=1.0, contrast_factor=1.0) -> Image.Image:
    if choice == "None":
        return img.copy()

    img_out = img.copy()

    if choice == "Brightness":
        enhancer = ImageEnhance.Brightness(img_out)
        img_out = enhancer.enhance(brightness_factor)

    elif choice == "Contrast":
        enhancer = ImageEnhance.Contrast(img_out)
        img_out = enhancer.enhance(contrast_factor)

    elif choice == "Invert":
        img_out = ImageOps.invert(img_out)

    elif choice == "Enhancement (Auto Equalize)":
        img_out = ImageOps.equalize(img_out)

    elif choice == "Grayscale":
        img_out = ImageOps.grayscale(img_out)

    return img_out


# Main area: show original and processed
if uploaded_file is None:
    st.info("Please upload an image from the sidebar to start.")
    st.stop()

# Load image
try:
    original = load_image(uploaded_file)
except Exception as e:
    st.error(f"Unable to read image. Try another file. ({e})")
    st.stop()

# Apply filter
processed = apply_filter(original, filter_choice, brightness_factor, contrast_factor)

# Dynamic title for processed image
if filter_choice == "None":
    processed_title = "Processed Image (No Filter)"
else:
    processed_title = f"After {filter_choice} Filter"

# Layout: original and processed side by side
col1, col2 = st.columns(2)
with col1:
    st.subheader("Original Image")
    st.image(original, use_container_width=True)   # ✅ replaced deprecated parameter

with col2:
    st.subheader(processed_title)
    st.image(processed, use_container_width=True)  # ✅ replaced deprecated parameter

# Download processed image
def get_image_bytesio(img: Image.Image, fmt="PNG"):
    buf = BytesIO()
    img.save(buf, format=fmt)
    buf.seek(0)
    return buf

buf = get_image_bytesio(processed)
st.download_button(
    label="Download Processed Image",
    data=buf,
    file_name="processed_image.png",
    mime="image/png"
)

# Optional info
st.sidebar.markdown("---")
st.sidebar.write("Image size:", f"{original.width} x {original.height} pixels")
st.sidebar.write("Mode:", original.mode)
