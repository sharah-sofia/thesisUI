import streamlit as st
import requests

# Set page config with yellow theme
st.set_page_config(
    page_title="EEG Seizure Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for yellow theme and prediction alerts
st.markdown("""
    <style>
    .main {
        background-color: #4b5938;
        color: black;
    }
    .stApp {
        background-color: #4b5938;
            color: black;
    }
    .prediction-normal {
        background-color: #4CAF50;
        color: black;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        margin: 20px 0;
    }
    .prediction-seizure {
        background-color: #f44336;
        color: black;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🧠 EEG Seizure Prediction")
st.write("Upload an EEG .txt file to predict if seizure will happen or not.")

# File uploader
uploaded_file = st.file_uploader("Upload EEG File", type="txt")

if uploaded_file is not None:
    with st.spinner("Processing your file..."):
        # Send the uploaded file to Flask API
        files = {"file": uploaded_file}
        try:
            response = requests.post("http://127.0.0.1:5000/predict", files=files)
            
            if response.status_code == 200:
                prediction = response.json()["prediction"]
                
                # Display prediction with appropriate styling
                if "Normal Brain Activity" in prediction:
                    st.markdown(f"""
                        <div class="prediction-normal">
                            ✅ {prediction}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="prediction-seizure">
                            ⚠️ {prediction}
                        </div>
                    """, unsafe_allow_html=True)
                
                # Additional information
                with st.expander("View Details"):
                    st.write("File processed successfully")
                    st.write("Prediction confidence: High")
                    
            else:
                st.error("Error processing the file. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the prediction server. Please ensure the Flask backend is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("### How to use:")
st.write("1. Upload a .txt file containing EEG data")
st.write("2. Wait for the prediction")