from google import genai
from google.genai.types import GenerateContentConfig, Modality
from PIL import Image
from io import BytesIO

# -----------------------------------
# 1. Create Gemini client
# -----------------------------------
client = genai.Client(api_key="AQ.Ab8RN6LHEbzX-W-rcSTk-Xfpky72SOuoG3LAI6NgnBnPPXpWvg")

# -----------------------------------
# 2. Input image
# -----------------------------------
image_path = "stone.png"
input_image = Image.open(r'C:\Users\i-bhakti.patel\Desktop\image.py\necklec.png')

# -----------------------------------
# 3. Get dynamic instruction
# -----------------------------------
user_instruction = input(
    "What gemstone changes do you want? "
)

# -----------------------------------
# 4. Create strong editing prompt
# -----------------------------------
prompt = f"""
You are a professional jewellery image editor.
EDIT THE PROVIDED JEWELLERY IMAGE ACCORDING TO THE USER'S INSTRUCTION.

USER INSTRUCTION:
{user_instruction}

VERY IMPORTANT RULES:
1. Change ONLY the gemstones mentioned in the user's instruction.
2. Do NOT redesign the jewellery.
3. Do NOT change the metal.
4. Do NOT change the jewellery shape or structure.
5. Do NOT change the number of stones.
6. Do NOT move any stone.
7. Do NOT change stone sizes or cuts unless explicitly requested.
8. Keep all settings, prongs, bezels and mountings unchanged.
9. Preserve the original camera angle and composition.
10. Preserve the original background.
11. Preserve realistic lighting, reflections and shadows.
12. Every gemstone that is NOT requested to change must remain unchanged.
13. If multiple stones match the user's description, apply the requested
    change to ALL matching stones.
14. If the user specifies a particular stone such as center, middle,
    left, right, first, second, third, etc., identify that stone from
    its position in the image.
15. Make the replacement gemstones look physically realistic and
    naturally mounted in the existing jewellery.

The final image must look like the ORIGINAL jewellery photograph,
with ONLY the requested gemstone changes applied.
Do not create a new jewellery design.
"""

# -----------------------------------
# 5. Send image + dynamic instruction
# -----------------------------------
response = client.models.generate_content(
    model="gemini-3.1-flash-image",
    contents=[prompt, input_image],
    config=GenerateContentConfig(
        response_modalities=[Modality.TEXT, Modality.IMAGE],
    ),
)

# -----------------------------------
# 6. Save result
# -----------------------------------
output_path = "edited_stone.png"
saved = False

for part in response.candidates[0].content.parts:
    if part.text:
        print("Model note:", part.text)
    elif part.inline_data:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save(output_path)
        saved = True

if saved:
    print(f"Done! Output saved to: {output_path}")
else:
    print("No image was returned. Check the model response/prompt.")