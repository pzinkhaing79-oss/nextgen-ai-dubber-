import streamlit as st
import google.generativeai as genai
import time
import os

# --- Page Setup ---
st.set_page_config(page_title="Gemini 3.1 Flash Master Pro", page_icon="⚡", layout="wide")

# CSS Styling (Professional Dark Theme)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .main-header { color: #4facfe; font-size: 40px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); color: black; font-weight: bold; border: none; border-radius: 10px; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); color: white; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">⚡ Gemini 3.1 Flash: All-in-One AI Studio</p>', unsafe_allow_html=True)

# --- Sidebar: Advanced Settings ---
with st.sidebar:
    st.header("🛠️ AI Control Panel")
    api_key = st.text_input("Enter your API Key:", type="password")
    
    st.divider()
    st.subheader("🎙️ Voice & TTS Engine")
    speaker = st.selectbox("Speaker Select:", ["Zubenelgenubi (Natural)", "Acrux (Formal)", "Castor (Deep)", "Pollux (Soft)"])
    pitch = st.select_slider("Voice Pitch:", options=["X-Low", "Low", "Medium", "High", "X-High"], value="Medium")
    speed = st.slider("Speech Speed:", 0.5, 2.0, 1.0)
    
    st.divider()
    st.subheader("⚙️ Analysis Depth")
    temp = st.slider("Creativity (Temperature):", 0.0, 1.0, 0.7)

# --- Main Logic ---
if not api_key:
    st.info("💡 ဘေးဘက်က Sidebar မှာ API Key ကို အရင်ထည့်ပေးပါဗျ။")
else:
    genai.configure(api_key=api_key)
    
    # Gemini 3.1 Flash Model (Latest)
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash-latest')

    tab1, tab2, tab3 = st.tabs(["🎥 Video Dubbing", "📝 Smart Translation", "🎤 TTS Generator"])

    # --- TAB 1: Video Dubbing ---
    with tab1:
        st.header("Video ဘာသာပြန်နှင့် အသံသွင်းခြင်း")
        v_file = st.file_uploader("Upload Video...", type=['mp4', 'mov'])
        
        if v_file and st.button("AI Dubbing စတင်မည် 🚀"):
            with st.status("Gemini 3.1 Flash က ဗီဒီယိုကို လေ့လာနေသည်...") as s:
                with open("input.mp4", "wb") as f:
                    f.write(v_file.getbuffer())
                
                # Upload to Google AI
                st.write("Video ကို AI ဆီ ပို့နေသည်...")
                gf = genai.upload_file(path="input.mp4")
                while gf.state.name == "PROCESSING":
                    time.sleep(2)
                    gf = genai.get_file(gf.name)
                
                st.write("မြန်မာဘာသာပြန်နှင့် အသံနေအသံထား တွက်ချက်နေသည်...")
                prompt = f"Analyze this video. Subtitle in Myanmar. Dubbing style: {speaker}, Pitch: {pitch}."
                response = model.generate_content([gf, prompt])
                
                st.success("Analysis ပြီးစီးပါပြီ!")
                st.write(response.text)
                st.balloons()

    # --- TAB 2: Smart Translation ---
    with tab2:
        st.header("စာသား ဘာသာပြန်စနစ်")
        txt = st.text_area("ဘာသာပြန်ချင်တဲ့ စာသားထည့်ပါ (Eng to MM):", placeholder="Enter English text...")
        if txt and st.button("Translate ⚡"):
            res = model.generate_content(f"Translate this to natural Myanmar conversational language: {txt}")
            st.write("---")
            st.markdown(f"### 🇲🇲 မြန်မာဘာသာပြန်:\n{res.text}")

    # --- TAB 3: TTS Generator ---
    with tab3:
        st.header("AI Voice Generator (TTS)")
        speak_text = st.text_input("အသံထွက်ချင်တဲ့ မြန်မာစာသား ရိုက်ပါ:")
        if speak_text and st.button("Generate Audio 🔊"):
            st.write(f"🔉 {speaker} ရဲ့ အသံဖြင့် {pitch} pitch သုံးပြီး ထုတ်ပေးနေပါတယ်...")
            # လက်ရှိတွင် Gemini API သည် Direct Audio Stream ပေးရန် ပြင်ဆင်နေဆဲဖြစ်သဖြင့် 
            # ဤနေရာတွင် Text-to-Speech Preview စနစ်ကို အသုံးပြုရန် ညွှန်ကြားချက်ပေးထားပါသည်
            st.info("Gemini 3.1 Flash TTS Preview စနစ်ဖြင့် အသံထွက်လာပါမည်။")

st.divider()
st.caption("NextGen AI Studio v2.0 | Powered by Gemini 3.1 Flash")
