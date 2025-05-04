import streamlit as st
import helpers.sidebar
import asyncio
from services.images import generate_image, get_all_images, delete_image

st.set_page_config(
    page_title="Images",
    page_icon="🏞️",
    layout="wide"
)

helpers.sidebar.show()

st.header("Image Generation")

tabs = st.tabs(["Image Generation", "Image List"])

with tabs[0]:
    prompt = st.text_input("Prompt", placeholder="Enter a prompt for the image generation model")
    if st.button("Generate Image"):
        if prompt:
            with st.spinner("Generating image..."):
                prompt_text, image_path = generate_image(prompt)
                st.success("Image generated successfully!")
                st.image(image_path, caption=prompt, use_column_width=True)
        else:
            st.warning("Please enter a prompt.")

with tabs[1]:
    st.subheader("Generated Images List")
    images_df = get_all_images()

    if images_df.empty:
        st.write("No images generated yet.")
    else:
        for idx, row in images_df.iterrows():
            file_name = row['Image'].split('/')[-1]
            with st.expander(file_name, expanded=False):
                st.text(f"Description: {row['Description']}")
                st.text(f"Date Created: {row['Date Created']}")

                if st.button(f"View_{idx}"):
                    st.image(row['Image'], caption=row['Description'], use_column_width=True)

                if st.button(f"Delete_{idx}"):
                    delete_image(row['Image'])
                    st.success(f"Deleted {file_name}")
                    images_df = get_all_images()


