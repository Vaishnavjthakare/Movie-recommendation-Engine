import streamlit as st
import json
import os

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        color: #E50914;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #888888;
        margin-bottom: 1.5rem;
    }
    .movie-card {
        background-color: #1e1e24;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 14px;
        height: 100%;
        border-left: 4px solid #E50914;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .movie-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 6px;
    }
    .movie-genre {
        display: inline-block;
        background-color: #2b2d42;
        color: #edf2f4;
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 12px;
        margin-right: 4px;
        margin-bottom: 6px;
    }
    .movie-overview {
        font-size: 0.85rem;
        color: #b0b0b0;
        line-height: 1.35;
    }
    .selected-box {
        background: linear-gradient(135deg, #1f1f2e 0%, #16161d 100%);
        border: 1px solid #33334d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "movies.json")
    if not os.path.exists(file_path):
        st.error(f"Data file '{file_path}' not found!")
        return {}, []
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    movie_dict = {item["title"]: item for item in data}
    titles = sorted(list(movie_dict.keys()))
    return movie_dict, titles

movie_dict, titles = load_data()

st.markdown('<div class="main-header">🎬 CineMatch: Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Discover your next favorite movie using TF-IDF Content-Based Filtering</div>', unsafe_allow_html=True)

if not titles:
    st.warning("No movie data loaded. Please make sure movies.json is available in the workspace.")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    top_n = st.slider("Number of Recommendations", min_value=3, max_value=10, value=6, step=1)
    
    st.markdown("---")
    st.markdown("### 📊 Dataset Info")
    st.write(f"**Total Movies:** {len(titles):,}")
    st.write("**Model:** TF-IDF & Cosine Similarity")
    st.write("**Features Used:** Genres, Keywords, Overview, Cast, Director, Tagline")
    st.markdown("---")
    st.caption("Built with Streamlit & Scikit-Learn")

# Session state to handle clicking a recommendation
if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = "The Dark Knight" if "The Dark Knight" in titles else titles[0]

# Search / Select box
default_index = titles.index(st.session_state.selected_movie) if st.session_state.selected_movie in titles else 0
selected_movie = st.selectbox(
    "🔍 Search or select a movie:",
    options=titles,
    index=default_index,
    key="movie_select"
)

# If changed via selectbox
if selected_movie != st.session_state.selected_movie:
    st.session_state.selected_movie = selected_movie

movie_info = movie_dict.get(st.session_state.selected_movie)

if movie_info:
    # Display current movie details
    st.markdown(f"""
    <div class="selected-box">
        <h2 style="margin-top: 0; color: #ffffff;">{movie_info['title']}</h2>
        <p style="margin-bottom: 8px;">
            {''.join([f'<span class="movie-genre">{g.strip()}</span>' for g in movie_info.get('genres', '').split() if g.strip()])}
        </p>
        <p style="color: #cccccc; font-size: 0.95rem; margin-bottom: 0;">{movie_info.get('overview', 'No overview available.')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader(f"🍿 Recommended Movies based on '{movie_info['title']}':")
    
    recommendations = movie_info.get("recommendations", [])[:top_n]

    if not recommendations:
        st.info("No recommendations found for this title.")
    else:
        # Arrange in a grid of 3 columns
        cols_per_row = 3
        for row_start in range(0, len(recommendations), cols_per_row):
            cols = st.columns(cols_per_row)
            for idx, col in enumerate(cols):
                rec_idx = row_start + idx
                if rec_idx < len(recommendations):
                    rec_title = recommendations[rec_idx]
                    rec_data = movie_dict.get(rec_title, {})
                    rec_genres = rec_data.get("genres", "")
                    rec_overview = rec_data.get("overview", "No overview available.")
                    if len(rec_overview) > 160:
                        rec_overview = rec_overview[:160] + "..."

                    genres_html = ''.join([f'<span class="movie-genre">{g.strip()}</span>' for g in rec_genres.split()[:3] if g.strip()])

                    with col:
                        st.markdown(f"""
                        <div class="movie-card">
                            <div class="movie-title">#{rec_idx + 1} {rec_title}</div>
                            <div>{genres_html}</div>
                            <div class="movie-overview">{rec_overview}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"Explore '{rec_title}'", key=f"btn_{rec_idx}_{rec_title}"):
                            st.session_state.selected_movie = rec_title
                            st.rerun()
