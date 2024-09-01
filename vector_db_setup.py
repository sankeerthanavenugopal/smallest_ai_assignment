from qdrant_client import QdrantClient, models
# from qdrant_client.http.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer("all-MiniLM-L6-v2")

qdrant_client = QdrantClient(
    url="d1773b90-f023-4e35-8df1-68355e8887f0.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="98tDhIEfYGWJekoOLQuio2h6TfPQEn_zAm56H98L6ZJwLNjx1DAdXA",
)

# collection_name = "emergencies"
# qdrant_client.create_collection(
#     collection_name=collection_name,
#     vectors_config=models.VectorParams(size=encoder.get_sentence_embedding_dimension(),  # Vector size is defined by used model
#         distance=models.Distance.COSINE,
#     ),
# )

# emergency_instructions_list = [
#     {
#         "scenario": "patient is not breathing at all",
#         "instruction": "Perform CPR immediately. Start by placing your hands in the center of the chest and pressing hard and fast, at a rate of 100-120 compressions per minute. If trained, give rescue breaths after every 30 compressions. Continue until emergency services arrive."
#     },
#     {
#         "scenario": "person is unconscious and not breathing",
#         "instruction": "Perform CPR immediately. Place the person on their back, interlock your fingers, and press hard and fast on the center of the chest. If trained, give two rescue breaths after every 30 compressions. Keep going until help arrives."
#     },
#     {
#         "scenario": "someone has stopped breathing and needs help",
#         "instruction": "Administer CPR right away. Begin chest compressions by placing the heel of your hand on the center of the chest and pressing down at least 2 inches deep. Give 30 compressions followed by 2 rescue breaths if possible."
#     },
#     {
#         "scenario": "severe bleeding from a wound",
#         "instruction": "Apply firm, direct pressure to the wound using a clean cloth or bandage. If the bleeding doesn’t stop, apply more cloths or bandages and press harder. Keep the wound elevated if possible, and seek medical attention immediately."
#     },
#     {
#         "scenario": "bleeding from a deep cut",
#         "instruction": "Cover the cut with a sterile cloth and press down hard to stop the bleeding. If the bleeding continues, add more cloths on top without removing the initial one and maintain pressure. Get medical help as quickly as possible."
#     },
#     {
#         "scenario": "massive bleeding from an injury",
#         "instruction": "Immediately cover the wound with a clean cloth and apply as much pressure as you can. If possible, tie a bandage or cloth around the wound to maintain pressure and keep the injured part elevated above the heart level. Call for emergency medical services right away."
#     },
#     {
#         "scenario": "heavy bleeding that won't stop",
#         "instruction": "Keep pressing on the wound with a cloth or your hand, and do not remove any bandages even if they become soaked with blood. Elevate the injured area if you can, and get emergency medical assistance immediately."
#     },
#     {
#         "scenario": "person is choking and can't breathe",
#         "instruction": "Perform the Heimlich maneuver. Stand behind the person, wrap your arms around their waist, and make a fist with one hand. Place the thumb side of your fist just above the navel, grab it with your other hand, and thrust inward and upward sharply. Repeat until the object is expelled."
#     },
#     {
#         "scenario": "someone is choking on food",
#         "instruction": "Quickly do the Heimlich maneuver: stand behind them, wrap your arms around their waist, and pull sharply inward and upward just above their belly button. Continue until the blockage is cleared and the person can breathe again."
#     },
#     {
#         "scenario": "person has severe chest pain",
#         "instruction": "This could be a heart attack. Call emergency services immediately. If the person is conscious, have them sit down and rest while waiting for help. If they are not allergic, give them an aspirin to chew slowly. Monitor them closely and be prepared to perform CPR if they lose consciousness."
#     },
#     {
#         "scenario": "someone is having a heart attack",
#         "instruction": "Call emergency services right away. While waiting, help the person to sit down and remain calm. If they are not allergic, they should chew an aspirin slowly. Keep them calm and monitor their condition until help arrives. If they stop breathing, be prepared to start CPR."
#     },
#     {
#         "scenario": "person has lost consciousness suddenly",
#         "instruction": "Check if they are breathing and have a pulse. If they are not breathing, start CPR immediately. If they are breathing, place them in the recovery position (on their side with the head tilted slightly back) and call for emergency help. Monitor their condition until help arrives."
#     },
#     {
#         "scenario": "someone fainted and is unresponsive",
#         "instruction": "Quickly check their breathing and pulse. If there is no breathing or pulse, begin CPR immediately. If they are breathing, roll them onto their side and keep their airway clear. Call emergency services and stay with the person until they arrive."
#     },
#     {
#         "scenario": "person has a seizure",
#         "instruction": "Do not try to restrain them. Move any dangerous objects out of the way and place something soft under their head. Once the seizure stops, turn them onto their side to help keep their airway clear. Stay with them until they fully regain consciousness and seek medical advice."
#     },
#     {
#         "scenario": "someone is having a seizure",
#         "instruction": "Clear the area around them to prevent injury, but do not hold them down. Place a soft object under their head to protect it. After the seizure ends, gently roll them onto their side to keep their airway open. Stay with them until they are fully awake and aware."
#     },
#     {
#         "scenario": "person is severely burned",
#         "instruction": "Immediately cool the burn by running it under cool (not cold) water for at least 10 minutes. Do not apply ice, as it can damage the tissue further. Cover the burn with a sterile, non-stick dressing or a clean cloth. Seek emergency medical care as soon as possible."
#     },
#     {
#         "scenario": "severe burn injury",
#         "instruction": "Cool the burn with cool running water for at least 10-15 minutes. Avoid using ice or very cold water. Cover the burn loosely with a sterile dressing or a clean cloth. Do not apply creams or ointments. Seek emergency medical attention immediately."
#     },
#     {
#         "scenario": "someone has ingested poison",
#         "instruction": "Call poison control immediately for specific advice. Do not induce vomiting unless instructed by a medical professional. Keep the person calm and monitor their symptoms closely. If they start having difficulty breathing or lose consciousness, call emergency services right away."
#     },
#     {
#         "scenario": "person has swallowed a toxic substance",
#         "instruction": "Immediately contact poison control for guidance. Do not make the person vomit unless advised by a medical professional. Keep them calm and avoid giving them anything to eat or drink until you have further instructions. If they show severe symptoms, call emergency services immediately."
#     }
# ]

# qdrant_client.upload_points(
#     collection_name=collection_name,
#     points=[
#         models.PointStruct(
#             id=idx, vector=encoder.encode(instructions["scenario"]).tolist(), payload=instructions
#         )
#         for idx, instructions in enumerate(emergency_instructions_list)
#     ],
# )

from qdrant_client.http.models import Distance, VectorParams, PointStruct

# collection_name_choices = "choices"

# qdrant_client.create_collection(
#     collection_name=collection_name_choices,
#     vectors_config=models.VectorParams(size=encoder.get_sentence_embedding_dimension(), distance=Distance.COSINE),
# )

# # Insert the two choices into Qdrant
# choices =  [{
#         "scenario": "I would like to leave a message",
#         "instruction": "Please leave a message"
#     },
#     {
#         "scenario": "I have an emergency",
#         "instruction": "What's your emergency?"
#     }]

# qdrant_client.upload_points(
#     collection_name=collection_name_choices,
#     points=[
#         models.PointStruct(
#             id=idx, vector=encoder.encode(instructions["scenario"]).tolist(), payload=instructions
#         )
#         for idx, instructions in enumerate(choices)
#     ],
# )

collection_name_response = "response"

qdrant_client.create_collection(
    collection_name=collection_name_response,
    vectors_config=models.VectorParams(size=encoder.get_sentence_embedding_dimension(), distance=Distance.COSINE),
)

response = [{
        "scenario": "The arrival will be too late",
        "instruction": "too late"
    }
    ]


qdrant_client.upload_points(
    collection_name=collection_name_response,
    points=[
        models.PointStruct(
            id=idx, vector=encoder.encode(instructions["scenario"]).tolist(), payload=instructions
        )
        for idx, instructions in enumerate(response)
    ],
)