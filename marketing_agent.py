import streamlit as st
import openai
import pandas as pd

st.title("High-end Marketing Copy & Competitor Comparison Agent")

# 输入区
product_name = st.text_input("Product Name", "TurboPoly Fan 008S")
product_specs = st.text_area("Product Specs (English)", "TurboWind™: Max air speed 26 ft/s\nHyperSilent™: 20dB ultra-quiet\n3D automatic oscillation: 120° vertical + 120° horizontal\n1500+ customizable RGB ambiance lights\nSmart control: App, Alexa, Google Home, Siri")
brand_style = st.text_input("Brand Style Reference", "Dreo, Dyson, B&O")
competitors = st.text_area("Competitors (one per line)", "Shark\nVornado\nLasko")
target_audience = st.text_input("Target Audience", "High-end families, mothers & babies, tech lovers")
channel = st.selectbox("Channel", ["Amazon", "Official Website", "Social Media", "PR"])

openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")

if st.button("Generate Marketing Copy & Comparison Table"):
    # 生成文案的Prompt
    prompt = f"""
You are a senior copywriter for a high-end home appliance brand. Please generate a {channel} product description in elegant, concise, and emotionally resonant English, referencing the tone of {brand_style}. Highlight the following features and make sure to differentiate from competitors: {competitors.replace(chr(10), ', ')}.

Product specs:
{product_specs}

Target audience: {target_audience}

Please also provide 2 slogan options and a comparison table with the main competitors.
"""
    if not openai_api_key:
        st.warning("Please enter your OpenAI API Key.")
    else:
        openai.api_key = openai_api_key
        with st.spinner("Generating..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # 或 "gpt-4"（如有权限）
                messages=[{"role": "system", "content": "You are a professional English marketing copywriter."},
                          {"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.7
            )
            output = response.choices[0].message.content
            st.markdown("### AI Generated Copy & Comparison")
            st.write(output)