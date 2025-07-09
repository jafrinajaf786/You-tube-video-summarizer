import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator

# Get YouTube transcript text
def get_transcript(video_url):
    video_id = video_url.split("v=")[-1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_text = " ".join([item['text'] for item in transcript])
    return full_text

# Simple rule-based summary: take first N sentences
def basic_summary(text, num_sentences=20):
    sentences = text.split('. ')
    return ". ".join(sentences[:num_sentences]) + "."

# Streamlit App
st.title(" 🔴▶️ 𝚈𝚘𝚞𝚝𝚞𝚋𝚎 \n AI Powered YOUTUBE Vedios Sumarizer")
st.markdown("Paste a YouTube video link. It will show a basic summary of the transcript.")

url = st.text_input("🔗 Enter YouTube Video URL")

# Store transcript in session_state
if "transcript" not in st.session_state:
    st.session_state.transcript = ""

# Summarize button
if st.button("Summarize Transcript"):
    with st.spinner("⏳ Fetching transcript..."):
        transcript = get_transcript(url)
        st.session_state.transcript = transcript  # Save to session

    if st.session_state.transcript.startswith("❌") or st.session_state.transcript.startswith("⚠️"):
        st.error(st.session_state.transcript)
    else:
        st.success("Transcript fetched!")
        st.subheader("📄 Basic Summary (first few lines):")
        st.write(basic_summary(st.session_state.transcript))
        st.subheader("📝 Full Transcript:")
        st.text_area("Transcript", st.session_state.transcript, height=300)

# Show translation options only if transcript exists
if st.session_state.transcript:
    languages = [
        "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Assamese", "Azerbaijani", "Bashkir", "Basque", 
        "Belarusian", "Bengali", "Bislama", "Bosnian", "Bulgarian", "Burmese", "Catalan", "Cebuano", "Chichewa", 
        "Chinese", "Chuvash", "Czech", "Danish", "Dhivehi", "Dutch", "English", "Esperanto", "Estonian", "Ewe", 
        "Fijian", "Finnish", "French", "Georgian", "German", "Greek", "Gujarati", "Haitian Creole", "Hausa", 
        "Hebrew", "Hindi", "Hmong", "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish", "Italian", "Japanese", 
        "Javanese", "Kazakh", "Khmer", "Kinyarwanda", "Korean", "Kurdish", "Kyrgyz", "Lao", "Latin", "Latvian", 
        "Lingala", "Lithuanian", "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi", 
        "Mongolian", "Nepali", "Norwegian", "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Quechua", 
        "Romanian", "Russian", "Samoan", "Scots Gaelic", "Serbian", "Sesotho", "Shona", "Sindhi", "Sinhala", 
        "Slovak", "Slovene", "Somali", "Spanish", "Sundanese", "Swahili", "Swedish", "Tajik", "Tamil", "Telugu", 
        "Thai", "Turkish", "Ukrainian", "Urdu", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish", "Yoruba", "Zulu"
    ]

    st.subheader("🌐 Translate Summary")
    select_lang = st.selectbox("Select your translated language", options=languages)
    
    if st.button("Translate"):
        translator = Translator()
        translated = translator.translate(basic_summary(st.session_state.transcript), dest=select_lang)
        st.success("✅ Translated Summary:")
        st.write(translated.text)
