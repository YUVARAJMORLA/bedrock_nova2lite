import streamlit as st
import boto3
from botocore.config import Config


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nova 2 Lite Chat",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# BEDROCK CONFIGURATION
# ============================================================

MODEL_ID = (
    "arn:aws:bedrock:us-east-1:776817040428:"
    "inference-profile/global.amazon.nova-2-lite-v1:0"
)

REGION = "us-east-1"


# ============================================================
# BEDROCK CLIENT
# ============================================================

@st.cache_resource
def get_bedrock_client():

    return boto3.client(
        "bedrock-runtime",
        region_name=REGION,
        config=Config(
            read_timeout=3600
        )
    )


bedrock = get_bedrock_client()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# HEADER
# ============================================================

st.title("🤖 Nova 2 Lite Chat")

st.caption(
    "Amazon Nova 2 Lite • AWS Bedrock Converse API"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Settings")

    st.write("**Model**")
    st.code("Nova 2 Lite")

    st.write("**Region**")
    st.code(REGION)

    st.write("**Reasoning**")
    st.code("Low")

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# DISPLAY CONVERSATION HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["text"])


# ============================================================
# INPUT AREA
# ============================================================

st.divider()

question = st.text_area(
    "Ask Nova 2 Lite",
    placeholder="Type your question here...",
    height=120
)


# ============================================================
# BUTTONS
# ============================================================

col1, col2 = st.columns([3, 1])

with col1:

    submit = st.button(
        "🚀 Submit",
        type="primary",
        use_container_width=True
    )

with col2:

    clear = st.button(
        "🗑️ Clear",
        use_container_width=True
    )


# ============================================================
# CLEAR BUTTON
# ============================================================

if clear:

    st.session_state.messages = []
    st.rerun()


# ============================================================
# SUBMIT QUESTION
# ============================================================

if submit:

    question = question.strip()

    if not question:

        st.warning("Please enter a question.")

    else:

        # ----------------------------------------------------
        # Display user question
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "text": question
            }
        )

        # ----------------------------------------------------
        # Build Converse API messages
        # ----------------------------------------------------

        converse_messages = []

        for message in st.session_state.messages:

            converse_messages.append(
                {
                    "role": message["role"],
                    "content": [
                        {
                            "text": message["text"]
                        }
                    ]
                }
            )

        # ----------------------------------------------------
        # Call Nova
        # ----------------------------------------------------

        with st.spinner("Nova 2 Lite is thinking..."):

            try:

                response = bedrock.converse(

                    modelId=MODEL_ID,

                    messages=converse_messages,

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

                # ------------------------------------------------
                # Extract response
                # ------------------------------------------------

                assistant_message = response[
                    "output"
                ][
                    "message"
                ]

                assistant_text = ""

                for content in assistant_message["content"]:

                    if "text" in content:

                        assistant_text += content["text"]


                # ------------------------------------------------
                # Store assistant response
                # ------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "text": assistant_text
                    }
                )

                # ------------------------------------------------
                # Refresh UI
                # ------------------------------------------------

                st.rerun()

            except Exception as e:

                st.error(
                    f"Error communicating with Amazon Bedrock:\n\n{str(e)}"
                )