import streamlit as st
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image  # Import the Image module from PIL

# Load the CLIP model and processor
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")

# Set the title and description of your Streamlit app
st.title("Image Captioning App")
st.write("Upload an image, and the app will generate a caption for it.")

# Upload an image using Streamlit's file uploader widget
uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

# Check if an image is uploaded
if uploaded_image:
    # Display the uploaded image
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    # Generate captions when a button is clicked
    if st.button("Generate Caption"):
        # Read and preprocess the uploaded image
        image = Image.open(uploaded_image)  # Open the uploaded image

        # Generate a caption for the image
        inputs = processor(text="a photo of a " + st.text_input("Describe the image:", "flower"), images=image, return_tensors="pt")
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(1)
        label = processor.decode(probs.argmax(1)[0])

        # Display the generated caption
        st.subheader("Generated Caption:")
        st.write(label)
