import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

st.set_page_config(page_title="Trilok AI Creator Studio", page_icon="🎬", layout="centered")

st.title("🎬 Trilok AI - स्टोरी और ऑडियो क्रिएटर")
st.markdown("---")
st.write("यहाँ अपना विषय लिखें। यह टूल आपके लिए बेहतरीन कहानी लिखेगा और उसका वॉयसओवर तैयार कर देगा—**बिल्कुल मुफ्त!**")

st.sidebar.header("🔑 सेटिंग्स")
api_key = st.sidebar.text_input("अपनी Google Gemini API Key यहाँ डालें:", type="password")

st.sidebar.markdown("---")
st.sidebar.info("💡 यह टूल पूरी तरह से फ्री है।")

user_topic = st.text_area("आप किस विषय पर कहानी लिखना चाहते हैं?", placeholder="जैसे: राजा रानी और उसका चालक प्रधानमंत्री...")
language_option = st.selectbox("आवाज की भाषा चुनें (Language):", ["Hindi", "English"])

if st.button("🚀 कहानी और ऑडियो जनरेट करें"):
    if not api_key:
        st.warning("⚠️ कृपया पहले बाएं साइडबार में अपनी Google Gemini API Key दर्ज करें।")
    elif not user_topic:
        st.warning("⚠️ कृपया कहानी का विषय लिखें।")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # यह तरीका खुद-ब-खुद आपके अकाउंट का सबसे सही और चालू मॉडल ढूंढ लेगा, नाम बदलने की कभी जरूरत नहीं पड़ेगी
            model = None
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    if 'flash' in m.name or 'pro' in m.name:
                        model = genai.GenerativeModel(m.name)
                        break
            if model is None:
                model = genai.GenerativeModel('gemini-pro')

            with st.spinner("⏳ AI आपकी कहानी लिख रहा है और आवाज़ तैयार हो रही है..."):
                response = model.generate_content(f"एक बहुत ही दिलचस्प और अच्छी कहानी इस विषय पर लिखें: {user_topic}")
                story_output = response.text
                
                lang_code = 'hi' if language_option == "Hindi" else 'en'
                tts = gTTS(text=story_output, lang=lang_code, slow=False)
                audio_file = "trilok_audio.mp3"
                tts.save(audio_file)
            
            st.success("🎉 आपकी कहानी और ऑडियो तैयार हो गए हैं!")
            st.subheader("📖 AI द्वारा रचित कहानी:")
            st.write(story_output)
            
            st.subheader("🎧 ऑडियो सुनें:")
            st.audio(audio_file, format='audio/mp3')
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📥 टेक्स्ट डाउनलोड (TXT)", data=story_output, file_name="story.txt", mime="text/plain")
            with col2:
                with open(audio_file, "rb") as f:
                    st.download_button("📥 ऑडियो डाउनलोड (MP3)", data=f, file_name="audio.mp3", mime="audio/mp3")
            
        except Exception as e:
            st.error(f"❌ कुछ गड़बड़ी हुई है: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Designed & Created by Trilok Singh | 100% Free & Open AI Tool</p>", unsafe_allow_html=True)
