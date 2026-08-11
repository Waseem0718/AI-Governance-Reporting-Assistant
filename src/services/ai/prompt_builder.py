class PromptBuilder:
    """
    Converts AI Context into an LLM prompt.
    """

    SYSTEM_PROMPT = """
You are an AI Governance Reporting Assistant.

Your task is to summarize software development activities for governance meetings.

Guidelines:

- Write in professional business language.
- Focus only on important business changes.
- Ignore repetitive stable periods.
- Mention releases, APIs, migrations, infrastructure and business features.
- Do not invent information.
- Keep the summary concise.
"""

    @classmethod
    def build(cls, context):

        user_prompt = ""

        user_prompt += cls._build_topic(context)

        user_prompt += cls._build_timeline(context)

        user_prompt += cls._build_story(context)

        user_prompt += cls._build_current_state(context)

        user_prompt += cls._build_milestones(context)

        user_prompt += """

Based ONLY on the information provided above:

Generate a governance report with the following sections.

1. Executive Summary
   - Overall progress in 2-3 sentences.

2. Key Developments
   - Mention all releases, APIs, business features,
     migrations and infrastructure changes.
   - Do not omit any release.

3. Current State
   - Summarize the latest business state.

4. Risks
   - Mention only if any risk is evident from the supplied information.
   - Otherwise write "No risks identified."

5. Next Expected Activities
   - Infer only from the development timeline.
   - Do not invent future work.
"""

        return {

            "system": cls.SYSTEM_PROMPT.strip(),

            "user": user_prompt.strip()

        }

    @staticmethod
    def _build_topic(context):

        return f"""
Topic

{context["topic"]}

"""

    @staticmethod
    def _build_timeline(context):

        summary = context["timeline_summary"]

        return f"""
Timeline Summary

Duration:
{summary["start_date"]} to {summary["end_date"]}

Business Changes:
{summary["business_changes"]}

Stable Periods:
{summary["stable_periods"]}

Current Status:
{summary["current_status"]}

Environment:
{summary["environment"]}

"""

    @staticmethod
    def _build_story(context):

        text = "Business Story\n\n"

        for line in context["business_story"]:
            text += f"- {line}\n"

        text += "\n"

        return text

    @staticmethod
    def _build_current_state(context):

        state = context["current_state"]

        text = "Current State\n\n"

        for key, value in state.items():
            text += f"{key}: {value}\n"

        text += "\n"

        return text

    @staticmethod
    def _build_milestones(context):

        text = "Business Milestones\n\n"

        for milestone in context["business_milestones"]:
            text += f"- {milestone}\n"

        text += "\n"

        return text
    
        
    @classmethod
    def build_governance_prompt(cls, contexts):

        user_prompt = ""

        for context in contexts:

            user_prompt += "\n"
            user_prompt += "=" * 60
            user_prompt += "\n"

            user_prompt += cls._build_topic(context)

            user_prompt += cls._build_timeline(context)

            user_prompt += cls._build_story(context)

            user_prompt += cls._build_current_state(context)

            user_prompt += cls._build_milestones(context)

        user_prompt += """

Based ONLY on the information provided above.

Generate ONE consolidated monthly governance report.

STRICT RULES

1. Use ONLY the supplied information.
2. Do NOT invent releases, risks, deployments, migrations or future work.
3. If a release name appears in the supplied data, preserve the exact release name.
4. Mention ALL releases listed in the Current State or Business Milestones. Do not omit any release.
5. Mention APIs, integrations, technologies and infrastructure only if they appear in the supplied information.
6. If no risks are explicitly evident, write "No risks identified."
7. If next activities cannot be determined from the supplied timeline, write "No further planned activities identified."
8. Do not rewrite release names or abbreviate them.
9. Keep the report factual, concise and suitable for executive governance meetings.

Generate the report with the following sections:

1. Executive Summary
   - 2-3 concise paragraphs summarizing overall monthly progress.

2. Major Development Highlights
   - Mention all releases.
   - Mention APIs.
   - Mention business features.
   - Mention infrastructure changes.
   - Mention migrations if present.

3. Business Progress by Topic
   - Summarize each application/topic in 2-4 sentences.

4. Current Overall Delivery Status
   - Summarize the latest overall delivery state.

5. Risks
   - Mention only risks supported by the supplied information.
   - Otherwise write "No risks identified."

6. Next Planned Activities
   - Infer only from the supplied timeline.
   - Do not invent future work.
"""

        return {

            "system": cls.SYSTEM_PROMPT.strip(),

            "user": user_prompt.strip()

        }