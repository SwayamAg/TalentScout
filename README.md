# TalentScout Hiring Assistant 🤖

An AI-powered hiring assistant chatbot built using **Streamlit** and **Azure OpenAI (GPT-4o-mini)** to automate initial candidate screening through structured conversations and dynamic technical question generation.

---

## 📌 Project Overview

TalentScout is designed to assist recruitment teams by conducting **initial candidate screening**.  
The chatbot collects essential candidate details, understands the candidate’s declared tech stack, and generates **relevant technical interview questions** tailored to that stack.

The system focuses on:
- Prompt engineering
- Context-aware interaction
- Privacy-first data handling
- Clean, explainable architecture

---

## 🎯 Key Features

- **Interactive Streamlit Chat UI**
- **Step-by-step candidate information gathering**
- **Tech stack–based technical question generation (3–5 questions)**
- **Context-aware conversation flow**
- **Graceful exit handling**
- **Session-only, in-memory data handling**

---

## 🎥 Project Preview (Demo)

> 📌 **Demo Video:**  
> [Watch the demo video on Google Drive](https://drive.google.com/file/d/1oA0PWhOm9C4mDXy1nSvc1_Wm5ZyUKnqe/view?usp=sharing)

---

## 🧠 Prompt Engineering Strategy

The project uses carefully designed prompts to:

1. **Define the chatbot role**  
   A system prompt restricts the chatbot strictly to hiring and technical screening.

2. **Guide technical question generation**  
   A structured prompt template ensures:
   - Stack-specific questions
   - No answers or hints
   - Appropriate difficulty level

3. **Maintain coherent conversation flow**  
   Prompts and application logic work together to ensure the chatbot does not deviate from its purpose.

---

## 🏗️ System Architecture

```
├── app.py              # Streamlit UI and conversation flow
├── llm_client.py       # Azure OpenAI (GPT-4o-mini) client wrapper
├── conversation.py     # Conversation logic and helpers
├── prompts.py          # System and task-specific prompts
├── requirements.txt    # Project dependencies
├── .env                # Environment variables (not committed)
```

---

## ⚙️ Working of the Project

### **Conversation Flow & State Management**

The application uses a **step-based state machine** to manage the conversation flow through Streamlit's `st.session_state`. Here's how it works:

#### **Step 0: Initialization**
- When the app loads for the first time, `step = 0`
- The chatbot displays a greeting message (`get_greeting_message()`)
- Immediately asks for the first field: **"Full Name"**
- Sets `step = 1` and initializes `field_index = 0`

#### **Step 1: Candidate Information Collection**
- The app collects **6 fields sequentially** using `field_index` to track progress:
  1. Full Name
  2. Email Address
  3. Phone Number
  4. Years of Experience
  5. Desired Position(s)
  6. Current Location
- For each user input:
  - Stores the value in `candidate_data[field_name]`
  - Increments `field_index`
  - If more fields remain → asks for the next field
  - If all fields collected → moves to `step = 2` and asks for tech stack

#### **Step 2: Tech Stack & Question Generation**
- User provides their tech stack (e.g., "Python, Django, PostgreSQL, React")
- The app:
  1. Stores tech stack in `candidate_data["Tech Stack"]`
  2. Displays: *"Generating technical questions based on your tech stack..."*
  3. Calls `generate_technical_questions(tech_stack)` from `conversation.py`
  4. This function:
     - Formats `TECH_QUESTION_PROMPT_TEMPLATE` with the tech stack
     - Creates a messages array with `SYSTEM_PROMPT` and the formatted prompt
     - Calls `get_llm_response()` from `llm_client.py`
     - Returns 3–5 technical questions from Azure OpenAI
  5. Displays the generated questions
  6. Shows closing message
  7. Sets `step = 3` (conversation ends)

#### **Step 3: Conversation Complete**
- No further input is processed
- All collected data remains in `st.session_state.candidate_data` (in-memory only)

### **Component Interactions**

```
┌─────────────┐
│   app.py    │  ← Main UI & State Management
└──────┬──────┘
       │
       ├──→ conversation.py
       │      ├──→ get_greeting_message()
       │      ├──→ get_closing_message()
       │      ├──→ is_exit_message()
       │      └──→ generate_technical_questions()
       │              │
       │              └──→ llm_client.py
       │                     └──→ get_llm_response()
       │                             │
       │                             └──→ Azure OpenAI API
       │
       └──→ prompts.py
              ├──→ SYSTEM_PROMPT
              └──→ TECH_QUESTION_PROMPT_TEMPLATE
```

### **Key Mechanisms**

1. **State Persistence**
   - `st.session_state.messages`: Stores entire chat history
   - `st.session_state.step`: Tracks conversation phase (0, 1, 2, 3)
   - `st.session_state.candidate_data`: Dictionary of collected information
   - `st.session_state.field_index`: Tracks which field is being collected

2. **Rerun Behavior**
   - Streamlit reruns the entire script on each user interaction
   - `st.rerun()` is called after processing user input to refresh the UI
   - State variables persist across reruns, maintaining conversation context

3. **Exit Handling**
   - User can type: `exit`, `quit`, `done`, or `thank you` (case-insensitive, exact match)
   - Triggers `is_exit_message()` → displays closing message → calls `st.stop()`

4. **LLM Integration**
   - `llm_client.py` initializes `AzureOpenAI` client using environment variables
   - `get_llm_response()` uses temperature `0.3` for consistent, deterministic output
   - Model deployment name is read from `AZURE_OPENAI_DEPLOYMENT_NAME`

5. **Prompt Engineering**
   - `SYSTEM_PROMPT` defines the chatbot's role and constraints
   - `TECH_QUESTION_PROMPT_TEMPLATE` is dynamically filled with candidate's tech stack
   - Prompts ensure no answers are provided, only questions

### **Data Flow Example**

```
User Input: "John Doe"
    ↓
app.py: Stores in candidate_data["Full Name"]
    ↓
app.py: Increments field_index, asks for Email
    ↓
User Input: "john@example.com"
    ↓
... (continues for all 6 fields)
    ↓
User Input: "Python, Django, PostgreSQL"
    ↓
app.py: Calls generate_technical_questions("Python, Django, PostgreSQL")
    ↓
conversation.py: Formats prompt with tech stack
    ↓
llm_client.py: Sends request to Azure OpenAI
    ↓
Azure OpenAI: Returns 3-5 technical questions
    ↓
app.py: Displays questions + closing message
```

---

## 🔐 Data Handling & Privacy

- Candidate data is stored **only in memory** using `st.session_state`
- No databases, files, or logs are used to persist data
- Data is automatically cleared when the session ends or the page is refreshed
- This approach aligns with **privacy-by-design** principles and GDPR-friendly practices for demo systems

---

## ⚙️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **LLM:** Azure OpenAI (GPT-4o-mini)
- **Environment Management:** python-dotenv

---

## 🚀 How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone <your-repo-url>
cd TalentScout
```

### 2️⃣ Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables
Create a `.env` file:
```env
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 5️⃣ Run the application
```bash
streamlit run app.py
```

---

## 🧪 Example Flow

1. Chatbot greets the candidate and explains its purpose  
2. Collects candidate details:
   - Name, Email, Phone, Experience, Desired Role, Location
3. Prompts for tech stack
4. Generates 3–5 tailored technical questions
5. Ends the conversation gracefully

---

## ⚠️ Challenges & Solutions

### 1️⃣ Managing conversation flow in Streamlit
Streamlit reruns the script on every user interaction. This was addressed using `st.session_state` along with step-based and index-based tracking to preserve conversation context and ensure a coherent, sequential flow.

### 2️⃣ Azure OpenAI integration
Azure OpenAI requires deployment-based routing and explicit API versioning. The project uses the `AzureOpenAI` client with a fixed API version to ensure stable and correct communication with the GPT-4o-mini model.

### 3️⃣ Data privacy considerations
To avoid unnecessary storage of sensitive information, all candidate data is handled in-memory only and is automatically cleared when the session ends or the page is refreshed, ensuring privacy-first behavior.

---

## 🔮 Future Enhancements

- Follow-up and adaptive questioning based on candidate responses
- Candidate proficiency scoring
- Integration with databases or ATS systems
- Use of **LangChain** for advanced prompt chaining and conversational memory
- Multilingual support

---

## 💳 Credits

- Built with ❤️ by [Swayam Agarwal](https://github.com/SwayamAg)
- Uses [Streamlit](https://streamlit.io/), [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service), and [Python](https://www.python.org/)

---

## 📄 License

### *Usage Terms*

- This project is provided as-is for learning and demonstration purposes
- Not intended for production use without proper security, error handling, and compliance measures
- Candidate data is handled in-memory only and is not persisted (see [Data Handling & Privacy](#-data-handling--privacy))
- Users are responsible for ensuring compliance with data protection regulations (GDPR, CCPA, etc.) if deploying

### *Attribution*

If you use this project as a reference or base for your own work, please provide appropriate attribution to the original project.
