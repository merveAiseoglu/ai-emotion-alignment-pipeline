import requests
import streamlit as st
from config.settings import TMDB_API_KEY

class TMDBService:
    def __init__(self):
        self.api_key = TMDB_API_KEY
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"

    def search_movie(self, query):
        """Film ismine göre arama yapar, özet ve OYUNCU KADROSUNU (Cast) döndürür."""
        if not query or not self.api_key:
            return None

        try:
            # 1. FİLM ARA (Türkçe)
            url = f"{self.base_url}/search/movie"
            params = {
                "api_key": self.api_key,
                "query": query,
                "language": "tr-TR" 
            }
            response = requests.get(url, params=params)
            data = response.json()

            if data["results"]:
                # --- İYİLEŞTİRME: EN POPÜLER OLANI SEÇ ---
                # Sonuçları 'popularity' puanına göre tersten sırala (En yüksek puan en başa)
                sorted_results = sorted(data["results"], key=lambda x: x.get('popularity', 0), reverse=True)
                movie = sorted_results[0] # Şimdi en popüler olanı aldık
                
                movie_id = movie["id"]

                # 2. ÖZET KONTROLÜ (DİL FALLBACK)
                overview = movie["overview"]
                # Eğer Türkçe özet boşsa, İngilizce veriyi çekelim
                if not overview:
                    en_url = f"{self.base_url}/movie/{movie_id}"
                    en_params = {"api_key": self.api_key, "language": "en-US"}
                    en_data = requests.get(en_url, params=en_params).json()
                    overview = en_data.get("overview", "Özet bulunamadı.") + " (İngilizce kaynaktan alındı)"

                # 3. OYUNCULARI (Credits) ÇEKMEK
                credits_url = f"{self.base_url}/movie/{movie_id}/credits"
                credits_response = requests.get(credits_url, params={"api_key": self.api_key})
                credits_data = credits_response.json()

                # İlk 10 oyuncuyu alalım
                cast_list = []
                if "cast" in credits_data:
                    for actor in credits_data["cast"][:10]: 
                        cast_list.append(f"{actor['character']} ({actor['name']})")

                return {
                    "title": movie["title"],
                    "overview": overview,
                    "poster_path": f"{self.image_base_url}{movie['poster_path']}" if movie.get('poster_path') else None,
                    "release_date": movie.get("release_date", "Bilinmiyor"),
                    "cast": cast_list 
                }
            return None
        except Exception as e:
            st.error(f"TMDB Bağlantı Hatası: {e}")
            return None