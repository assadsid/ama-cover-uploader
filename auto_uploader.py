import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import asyncio
import re
from io import BytesIO
import os

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
    word_x = get_center_x(word, font_medium)
    number_y = int(height * 0.38)
    word_y = number_y + 65

    draw.text((number_x, number_y), number, font=font_large, fill="black")
    draw.text((word_x, word_y), word.upper(), font=font_medium, fill=(160, 32, 85))

    return img

# ----- Streamlit UI -----
st.set_page_config(page_title="AMA Auto Facebook Uploader", layout="centered")
st.title("🤖 AMA Auto Facebook Cover Uploader")

# Prevent re-running on every rerun
if "uploaded" not in st.session_state:
    with st.spinner("Scraping AMA data & generating image..."):
        # Step 1: Get scraped result
        result = asyncio.run(get_result())
        response_text = result.final_output

        # Step 2: Extract numbers
        num_match = re.search(r"Number of Accounts:\s*([\d,]+)", response_text)
        word_match = re.search(r"Accounts in Word:\s*([\w\. ]+)", response_text)

        number = num_match.group(1) if num_match else "N/A"
        word = word_match.group(1) if word_match else "N/A"

        # Step 3: Generate Image
        image = generate_image(number, word)
        buf = BytesIO()
        image.save(buf, format="JPEG")
        byte_data = buf.getvalue()

        # Save image to file
        img_path = "ama_facebook_cover.jpg"
        with open(img_path, "wb") as f:
            f.write(byte_data)

        # Step 4: Upload to Facebook
        upload_result = upload_facebook_cover(img_path)

        if isinstance(upload_result, dict):
            if upload_result.get("success"):
                st.success("✅ Your AMA Cover has been updated on Facebook.")
            else:
                st.error(f"❌ Upload failed: {upload_result.get('error')}")
        else:
            st.write(upload_result)

        # Optional: preview the generated image
        st.image(image, caption="Generated AMA Facebook Cover", use_container_width=True)

        st.session_state.uploaded = True  # prevent rerun

else:
    st.info("✅ AMA Cover was already updated in this session.")
