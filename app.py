import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# ==============================================================================
# 1. PAGE CONFIGURATION
# (MUST be the very first Streamlit command)
# ==============================================================================
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# ==============================================================================
# 2. DATA SETUP AND LOADING
# ==============================================================================

# Define local paths for data files
os.makedirs("data", exist_ok=True)
movies_path = "data/movies_df.pkl"
cosine_path = "data/cosine_sim.pkl"

# Google Drive URLs for public data access
movies_url = "https://drive.google.com/uc?id=1Kp94CoUx6TEa0IGWwWXkeCYoxwBvqUGi"
cosine_url = "https://drive.google.com/uc?id=1Gx125x80yaKdYB-nikg2L7pzaavSuSP7"

# Download data files if they do not exist locally
if not os.path.exists(movies_path):
    with st.spinner("Downloading movie data..."):
        gdown.download(movies_url, movies_path, quiet=False)
if not os.path.exists(cosine_path):
    with st.spinner("Downloading similarity matrix..."):
        gdown.download(cosine_url, cosine_path, quiet=False)


@st.cache_data
def load_data(m_path, c_path):
    """Loads and caches the movie DataFrame and similarity matrix."""
    movies_data = pickle.load(open(m_path, "rb"))
    movies_df = pd.DataFrame(movies_data)
    cosine_sim_matrix = pickle.load(open(c_path, "rb"))
    return movies_df, cosine_sim_matrix

with st.spinner("Initializing Movie Database..."):
    movies, cosine_sim = load_data(movies_path, cosine_path)


# ==============================================================================
# 3. CORE FUNCTIONS
# ==============================================================================

def fetch_poster(movie_id=None):
    """Fetches poster from TMDB using API key or returns a placeholder URL."""
    try:
        api_key = st.secrets.get("api_keys", {}).get("tmdb")
    except Exception:
        api_key = None

    if api_key and movie_id:
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')
                if poster_path:
                    return "https://image.tmdb.org/t/p/w500" + poster_path
        except:
            pass

    # Fallback placeholder image URL (500x750 for 2:3 aspect ratio)
    return "https://via.placeholder.com/500x750.png?text=Poster+Unavailable"

def recommend(title, n=5):
    """Computes and returns the top n movie recommendations based on similarity score."""
    if title not in movies['title'].values:
        return [], []

    # Get the index of the movie that matches the title
    idx = movies[movies['title'] == title].index[0]
    
    # Get the similarity scores for all movies and sort them
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the scores of the top n movies (skipping the first one, which is the movie itself)
    sim_scores = sim_scores[1:n+1]  
    
    # Extract titles and fetch posters for the recommended movies
    rec_titles = [movies.iloc[i[0]].title for i in sim_scores]
    rec_posters = [fetch_poster(movies.iloc[i[0]].movie_id) for i in sim_scores]
    return rec_titles, rec_posters


# ==============================================================================
# 4. STREAMLIT UI LAYOUT
# ==============================================================================

# Fixed number of recommendations since the slider was removed
RECOMMENDATION_COUNT = 5 

# --- Sidebar ---
with st.sidebar:
    st.header("🍿 Movie Recommender")
    st.markdown("---")
    # Concise technology stack description
    st.markdown("Built with **love** ❤️ using **Python** 🐍, **Pandas** 🐼, **Scikit-learn** 🧠 & **Streamlit** ✨.")
    st.markdown("---")
    st.caption("Posters are sourced from TMDB (optional API key required).")


# --- Main Page ---
st.title("🎬 Movie Recommendation System")
st.markdown("#### Discover movies similar to your favorites.")

# User input container for cleaner grouping
with st.container(border=True):
    # CORRECTED ORDER: Header appears before the selectbox
    st.subheader("Select Your Movie 🔍")
    movie_list = movies['title'].values
    
    selected_movie = st.selectbox(
        "Start typing to search for a movie:", 
        movie_list,
        index=None,
        placeholder="Search here...",
        label_visibility="visible"
    )

# Logic to run recommendation upon selection and button click
if selected_movie:
    if st.button(f"🎬 Get Recommendations", use_container_width=True, type="primary"):
        with st.spinner("Finding cinematic matches..."):
            names, posters = recommend(selected_movie, n=RECOMMENDATION_COUNT)
        
        st.divider()
        st.header(f"Top {RECOMMENDATION_COUNT} Recommendations for **{selected_movie}**:")
        
        # Display results in columns (no custom CSS)
        cols = st.columns(RECOMMENDATION_COUNT)
        
        for idx, col in enumerate(cols):
            with col:
                # use_column_width=True is key for responsive image sizing
                st.image(posters[idx], use_column_width=True) 
                st.caption(names[idx]) 
                

