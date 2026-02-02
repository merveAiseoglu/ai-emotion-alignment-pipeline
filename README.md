# 🧪 AI Emotion Alignment Pipeline

**An automated LLM pipeline that generates creative content and quantitatively evaluates emotional consistency using an LLM-as-a-Judge approach.**

![AI Emotion Alignment Pipeline Screenshot](assets/pipeline.png)
> *Figure 1: The pipeline interface showing the generation (Step 1), evaluation logic (Step 2), and the final alignment score.*

---

## 🚀 Project Purpose (Why?)

Large Language Models (LLMs) are inherently stochastic and subjective. When building AI applications, relying solely on generation is insufficient; we need ways to measure **reliability and adherence to intent.**

This project addresses the challenge of **subjectivity in AI outputs**. While the domain is "movie endings," the core engineering goal is to demonstrate an **automated evaluation pipeline (LLM-as-a-Judge)**. It aims to transform subjective qualities (like emotional tone) into measurable, numeric data points.

---

## ⚙️ How It Works (Pipeline Flow)

The system operates on a linear 3-step pipeline:

1.  **Context & Generation:** The system retrieves **structured movie context via an external API** and uses an LLM to generate an alternative ending based on a specific target emotion (e.g., "Tragic").
2.  **LLM-as-a-Judge Evaluation:** The generated text is passed to a second, impartial LLM instance acting as a "Critic."
3.  **Scoring & Reasoning:** The Evaluator analyzes the text against the user's intent and outputs a numeric **Alignment Score (0–100)** along with a logical reasoning.

---

## 🧠 What is "Emotion Alignment"?

Emotion Alignment refers to the consistency between the **user's intended emotional tone** and the **actual model output**.

This metric does **NOT** measure:
* ❌ Creative writing quality
* ❌ Plot originality
* ❌ Grammatical perfection

It **STRICTLY** measures:
* ✅ Whether the dominant emotional arc of the generated text matches the target constraint.

**This makes it suitable for evaluating intent adherence in constrained generation tasks.**

---

## ⚖️ Evaluation Logic (Scoring System)

The evaluator is prompted to act as an impartial judge, scoring alignment on a strict scale:

| Score Range | Interpretation |
|:---:|:---|
| **90–100** | **Strong Alignment:** The emotion is consistently dominant and clear. |
| **70–89** | **Moderate Alignment:** The emotion is present but lacks intensity or consistency. |
| **< 70** | **Weak Alignment:** The output is neutral, contradictory, or **diverges significantly from the intended emotional arc.** |

---

## 📝 Example Output

Here is a sample output from the pipeline:

* **Target Emotion:** `Tragic`
* **Generated Story:** *(Summary: The protagonist fails to save the city, and the screen fades to black amidst the ruins.)*
* **Alignment Score:** `95/100 (Strong Alignment)`
* **Evaluator Reasoning:** *"The story consistently conveys a tragic tone from beginning to end. The resolution of the characters' struggles results in failure and loss, aligning perfectly with the target emotion of tragedy."*

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Core Logic:** OpenAI API (**Separate LLM calls for Generation and Evaluation**)
* **Interface:** Streamlit
* **Data Source:** TMDB API (For real-time structured context retrieval)
* **Architecture:** Service-Oriented (Separated Generator and Evaluator services)

---

## 💡 Key Takeaways (What I Learned)

Building this project highlighted several core AI Engineering concepts:

* **LLM-as-a-Judge Pattern:** Implementing a secondary model to audit and quality-check the outputs of a primary model is essential for scalable AI systems.
* **Prompt Separation:** The importance of isolating "Generator" prompts from "Evaluator" prompts to prevent context bleeding and bias.
* **Pipeline Architecture:** Thinking in workflows (Input -> Process -> Audit -> Output) rather than simple request/response cycles.
* **Output Controllability:** Using strict system instructions to force the LLM into specific output formats (JSON/Structured text) for parsing.

---

## 🏆 Value Proposition

This project serves as a proof-of-concept for **Self-Reflective AI Systems**. It demonstrates the ability to move beyond simple chatbots and build structured, verifiable, and measurable AI workflows, which is a critical requirement for production-grade LLM applications.

## 🏃‍♂️ How to Run

Follow these steps to set up and run the project locally.

### **1. Clone the Repository**
```bash
git clone [https://github.com/merveAiseoglu/ai-emotion-alignment-pipeline.git](https://github.com/merveAiseoglu/ai-emotion-alignment-pipeline.git)
cd ai-emotion-alignment-pipeline
 ```

### **2.Install Dependencies**
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```
### **3.Set Up Environment Variables**
*Create a .env file in the root directory to store your API keys securely.
*Note: You need an OpenAI API key and a TMDB API Key.
*.env file content:
```bash
OPENAI_API_KEY="sk-proj-..."
TMDB_API_KEY="your_tmdb_key_here"
```
### **4. Launch the Application**
Start the Streamlit interface:
```bash
streamlit run main.py
```






