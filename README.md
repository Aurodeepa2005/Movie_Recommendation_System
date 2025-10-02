# 🎬 Personalized Movie Recommendation System

This project is a content-based movie recommendation system built with Python and Streamlit. It uses pre-computed movie features and a Cosine Similarity matrix to quickly suggest the top 5 most similar movies based on a user's selection.

## ✨ Live Demo
The application is deployed and available on Streamlit Cloud:

[Live Application Link Here](https://movierecommendationsystem-byauro.streamlit.app/)

## ⚙️ Technology Stack
- **Language:** Python 🐍
- **Framework:** Streamlit ✨ (for interactive web application development)
- **Data Manipulation:** Pandas 🐼
- **Machine Learning Logic:** Scikit-learn 🧠 (used for Cosine Similarity calculation, although the matrix is pre-computed)
- **Data Loading:** gdown (to securely load large model files from Google Drive)
- **API Integration:** requests (for fetching real-time movie posters and details from TMDB)

## 🚀 Getting Started

Follow these steps to set up and run the application locally.

### Prerequisites
- Python 3.8+
- A TMDB API Key (required to fetch movie posters)

### 1. Clone the Repository
```bash
git clone https://github.com/YourUsername/YourRepoName.git
cd YourRepoName
```
2. Set up Virtual Environment

It is recommended to use a virtual environment:
# Create and activate environment
```bash
python -m venv venv

# On Windows:
.\venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```
3. Install Dependencies

Install all required packages listed in the requirements.txt file:
```bash
pip install -r requirements.txt
```
4. Configure API Key (Crucial Step!)

To enable the app to fetch real movie posters, you must create a local secrets file.
Create a folder named .streamlit in the root directory of your project.
Inside the .streamlit folder, create a file named secrets.toml.
Add your TMDB API key to this file exactly as shown below:
```bash
# .streamlit/secrets.toml
[api_keys]
tmdb = "PASTE_YOUR_TMDB_API_KEY_HERE"
```
5. Run the Application

Start the Streamlit application from your terminal:
```bash
streamlit run app.py
```
The app will automatically open in your web browser.

🔑 Features

1.Content-Based Filtering: Uses Cosine Similarity on cleaned movie metadata to generate recommendations.

2.External Data Loading: Efficiently downloads large pre-trained data (.pkl files) using gdown on startup.

3.Dynamic Poster Fetching: Integrates with the TMDB API to display actual movie posters alongside recommendations.

4.Responsive UI: Built with Streamlit, ensuring a clean and usable interface on both desktop and mobile devices.

5.Secure API Handling: Utilizes Streamlit's built-in st.secrets manager for safely deploying the TMDB API key.
