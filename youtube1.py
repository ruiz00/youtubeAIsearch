import os
from urllib.parse import urlparse, parse_qs
from google import genai
from google.genai import types
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# --- Configuration ---
YOUTUBE_API_KEY = "YOUR YOUTUBE API KEY"  # Replace with your key or set as env var
GEMINI_API_KEY = "YOUR GEMINI API KEY"    # Replace with your key or set as env var

# YouTube API details
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


# --- Extract Video ID from URL or direct ID ---
def extract_video_id(url_or_id):
    """Extracts the video ID from a YouTube URL or returns it if it's already an ID."""
    if len(url_or_id) == 11 and "http" not in url_or_id:
        return url_or_id

    try:
        parsed_url = urlparse(url_or_id)
        hostname = parsed_url.hostname.lower() if parsed_url.hostname else ""

        if hostname in ["www.youtube.com", "youtube.com", "m.youtube.com"]:
            if parsed_url.path == "/watch":
                return parse_qs(parsed_url.query)["v"][0]
        elif hostname == "youtu.be":
            return parsed_url.path.lstrip("/")
        else:
            raise ValueError("Invalid YouTube URL format")
    except Exception:
        raise ValueError(f"Could not extract video ID from: {url_or_id}")


# --- YouTube Authentication ---
def youtube_authenticate():
    """Authenticates with the YouTube Data API using an API key."""
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY is not set.")
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)


# --- Fetch Comments from YouTube ---
def get_video_comments(youtube_service, video_id, max_comments_to_fetch=500):
    """Fetches comments from a YouTube video."""
    comments = []
    next_page_token = None
    fetched_count = 0

    try:
        while True:
            request = youtube_service.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response["items"]:
                if fetched_count >= max_comments_to_fetch:
                    break
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comments.append(comment["textDisplay"])
                fetched_count += 1

            if fetched_count >= max_comments_to_fetch:
                break

            next_page_token = response.get("nextPageToken")

            if not next_page_token:
                break

    except HttpError as e:
        print(f"HTTP error {e.resp.status}: {e.content}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return comments


# --- Analyze Comments using Gemini API ---
def analyze_comments_with_gemini(comments_list, video_id):
    """Analyzes comments using Gemini API for relevance."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Use a model that supports generateContent
    model_name = "gemini-2.0-flash"  # Change if needed after listing available models

    if not comments_list:
        return "Not enough comments for a meaningful relevance assessment."

    sample_size = min(len(comments_list), 50)
    sampled_comments = "\n".join(comments_list[:sample_size])

    prompt = f"""
    You are an AI assistant tasked with determining the relevance of a YouTube video based on its comments.
    Consider the following {sample_size} comments from a YouTube video (ID: {video_id}).

    Comments:
    {sampled_comments}

    Based *only* on these comments, classify the video's relevance as one of:
    - Relevant
    - Moderately Relevant
    - Not Relevant

    Follow the label with a brief justification.
    """

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

    try:
        response = client.models.generate_content(model=model_name, contents=contents)
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            return "Gemini response was empty or malformed."
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return "Error during analysis."


# --- Main Function ---
def get_video_relevance(video_url_or_id):
    """Fetches comments and analyzes relevance of a YouTube video."""
    try:
        video_id = extract_video_id(video_url_or_id)
    except ValueError as e:
        return f"Error: {e}"

    print(f"\n--- Checking relevance for video: {video_url_or_id} ---")

    try:
        youtube_service = youtube_authenticate()
    except ValueError as e:
        return f"Error: {e}"

    print("Fetching comments...")
    comments = get_video_comments(youtube_service, video_id, max_comments_to_fetch=100)

    if not comments:
        return f"No comments found or could not be retrieved for {video_url_or_id}."

    print(f"Fetched {len(comments)} comments. Analyzing with Gemini...")
    relevance_assessment = analyze_comments_with_gemini(comments, video_id)

    return relevance_assessment


# --- Loop for Multiple Videos ---
if __name__ == "__main__":
    while True:
        user_link = input("\nEnter a YouTube video link or ID: ").strip()
        result = get_video_relevance(user_link)
        print("\nRelevance Assessment:\n", result)

        again = input("\nDo you want to analyze another video? (y/n): ").strip().lower()
        if again != "y":
            print("Exiting program. Goodbye!")
            break
