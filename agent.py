import os
import pathlib

from google import genai
from google.adk.agents import Agent
from google.adk.tools import load_artifacts  # type: ignore

from .common.llm import GeminiWithLocation
from .common.utils import load_prompt
from .config import config
from .tools import (
    get_current_date_time,
    publish_file,
    render_html,
    submit_feedback,
    scan_video_for_privacy_violations,
    generate_compliance_report,
)

# ---------------------------------------------------------------------------
# Videonymizer Compliance Agent (Root)
# ---------------------------------------------------------------------------

skills = []

videonymizer_agent = Agent(
    model=GeminiWithLocation(
        model=config.agent_settings.model, location=config.GOOGLE_GENAI_LOCATION
    ),
    name="videonymizer",
    description="Agent for student video PII identification and compliance scrubbing",
    instruction=load_prompt(os.path.dirname(__file__), "youtube_agent.txt"),
    sub_agents=[],
    tools=[
        get_current_date_time,
        publish_file,
        render_html,
        submit_feedback,
        load_artifacts,
        scan_video_for_privacy_violations,
        generate_compliance_report,
    ],
    generate_content_config=genai.types.GenerateContentConfig(
        max_output_tokens=config.YOUTUBE_AGENT_MAX_OUTPUT_TOKENS,
    ),
)

root_agent = videonymizer_agent

from google.adk.apps import App

app = App(root_agent=root_agent, name="videonymizer")