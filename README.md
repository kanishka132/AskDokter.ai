# AskDokter.ai 🩺🤖

**Your AI-powered health companion – Empowering accurate, accessible, and respectful healthcare guidance anytime, anywhere.**

---

## 🌟 Overview

**AskDokter.ai** is a web-based AI health assistant that integrates three key tools:

* ✅ **Myth Buster** – Debunks common health myths with trusted, evidence-based explanations.
* 🤒 **Interactive Symptom Checker** – Asks tailored follow-up questions to understand user symptoms and provides possible diagnoses with severity and care tips.
* 🧠 **Mental Health Assistant** – Offers a safe space for users to express their thoughts and emotions, responding with supportive and mental wellness–focused guidance.

---

## 🚀 Inspiration

Healthcare misinformation and accessibility gaps inspired this project. We wanted to create a digital space where users could receive reliable medical support, especially when immediate consultation isn't available. With AI, we aimed to simulate respectful and informed interactions similar to real consultations.

---

## 🛠️ Built With

* **Frontend**: HTML5, CSS3, JavaScript
* **Backend**: Python, Flask
* **AI Integration**: [Perplexity Sonar API](https://docs.perplexity.ai/) (Sonar and Sonar-Pro used)
* **Rendering**: Jinja2 Templating
* **Markdown Processing**: Python-Markdown
* **Session Management**: Flask Session

---

## 🔍 How It Works

* User visits the homepage and selects one of the three features.
* Each feature is backed by a Flask route and renders a dynamic page.
* The backend sends conversational prompts to **Perplexity’s Sonar API**, maintaining message history for coherent back-and-forth interaction.
* For the **Symptom Checker**, the API is guided by a carefully crafted system prompt to simulate step-by-step diagnosis logic, including:

  * One question at a time
  * Recognizing user selection by number
  * Only returning diagnosis when enough info is gathered
* The **Mental Health Assistant** uses tone-tuned prompts to offer emotionally sensitive replies.

---

## 💡 What We Learned

* Prompt engineering is essential for guiding AI behavior, especially in health contexts.
* Building a multi-route Flask app with session tracking for each tool was key to modularizing the features.
* Balancing medical accuracy with friendly UX was a rewarding challenge.

---

## ⚠️ Challenges Faced

* Managing dynamic state and session data without a database.
* Ensuring the AI doesn’t repeat questions or offer citations unless required.
* Making the UI accessible and responsive while maintaining clarity in long AI responses.

---

## 🔮 What's Next for AskDokter.ai

* 🧪 Integrate a **Prescription Analyzer** for drug safety checks
* 📊 Track user input patterns anonymously to improve prompt handling
* 🌐 Translate responses into **multiple languages** for global access
* 🗣️ Add **voice input/output** for accessibility
* 📱 Deploy as a mobile-first PWA (Progressive Web App)

---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/askdokter.ai.git
cd askdokter.ai
pip install -r requirements.txt
```

Set your **Perplexity API key** in the script.

Run the app:

```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000)

---

## 📡 API Used

**Perplexity Sonar API** – Used for all AI-powered responses. Each tool sends role-based messages to the API, guiding the model to behave like a respectful health assistant, tailored for either myth busting, symptom diagnosis, or mental health support.

---

## 🙌 Acknowledgements

Thanks to **Perplexity AI** for enabling this project with their Sonar API and to the open-source communities supporting Flask and Python.
