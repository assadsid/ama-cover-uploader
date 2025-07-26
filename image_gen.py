import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import asyncio
import re
from io import BytesIO

from my_agents.facebook_agent import upload_facebook_cover
from agents import Runner, set_tracing_disabled
from my_agents.scraper_agent import agent2

set_tracing_disabled(True)

# ----- Async Agent Call -----
async def get_result():
    return await Runner.run(
        starting_agent=agent2,
        input="Total AMA Accounts"
    )

# ----- Image Generator -----
def generate_image(number, word):
    img = Image.open("main_img.jpeg").convert("RGB")
    draw = ImageDraw.Draw(img)
    width, height = img.size

    try:
        font_large = ImageFont.truetype("pop-black.ttf", 60)
        font_medium = ImageFont.truetype("pop-ebold.ttf", 30)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()

    def get_center_x(text, font):
        return (width - draw.textlength(text, font=font)) / 2

    number_x = get_center_x(number, font_large)
    word_x = get_center_x(word.upper(), font_medium)
    number_y = int(height * 0.38)
    word_y = number_y + 65

    draw.text((number_x, number_y), number, font=font_large, fill="black")
    draw.text((word_x, word_y), word.upper(), font=font_medium, fill=(160, 32, 85))

    return img

# ----- Streamlit UI -----
st.set_page_config(page_title="AMA Image Generator", layout="centered")
st.title("\U0001F4CA AMA Account Facebook Image Generator")

# State holders
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None
if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None

# --- Main Action Button ---
if st.button("\U0001F504 Get Latest AMA Total & Generate Image"):
    with st.spinner("Scraping and generating image..."):
        result = asyncio.run(get_result())
        response_text = result.final_output

        num_match = re.search(r"Number of Accounts:\s*([\d,]+)", response_text)
        word_match = re.search(r"Accounts in Word:\s*([\w\. ]+)", response_text)

        number = num_match.group(1) if num_match else "N/A"
        word = word_match.group(1) if word_match else "N/A"

        st.success("\u2705 Data Scraped & Image Ready!")

        # Generate and display
        image = generate_image(number, word)
        st.image(image, caption="Generated Facebook Cover", use_container_width=True)

        # Save for session use
        st.session_state.generated_image = image

        # Save image to buffer
        buf = BytesIO()
        image.save(buf, format="JPEG")
        st.session_state.image_bytes = buf.getvalue()

        # Save image to disk for Facebook upload
        with open("ama_facebook_cover.jpg", "wb") as f:
            f.write(st.session_state.image_bytes)

# --- Download Button ---
if st.session_state.image_bytes:
    st.download_button(
        label="\U0001F4E5 Download Image",
        data=st.session_state.image_bytes,
        file_name="ama_facebook_cover.jpg",
        mime="image/jpeg"
    )

# --- Upload to Facebook Cover ---
if st.session_state.generated_image:
    if st.button("\U0001F4E4 Upload to Facebook Cover"):
        with st.spinner("Uploading image to Facebook..."):
            result = upload_facebook_cover("ama_facebook_cover.jpg")
            if result.get("success"):
                st.success("Cover photo uploaded successfully!")
            else:
                st.error(f"Upload failed: {result.get('error')}")
