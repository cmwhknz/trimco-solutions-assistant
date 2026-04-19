import os
import requests
import streamlit as st

st.set_page_config(page_title="Trimco Solutions Assistant")

# Sidebar width (CSS hack)
st.markdown(
    """
    
    <style>
        /* Sidebar font size */
        section[data-testid="stSidebar"] {
            font-size: 14px !important;
        }

        /* Optional: make headers smaller */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            font-size: 16px !important;
        }

        /* Optional: shrink markdown text (lists, etc.) */
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] li {
            font-size: 13px !important;
        }

    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Trimco Solutions Assistant")

# Sidebar content
with st.sidebar:
    st.header("範例問題 / Template Questions")

    st.markdown("""
    - 找一個與 DPP（數位產品護照）準備相關的客戶案例
    - 哪個案例最適合展示品牌如何開始導入 DPP？
    - 找一個使用 QR code 做產品透明度或消費者互動的案例
    - 找一個品牌導入 RFID source tagging 的案例
    - 哪個案例最能說明 RFID 如何提升營運效率？
    - 找一個與 traceability（產品追溯）相關的實際應用案例
    - 哪個案例最適合用來說明永續與合規（compliance）？
    - 比較 Bergans 與 Sports Group Denmark 在 DPP 上的做法
    - 哪個案例最適合用來說服客戶導入 ProductDNA？
    - 根據案例，幫我整理 3 個 Trimco 的銷售說法（含實際例子）
    - Find a customer case related to DPP readiness
    - Which case best demonstrates how a brand started its DPP journey?
    - Find a case using QR codes for transparency or consumer engagement
    - Find a case where a brand adopted RFID source tagging
    - Which case shows how RFID improved operational efficiency?
    - Find a real example of traceability implementation
    - Which case is best to demonstrate sustainability and compliance?
    - Compare Bergans and Sports Group Denmark on their DPP approach
    - Which case is most suitable to support selling ProductDNA?
    - Based on cases, generate 3 sales talking points with examples
    """)

    st.caption("Internal Knowledge Assistant")

# Environment variables
AGENT_ENDPOINT = os.getenv("AGENT_ENDPOINT", "").rstrip("/")
AGENT_ACCESS_KEY = os.getenv("AGENT_ACCESS_KEY", "")

if not AGENT_ENDPOINT or not AGENT_ACCESS_KEY:
    st.error("Missing AGENT_ENDPOINT or AGENT_ACCESS_KEY")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "查詢 Trimco 產品與解決方案 / Query Trimco products & solutions"
        }
    ]

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("請輸入你的問題 / Ask your question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("思考中... Thinking..."):
            try:
                url = f"{AGENT_ENDPOINT}/api/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {AGENT_ACCESS_KEY}",
                    "Content-Type": "application/json",
                }

                payload = {
                    "messages": st.session_state.messages,
                    "stream": False
                }

                resp = requests.post(url, headers=headers, json=payload, timeout=120)
                resp.raise_for_status()
                data = resp.json()

                answer = data["choices"][0]["message"]["content"]
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Request failed: {e}")