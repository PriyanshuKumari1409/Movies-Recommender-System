# Movie Recommender System

A content-based movie recommender system built using **Python**, **Streamlit**, and **Machine Learning**.  
It suggests similar movies based on your selection using **Cosine Similarity**.


## Tech Stack

**Language**   Python
**Libraries**  Pandas, Scikit-learn, NumPy, Streamlit, Requests
 **Data**      IMDb Movie Dataset
**API**        OMDb API

## How It Works
1. The dataset is processed and features like **genres, overview, cast, and keywords** are combined into a single text field.  
2. Text data is vectorized using **TF-IDF Vectorizer**.  
3. Similarity between movies is computed using **Cosine Similarity**.  
4. Given a selected movie, the app fetches the **top 5 most similar movies**.  
5. Poster URLs are fetched dynamically via the **OMDb API**.

6. ##  Machine Learning Workflow

- **Feature Engineering** → Combine multiple movie attributes into one text column.  
- **Vectorization** → Convert text to numerical vectors using `TfidfVectorizer`.  
- **Similarity Computation** → Use `cosine_similarity()` to find related movies.  
- **Model Saving** → Save data & similarity matrix using `pickle` for faster loading.

##  Installation & Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/PriyanshuKumari1409/Movies-Recommender-System.git
   cd Movies-Recommender-System

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3.Run the app:
  ```bash
streamlit run app.py

4.Select a movie and view recommendations instantly!
