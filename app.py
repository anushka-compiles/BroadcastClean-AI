
import streamlit as st
import numpy as np
import soundfile as sf
import noisereduce as nr
import io

# Page configuration
st.set_page_config(
    page_title="BroadcastClean AI",
    page_icon="🎙️",
    layout="wide"
)

# Custom dashboard styling
st.markdown("""
<style>
.stApp {
    background-color: #101827;
    color: white;
}
h1, h2, h3 {
    color: #55D6BE;
}
.stButton>button {
    background-color: #00A896;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 22px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #028090;
    color: white;
}
[data-testid="stFileUploader"] {
    background-color: #1B263B;
    border-radius: 12px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# Application heading
st.title("🎙️ BroadcastClean AI")
st.subheader("Intelligent Audio Noise Reduction and Enhancement System")
st.markdown(
    "Improve audio clarity by reducing unwanted background noise "
    "from recorded broadcasting audio."
)

st.divider()

# Upload section
st.header("📁 Upload Audio Recording")

uploaded_file = st.file_uploader(
    "Choose a noisy audio file",
    type=["wav"]
)

if uploaded_file is not None:

    # Read uploaded audio
    audio_data, sample_rate = sf.read(
        uploaded_file,
        dtype="float32",
        always_2d=True
    )

    # Original audio preview
    st.header("🎧 Original Audio")

    original_buffer = io.BytesIO()
    sf.write(
        original_buffer,
        audio_data,
        sample_rate,
        format="WAV"
    )

    st.audio(original_buffer.getvalue(), format="audio/wav")

    st.write(f"**Sample Rate:** {sample_rate} Hz")
    st.write(f"**Duration:** {len(audio_data) / sample_rate:.2f} seconds")
    st.write(f"**Channels:** {audio_data.shape[1]}")

    st.divider()

    # Noise reduction
    st.header("⚙️ Audio Enhancement")

    if st.button("✨ Reduce Background Noise"):

        with st.spinner("Processing audio... Please wait."):

            try:
                enhanced_channels = []

                for channel in range(audio_data.shape[1]):

                    enhanced = nr.reduce_noise(
                        y=audio_data[:, channel],
                        sr=sample_rate,
                        stationary=False,
                        prop_decrease=0.85
                    )

                    enhanced_channels.append(enhanced)

                enhanced_audio = np.column_stack(
                    enhanced_channels
                )

                # Save enhanced audio in memory
                enhanced_buffer = io.BytesIO()

                sf.write(
                    enhanced_buffer,
                    enhanced_audio,
                    sample_rate,
                    format="WAV",
                    subtype="PCM_16"
                )

                st.session_state["enhanced_audio"] = (
                    enhanced_buffer.getvalue()
                )

                st.success(
                    "Background noise reduction completed successfully!"
                )

            except Exception as e:
                st.error(f"Audio processing failed: {e}")

    # Enhanced audio preview
    if "enhanced_audio" in st.session_state:

        st.divider()
        st.header("🔊 Enhanced Audio")

        st.audio(
            st.session_state["enhanced_audio"],
            format="audio/wav"
        )

        st.download_button(
            label="⬇️ Download Enhanced Audio",
            data=st.session_state["enhanced_audio"],
            file_name="BroadcastClean_Enhanced.wav",
            mime="audio/wav"
        )

        st.success("Your enhanced audio is ready!")

else:
    st.info("Please upload a WAV audio recording to get started.")

st.divider()

st.markdown(
    "<center>BroadcastClean AI | Audio Enhancement System</center>",
    unsafe_allow_html=True
)
