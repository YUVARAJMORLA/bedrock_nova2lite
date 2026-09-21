import boto3
from botocore.config import Config

# --------------------------------------------------
# Bedrock Runtime Client
# --------------------------------------------------

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    config=Config(
        read_timeout=3600
    )
)

# --------------------------------------------------
# Model
# --------------------------------------------------

MODEL_ID = (
    "arn:aws:bedrock:us-east-1:776817040428:"
    "inference-profile/global.amazon.nova-2-lite-v1:0"
)

# --------------------------------------------------
# Conversation History
# --------------------------------------------------

messages = []

print("=" * 60)
print("        Amazon Nova 2 Lite - Terminal Chat")
print("=" * 60)
print("Type your question and press Enter.")
print("Type 'exit' to stop the conversation.")
print("=" * 60)

# --------------------------------------------------
# Continuous Conversation
# --------------------------------------------------

while True:

    try:
        user_prompt = input("\nYou: ").strip()

        # Exit command
        if user_prompt.lower() == "exit":
            print("\nConversation ended.")
            break

        # Ignore empty input
        if not user_prompt:
            continue

        # Add user message to conversation history
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "text": user_prompt
                    }
                ]
            }
        )

        # --------------------------------------------------
        # Call Amazon Nova 2 Lite using Converse API
        # --------------------------------------------------

        response = bedrock.converse(
            modelId=MODEL_ID,

            messages=messages,

            inferenceConfig={
                "maxTokens": 10000,
                "stopSequences": [],
                "temperature": 1
            },

            additionalModelRequestFields={
                "reasoningConfig": {
                    "type": "enabled",
                    "maxReasoningEffort": "low"
                }
            },

            performanceConfig={
                "latency": "standard"
            }
        )

        # --------------------------------------------------
        # Extract assistant response
        # --------------------------------------------------

        assistant_message = response["output"]["message"]

        assistant_text = ""

        for content in assistant_message["content"]:
            if "text" in content:
                assistant_text += content["text"]

        print("\nNova 2 Lite:")
        print(assistant_text)

        # --------------------------------------------------
        # Add Nova's response to conversation history
        # --------------------------------------------------

        messages.append(
            {
                "role": "assistant",
                "content": [
                    {
                        "text": assistant_text
                    }
                ]
            }
        )

    except KeyboardInterrupt:
        print("\n\nConversation ended.")
        break

    except Exception as e:
        print("\nError:", e)