import streamlit as st
import requests
import re


API_URL = "http://127.0.0.1:8000/search"


st.set_page_config(page_title="💊 Medicine Search", page_icon="💊")


st.markdown(
    """
    <div style="text-align:center;">
        <h1 style="color:#1f4e79; font-family:Arial, sans-serif;">💊 Intelligent Medicine Search</h1>
        <p style="font-size:16px; color:#555;">
            Search medicines using <b>Prefix</b>, <b>Substring</b>, <b>Full Text</b>, or <b>Fuzzy</b> search
        </p>
        <hr style="border:1px solid #E0E0E0;">
    </div>
    """,
    unsafe_allow_html=True
)


with st.form("search_form"):
    query = st.text_input("🔍 Enter medicine name", placeholder="e.g., Paracetamol")
    search_type = st.selectbox(
        "Search type",
        ["prefix", "substring", "fulltext", "fuzzy"],
        index=3
    )
    submitted = st.form_submit_button("Search 🚀")

def highlight_match(text, query):
    """Bold the matched parts of the medicine name"""
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda m: f"<b style='color:#d9534f;'>{m.group(0)}</b>", text)


if submitted and query:
    with st.spinner("🔎 Searching..."):
        try:
            response = requests.get(f"{API_URL}/{search_type}", params={"q": query})
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])

                if results:
                    st.success(f"✅ Found {len(results)} matches for **{query}**")

                    
                    for med in results:
                        st.markdown(
                            f"""
                            <div style="
                                padding:15px;
                                margin:10px 0;
                                border-radius:10px;
                                background-color:#f7f9fc;
                                border:1px solid #cbd6e2;
                                font-size:16px;
                                font-weight:bold;
                                color:#1f4e79;
                                box-shadow:0 4px 6px rgba(0,0,0,0.08);
                                text-align:center;
                                transition: all 0.2s ease-in-out;
                            " onmouseover="this.style.transform='scale(1.03)';" onmouseout="this.style.transform='scale(1)';">
                                {highlight_match(med, query)}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.info(f"⚠️ No results found for '{query}'. Try another search or check spelling.")
            else:
                st.error(f"❌ API Error: {response.status_code}")
        except Exception as e:
            st.error(f"🚨 Connection error: {e}")
