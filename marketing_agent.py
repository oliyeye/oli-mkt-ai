import streamlit as st
import openai
import pandas as pd

# ====== 自定义CSS，品牌色+字体+动效+响应式 ======
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&family=Manrope:wght@400;700&display=swap');
    html, body, .stApp {
        background-color: #181A1B !important;
        color: #fff !important;
        font-family: 'DM Sans', 'Manrope', 'Segoe UI', 'Arial', sans-serif !important;
        font-size: 18px;
    }
    /* LOGO区 */
    .logo-title {
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 0.5em;
    }
    .logo-circle {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #d6f47a 60%, #b8d95e 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 1.6em;
        color: #181A1B;
        box-shadow: 0 2px 12px #d6f47a44;
        animation: popin 1s cubic-bezier(.68,-0.55,.27,1.55);
    }
    @keyframes popin {
        0% { transform: scale(0.5); opacity: 0;}
        80% { transform: scale(1.1);}
        100% { transform: scale(1); opacity: 1;}
    }
    .main-title {
        font-size: 2.2em;
        font-weight: 800;
        background: linear-gradient(90deg, #d6f47a 30%, #fff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientMove 2.5s ease-in-out infinite alternate;
    }
    @keyframes gradientMove {
        0% {background-position: 0%;}
        100% {background-position: 100%;}
    }
    .subtitle {
        color: #fff;
        font-size: 1.1em;
        margin-bottom: 1.2em;
        opacity: 0.85;
    }
    /* 输入区美化 */
    .stTextInput>div>div>input, .stTextArea>div>textarea, .stSelectbox>div>div>div>div {
        background-color: #232526 !important;
        color: #fff !important;
        border-radius: 10px;
        border: 1.5px solid #d6f47a;
        font-size: 1em;
        transition: box-shadow 0.2s, border 0.2s;
        box-shadow: 0 1px 6px #d6f47a22;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>textarea:focus {
        border: 2px solid #d6f47a;
        box-shadow: 0 0 0 2px #d6f47a55;
    }
    /* 按钮美化+动效 */
    .stButton>button {
        background-color: #d6f47a;
        color: #181A1B;
        border-radius: 10px;
        font-size: 1.1em;
        font-weight: 700;
        padding: 0.6em 2.2em;
        border: none;
        margin-top: 0.5em;
        margin-bottom: 1.2em;
        box-shadow: 0 2px 12px #d6f47a33;
        transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #b8d95e;
        color: #181A1B;
        transform: translateY(-2px) scale(1.04);
        box-shadow: 0 6px 24px #d6f47a55;
    }
    /* 标题/分割线 */
    .stMarkdown h3 {
        color: #d6f47a;
        font-weight: 700;
        margin-top: 1.5em;
    }
    hr {
        border: none;
        border-top: 1.5px solid #d6f47a33;
        margin: 2em 0 1.2em 0;
    }
    /* 响应式布局 */
    @media (max-width: 600px) {
        .main-title { font-size: 1.3em;}
        .logo-circle { width: 36px; height: 36px; font-size: 1.1em;}
        .subtitle { font-size: 1em;}
        html, body, .stApp { font-size: 15px;}
    }
    /* 页脚 */
    .footer {
        text-align: center;
        color: #b8d95e;
        font-size: 0.95em;
        margin-top: 2.5em;
        opacity: 0.7;
    }
    a, a:visited {
        color: #d6f47a !important;
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# ====== LOGO区和标题 ======
st.markdown("""
<div class="logo-title">
    <div class="logo-circle">OA</div>
    <div>
        <div class="main-title">Olify.AI Marketing Agent</div>
        <div class="subtitle">AI-driven marketing copy & competitor analysis, in your brand style.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ====== 主体表单 ======
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

st.markdown("<hr>", unsafe_allow_html=True)

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
            st.markdown("<h3>AI Generated Copy & Comparison</h3>", unsafe_allow_html=True)
            st.write(output)
        except Exception as e:
            st.error(f"Error: {e}")

# ====== 页脚 ======
st.markdown("""
    <div class="footer">
        © 2025 Olify.AI &nbsp;|&nbsp; <a href="https://www.olify.ai/" target="_blank">Back to Home</a>
    </div>
""", unsafe_allow_html=True)
