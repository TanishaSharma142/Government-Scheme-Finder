# GovScheme AI

**GovScheme AI** is a smart, empathetic agent designed to bridge the gap between Indian citizens and government benefits. Using **Retrieval-Augmented Generation (RAG)**, it analyzes user profiles (age, income, occupation) against a verified database of schemes to provide accurate, hallucination-free eligibility results.

## 🛑 The Problem Solved
Navigating the Indian government welfare system is overwhelming.
* **Fragmentation:** There are hundreds of schemes (Central & State) scattered across different websites.
* **Complexity:** Eligibility rules involve complex combinations of age, income, caste, and disability status.
* **Information Gap:** Most citizens, especially in rural areas, are unaware of the benefits they are legally entitled to (e.g., *PM-Kisan*, *Ayushman Bharat*).

## 💡 Why a "Code Agent" is Better than ChatGPT?
You might ask: *"Why not just use ChatGPT?"*

| Feature | ❌ Standard LLM (ChatGPT/Gemini) | ✅ SLM trained for particular use |
| :--- | :--- | :--- |
| **Accuracy** | **Hallucinates.** It often invents schemes or mixes up eligibility criteria (e.g., confusing State vs. Central rules). | **100% Deterministic.** It uses Python logic (`if income < 200000`) to strictly validate eligibility against a verified database. |
| **Data Freshness** | **Outdated.** Training data has a cutoff; it doesn't know about schemes launched last week. | **Real-Time.** We simply update the local `schemes.json` file, and the agent is instantly updated without re-training. |
| ** reasoning** | **Probabilistic.** It "guesses" the next word. It struggles with strict math comparisons (e.g., `<` or `>`). | **Logical.** The agent writes and executes actual Python code to compare user data against scheme rules. |
| **Privacy** | **Cloud-Dependent.** User data (income, caste) is sent to external servers for processing. | **Privacy-First.** The logic runs locally or on a controlled backend; personal PII doesn't need to be stored. |

**In short:** We use the LLM as a *reasoning engine* to understand the user, but we use **Code Tools** to ensure the final answer is factually correct.

## 🚀 Key Features
* **🎯 Precision Matching:** Filters schemes based on strict logic (Age, Income, Caste, State) using `smolagents`.
* **🧠 RAG Architecture:** Grounds answers in a local verified dataset (`schemes.json`) instead of generic LLM training data.
* **🔒 Privacy First:** Runs locally; no user data is stored or sent to external servers.
* **🛠️ Developer Admin Mode:** Hidden debug features unlockable via **Requestly** (see below).

## 🛠️ Tech Stack
* **Framework:** Streamlit (Frontend)
* **AI Engine:** `smolagents` (Logic) + Hugging Face `Zephyr/Qwen` (Inference)
* **Tooling:** Requestly (Traffic Modification & Testing)
* **Language:** Python 3.10+

## ⚙️ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone (https://github.com/TanishaSharma142/Government-Scheme-Finder)
    cd Government-Scheme-Finder
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up keys**
    Create a `.env` file and add your Hugging Face token:
    ```ini
    HF_TOKEN=hf_your_token_here
    ```

4.  **Run the App**
    ```bash
    streamlit run app.py
    ```

---

## 🐞 Hackathon Feature: Requestly Integration

Feature Used: Modify Query Parameters / URL Rules
Goal: Implement a zero-code "Feature Flag" and production debugging environment.

🤔 The "Why": The Problem We Faced
When building GovScheme AI, we needed a way to monitor the AI agent's internal state—like LLM latency, the specific model being called (e.g., our custom Smolified model vs. Zephyr), and server health.
However, showing this technical data to an average citizen (the end-user) would ruin the simple, accessible UI. We needed a "God Mode" or "Admin Dashboard" for developers to test the live app, but we didn't have the time to build a full authentication system just for a hackathon demo.

🛠️ The "How": Our Requestly Solution
We used Requestly to act as an invisible feature flag system.
The Rule: We created a Requestly rule that intercepts traffic to our application (localhost:8501 or our deployment URL).
The Injection: The rule automatically appends a hidden query parameter: ?mode=admin.
The Logic: Inside our Streamlit application (app.py), we wrote a simple listener:
Python
query_params = st.query_params
if query_params.get("mode") == "admin":
    # Unlock hidden developer UI
📍 The "Where": The Impact on the Project
By simply toggling the Requestly extension ON, the application instantly transforms.

The injected parameter triggers a hidden rendering block in our code, revealing a 🔴 REQUESTLY DEBUG MODE banner and unlocking a secret sidebar dashboard. This dashboard streams live analytics (Model Version, Inference Latency, and Tool Call Status) that are otherwise completely invisible to regular users.

Conclusion: Requestly allowed us to test production-grade debugging and feature toggling without altering our codebase or deploying new environments. It proved that browser-level network modification is an incredibly powerful tool for AI application developers.

## 📂 Project Structure

```text
├── app.py             # Main Application (Streamlit + Requestly Logic)
├── agent.py           # AI Agent Logic & Tools
├── schemes.json       # The Knowledge Base (Database)
├── requirements.txt   # Dependencies
└── README.md          # Documentation
```

## 🤝 Contributing
Built for the **Krackhack3.0**. Suggestions and pull requests are welcome!
