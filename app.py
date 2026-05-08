import streamlit as st
from google import genai
from PIL import Image
from huggingface_hub import InferenceClient

# Page Configuration
st.set_page_config(page_title="Chaos Generator", page_icon="🌀")

# Sidebar for API Key Management
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
hf_token = st.sidebar.text_input("Enter Hugging Face Token", type="password")

# Initialize clients
gemini_client = genai.Client(api_key=api_key) if api_key else None
hf_client = InferenceClient(provider="auto", api_key=hf_token) if hf_token else None

st.title("🌀 Chaos Generator App")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Daily Horoscope", "Diary", "Photobook"])

with tab1:
    st.header("🔮 Mirror Mirror On The Wall")
    sun_sign = st.selectbox("Select your sign", ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"])
    if st.button("Look into the Mirror"):
        if not gemini_client:
            st.error("Please enter your Gemini API key in the sidebar first.")
        else:
            with st.spinner("Reflecting..."):
                try:
                    prompt = f"Write a daily horoscope for {sun_sign}. Start with standard, gentle astrology tropes, but quickly pivot into a blunt, dark, and sad reflection of a difficult phase in human life. It should bring the reader down and must end with an ominous warning. Keep it under 4 sentences."
                    response = gemini_client.models.generate_content(model='gemini-3-flash-preview', contents=prompt)
                    st.write(response.text)
                except Exception as e:
                    st.error(f"API Error: {e}")

with tab2:
    st.header("📜 What If")
    st.write("Ever wonder what could happen differently? Tell a story here.")
    user_script = st.text_area("e.g., 'I met someone I hate.'")
    if st.button("Rewrite Fate"):
        if not gemini_client:
            st.error("Please enter your Gemini API key in the sidebar first.")
        elif not user_script.strip():
            st.warning("Please enter a scenario.")
        else:
            with st.spinner("Writing a new outcome..."):
                try:
                    prompt = f"Take the following diary entry or scenario and write a completely different outcome. Depending on the core context of the prompt, make the new outcome either hyper-romantic or hyper-tragic. Do not hold back on the psychological intensity or dark themes. Keep it under 150 words.\n\nScenario: {user_script}"
                    response = gemini_client.models.generate_content(model='gemini-3-flash-preview', contents=prompt)
                    st.write(response.text)
                except Exception as e:
                    st.error(f"API Error: {e}")

with tab3:
    st.header("👁️ Not Your Typical Image Generator")
    st.write("Upload an image. We will inject it with artifacts, mutations, and structural failure.")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        input_image_bytes = uploaded_file.read()
        st.image(input_image_bytes, caption="Original Image", use_container_width=True)
        
        if st.button("Inject Chaos"):
            if not hf_client:
                st.error("Hugging Face key is required in the sidebar.")
            else:
                with st.spinner("Corrupting image composition..."):
                    try:
                        corrupted_image = hf_client.image_to_image(
                            image=input_image_bytes,
                            prompt="cursed, mutated, extra limbs, glitch art, severe compression artifacts, terrifying, distorted faces, nightmare, deep fried, wrong anatomy, 3 hands",
                            model="black-forest-labs/FLUX.2-klein-4B"
                        )
                        st.image(corrupted_image, caption="Structural Integrity Compromised", use_container_width=True)
                    except Exception as e:
                        st.error(f"HF Provider Error: {e}")