from quart import Quart, render_template, request, jsonify
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import random
import asyncio
import time
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

emergency_task = None
start_time = None

app = Quart(__name__)

client = OpenAI()

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_ENDPOINT"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

# Initialize SentenceTransformer
encoder = SentenceTransformer("all-MiniLM-L6-v2")

# Constants
COLLECTION_NAME = "emergencies"
CHOICES_COLLECTION = "choices"
RESPONSE_COLLECTION = "response"
RELEVANCE_THRESHOLD = 0.5


def get_user_intent(user_input):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are Dr. Aldrin’s reception bot, and your task is to tell what is the intention of a user. The intention of the user can only be of the following format:
    “emergency” - User has an emergency
    “message” - User just wants to send a message
    “NOTA” - None of the above intentions

    **Instructions**
    1. Your output should be only be in a specified JSON format only.
    2. You can only fill the intentions that have been mentioned and no other intentions

    **Output Format**
    {
        “intent”: “str”
    }
    """,
            },
            {"role": "user", "content": user_input},
        ],
        response_format={"type": "json_object"},
    )

    output = json.loads(completion.choices[0].message.content)
    return output["intent"]


async def get_emergency_instruction(user_input):
    # Simulate delay
    await asyncio.sleep(15)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are Dr. Aldrin’s reception bot, and your task is to identify if the user input is a medical emergency and
        tell the user what the immediate next steps are and how can they help themselves or the other person given a medical emergency.
        
    **Instructions**
    1. Your output should be only be in a specified JSON format only.
    2. If it's not a medical emergency, set "emergency" = "False" and in "instructions" only tell them it's not a medical emergency that's it.

    **Output Format**
    {
        "emergency" : "str"
        “instructions”: "str"
    }
    """,
            },
            {"role": "user", "content": user_input},
        ],
        response_format={"type": "json_object"},
    )

    output = json.loads(completion.choices[0].message.content)
    return output
    # return


# def get_user_response(user_input):
#     hits = qdrant_client.query_points(
#         collection_name=RESPONSE_COLLECTION,
#         query=encoder.encode(user_input).tolist(),
#         limit=1,
#     ).points

#     if hits and hits[0].score >= RELEVANCE_THRESHOLD:
#         if hits[0].payload["instruction"] == "too late":
#             return "too late"
#     return "unknown"


def get_user_response(user_input):
    # Step 1: Determine the intent of the first input
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are Dr. Aldrin’s reception bot, and your task is to identify the types of user input and reply appropriately.
                                             
            **Instructions**
            1. Your output should be only be in a specified JSON format only.
            2. If the user says the arrival time of the doctor is too late, your response should be too late 
            3. If user_input_1 is something different reply back asking them not to worry and that Dr. Adrin will be with them shortly
            **Output Format**
            {
                “response”: “str”
            }
            """,
            },
            {"role": "user", "content": user_input},
        ],
        response_format={"type": "json_object"},
    )

    output = json.loads(completion.choices[0].message.content)
    return output


# user_input2 = "We would suggest that you Call emergency services immediately (911 in the U.S.). If you or someone else is experiencing chest pain, difficulty breathing, or other symptoms of a heart attack, chew an aspirin (if not allergic) while waiting for help and remain calm. Do not leave the person alone and ensure they are in a comfortable position. "
# user_input1 = "oh my god that will be too late. ill die "


@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/chat", methods=["POST"])
async def chat():
    global emergency_task
    global start_time

    data = await request.json
    user_input = data["message"]
    flow_state = data["flowState"]
    emergency_description = data.get("emergencyDescription", "")

    if flow_state is None:
        user_intent = get_user_intent(user_input)
        if user_intent == "emergency":
            return jsonify(
                {"response": "What is your emergency?", "flowState": "emergency"}
            )
        elif user_intent == "message":
            return jsonify(
                {"response": "Please leave your message.", "flowState": "message"}
            )
        else:
            return jsonify(
                {
                    "response": "I'm sorry, I couldn't determine your intent. Could you please clarify?",
                    "flowState": None,
                }
            )

    elif flow_state == "emergency":
        # Start the emergency instruction task
        start_time = time.time()
        emergency_task = asyncio.create_task(get_emergency_instruction(user_input))

        # Immediately ask for location
        location_response = "I am checking what you should do immediately. Meanwhile, can you tell me which area you are located right now?"

        return jsonify(
            {
                "response": location_response,
                "flowState": "emergency_location",
                "emergencyDescription": user_input,
            }
        )

    elif flow_state == "emergency_location":
        # User has provided location, now we generate estimated time
        estimated_time = random.randint(5, 20)
        eta_response = f"Dr. Adrin will be coming to your location at {user_input} immediately. Estimated time of arrival: {estimated_time} minutes."

        # if emergency_task.done():
        #     emergency_instruction = await emergency_task
        #     instruction = emergency_instruction['instruction']
        #     if instruction == "I didn't get that, can you please repeat?":
        #         return jsonify({
        #     "response": "I didn't get that, can you please repeat? \n What is your emergency",
        #     "flowState": "emergency"
        # })

        #     time_executed = time.time() - start_time
        #     delay = max(0, 15 - time_executed + 3)
        #     eta_response += f"\n\n We would suggest that you {instruction} Don't worry, please follow these steps, Dr. Adrin will be with you shortly."
        #     return jsonify({
        #         "response": eta_response,
        #         "flowState": "emergency_eta",
        #         "emergencyDescription": emergency_description,
        #         "estimatedTime": estimated_time
        #     })

        # time_executed = time.time() - start_time
        # delay = max(0, 15 - time_executed + 3)
        # return jsonify({
        #     "response": eta_response,
        #     "flowState": "emergency_eta",
        #     "emergencyDescription": emergency_description,
        #     "estimatedTime": estimated_time,
        #     "recall_delay": delay
        # })

        ###
        if emergency_task.done():
            emergency_instruction = await emergency_task
            if emergency_instruction["emergency"] == "False":

                return jsonify(
                    {
                        "response": emergency_instruction["instructions"],
                        "flowState": None,  ###
                    }
                )
            else:
                eta_response += f"\n\n We would suggest that you {emergency_instruction['instructions']} Don't worry, please follow these steps, Dr. Adrin will be with you shortly."
                return jsonify(
                    {
                        "response": eta_response,
                        "flowState": "emergency_eta",
                        "emergencyDescription": emergency_description,
                        "estimatedTime": estimated_time,
                    }
                )

        time_executed = time.time() - start_time
        delay = max(0, 15 - time_executed + 3)
        return jsonify(
            {
                "response": eta_response,
                "flowState": "emergency_eta",
                "emergencyDescription": emergency_description,
                "estimatedTime": estimated_time,
                "recall_delay": delay,
            }
        )

    # elif flow_state == "emergency_eta":
    #     if get_user_response(user_input) == "too late":           ##########
    #         # Attempt to retrieve the emergency instruction
    #         try:
    #             if emergency_task.done():
    #                 emergency_instruction = await emergency_task
    #                 if not emergency_instruction["emergency"]:
    #                     return jsonify({
    #                     "response": emergency_instruction["instructions"],
    #                     "flowState": "emergency"
    #                 })
    #                 full_response = f"I understand that you are worried that Dr. Adrin will arrive too late. Meanwhile, we would suggest that you {emergency_instruction['instructions']} Don't worry, please follow these steps, Dr. Adrin will be with you shortly."
    #                 return jsonify({
    #                     "response": full_response,
    #                     "flowState": None
    #                 })

    #             else:
    #                 time_executed = time.time() - start_time
    #                 delay = max(0, 15 - time_executed + 3)  # calculate the delay for the next API call

    #                 full_response = "I apologize, I'm still preparing the best steps for you to follow. Please stay on the line, and I'll provide instructions as soon as possible."
    #                 return jsonify({
    #                     "response": full_response,
    #                     "flowState": "emergency_eta",
    #                     "time_executed": time_executed,
    #                     "recall_delay": delay
    #                 })

    #         except asyncio.TimeoutError:
    #             full_response = "I apologize, I'm still preparing the best steps for you to follow. Please stay on the line, and I'll provide instructions as soon as possible."

    #     elif user_input == "":
    #         if emergency_task.done():
    #             emergency_instruction = await emergency_task
    #             instruction = emergency_instruction['instruction']
    #             response = f"We would suggest that you {instruction} Don't worry, please follow these steps, Dr. Adrin will be with you shortly."
    #             return jsonify({
    #                 "response": response,
    #                 "flowState": "emergency_eta",
    #                 "emergencyDescription": emergency_description
    #             })
    #     else:
    #         return jsonify({"response": "Don’t worry, please follow these steps, Dr. Adrin will be with you shortly",
    #                 "flowState": None,
    #             })

    elif flow_state == "emergency_eta":
        output = get_user_response(user_input)
        if output["response"] == "too late":  ##########
            # Attempt to retrieve the emergency instruction
            try:
                if emergency_task.done():
                    emergency_instruction = await emergency_task
                    if emergency_instruction["emergency"] == "False":
                        return jsonify(
                            {
                                "response": emergency_instruction["instructions"],
                                "flowState": None,
                            }
                        )
                    else:
                        full_response = f"I understand that you are worried that Dr. Adrin will arrive too late. Meanwhile, we would suggest that you {emergency_instruction['instructions']} Don't worry, please follow these steps, Dr. Adrin will be with you shortly."
                        return jsonify({"response": full_response, "flowState": None})

                else:
                    time_executed = time.time() - start_time
                    delay = max(
                        0, 15 - time_executed + 3
                    )  # calculate the delay for the next API call

                    full_response = "I apologize, I'm still preparing the best steps for you to follow. Please stay on the line, and I'll provide instructions as soon as possible."
                    return jsonify(
                        {
                            "response": full_response,
                            "flowState": "emergency_eta",
                            "time_executed": time_executed,
                            "recall_delay": delay,
                            "late": "too late",  ###
                        }
                    )

            except asyncio.TimeoutError:
                full_response = "I apologize, I'm still preparing the best steps for you to follow. Please stay on the line, and I'll provide instructions as soon as possible."

        elif user_input == "":
            if emergency_task.done():
                emergency_instruction = await emergency_task
                if emergency_instruction["emergency"] == "False":
                    return jsonify(
                        {
                            "response": emergency_instruction["instructions"],
                            "flowState": None,
                        }
                    )
                else:
                    response = f"We would suggest that you {emergency_instruction['instructions']} Don't worry, please follow these steps, Dr. Adrin will be with you shortly."
                    return jsonify(
                        {
                            "response": response,
                            "flowState": "emergency_eta",
                            "emergencyDescription": emergency_description,
                        }
                    )
        else:
            return jsonify(
                {
                    "response": output["response"],
                    "flowState": None,
                }
            )

    elif flow_state == "message":
        return jsonify(
            {
                "response": "Thank you for your message. We will forward it to Dr. Adrin.",
                "flowState": None,
            }
        )

    else:
        return jsonify(
            {
                "response": "I don't understand that. Could you please clarify?",
                "flowState": None,
            }
        )


if __name__ == "__main__":
    app.run(debug=True)
