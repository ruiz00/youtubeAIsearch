
# YouTube Video Relevance Analyzer

This project analyzes the **relevance of a YouTube video** based on its **comments** using the **YouTube Data API** for fetching comments and **Google Gemini API** for text analysis.

The tool:

* Fetches up to 100 top-level comments for a given YouTube video
* Uses a large language model (Gemini) to classify the video as:

  * **Relevant**
  * **Moderately Relevant**
  * **Not Relevant**
* Allows you to analyze **multiple videos in one session** interactively

---

## 🚀 Features

* **Interactive Prompt**: Enter YouTube video links directly
* **Automatic Video ID Extraction**: Works with standard YouTube links (e.g., `https://youtu.be/...` or `https://www.youtube.com/watch?v=...`)
* **Comments Fetching**: Pulls up to 100 recent top-level comments per video
* **AI Analysis**: Classifies relevance based on comment content
* **Multiple Video Support**: Analyze as many videos as you want in a single run

---

## 📋 Requirements

* Python 3.8+
* YouTube Data API Key
* Google Gemini API Key

---

## 📦 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ruiz00/youtubeAIsearch/
   cd youtubeAIsearch
   ```

2. **Install dependencies**:

   ```bash
   pip install --upgrade google-api-python-client google-genai
   ```

3. **Set API Keys**:
   Get your keys from:

   * [YouTube Data API](https://console.cloud.google.com/apis)
   * [Google AI Studio](https://aistudio.google.com/)

   Set them as environment variables:

   ```bash
   export YOUTUBE_API_KEY="your_youtube_api_key_here"
   export GEMINI_API_KEY="your_gemini_api_key_here"
   ```

   Or replace them directly in the script (not recommended for production).

---

## 🧑‍💻 Usage

Run the script:

```bash
python3 youtube_analyzer.py
```

Example session:

```
Enter a YouTube video link or ID: https://youtu.be/25iMrJDyIDk
Fetching comments...
Fetched 100 comments. Analyzing with Gemini...

Relevance Assessment:
Relevant - The comments discuss the tutorial content in detail.

Do you want to analyze another video? (y/n): y
Enter a YouTube video link or ID: https://youtu.be/abcd1234
...
```

---

## 🛠️ Project Structure

```
youtube-relevance-analyzer/
│-- youtube_analyzer.py      # Main script
│-- README.md                 # Project documentation
│-- requirements.txt          # Python dependencies
```

---

## ⚙️ Configuration

You can modify:

* `max_comments_to_fetch`: Number of comments to analyze
* `model_name`: Choose from available Gemini models
* `sample_size`: Number of comments used for analysis

---

## 📌 To-Do / Future Enhancements

* [ ] Store results in a CSV or Markdown file automatically
* [ ] Add sentiment analysis for comments
* [ ] Create a simple web interface for non-technical users

---
