# MCQ Generator Application with LangChain and Groq

An AI-powered web application that automatically generates and evaluates
Multiple Choice Questions (MCQs) from user-uploaded text or PDF documents. The
project is built using **Streamlit**, **LangChain**, and **Groq's LLM**.

## 📺 Demo

<video src="localhost-app.webm" width="100%" controls></video>

---

## 🚀 Key Features

- **Document Support:** Upload `.txt` and `.pdf` files. Text is parsed and
  extracted dynamically.
- **Custom MCQ Parameters:** Customize the number of questions, target subject,
  and difficulty tone (Easy, Intermediate, Hard).
- **AI Pipelines (LangChain):**
  - **Generation Chain:** Uses a custom prompt template and a reference JSON
    schema (`response.json`) to return structured questions.
  - **Review Chain:** Acts as a subject-matter expert to review and evaluate the
    complexity of the generated quiz.
  - **Sequential Chain execution:** Generates and reviews the quiz in a single
    user action.
- **Formatted UI Output:** Displays generated MCQs inside an interactive
  Streamlit table and presents the expert review evaluation in structured
  markdown.
- **Logging System:** Implements modular logging to capture execution and trace
  errors under the `logs/` directory.

---

## 📂 Project Structure

```text
mcqgen/
│
├── .env                  # Local environment variable configuration (API keys)
├── .env.example          # Reference template for environment variables
├── .gitignore            # Git ignore file
├── app.py                # Main Streamlit application entrypoint
├── requirements.txt      # Python dependencies
├── response.json         # Reference schema for JSON output format
├── setup.py              # Packaging script for local installation
│
├── experiment/           # Notebooks and testing data
│   ├── mcqgen.ipynb      # Development playground / Jupyter Notebook
│   └── test.txt          # Sample test text file
│
├── logs/                 # Directory containing application run logs
│
└── src/                  # Source directory for modular code
    └── mcqgen/
        ├── __init__.py   # Packaged source marker
        ├── logger.py     # Custom logger configuration
        ├── MCQGenerator.py # LangChain chain pipeline definition
        └── utils.py      # File parsers and data processing utilities
```

---

## 🛠️ Local Installation & Setup

Follow these instructions to run the application on your local machine:

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd mcqgen
```

### 2. Create and Activate a Virtual Environment

```bash
# Create environment
python -m venv .venv

# Activate on Windows:
.venv\Scripts\activate

# Activate on macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

Install all required libraries including the package in editable mode:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Open `.env` and fill in your Groq API Key:

```env
GROQ_API_KEY="your_groq_api_key_here"
```

### 5. Launch the Streamlit App

```bash
streamlit run app.py
```

---

## ☁️ Deployment Steps (AWS EC2)

Deploy the Streamlit application to an AWS EC2 instance:

### 1. Setup AWS EC2 Instance

1. Log in to the [AWS Management Console](https://aws.amazon.com/console/).
2. Navigate to **EC2** and select **Launch Instance**.
3. Select **Ubuntu Server** as the Amazon Machine Image (AMI).
4. Select your desired instance type (e.g., `t2.micro` or similar).
5. Choose or create a Key Pair (`.pem`) for SSH access.
6. Under **Security Groups**, configure the inbound rules:
   - Allow **SSH** (port `22`) for your IP address.
   - Allow **Custom TCP** (port `8501`) from anywhere (or restricted IP ranges)
     to expose Streamlit's web port.
7. Click **Launch Instance**.

### 2. Connect & Prepare the Instance

Connect to the server via SSH:

```bash
ssh -i "your-key-pair.pem" ubuntu@your-instance-public-ip
```

Update system packages and install prerequisites:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install git curl unzip tar make sudo vim wget -y
```

### 3. Clone and Install Project

Clone your repository:

```bash
git clone <your-repository-url>
cd mcqgen
```

Install Pip and Python libraries:

```bash
sudo apt install python3-pip -y
pip3 install -r requirements.txt
```

### 4. Setup Secrets & API Key

Create a `.env` file on the server:

```bash
touch .env
nano .env
```

Paste your Groq API key:

```env
GROQ_API_KEY="your_actual_groq_api_key"
```

_(Press `Ctrl+O` then `Enter` to save, and `Ctrl+X` to exit nano)_

### 5. Run Streamlit in the Background

Run the Streamlit application in background mode so that it doesn't shut down
when the SSH session ends:

```bash
nohup python3 -m streamlit run app.py &
```

You can now view your app in a web browser at:
`http://your-instance-public-ip:8501`
