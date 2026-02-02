import streamlit as st
import time
from config.settings import TARGET_EMOTIONS
from services.openai_service import OpenAIService
from services.tmdb_service import TMDBService

st.set_page_config(page_title="AI Story Alignment Pipeline", page_icon="🧪", layout="wide")

ai_service = OpenAIService()
tmdb_service = TMDBService()

def parse_evaluation(eval_text):
    """LLM çıktısını (Score/Reasoning) parçalar."""
    try:
        lines = eval_text.strip().split('\n')
        score_line = [l for l in lines if "Score:" in l][0]
        reason_line = [l for l in lines if "Reasoning:" in l][0]
        score = int(score_line.split("Score:")[1].strip())
        reason = reason_line.split("Reasoning:")[1].strip()
        return score, reason
    except Exception as e:
        return 0, f"Format Hatası: {eval_text}"

def get_score_label(score):
    """Puanı yorumlayarak etiket döndürür."""
    if score >= 90:
        return "Strong Alignment"
    elif score >= 70:
        return "Moderate Alignment"
    else:
        return "Weak Alignment"

def main():
    st.title("🧪 AI Emotion Alignment Pipeline")
    
    # --- YENİ EKLENEN: PIPELINE AÇIKLAMASI ---
    st.info("""
    **Pipeline Logic:**
    1. LLM generates an alternative movie ending based on a target emotion.
    2. A second LLM evaluates emotional alignment as an impartial judge.
    3. The system outputs a numeric alignment score with reasoning.
    """)
    
    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Girdi Parametreleri")
        movie_query = st.text_input("Film Adı", "Inception")
        target_emotion = st.selectbox("Hedeflenen Duygu (Target Emotion)", TARGET_EMOTIONS)
        
        movie_data = None
        if movie_query:
            with st.spinner("TMDB verisi çekiliyor..."):
                movie_data = tmdb_service.search_movie(movie_query)
            
            if movie_data:
                st.image(movie_data['poster_path'], width=100)
                st.caption(f"{movie_data['title']} ({movie_data['release_date'][:4]})")
                
                # --- DÜZELTME: ÖZETİ TAM OKUMAK İÇİN EXPANDER ---
                with st.expander("📄 Orijinal Film Özetini Oku"):
                    st.write(movie_data['overview'])
    
    with col2:
        st.subheader("2. Pipeline İşleyişi")
        run_btn = st.button("🚀 Pipeline'ı Başlat", type="primary", use_container_width=True)

        if run_btn and movie_data:
            with st.status("Pipeline Çalışıyor...", expanded=True) as status:
                
                # ADIM 1: GENERATION
                st.write("📝 **Step 1: Story Generation**")
                st.write(f"Model, '{target_emotion}' tonunda yazıyor...")
                
                generated_story = ai_service.generate_ending(
                    movie_name=movie_data['title'],
                    summary=movie_data['overview'],
                    emotion=target_emotion
                )
                st.write("✅ Hikaye üretildi.")
                time.sleep(0.5)

                # ADIM 2: EVALUATION
                st.write("⚖️ **Step 2: Emotion Alignment Evaluation**")
                st.write("Prompt engineering ile değerlendirme yapılıyor...")
                
                eval_result_text = ai_service.evaluate_alignment(generated_story, target_emotion)
                score, reason = parse_evaluation(eval_result_text)
                
                status.update(label="Pipeline Tamamlandı!", state="complete", expanded=False)

            st.divider()
            st.markdown("### 📊 Analiz Sonuçları")
            
            # --- YENİ EKLENEN: SCORE ETİKETİ ---
            score_label = get_score_label(score)
            
            col_metric, col_bar = st.columns([1, 3])
            with col_metric:
                # Skoru ve Etiketi Birlikte Gösteriyoruz
                st.metric(label="Alignment Score", value=f"{score}/100", delta=score_label)
            
            with col_bar:
                st.progress(score / 100)
                if score >= 90:
                    st.success(f"**{score_label}:** {reason}")
                elif score >= 70:
                    st.warning(f"**{score_label}:** {reason}")
                else:
                    st.error(f"**{score_label}:** {reason}")

            st.markdown("---")
            st.markdown("#### 📖 Üretilen Final:")
            st.write(generated_story)

if __name__ == "__main__":
    main()