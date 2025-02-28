import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import time  # For loading effect

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# File paths
MODEL_PATH = "Model/keras_model.h5"
LABELS_PATH = "Model/labels.txt"

# Custom Styling
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #1e3c72, #2a5298);
        color: white;
    }
    .stApp {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 20px;
        border-radius: 15px;
    }
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton button:hover {
        background-color: #d43f3f;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the trained Keras model
@st.cache_resource
def load_trained_model():
    return load_model(MODEL_PATH, compile=False)

model = load_trained_model()

# Load class labels dynamically from labels.txt
def load_labels():
    with open(LABELS_PATH, "r") as f:
        return [label.strip().split(maxsplit=1)[-1] for label in f.readlines()]  # Extract only the blood group

LABELS = load_labels()


# Streamlit UI
st.markdown("<h1 style='text-align: center;'>🔬 Blood Group Detection from Fingerprint 🩸</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Upload a fingerprint image", type=["jpg", "png", "jpeg", "bmp"])

if uploaded_file:
    with st.spinner("Processing Image... 🔍"):
        time.sleep(1.5)
    
    image_data = Image.open(uploaded_file).convert("RGB")
    # st.image(image_data, caption="📷 Uploaded Image", use_column_width=True)
    st.image(image_data, caption="📷 Uploaded Image",use_container_width=True)

    # Resize and preprocess image
    size = (224, 224)
    image_data = ImageOps.fit(image_data, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image_data).astype(np.float32)
    normalized_image_array = (image_array / 127.5) - 1
    input_tensor = np.expand_dims(normalized_image_array, axis=0)

    # Prediction loading effect
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
    
    prediction = model.predict(input_tensor)[0]
    predicted_index = np.argmax(prediction)
    predicted_label = LABELS[predicted_index]
    confidence_score = prediction[predicted_index]

    # Display results
    st.markdown(
        f"""
        <div style="background: #fff; padding: 20px; border-radius: 10px; text-align: center;">
            <h2 style="color: #ff4b4b;">🩸 Predicted Blood Group: {predicted_label}</h2>
            <h3>Confidence Score: {confidence_score:.2%}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display class probabilities
    st.subheader("📊 Class Probabilities:")
    probs = {LABELS[i]: round(pred, 4) for i, pred in enumerate(prediction)}
    st.json(probs)
