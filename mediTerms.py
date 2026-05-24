import streamlit as st
from google import genai

# Set up the webpage layout and design
st.set_page_config(page_title="MediTerms AI", page_icon="🏥", layout="centered")

st.title("🏥 MediTerms AI")
st.subheader("Translate complex medical jargon into everyday language.")
st.markdown("---")

# 🔑 PASTE YOUR GEMINI API KEY HERE BEFORE TESTING!
GEMINI_API_KEY = "Your_api_key"

# Define our sample texts
example_1 = "Patient presents with acute nasopharyngitis, persistent cephalea, and mild bilateral otitis media. Recommended course of action includes a 5-day regimen of oral amoxicillin."
example_2 = "ECG reveals sinus tachycardia. Patient reports mild dyspnea on exertion and left-sided thoracic discomfort. Rule out acute myocardial infarction. Referred to cardiology."

# 1. Dropdown Selection Menu for Examples
st.markdown("### 🧪 Select a Medical Note to Test")
option = st.selectbox(
    "Choose a preset example or select 'Custom Input' to type your own:",
    ("Custom Input (Type below)", "Example 1: ENT Infection", "Example 2: Heart/Chest Concern")
)

# Set the text area value based on the dropdown choice
if option == "Example 1: ENT Infection":
    chosen_text = example_1
elif option == "Example 2: Heart/Chest Concern":
    chosen_text = example_2
else:
    chosen_text = ""

# 2. Main Input Text Area
medical_note = st.text_area(
    "Paste your medical report or doctor's note here:", 
    value=chosen_text,
    height=180,
    placeholder="Type or paste medical text here..."
)

# 3. Running the AI Translation
if st.button("✨ Translate Note", type="primary"):
    if GEMINI_API_KEY == "YOUR_ACTUAL_GEMINI_API_KEY_HERE" or not GEMINI_API_KEY:
        st.error("Please replace 'YOUR_ACTUAL_GEMINI_API_KEY_HERE' in your code with your real key from Google AI Studio!")
    elif not medical_note:
        st.warning("Please type a note or choose an example from the dropdown menu above first!")
    else:
        with st.spinner("🧠 AI is analyzing and translating medical terms..."):
            try:
                # Initialize the Gemini Client
                client = genai.Client(api_key=GEMINI_API_KEY)
                
                prompt_instructions = f"""
                You are a helpful medical translator. Your task is to translate complex medical terms and clinical doctor notes into plain, simple, everyday English that a regular patient can easily understand.
                
                Structure your output cleanly with these three distinct headings:
                ### 📝 Plain English Translation
                (Explain the text in simple terms)
                
                ### 🔑 Key Takeaways
                (Bullet points of the most critical details)
                
                ### 👟 Suggested Next Steps
                (What questions or actions the patient should discuss with their doctor)
                
                Important: Include a brief disclaimer at the very bottom stating that you are an AI translator, not a doctor, and this is for educational purposes only.
                
                Here is the medical note to translate:
                {medical_note}
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_instructions,
                )
                
                st.markdown("---")
                st.success("Analysis Complete!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
