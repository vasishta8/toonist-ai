from langchain_groq import ChatGroq
from langchain import LLMChain
from langchain.prompts import PromptTemplate
import json
from dotenv import load_dotenv
#from stable_paid_api import image_gen
import re
from groq import Groq
import os

# Load environment variables
load_dotenv()

# Utility function to extract JSON object from string
def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

# Image prompt template
image_prompt = '''You are tasked with generating a **detailed comic book scene description** based on the following scene text and context. The goal is to generate a **standard comic book-style image** suitable for the scene in question.

### **Instructions:**
1. **Context**: You will receive the **scene description** for the current panel in a comic book. Additionally, you will be given the **scene descriptions of previous panels** to provide the necessary context for the ongoing narrative.
2. **Create a comic book image**: Based on the provided scene description and context, generate a detailed **comic book-style image prompt** for the current panel. The image should be drawn in a **Marvel comic book style** with dynamic, bold imagery and dramatic perspectives. 
3. **Ensure continuity**: Use the context from previous scenes to maintain **visual consistency**, ensuring characters, actions, and settings follow a logical progression.
4. **Include visual elements** like lighting, action, character positioning, and the environment. The description should be **detailed** to guide the artist in creating the image.
5. **Make sure the image is in a marvel comic book style**
6. **All the characters present in the scene should be in the screen**

### **Formatting:**
- Your response should be in **JSON format** with **two keys**: 
  - **`scene_description`**: A detailed description of the scene, capturing visual elements, action, lighting, and environment.
  - **`summary`**: A concise summary of the scene, capturing the essence, context, and mood of the scene.

### **Input Example:**

**Current Scene (Panel 3):**  
*Spider-Man swings into action to stop a villain who is causing destruction in the city.*

**Previous Scenes:**
1. *Spider-Man is perched on top of a building, overlooking the city.*
2. *The villain, Dr. Octopus, unleashes mechanical tentacles to wreak havoc.*

### **Expected Output Example:**
```json
{
  "scene_description": "Spider-Man swings into action, his webbing creating streaks in the air. The city skyline looms in the background as Dr. Octopus’s mechanical tentacles lash out, causing chaos below. The sun is setting, casting long shadows and creating an orange glow. Spider-Man’s suit is vibrant, contrasting against the destruction below. The scene captures the intensity of the battle, with dynamic lines and dramatic shading, characteristic of classic Marvel comic book illustrations.",
  "summary": "Spider-Man swings into action to stop Dr. Octopus, whose mechanical tentacles are causing chaos in the city. The battle intensifies against a backdrop of the setting sun."
}

Current scene that you need to create an image prompt for is :
'''

# PromptTemplate (if you plan to use it later)
first_prompt = PromptTemplate(
    template=image_prompt,
    input_variables=["current_scene", "previous_scenes", "dialogue"]
)

# Initialize LLM (not used in this version, but shown for reference)
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)
first_llm_chain = LLMChain(llm=llm, prompt=first_prompt)

print("done till now")

# Converts speaker + text into formatted dialogue
def speaker_text(input_dict):
    return f"{input_dict.get('speaker', '')}: {input_dict.get('text', '')}"

# Main processing function
def process_json2(json_output):
    pages = json_output.get("pages", []) 
    previous_summary = ""
    scene_summary_list = [] 
    output_list = []

    for page in pages:
        panels = page.get("panels", []) 
        panel_no = 1
        page_output_list = []

        for panel in panels:
            scene_desc = panel.get("scene")
            image_path = ""

            if scene_desc:
                dialogue = panel.get("dialogue", {})
                speaker = dialogue.get("speaker", "")
                text = dialogue.get("text", "")
                dialogue_line = f"{speaker}: {text}"

                prompt_input = f"\nCurrent Scene: {scene_desc} \nPrevious Scene's Summary: {previous_summary}\nCharacter Dialogue: {dialogue_line}"

                tries = 0
                while tries < 2:
                    try:
                        response = client.chat.completions.create( 
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": image_prompt + prompt_input}],
                            temperature=0.95
                        )
                        break
                    except Exception as e:
                        print(f"Error during generation: {e}")
                        tries += 1
                else:
                    continue  # Skip this panel if generation fails

                try:
                    img_prompt_raw = extract_json(response.choices[0].message.content)
                    if not img_prompt_raw:
                        print("No JSON found in the model response.")
                        continue  # Skip this panel if JSON is missing
                    try:
                        img_json = json.loads(img_prompt_raw)
                    except json.JSONDecodeError as e:
                        print(f"Failed to decode JSON: {e}")
                        continue
                    scene_description = img_json.get('scene_description', 'No description provided')
                    summary = img_json.get('summary', 'No summary provided')
                except Exception as e:
                    print(f"Error parsing JSON: {e}")
                    continue

                scene_summary_list.append({
                    'scene': scene_description,
                    'summary': summary
                })

                image_path = f"page_{page['page_number']}_panel_{panel_no}"
                full_prompt = "Generate an image based on this scene description: " + scene_description
                print(full_prompt)
                #image_gen(full_prompt, image_path)
                previous_summary = summary

            panel_output = {
                "panel_number": panel_no,
                "dialogue": panel.get('dialogue', {}),
                "image_path": image_path
            }
            page_output_list.append(panel_output)
            panel_no += 1

        output_list.append(page_output_list)

    print(output_list)
    return scene_summary_list

#Example usage (uncomment and provide valid JSON to test):
with open("backend/comic_story_4.json", "r") as file:
     json_output = json.load(file)
scenes_summaries = process_json2(json_output)
print(scenes_summaries)
