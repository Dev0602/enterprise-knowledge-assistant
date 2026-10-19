import streamlit as st

from src.rag_pipeline import RAGPipeline


# -----------------------------------------
# Page configuration
# -----------------------------------------

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    layout="centered",
)


# -----------------------------------------
# Title
# -----------------------------------------

st.title("Enterprise Knowledge Assistant")

st.caption(
    "Ask questions about company policies "
    "and internal documents."
)


# -----------------------------------------
# Create RAG pipeline
# -----------------------------------------

@st.cache_resource
def load_rag_pipeline():
    return RAGPipeline(n_results=3)


rag = load_rag_pipeline()


# -----------------------------------------
# Store chat history
# -----------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------------------
# Display previous messages
# -----------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        # -----------------------------------------
        # Sources
        # -----------------------------------------

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            with st.expander("Sources"):

                source_details = message.get(
                    "source_details",
                    []
                )

                if source_details:

                    for detail in source_details:

                        source = detail["source"]
                        page_number = detail.get(
                            "page_number"
                        )
                        passage = detail.get(
                            "passage",
                            ""
                        )

                        if page_number:
                            st.markdown(
                                f"**{source} — Page {page_number}**"
                            )
                        else:
                            st.markdown(
                                f"**{source}**"
                            )

                        if passage:
                            st.caption(passage)

                else:

                    for source in message["sources"]:
                        st.write(f"- {source}")

        # -----------------------------------------
        # Grounding status
        # -----------------------------------------

        if (
            message["role"] == "assistant"
            and message.get("grounding")
        ):

            verdict = message["grounding"]["verdict"]

            if verdict == "SUPPORTED":
                st.success("Answer grounded in company information.")

            elif verdict == "ABSTENTION":
                st.warning(
                    "Information not found in the knowledge base."
                )

            else:
                st.error(
                    "Answer could not be verified against the knowledge base."
                )


# -----------------------------------------
# Chat input
# -----------------------------------------

question = st.chat_input(
    "Ask a question about your company documents..."
)


# -----------------------------------------
# Process question
# -----------------------------------------

if question:

    # -----------------------------------------
    # Display user question
    # -----------------------------------------

    with st.chat_message("user"):
        st.write(question)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # -----------------------------------------
    # Generate answer
    # -----------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching the knowledge base..."
        ):

            result = rag.ask(question)

        answer = result["answer"]
        sources = result["sources"]
        source_details = result.get(
            "source_details",
            []
        )
        grounding = result["grounding"]

        # -----------------------------------------
        # Display answer
        # -----------------------------------------

        st.write(answer)

        # -----------------------------------------
        # Display grounding status
        # -----------------------------------------

        verdict = grounding["verdict"]

        if verdict == "SUPPORTED":

            st.success(
                "Answer grounded in company information."
            )

        elif verdict == "ABSTENTION":

            st.warning(
                "Information not found in the knowledge base."
            )

        else:

            st.error(
                "Answer could not be verified against the knowledge base."
            )

        # -----------------------------------------
        # Display sources
        # -----------------------------------------

        if sources:

            with st.expander("Sources"):

                if source_details:

                    for detail in source_details:

                        source = detail["source"]
                        page_number = detail.get(
                            "page_number"
                        )
                        passage = detail.get(
                            "passage",
                            ""
                        )

                        if page_number:
                            st.markdown(
                                f"**{source} — Page {page_number}**"
                            )
                        else:
                            st.markdown(
                                f"**{source}**"
                            )

                        if passage:
                            st.caption(passage)

                else:

                    for source in sources:
                        st.write(f"- {source}")

    # -----------------------------------------
    # Save assistant message
    # -----------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "source_details": source_details,
            "grounding": grounding,
        }
    )