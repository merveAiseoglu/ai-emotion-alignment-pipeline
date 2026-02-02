from openai import OpenAI
from config.settings import OPENAI_API_KEY, AI_MODEL

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_ending(self, movie_name, summary, emotion):
        """
        AŞAMA 2: Story Generation
        """
        system_prompt = f"""
        Sen yaratıcı bir senaristsin. Görevin '{movie_name}' filmi için ALTERNATİF bir final yazmak.
        
        KURALLAR:
        1. Hedef Duygu: {emotion.upper()}
        2. Bu duygu final sahnesinde çok baskın hissedilmeli.
        3. Mantık hatası yapma, karakterler tutarlı kalsın.
        4. Ortalama 200-300 kelime olsun.
        """
        
        user_prompt = f"Orijinal Özet: {summary}\n\nLütfen '{emotion}' tonunda yeni bir final yaz."

        try:
            response = self.client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Hata: {str(e)}"

    def evaluate_alignment(self, generated_story, target_emotion):
        """
        AŞAMA 3: Emotion Alignment Evaluation (LLM-as-a-Judge)
        Güncellenmiş 'Impartial Evaluator' promptunu kullanır.
        """
        
        # Senin gönderdiğin 'System' kısmı (Talimatlar ve Kurallar)
        system_prompt = """You are an impartial evaluator.

Your task is to evaluate how well the emotional tone of the given story aligns with the target emotion specified by the user.

Evaluation Instructions:
- Focus ONLY on emotional alignment.
- Do NOT evaluate writing quality, creativity, or plot originality.
- Assess whether the dominant emotional arc of the story consistently matches the target emotion from beginning to end.

Scoring Rules:
- Score the alignment on a scale from 0 to 100.
- 0–30: Emotion is mostly absent or contradictory.
- 31–60: Emotion is partially present but inconsistent.
- 61–85: Emotion is clear and mostly consistent.
- 86–100: Emotion is strongly and consistently conveyed throughout.

Output Format (STRICT):
Score: <number between 0 and 100>
Reasoning: <2–3 concise sentences explaining the score>"""

        # Senin gönderdiğin 'User' kısmı (Değişken Veriler)
        user_prompt = f"""Target Emotion:
{target_emotion}

Story:
{generated_story}"""

        try:
            response = self.client.chat.completions.create(
                model=AI_MODEL, 
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0 # Tutarlı puanlama için sıfır
            )
            return response.choices[0].message.content
        except Exception as e:
            return "Score: 0\nReasoning: Evaluation error occurred."