import streamlit as st
import openai
import pandas as pd

# ====== 自定义CSS，统一olify.ai风格 ======
st.markdown("""
    <style>
    body, .stApp {
        background-color: #181A1B;
        color: #fff;
    }
    .stTextInput>div>div>input, .stTextArea>div>textarea, .stSelectbox>div>div>div>div {
        background-color: #232526 !important;
        color: #fff !important;
        border-radius: 8px;
        border: 1px solid #2b7cff;
    }
    .stButton>button {
        background-color: #2b7cff;
        color: #fff;
        border-radius: 8px;
        font-size: 1.1em;
        padding: 0.5em 2em;
        border: none;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background-color: #1a5dcc;
        color: #fff;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #fff;
    }
    .stSelectbox>div>div>div>div {
        color: #fff !important;
    }
    .stAlert {
        background-color: #232526 !important;
        color: #fff !important;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ====== 页面内容 ======
st.markdown("<h1 style='color:#2b7cff;font-size:2.5em;font-weight:800;'>Olify.AI Marketing Agent</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#fff;font-weight:400;'>AI-driven marketing copy & competitor analysis, in your brand style.</h3>", unsafe_allow_html=True)
st.markdown("---", unsafe_allow_html=True)

provider = st.selectbox(
    "Select LLM Provider",
    ["DeepSeek", "OpenAI"]
)

if provider == "DeepSeek":
    api_key = st.text_input("Enter your DeepSeek API Key", type="password")
    base_url = "https://api.deepseek.com/v1"
    model_name = "deepseek-chat"
else:
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    base_url = None
    model_name = "gpt-3.5-turbo"

product_name = st.text_input("Product Name", "TurboPoly Fan 008S")
product_specs = st.text_area(
    "Product Specs (English)",
    "TurboWind™: Max air speed 26 ft/s\nHyperSilent™: 20dB ultra-quiet\n3D automatic oscillation: 120° vertical + 120° horizontal\n1500+ customizable RGB ambiance lights\nSmart control: App, Alexa, Google Home, Siri"
)
brand_style = st.text_input("Brand Style Reference", "Dreo, Dyson, B&O")
competitors = st.text_area("Competitors (one per line)", "Shark\nVornado\nLasko")
target_audience = st.text_input("Target Audience", "High-end families, mothers & babies, tech lovers")
channel = st.selectbox("Channel", ["Amazon", "Official Website", "Social Media", "PR"])

st.markdown("---", unsafe_allow_html=True)

if st.button("Generate Marketing Copy & Comparison Table"):
    prompt = f"""
You are a senior copywriter for a high-end home appliance brand. Please generate a {channel} product description in elegant, concise, and emotionally resonant English, referencing the tone of {brand_style}. Highlight the following features and make sure to differentiate from competitors: {competitors.replace(chr(10), ', ')}.

Product specs:
{product_specs}

Target audience: {target_audience}

Please also provide 2 slogan options and a comparison table with the main competitors.
"""
    if not api_key:
        st.warning("Please enter your API Key.")
    else:
        try:
            if base_url:
                client = openai.OpenAI(
                    api_key=api_key,
                    base_url=base_url
                )
            else:
                client = openai.OpenAI(
                    api_key=api_key
                )
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a professional English marketing copywriter."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            output = response.choices[0].message.content
            st.markdown("<h3 style='color:#2b7cff;'>AI Generated Copy & Comparison</h3>", unsafe_allow_html=True)
            st.write(output)
        except Exception as e:
            st.error(f"Error: {e}")

# 页脚
st.markdown("""
    <hr>
    <div style='text-align:center; color:#888; font-size:0.9em;'>
        © 2025 Olify.AI &nbsp;|&nbsp; <a href="https://www.olify.ai/" style="color:#2b7cff;">Back to Home</a>
    </div>
""", unsafe_allow_html=True)
