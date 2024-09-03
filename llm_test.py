from openai import OpenAI
from dotenv import load_dotenv
import json 

load_dotenv()

client = OpenAI()

# completion = client.chat.completions.create(
#   model="gpt-4o-mini",
#   messages=[
#     {"role": "system", "content": """You are Dr. Aldrin’s reception bot, and your task is to identify if the user input is a medical emergency and
#      tell the user what the immediate next steps are and how can they help themselves or the other person given a medical emergency.
     
# **Instructions**
# 1. Your output should be only be in a specified JSON format only.
# 2. If it's not a medical emergency, set "emergency" = "False" and in "instructions" only tell them it's not a medical emergency that's it.

# **Output Format**
# {
#     "emergency" : "bool"
# 	“instructions”: "str"
# }
# """},
#     {"role": "user", "content": "I cant breathe"}
#   ], 
#   response_format={"type":"json_object"}
# )

# output = json.loads(completion.choices[0].message.content)
# print(output["emergency"])
# print(output["instructions"])


def get_user_response(user_input_1, user_input_2):
    # Step 1: Determine the intent of the first input
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are Dr. Aldrin’s reception bot, and your task is to identify the types of user input and reply appropriately.
                                             
            **Instructions**
            1. Your output should be only be in a specified JSON format only.
            2. If the user says the arrival time of the doctor is too late, your response should be too late 
            3. If user_input_1 is something different reply back asking them not to worry and that Dr. Adrin will be with them shortly
            **Output Format**
            {
                “response”: “str”
            }
            """},
            {"role": "user", "content": user_input_1}
        ], 
        response_format={"type":"json_object"}
    )

    output = json.loads(completion.choices[0].message.content)
    return output 

user_input2 = "We would suggest that you Call emergency services immediately (911 in the U.S.). If you or someone else is experiencing chest pain, difficulty breathing, or other symptoms of a heart attack, chew an aspirin (if not allergic) while waiting for help and remain calm. Do not leave the person alone and ensure they are in a comfortable position. "
user_input1 = "oh my god that will be too late. ill die "

output = get_user_response(user_input1, user_input2)
print(output["response"])