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
To demonstrate **Developer Tooling** and **Traffic Modification**, this app features a hidden **"Admin Mode"** that is only accessible by injecting a specific query parameter.

### How to Unlock Admin Mode (Demo):
1.  Install the **[Requestly Browser Extension](https://requestly.com/)**.
2.  Create a **Query Param Rule**:
    * **Condition:** URL Contains `localhost:8501`
    * **Param:** `mode`
    * **Value:** `admin`
3.  **Refresh the App.** You will see a **🔴 RED DEBUG BANNER** and a hidden **Analytics Dashboard** appear at the bottom.

> **Why this matters:** This allows developers to test "Pro" features or "Debug" states in production environments without changing the codebase.

---

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
