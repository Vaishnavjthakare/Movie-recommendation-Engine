import json
import sys
import os

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "movies.json")

def load_movies(file_path=DATA_FILE):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_index(movies):
    movie_dict = {}
    title_list = []
    for item in movies:
        title = item.get("title", "").strip()
        if title:
            movie_dict[title.casefold()] = item
            title_list.append(title)
    return movie_dict, title_list

def find_movie(query, movie_dict, title_list):
    query_clean = query.strip().casefold()
    # 1. Exact match (case-insensitive)
    if query_clean in movie_dict:
        return movie_dict[query_clean]
    
    # 2. Starts-with match
    for title in title_list:
        if title.casefold().startswith(query_clean):
            return movie_dict[title.casefold()]
            
    # 3. Substring match
    for title in title_list:
        if query_clean in title.casefold():
            return movie_dict[title.casefold()]
            
    return None

def recommend(movie_title, top_n=10):
    movies = load_movies()
    if not movies:
        return

    movie_dict, title_list = build_index(movies)
    movie = find_movie(movie_title, movie_dict, title_list)

    if not movie:
        print(f"\n[!] Movie '{movie_title}' not found in database.")
        print("Try another title or check your spelling.")
        return

    print("\n" + "=" * 60)
    print(f"[Movie] {movie['title']}")
    if movie.get("genres"):
        print(f"[Genres] {movie['genres']}")
    if movie.get("overview"):
        print(f"[Overview] {movie['overview']}")
    print("=" * 60)
    print(f"\nTop {top_n} Recommendations for '{movie['title']}':\n")

    recommendations = movie.get("recommendations", [])[:top_n]
    for idx, rec_title in enumerate(recommendations, 1):
        rec_data = movie_dict.get(rec_title.casefold())
        genres_str = f" - {rec_data.get('genres', '')}" if rec_data and rec_data.get('genres') else ""
        print(f"  {idx:2d}. {rec_title}{genres_str}")
    print()

def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        recommend(query)
    else:
        print("=" * 55)
        print("         Movie Recommendation System CLI           ")
        print("=" * 55)
        movies = load_movies()
        movie_dict, title_list = build_index(movies)
        print(f"Loaded {len(title_list)} movies successfully.")
        print("Type a movie title to get recommendations (or 'q' to quit).\n")
        
        while True:
            try:
                user_input = input("Enter movie name: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ("q", "quit", "exit"):
                    print("Goodbye!")
                    break
                recommend(user_input)
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break

if __name__ == "__main__":
    main()
