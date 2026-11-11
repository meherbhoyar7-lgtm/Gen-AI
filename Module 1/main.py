import os 
import json
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from schema import TextRequest

load_dotenv() # Load environment variables from .env file

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.") 

model = os.getenv("CHAT_MODEL")  # Default to "gemini-3.5-flash-lite" if not set  
if not model:
    raise ValueError("CHAT_MODEL is not set in the environment variables.") 

app = FastAPI(
    title="Module 1 - API Interaction of AI Tutor Project",
    description="This API allows you to generate text based on a given topic, course, and student level using the Gemini API.",
    version="1.0.0"
)

ai_client = genai.Client(api_key=gemini_api_key)

# Text input to generate explanantion for the topic, course and student level
@app.post("/generate-text")
async def generate_explanation(request: TextRequest):
    prompt = f"""
    You are an AI tutor creating study material for a student.
    Topic: "{request.topic}"
    Subject: "{request.course or "Not specified"}"
    Student level: "{request.student_level}"

    Explain the topic clearly and accurately using language suited to the student.
    Output a valid JSON response containing:
    1. "topic": string
    2. "lesson_content": string (clear explanation for study)
    3. "key_terms": list of objects with "term" and "definition" strings
    4. "example": string (a relevant example)
    5. "practice_questions": list of 3 questions
    """

    try:
        response = ai_client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                response_mime_type="application/json"
            )
        )

        response_json = json.loads(response.text)
        return JSONResponse(status_code=200, content=response_json)
            
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    #Academic Image Analysis and Explanation 
    @app.post("/analyze-image")
    async def analyze_image(File: UploadFile = File(...)):
        if file.content_type not in ["image/jpeg", "image/png"]:
            return JSONResponse(status_code=400, content={"error": "Invalid file type. Only JPEG and PNG files are allowed."})

        try:
            image_bytes = await file.read()
            image_input = types.Part.from_bytes(image_bytes, mime_type=file.content_type)

            prompt = f"""
            You are an AI tutor analyzing an academic image.
            Question: "{question}"

            Provide a clear and accurate explanation of the image in relation to the question.
            Output a valid JSON response containing:
            1. "image_analysis": string (detailed analysis of the image)
            2. "key_points": list of strings (important points from the analysis)
            3. "related_concepts": list of strings (concepts related to the image and question)
            """

            response = await ai_client.models.generate_content(
                model=model,
                contents=[prompt, image_input],
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    response_mime_type="application/json"
                )
            )

            response_json = json.loads(response.text)   
            return JSONResponse(status_code=200, content=response_json) 

        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})

    # Text Question and Audio Answer Evaluation
    @app.post("/evaluate-audio-answer")
    async def evaluate_audio_answer(file: UploadFile = File(...), question: str = Form(...)):
        if file.content_type not in ["audio/mpeg", "audio/wav"]:
            return JSONResponse(status_code=400, content={"error": "Invalid file type. Only MP3 and WAV files are allowed."})

        try:
            audio_bytes = await file.read()
            audio_input = types.Part.from_bytes(audio_bytes, mime_type=file.content_type)

            prompt = f"""
            You are an AI tutor evaluating a student's answer to a question.
            Question: "{question}"

            Evaluate the student's answer provided in the audio file.
            Output a valid JSON response containing:
            1. "evaluation": string (detailed evaluation of the answer)
            2. "score": integer (score out of 10)
            3. "feedback": string (constructive feedback for improvement)
            """

            response = await ai_client.models.generate_content(
                model=model,
                contents=[prompt, audio_input],
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    response_mime_type="application/json"
                )
            )

            response_json = json.loads(response.text)   
            return JSONResponse(status_code=200, content=response_json) 

        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})


# Video Analysis and Generate 3 MCQ Questi with options and answers
    @app.post("/analyze-video")
    async def analyze_video(file: UploadFile = File(...), question: str = Form(...)):
        if file.content_type not in ["video/mp4", "video/avi"]:
            return JSONResponse(status_code=400, content={"error": "Invalid file type. Only MP4 and AVI files are allowed."})

        try:
            video_bytes = await file.read()
            video_input = types.Part.from_bytes(video_bytes, mime_type=file.content_type)

            prompt = f"""
            You are an AI tutor analyzing an academic video.
            Question: "{question}"

            Provide a clear and accurate analysis of the video in relation to the question.
            Generate 3 multiple-choice questions (MCQs) based on the video content, each with 4 options and the correct answer.
            Output a valid JSON response containing:
            1. "video_analysis": string (detailed analysis of the video)
            2. "mcq_questions": list of objects with "question", "options" (list of strings), and "correct_answer" (string)
            """

            response = await ai_client.models.generate_content(
                model=model,
                contents=[prompt, video_input],
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    response_mime_type="application/json"
                )
            )

            response_json = json.loads(response.text)   
            return JSONResponse(status_code=200, content=response_json) 

        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})