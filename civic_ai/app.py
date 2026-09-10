"""
JanMitra AI - Civic Reporting AI Module
Phase 5: Streamlit UI

This is the demo interface you'll actually click through and show in
your viva. It imports analyze_complaint() from ai_analyzer.py and wraps
it in a simple web form - no new AI logic lives in this file.

IMPORTANT: run this with `streamlit run app.py`, NOT `python app.py`.
Streamlit apps need to be launched through the streamlit command so it
can start its own local web server.
"""

import json
import os
import tempfile

import streamlit as st

from ai_analyzer import analyze_complaint

st.set_page_config(page_title="JanMitra AI - Civic Reporting", page_icon="🏛️")

st.title("🏛️ JanMitra AI — Civic Reporting Assistant")
st.write("Describe a civic issue, optionally attach a photo, and let AI analyze it.")

complaint_text = st.text_area(
    "Describe the issue",
    placeholder="e.g. There is a huge pothole near my college gate...",
    height=120,
)

uploaded_image = st.file_uploader(
    "Optional: upload a photo of the issue",
    type=["jpg", "jpeg", "png"],
)

if uploaded_image is not None:
    st.image(uploaded_image, caption="Uploaded photo", width=300)

if st.button("Analyze Complaint", type="primary"):
    if not complaint_text.strip():
        st.warning("Please enter a complaint description first.")
    else:
        with st.spinner("Analyzing complaint..."):
            image_path = None
            if uploaded_image is not None:
                # Streamlit gives us the uploaded file in memory - we save
                # it to a temporary file on disk so PIL/Gemini can read it,
                # the same way analyze_complaint() expects a file path.
                suffix = os.path.splitext(uploaded_image.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_image.getvalue())
                    image_path = tmp.name

            try:
                result = analyze_complaint(complaint_text, image_path=image_path)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                result = None
            finally:
                if image_path and os.path.exists(image_path):
                    os.remove(image_path)

        if result:
            st.success("Analysis complete")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Category", result["category"])
                st.metric("Severity", result["severity"])
                st.metric("Priority Score", f"{result['priority']}/100")
            with col2:
                st.metric("Department", result["department"])
                st.metric("Confidence", f"{result['confidence']}%")

            st.subheader("Summary")
            st.write(result["summary"])

            st.subheader("Suggested Action")
            st.write(result["suggested_action"])

            with st.expander("Raw JSON (for developers)"):
                st.json(result)
