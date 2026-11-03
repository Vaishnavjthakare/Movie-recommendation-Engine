# 🎬 Movie Recommendation System

A content-based movie recommendation engine built using TF-IDF Vectorization and Cosine Similarity on the TMDB 5000 Movies dataset.

---

## 🚀 How to Run

You have two ways to run the project:

### Option 1: Web Interface (Streamlit)
Launch an interactive web dashboard in your browser:

```powershell
streamlit run app.py
```

### Option 2: Command Line (CLI)
Get recommendations directly in your terminal:

- **Quick recommendation for a movie:**
  ```powershell
  python recommend.py "The Dark Knight"
  ```
  or
  ```powershell
  python recommend.py "Avatar"
  ```

- **Interactive CLI mode:**
  ```powershell
  python recommend.py
  ```

---

## 📂 Project Structure

- `app.py`: Streamlit interactive web application with search, genre filters, and recommendation cards.
- `recommend.py`: Fast command-line recommendation script (supports direct queries and interactive mode).
- `movies.json`: Precomputed dataset containing 4,803 movies with metadata and top-10 similarity recommendations.
- `Movie_Recommendation.ipynb`: The Jupyter Notebook containing the data preprocessing, TF-IDF feature extraction, and cosine similarity modeling.
