EXTRACTION_PROMPT = """
You are an AI assistant. Your job is to convert a candidate's unstructured profile text into a structured JSON format.

Here is the unstructured profile:
{profile}

Your job:
- Read the profile and fill out each field in the EnhancedProfile format below.
- If some fields are not available, leave them empty.
- DO NOT fabricate or add information.
- Maintain all tech/tool names exactly as they appear in the profile but kindly correct any typos.
- Fix any typos in the tech/tool names.

{format_instructions}
"""

# ======= Prompt for Step 2: Enhance with JD =========

JD_ENHANCEMENT_PROMPT = """
You are an AI assistant that enhances software developer profiles based on job descriptions.

Job Description:
{jd}

Candidate Structured Profile:
{profile}

🧠 GENERAL RULES:
- Do not invent experience. Only extrapolate from the candidate's context.
- Maintain the structure, tone, and approximate length of the original profile.
- Only include additional technologies/tools that are mentioned in the JD but not in the profile — and integrate them naturally.
- Do NOT remove any content from the original profile.
- Skills must be behavioral only, may be you can look few keywords from profile and use the synonyms of them restrict it to be less than 5 skills,
  no tech skills or tools.
- Add emerging or trending skills **only if explicitly mentioned or implied in the JD** and if **they align with the candidate's experience or project context**.
- Include at least 2 relevant emerging technologies or tools not explicitly listed in the JD only if they are a logical fit for the candidate’s responsibilities or project context.
- If the JD mentions total years of experience required, ensure that the summary section reflects that same number clearly and naturally, even if not explicitly present in the profile.
- Ensure that at least one tool or technology from the JD (not already in the profile) is included in the enhanced profile — only if its use can be reasonably aligned with the candidate's context or project responsibilities.

🎯 SUMMARY SECTION:
- Rephrase and enhance the summary to be more compelling and JD-aligned.
- Do NOT mention technologies or tools in the summary.
- Add emphasis on experience areas, responsibilities, and behavioral strengths relevant to the JD.

🧩 PROJECTS SECTION:
- For each project:
  For each project in the profile:

- From the candidate's projects, choose the **top 3 that are most closely aligned with the JD in terms of responsibilities, tools, or domain relevance**. If none align clearly, select **any 3** from the original profile.

- Rephrase and expand the **Description** to make it clearer, more impactful, and better aligned with the responsibilities and expectations outlined in the JD.

- Ensure the **Contribution** section is written in concise bullet points. Maintain the original intent and structure while enhancing clarity and relevance.

- In the **Tech Stack**, include any missing tools, technologies, languages, frameworks, or platforms mentioned in the JD — but only if they could reasonably have been used in the context of the project.

- In the **Contribution**, only include tools or skills from the JD if their application would be contextually appropriate for that project.
  - Do not add irrelevant JD tools/skills that don't logically fit the project's description nature or scope.
  - Only enhance with JD elements when there is a clear functional or thematic alignment.

Be realistic, and context-aware while enriching the project with JD-relevant content.

Your task is to enhance rephrase the profile based on the JD, ensuring that everything is relevant and aligned with the JD.

  FORMAT TO FOLLOW:

- Name: <Candidate Name>
- Role: <Candidate Role>
- Summary: <Rephrased summary>

- Technologies: (Add missing tech requirements from JD)
  Backend Technologies: <comma-separated list>
  Frontend Technologies: <comma-separated list>
  Database: <comma-separated list>
  Tools: <comma-separated list>
  Programming Languages: <comma-separated list>
  AI Tools: <comma-separated list>

- Skills (Behavioral only from the JD and from the profile, no tech skills or tools):
  - Skill 1
  - Skill 2
  - ...

- Projects:
  1. Title: <Project Title>
     Tech Stack: <List of technologies/tools used, including JD-aligned additions>
     Description: <Expanded description aligned with JD, same length as original, try to have it in 3-5 lines>
     Contribution: (Try to have it in 3-5 lines)
     - Responsibility or contribution 1
     - Responsibility or contribution 2
     - ...
     
  2. Title: ...
     Tech Stack: ...
     Description: ...
     Contribution:
     - ...
     - ...

🧱 STRUCTURED FORMAT (MANDATORY):
{format_instructions}
"""
