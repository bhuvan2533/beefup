# EXTRACTION_PROMPT = """
# You are an AI assistant. Your job is to convert a candidate's unstructured profile text into a structured JSON format.

# Here is the unstructured profile:
# {profile}

# Your job:
# - Read the profile and fill out each field in the EnhancedProfile format below.
# - If some fields are not available, leave them empty.
# - DO NOT fabricate or add information.
# - Maintain all tech/tool names exactly as they appear in the profile but kindly correct any typos.
# - Fix any typos in the tech/tool names.

# {format_instructions}
# """

# # ======= Prompt for Step 2: Enhance with JD =========

# JD_ENHANCEMENT_PROMPT = """
# You are an AI assistant that enhances software developer profiles based on job descriptions.

# Job Description:
# {jd}

# Candidate Structured Profile:
# {profile}

# 🧠 GENERAL RULES:
# - Do not invent experience. Only extrapolate from the candidate's context.
# - Maintain the structure, tone, and approximate length of the original profile.
# - Only include additional technologies/tools that are mentioned in the JD but not in the profile — and integrate them naturally.
# - Do NOT remove any content from the original profile.
# - Skills must be behavioral only, may be you can look few keywords from profile and use the synonyms of them restrict it to be less than 5 skills,
#   no tech skills or tools.
# - Add emerging or trending skills **only if explicitly mentioned or implied in the JD** and if **they align with the candidate's experience or project context**.
# - Include at least 2 relevant emerging technologies or tools not explicitly listed in the JD only if they are a logical fit for the candidate's responsibilities or project context.
# - If the JD mentions total years of experience required, ensure that the summary section reflects that same number clearly and naturally, even if not explicitly present in the profile.
# - Ensure that at least one tool or technology from the JD (not already in the profile) is included in the enhanced profile — only if its use can be reasonably aligned with the candidate's context or project responsibilities.

# 🎯 SUMMARY SECTION:
# - Rephrase and enhance the summary to be more compelling and JD-aligned.
# - Do NOT mention technologies or tools in the summary.
# - Add emphasis on experience areas, responsibilities, and behavioral strengths relevant to the JD.

# 🧩 PROJECTS SECTION:
# - For each project:
#   For each project in the profile:

# - Arrange **all** the candidate's projects in the **order of their relevance to the JD**, starting with those most aligned in terms of responsibilities, tools, or domain relevance. Ensure every listed project is retained and rewritten, regardless of relevance level.

# - Rephrase and expand the **Description** to make it clearer, more impactful, and better aligned with the responsibilities and expectations outlined in the JD.

# - Ensure the **Contribution** section is written in concise bullet points. Maintain the original intent and structure while enhancing clarity and relevance.

# - In the **Tech Stack**, include any missing tools, technologies, languages, frameworks, or platforms mentioned in the JD — but only if they could reasonably have been used in the context of the project.

# - In the **Contribution**, only include tools or skills from the JD if their application would be contextually appropriate for that project.
#   - Do not add irrelevant JD tools/skills that don't logically fit the project's description nature or scope.
#   - Only enhance with JD elements when there is a clear functional or thematic alignment.

# - Add the following additional details for each project, ensuring they are clearly relevant to the JD:
#   - **Client**: Mention the client or organization the project was done for. Include its domain if stated in the profile; if not, infer based on context. If limited info is available, just state the name.
#   - **Business Case**: Summarize the core problem or goal the project aimed to solve, as described in the profile.
#   - **Solution**: Briefly describe the solution or approach taken to address the business case, aligning it with the expectations or themes in the JD.
#   - **Project Live Links**: Mention any live demo, website, or GitHub link listed in the profile, if available.

# - Ensure all the projects present in the input profile are included in the output, even if they are not directly relevant to the JD. The goal is to enhance the profile while maintaining all original projects.

# Be realistic and context-aware while enriching the project with JD-relevant content.

# Your task is to enhance rephrase the profile based on the JD, ensuring that everything is relevant and aligned with the JD.

#   FORMAT TO FOLLOW:

# - Name: <Candidate Name>
# - Role: <Candidate Role>
# - Summary: <Rephrased summary>

# - Technologies: (Add missing tech requirements from JD)
#   Backend Technologies: <comma-separated list>
#   Frontend Technologies: <comma-separated list>
#   Database: <comma-separated list>
#   Tools: <comma-separated list>
#   Programming Languages: <comma-separated list>
#   AI Tools: <comma-separated list>

# - Skills (Behavioral only from the JD and from the profile, no tech skills or tools):
#   - Skill 1
#   - Skill 2
#   - ...

# - Projects:
#   1. Title: <Project Title>
#      Tech Stack: <List of technologies/tools used, including JD-aligned additions>
#      Client: <Name of the client and domain if available, else just the name. If there is no client name given, infer the domain from the input profile>
#      Business Case: <Short statement of the problem the project aimed to solve, infer from the project description if not explicitly stated>
#      Solution: <Short explanation of the approach taken, inferred from the respective project description>
#      Description: <Expanded description aligned with JD, same length as original, try to have it in 3-5 lines>
#      Contribution: (Each point should be a well-articulated 30-40 worded sentences that clearly explains the action taken, its purpose, and if possible, the impact. Aim for 4-5 longer, context-rich points that reflect the JD responsibilities.)
#      - <Expanded, detailed contribution 1>
#      - <Expanded, detailed contribution 2>
#      - ...
#      Project Live Links: <Any provided link or demo URL, else leave empty>
     
#   2. Title: ...
#      Tech Stack: ...
#      Client: ...
#      Business Case: ...
#      Solution: ...
#      Description: ...
#      Contribution:
#      - ...
#      - ...
#      Project Live Links: ...

# - Skill Gaps: (Identify the tools, technologies, skills, or qualifications mentioned in the JD that are missing from the original profile. Use natural, easy-to-understand phrases to explain what is missing and why it's relevant — without strictly following one sentence structure. The goal is to highlight what's absent in a way the user can immediately understand.)
#   - <What's missing and why it matters>
#   - <What's missing and why it matters>
#   - ...

# - Technical Expertise:
#   (Based on the enhanced Technologies section, list 4-5 succinct, insightful technical capability statements. Each point should reflect a strength or area of competence in a practical, real-world or JD-relevant context. For example:)
#   - Proficient in building scalable backend systems using Node.js and Express.
#   - Skilled in designing responsive UI components with React and TailwindCSS.
#   - Experience integrating AI tools like LangChain or OpenAI APIs in production-grade apps.
#   - Adept at using Docker, GitHub Actions, and Jira for streamlined DevOps and task management.
#   - Strong command over relational and NoSQL databases including PostgreSQL and MongoDB.

# - percentage_match_before_enhancement: <Provide a numeric value strictly between 0 and 100 followed by the '%' symbol, e.g., 62%. This should reflect the estimated overlap between the original profile and the JD. Do not write descriptive text.>

# - percentage_match_after_enhancement: <Provide a numeric value strictly between 0 and 100 followed by the '%' symbol, e.g., 85%. This should reflect the estimated overlap between the enhanced profile and the JD. Do not write descriptive text.>

# 🧱 STRUCTURED FORMAT (MANDATORY):
# {format_instructions}
# """


EXTRACTION_PROMPT = """
You are an AI assistant. Convert the candidate's unstructured profile into a structured JSON format.

Profile:
{profile}

Instructions:
- Extract only what is present. Do not add or fabricate details.
- If any field is missing, leave it blank.
- Keep all tool/tech names exactly as in the profile, but fix spelling errors.
- Follow the EnhancedProfile schema.
- Be precise and consistent.

STRUCTURED FORMAT (MANDATORY):
{format_instructions}
"""


JD_ENHANCEMENT_PROMPT = """
You are an AI assistant enhancing structured developer profiles based on job descriptions.

Job Description:
{jd}

Candidate Structured Profile:
{profile}

GENERAL RULES:
- Keep structure, tone, and approximate length same as the input profile.
- Retain the role of the candidate, present in the input profile, in the enhanced profile as well.
- Add tools/technologies only if mentioned in JD and contextually applicable.
- Do not remove any original content.
- Use only behavioral skills (no technical tools); max 5. Synonyms allowed.
- Add 2 relevant emerging tools only if strongly aligned with projects or JD.
- If JD mentions years of experience, reflect it clearly in the Summary. 
- Add at least 1 relevant JD tool to Tech Stack (if missing and applicable).

SUMMARY:
- Rephrase to align with the JD — focus on responsibilities and behavioral strengths.
- No tool/tech names in the summary.
- Replace the experience given in the original profile with that required in the JD. In case a range is given as required experience, choose one value from that range to use as experience in the enhanced profile.
- Maximum number of words is ~30-40

PROJECTS:
- Retain all original projects.
- Rearrange based on relevance of the project use case to the JD.
- For each project:
  - Expand Description to match JD expectations.
  - Rewrite Contributions: 4-5 bullets, each ~25-35 words explaining action, purpose, and outcome.
  - Always prefer JD-specified tools and technologies over those in the original profile.
    - Replace tools in the original project (e.g., MongoDB, REST) with relevant, modern equivalents from the JD (e.g., PostgreSQL, GraphQL, Go, Supabase) — if the context or purpose is similar.
    - If the JD tools are **newer, more standard, or directly relevant**, assume they are used **in place of** older or unspecified tools in the profile.
    - Do this strictly for every project where such mapping is reasonable — do **not** retain outdated tools alongside JD ones.
    - Reflect this clearly in both the Tech Stack and Contribution sections of each project.
  - Add:
    - Client: Mention company (add domain if inferred or given).
    - Business Case: What problem it solved.
    - Solution: What was built or done.
    - Project Live Links: From profile if available.

TECHNOLOGIES:
- Update all categories using missing JD tech (only if project-relevant).
- Do not add irrelevant or unsupported tools.

SKILL GAPS:
- For each missing JD requirement, explain what is absent and why it matters — use short, understandable phrases.

TECHNICAL EXPERTISE:
- Based on final tech stack, add 4-5 strengths, each consisting of 20-30 words.
- Each should be practical, relevant to JD, and clearly expressed.

PERCENTAGE MATCH (IMPORTANT):
These two fields measure the overlap between the job description and the original candidate profile (before enhancement), and that between the job description and the enhanced profile (after enhancement):
- Compare the technologies, tools, behavioral skills, and responsibilities mentioned in the JD with those in the profile.
- Count how many distinct, relevant JD items are already in the profile before enhancement and how many are present after enhancement.
- Use this to estimate the match percentage as a whole number between 0 and 100.
- Return only the number — no symbol, no words. Example: 62

FORMAT TO FOLLOW:

- Name: <Candidate Name>
- Role: <Candidate Role>
- Summary: <Rephrased summary>

- Technologies:
  Backend Technologies: <...>
  Frontend Technologies: <...>
  Database: <...>
  Tools: <...>
  Programming Languages: <...>
  AI Tools: <...>

- Skills:
  - <Behavioral skill>
  - ...

- Projects:
  1. Title: ...
     Tech Stack: ...
     Client: ...
     Business Case: ...
     Solution: ...
     Description: ...
     Contribution:
     - ...
     - ...
     Project Live Links: ...

  2. Title: ...
     ...

- Skill Gaps:
  - <What's missing and why it matters>
  - ...

- Technical Expertise:
  - <Real-world technical capability based on tech stack>
  - ...

- Percentage Match between the given job description and the original profile (Candidate Structured Profile): <e.g., 61>
- Percentage Match between the given job description and the enhanced profile: <e.g., 87>

🧱 STRUCTURED FORMAT (MANDATORY):
{format_instructions}
"""
