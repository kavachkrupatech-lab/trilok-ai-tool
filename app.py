import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# पेज की सेटिंग और डिजाइन
st.set_page_config(
    page_title="Trilok AI Creator Studio", 
    page_icon="🎬", 
    layout="centered"
)

# ऐप का टाइटल (आपका ब्रांड नाम)
st.title("🎬 Trilok AI - स्टोरी और ऑडियो क्रिएटर")
st.markdown("---")
st.write("यहाँ अपना विषय लिखें। यह टूल आपके लिए बेहतरीन कहानी लिखेगा और उसका वॉयसओवर (ऑडियो) तैयार कर देगा—**बिल्कुल मुफ्त!**")

# साइडबार में API Key डालने की जगह
st.sidebar.header("🔑 सेटिंग्स")
api_key = st.sidebar.text_input("अपनी Google Gemini API Key यहाँ डालें:", type="password")

st.sidebar.markdown("---")
st.sidebar.info("💡 **टिप:** यह टूल पूरी तरह से फ्री है। Google AI Studio से फ्री API Key लेकर यहाँ डालनी है।")

# यूजर से विषय (Prompt) लेना
user_topic = st.text_area("आप किस विषय पर कहानी लिखना चाहते हैं?", placeholder="जैसे: शेर और चालाक बंदर...")

# भाषा चुनने का विकल्प
language_option = st.selectbox("आवाज की भाषा चुनें (Language):", ["Hindi", "English"])

# जनरेट करने का बटन
if st.button("🚀 कहानी और ऑडियो जनरेट करें"):
    if not api_key:
        st.warning("⚠️ कृपया पहले बाएं साइडबार (Sidebar) में अपनी Google Gemini API Key दर्ज करें।")
    elif not user_topic:
        st.warning("⚠️ कृपया कहानी का विषय लिखें।")
    else:
        try:
            # 1. Gemini AI को कॉन्फ़िगर करना और सही मॉडल चुनना
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            with st.spinner("⏳ AI आपकी कहानी लिख रहा है और आवाज़ तैयार हो रहा है... कृपया प्रतीक्षा करें"):
                prompt_instruction = f"एक बहुत ही दिलचस्प, आकर्षक और अच्छी कहानी या स्क्रिप्ट इस विषय पर लिखें: {user_topic}"
                response = model.generate_content(prompt_instruction)
                story_output = response.text
                
                # 2. कहानी को ऑडियो (Voiceover) में बदलना
                lang_code = 'hi' if language_option == "Hindi" else 'en'
                tts = gTTS(text=story_output, lang=lang_code, slow=False)
                audio_file = "trilok_audio.mp3"
                tts.save(audio_file)
            
            # सफलता का संदेश
            st.success("🎉 आपकी कहानी और ऑडियो सफलतापूर्वक तैयार हो गए हैं!")
            
            # रिजल्ट दिखाना (कहानी)
            st.subheader("📖 AI द्वारा रचित कहानी:")
            st.write(story_output)
            
            # ऑडियो प्लेयर
            st.subheader("🎧 ऑडियो सुनें:")
            st.audio(audio_file, format='audio/mp3')
            
            # डाउनलोड करने के विकल्प
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📥 टेक्स्ट डाउनलोड (TXT)", data=story_output, file_name="story.txt", mime="text/plain")
            with col2:
                with open(audio_file, "rb") as f:
                    st.download_button("📥 ऑडियो डाउनलोड (MP3)", data=f, file_name="audio.mp3", mime="audio/mp3")
            
        except Exception as e:
            st.error(f"❌ कुछ गड़बड़ी हुई है: {e}")

# फूटर
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Designed & Created by Trilok Singh | 100% Free & Open AI Tool</p>", unsafe_allow_html=True)
