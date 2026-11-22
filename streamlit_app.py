import streamlit as st
from app.database.repository import Repository

st.set_page_config(page_title="AI News Aggregator", page_icon="📰", layout="centered")

st.title("📰 AI News Aggregator")
st.caption("Scrapes OpenAI & Anthropic blogs, summarizes with an LLM (Groq), and shows the latest digests.")


@st.cache_data(ttl=300)
def load_digests(hours: int):
    repo = Repository()
    return repo.get_recent_digests(hours=hours)


days = st.sidebar.slider("Show news from last N days", 1, 30, 10)
source = st.sidebar.selectbox("Source", ["All", "openai", "anthropic", "youtube"])
search = st.sidebar.text_input("Search in title/summary")

digests = load_digests(days * 24)

if source != "All":
    digests = [d for d in digests if d["article_type"] == source]
if search:
    s = search.lower()
    digests = [d for d in digests if s in d["title"].lower() or s in d["summary"].lower()]

st.write(f"**{len(digests)} articles**")

for d in digests:
    with st.container(border=True):
        st.markdown(f"### [{d['title']}]({d['url']})")
        st.caption(f"{d['article_type'].upper()} · {d['created_at']:%d %b %Y}")
        st.write(d["summary"])