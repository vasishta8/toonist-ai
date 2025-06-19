import os
from dotenv import load_dotenv
from groq import Groq  # Import Groq's SDK
# from langchain_groq import ChatGroq
# from langchain import LLMChain
# from langchain.prompts import PromptTemplate
# from imagegeneration import generate_image
import json
import re
load_dotenv()
client = Groq(
    api_key= os.getenv("GROQ_API_KEY")
)


def extract_json(text):
    start = text.find('{')
    if start == -1:
        return None

    stack = []
    for i in range(start, len(text)):
        if text[i] == '{':
            stack.append('{')
        elif text[i] == '}':
            stack.pop()
            if not stack:
                try:
                    json_obj = text[start:i + 1]
                    json.loads(json_obj)  # validate it's valid JSON
                    return json_obj
                except json.JSONDecodeError:
                    return None
    return None


def create_story_agent(topic):
    prompt = f"""Create an engaging educative comic story about {topic} with this structure:
    - 3-4 pages, each with exactly 7 panels
    - Pages should have:
      - Famous masked villain(Thanos) causing a problem related to {topic}
      - Famous Superheroes (spiderman, ironman) resolving it through educational content
      - Panel 7 on each page must feature Dr. Gyaan explaining concepts.
    - Format:
        Page 1:
        Panel 1: [Scene description] | [Character]: [Dialogue]
        Panel 2: [Scene description] | [Character]: [Dialogue]
        ...
        Panel 7: Dr. Gyaan: [Educational explanation]
    Make the scene description very long and detailed. The scene description should include all the characters present in the moment. 
    The scene should describe how the character looks every single time. We need to do image generation on these descriptions.
    Make dialogues clear and friendly for kids and the size of a dialogue should be between 15 to 20 words.
    Make sure the dialogue is atleast 15 words long. DO NOT use any words less than 15 words.
    The story should be engaging, with dramatic scenes and kid-friendly action.
    Dr. Gyaan should explain the concept in maximum 22 words. Make sure it does not exceed 150 text-characters.
    Focus on {topic} concepts.
    Include dramatic scenes, kid-friendly action, and clear educational content."""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

# Agent 2: JSON Formatter
def format_json_agent(story_text):
    prompt = """Convert this comic story into perfect JSON format. Don't change the story, just format it into JSON.:
    Use this structure:
    {
      "pages": [
        {
          "page_number": 1,
          "panels": [
            {
              "panel_number": 1,
              "scene": "scene description",
              "dialogue": { "speaker": "name", "text": "dialogue" }
            },
            // Panels 2-6...
            {
              "panel_number": 7,
              "scene": null,
              "dialogue": { "speaker": "Dr. Gyaan", "text": "explanation" }
            }
          ]
        }
      ]
    }
    
    Rules:
    - Maintain exact structure
    - Dr. Gyaan ONLY in panel 7
    - scene for panel 7 must be null
    - Keep dialogues under 20 words except Dr. Gyaan
    - Ensure valid JSON syntax
    - The scenes should be descriptive and write the physical characteristics of the characters in the scene.
    - The dialogues should be clear and friendly for kids. Focus on concepts.
    The story is :

    """
    prompt += story_text
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    json_output = response.choices[0].message.content
    json_str = extract_json(json_output)
    if json_str is None:
        raise ValueError("No valid JSON found in the response.")
    parsed_json = json.loads(json_str)
    return parsed_json
# # Main execution
text_input = "Teach me about the water cycle"

# # Agent 1 creates story
story = create_story_agent(text_input)
print("Generated Story:\n", story)

# # Agent 2 formats to JSON
json_story = format_json_agent(story)
print("Formatted JSON:\n", json.dumps(json_story, indent=2))