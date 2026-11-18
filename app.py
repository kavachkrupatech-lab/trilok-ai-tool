import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# पेज की सेटिंग
st.set_page_config(page_title="Trilok AI Story & Audio Studio", page_icon="🎬", layout="centered")

st.title("🎬 Trilok AI - स्टोरी और ऑडियो क्रिएटर")
st.markdown("---")
st.write("यहाँ अपना विषय लिखें। यह टूल आपके लिए बेहतरीन कहानी लिखेगा और उसका वॉयसओवर (ऑडियो) तैयार कर देगा—**बिल्कुल मुफ्त!**")

# साइडबार में API Key
st.sidebar.header("🔑 सेटिंग्स")
api_key = st.sidebar.text_input("अपनी Google Gemini API Key यहाँ डालें:", type="password")

st.sidebar.markdown("---")
st.sidebar.info("💡 **टिप:** यदि 429 Quota Error आए, तो कृपया 40-50 सेकंड रुककर दोबारा कोशिश करें।")

user_topic = st.text_area("आप किस विषय पर कहानी लिखना चाहते हैं?", placeholder="जैसे: बंदर और शेर की कहानी...")
language_option = st.selectbox("आवाज की भाषा चुनें (Language):", ["Hindi", "English"])

if st.button("🚀 कहानी और ऑडियो जनरेट करें"):
    if not api_key:
        st.warning("⚠️ कृपया पहले बाएं साइडबार में अपनी Google Gemini API Key दर्ज करें।")
    elif not user_topic:
        st.warning("⚠️ कृपया कहानी का विषय लिखें।")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-3.8-flash')
            
            with st.spinner("⏳ AI आपकी कहानी लिख रहा है और आवाज़ तैयार हो रही है... कृपया इंतज़ार करें"):
                # 1. जेमिनी से कहानी जनरेट करना
                response = model.generate_content(f"एक बहुत ही दिलचस्प और अच्छी कहानी इस विषय पर लिखें: {user_topic}")
                story_output = response.text
                
                # 2. gTTS से ऑडियो बनाना
                lang_code = 'hi' if language_option == "Hindi" else 'en'
                tts = gTTS(text=story_output, lang=lang_code, slow=False)
                audio_file = "trilok_audio.mp3"
                tts.save(audio_file)
            
            st.success("🎉 आपकी कहानी और ऑडियो सफलतापूर्वक तैयार हो गए हैं!")
            
            # कहानी दिखाना
            st.subheader("📖 AI द्वारा रचित कहानी:")
            st.write(story_output)
            
            # ऑडियो प्लेयर
            st.subheader("🎧 ऑडियो सुनें:")
            st.audio(audio_file, format='audio/mp3')
            
            # डाउनलोड बटन
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
