import os
import json
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from dotenv import load_dotenv
import requests as http_requests

load_dotenv()

# Templates at root level - most reliable on Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, 
            template_folder=BASE_DIR,
            static_folder=os.path.join(BASE_DIR, 'static'))
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

print(f"[BOOT] GROQ_API_KEY={'SET' if GROQ_API_KEY else 'MISSING'}")
print(f"[BOOT] SUPABASE_URL={'SET' if SUPABASE_URL else 'MISSING'} ({SUPABASE_URL[:30]}...)" if SUPABASE_URL else "[BOOT] SUPABASE_URL=MISSING")
print(f"[BOOT] SUPABASE_KEY={'SET' if SUPABASE_KEY else 'MISSING'}")

_supabase_error = None

def get_supabase():
    global _supabase_error
    if not SUPABASE_URL or not SUPABASE_KEY:
        _supabase_error = f"Missing env: URL={'SET' if SUPABASE_URL else 'EMPTY'}, KEY={'SET' if SUPABASE_KEY else 'EMPTY'}"
        print(f"[Supabase] {_supabase_error}")
        return None
    try:
        from supabase import create_client
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        _supabase_error = None
        return client
    except Exception as e:
        _supabase_error = f"create_client error: {type(e).__name__}: {e}"
        print(f"[Supabase] {_supabase_error}")
        return None

def call_claude(prompt):
    """Call GROQ API (OpenAI-compatible) with Llama 3.3 70B model."""
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY not set. Add it in Render → Environment Variables."
    try:
        res = http_requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "max_tokens": 4096,
                "temperature": 0.7,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=60
        )
        data = res.json()
        if "error" in data:
            return f"API error: {data['error'].get('message', str(data['error']))}"
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

PROFILE = {
    "name": "Amretha Karthikeyan",
    "address": "#02-321 153 Gangsa Road, Singapore-670153",
    "mobile": "+65-90256503",
    "email": "amretha.ammu@gmail.com",
    "linkedin": "https://www.linkedin.com/in/amretha-nishanth-534b39101/",
    "headline": "Product Owner | Lead BA | Fintech & Digital Products · Singapore",
    "aiProjectUrl": "https://stock-monitor-8ak6.onrender.com",
    "summary": (
        "SAFe 6.0 certified Product Owner and Lead Business Analyst with 5+ years owning "
        "product backlogs and driving digital product delivery in fintech and banking. "
        "At KPMG Singapore, served as de-facto Product Owner for Loan IQ — a core banking "
        "platform — leading cross-functional squads (engineering, UX, QA) to ship features "
        "and deliver measurable business outcomes. Built and deployed a live AI-powered Trade "
        "Analysis platform using Claude Opus 4.6. Seeking in-house product roles to own "
        "roadmaps end-to-end, from discovery through to scale."
    ),
    "skills": [
        "Tableau", "Power BI", "PSQL", "Python", "Agile", "JIRA", "Excel",
        "Microsoft Project", "Product Vision", "Roadmapping", "Business Analysis",
        "Risk Mitigation", "Change Management", "Budget Forecasting", "Variance Analysis",
        "KPI Tracking", "Dashboard Reporting", "SAFe 6.0", "API integrations",
        "Loan IQ", "SQL", "Stakeholder Management", "Generative AI", "LLM",
        "Claude API", "AI product development", "Prompt Engineering"
    ],
    "certification": "Scaled Agile Framework 6.0 Product Owner/Product Management",
    "experience": [
        {
            "company": "KPMG, Singapore",
            "role": "Lead Business Analyst – Functional Consultant – Loan IQ",
            "period": "Feb 2021 – Present",
            "bullets": [
                "Served as de-facto Product Owner for Loan IQ core banking platform, owning the product backlog and driving sprint delivery for a cross-functional squad (engineering, UX, QA)",
                "Partnered with Enterprise Singapore on large-scale digital transformation projects",
                "Drove product scope decisions through impact analysis, generating ~5% additional business value",
                "Identified and delivered automation of interest computation workflow, eliminating 30 man-days of manual effort",
                "Owned and prioritised product backlog, ensuring alignment with business objectives and regulatory requirements",
                "Led sprint ceremonies (planning, reviews, retros, PI Planning) across multi-squad programme",
                "Managed 3rd party vendors, conducted go-live planning, and led data migrations from legacy systems",
                "Designed and executed end-to-end test scenarios on Loan IQ applications (M&A, Trade, WCL, FA)"
            ],
            "achievements": [
                "Drove ~5% business value through product scope and change request impact analysis",
                "Eliminated 30 man-days of manual work through automated interest computation feature",
                "Led team through critical sprint-to-SIT transition, maintaining delivery timeline"
            ]
        },
        {
            "company": "J.P. Morgan",
            "role": "Asset Management Virtual Internship",
            "period": "Oct 2023 – Jan 2024",
            "bullets": [
                "Gathered product requirements from trading/execution teams to build robust investor profiles",
                "Performed quantitative analysis of 5 stocks and recommended to 2 clients based on risk metrics",
                "Measured portfolio performance via KPIs: Annual Return, Portfolio Variance, Standard Deviation"
            ]
        },
        {
            "company": "Amazon Inc, India",
            "role": "Business Analyst",
            "period": "Mar 2018 – Mar 2019",
            "bullets": [
                "Built real-time quality monitoring dashboards using Power BI from SQL Server and MS Excel",
                "Translated business requirements into functional and non-functional specifications",
                "Analysed and visualised operational data using Tableau and Power BI"
            ]
        }
    ],
    "education": [
        {"degree": "Master of Science – Engineering Business Management", "school": "Coventry University, UK", "period": "Jul 2019 – Nov 2020"},
        {"degree": "Bachelor of Engineering – Electronics & Communication", "school": "Anna University, India", "period": "Jul 2012 – Jun 2016"}
    ],
    "projects": [
        {
            "title": "AI-Powered Trade Analysis Platform",
            "type": "Personal Project",
            "period": "2025",
            "url": "https://stock-monitor-8ak6.onrender.com",
            "tech": "Claude Opus 4.6 (Anthropic), Python, Flask, Render",
            "bullets": [
                "Designed and deployed a live AI-powered Trade Analysis platform using Claude Opus 4.6 — accessible at https://stock-monitor-8ak6.onrender.com",
                "Combined financial trade data and international trade flow analysis using generative AI",
                "Demonstrated end-to-end AI product development: problem definition, prompt engineering, LLM integration, Flask backend, and Render deployment",
                "Independently shipped a working AI product — demonstrating product ownership beyond theory"
            ]
        }
    ]
}

PRODUCT_FRAMING = """
CRITICAL POSITIONING — The candidate is transitioning from CONSULTING to IN-HOUSE PRODUCT roles:
- Reframe consulting experience → "Product Owner for product squad"
- Reframe "client delivery" → "shipped product features, owned backlog, drove sprint outcomes"
- DO NOT use: consultant, client, engagement, billable, service delivery
- DO USE: product, squad, roadmap, discovery, iteration, user value, outcome, feature, backlog
"""


# ─── MULTI-USER PROFILE SUPPORT ──────────────────────────────
# Amretha's profile is hardcoded as DEFAULT_PROFILE.
# Other users can upload their own profile via /api/profile/save.
# get_active_profile() returns user-uploaded profile if it exists, else default.

DEFAULT_PROFILE = PROFILE  # alias for clarity

def get_active_profile():
    """Return user-uploaded profile from Supabase, or fall back to hardcoded DEFAULT_PROFILE."""
    try:
        sb = get_supabase()
        if sb:
            res = sb.table("settings").select("value").eq("key", "user_profile").execute()
            if res.data and res.data[0].get("value"):
                custom = json.loads(res.data[0]["value"])
                if custom.get("name"):  # valid profile must have a name
                    return custom
    except Exception as e:
        print(f"[Profile] Error loading custom profile: {e}")
    return DEFAULT_PROFILE


def build_product_framing(profile):
    """Generate dynamic positioning text based on user profile."""
    name = profile.get("name", "the candidate")
    exp = profile.get("experience", [])
    current = exp[0] if exp else {}
    current_company = current.get("company", "their current company")
    return f"""
CRITICAL POSITIONING — {name} is transitioning from CONSULTING to IN-HOUSE PRODUCT roles:
- Reframe "{current_company} consultant" → "Product Owner for product squad"
- Reframe "client delivery" → "shipped product features, owned backlog, drove sprint outcomes"
- DO NOT use: consultant, client, engagement, billable, service delivery
- DO USE: product, squad, roadmap, discovery, iteration, user value, outcome, feature, backlog
"""


@app.route("/api/profile/save", methods=["POST"])
def save_profile():
    """Save a user-uploaded profile. Expects JSON with profile fields."""
    data = request.json or {}
    if not data.get("name"):
        return jsonify({"error": "Profile must include at least a name"}), 400

    # Normalize the profile structure
    profile = {
        "name":          data.get("name", "").strip(),
        "address":       data.get("address", "").strip(),
        "mobile":        data.get("mobile", "").strip(),
        "email":         data.get("email", "").strip(),
        "linkedin":      data.get("linkedin", "").strip(),
        "headline":      data.get("headline", "").strip(),
        "aiProjectUrl":  data.get("aiProjectUrl", "").strip(),
        "summary":       data.get("summary", "").strip(),
        "skills":        data.get("skills", []),
        "certification": data.get("certification", "").strip(),
        "experience":    data.get("experience", []),
        "education":     data.get("education", []),
        "projects":      data.get("projects", []),
    }

    # If skills came as a comma-separated string, split it
    if isinstance(profile["skills"], str):
        profile["skills"] = [s.strip() for s in profile["skills"].split(",") if s.strip()]

    try:
        sb = get_supabase()
        if not sb:
            return jsonify({"error": "Supabase not configured"}), 400
        sb.table("settings").upsert({"key": "user_profile", "value": json.dumps(profile)}, on_conflict="key").execute()
        return jsonify({"ok": True, "message": f"Profile saved for {profile['name']}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/profile/load", methods=["GET"])
def load_profile():
    """Load the active profile (custom or default)."""
    profile = get_active_profile()
    is_default = (profile.get("name") == DEFAULT_PROFILE.get("name") and
                  profile.get("email") == DEFAULT_PROFILE.get("email"))
    return jsonify({"profile": profile, "is_default": is_default})


@app.route("/api/profile/reset", methods=["POST"])
def reset_profile():
    """Reset to default profile (Amretha's hardcoded profile)."""
    try:
        sb = get_supabase()
        if sb:
            sb.table("settings").delete().eq("key", "user_profile").execute()
        return jsonify({"ok": True, "message": "Reset to default profile"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/profile/parse-resume", methods=["POST"])
def parse_resume_to_profile():
    """Use AI to parse a pasted resume into structured profile JSON."""
    data = request.json or {}
    resume_text = data.get("resumeText", "").strip()
    if not resume_text or len(resume_text) < 50:
        return jsonify({"error": "Please paste a resume with at least 50 characters"}), 400

    prompt = f"""Parse this resume into a structured JSON profile. Extract all information accurately.

RESUME TEXT:
{resume_text[:5000]}

Return ONLY valid JSON with this exact structure (no markdown, no extra text):
{{
  "name": "Full Name",
  "address": "Address if mentioned",
  "mobile": "Phone number",
  "email": "Email address",
  "linkedin": "LinkedIn URL",
  "headline": "Professional headline (e.g., 'Product Manager | Fintech | Singapore')",
  "aiProjectUrl": "Any project/portfolio URL mentioned",
  "summary": "Professional summary (2-3 sentences)",
  "skills": ["Skill 1", "Skill 2", "Skill 3"],
  "certification": "Certifications listed, comma separated",
  "experience": [
    {{
      "company": "Company Name",
      "role": "Job Title",
      "period": "Start – End",
      "bullets": ["Achievement/responsibility 1", "Achievement 2"],
      "achievements": ["Key achievement 1"]
    }}
  ],
  "education": [
    {{"degree": "Degree Name", "school": "University Name", "period": "Start – End"}}
  ],
  "projects": [
    {{
      "title": "Project Name",
      "type": "Project type",
      "period": "Year",
      "url": "URL if any",
      "tech": "Technologies used",
      "bullets": ["Description 1"]
    }}
  ]
}}

If a field is not found in the resume, use empty string "" or empty array [].
Extract ALL experience entries, education, and skills mentioned."""

    result = call_claude(prompt)
    try:
        import re
        clean = re.sub(r'```json|```', '', result).strip()
        m = re.search(r'\{.*\}', clean, re.DOTALL)
        if m:
            profile = json.loads(m.group())
            return jsonify({"profile": profile})
        return jsonify({"error": "Could not parse AI response into profile JSON"}), 500
    except Exception as e:
        return jsonify({"error": f"Parse error: {str(e)}", "raw": result}), 500

def is_ai_role(jd, role_type):
    ai_terms = ["ai", "artificial intelligence", "machine learning", "ml", "llm",
                "generative ai", "genai", "nlp", "gpt", "claude", "openai",
                "foundation model", "large language model", "ai product", "data science"]
    text = (jd + " " + role_type).lower()
    return any(t in text for t in ai_terms)


# ─── ROUTES ───────────────────────────────────────────────

@app.route("/", methods=["GET", "HEAD"])
@app.route("/index.html")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        app.logger.error(f"Template error: {e}")
        return f"<h2>App is running!</h2><p>Template error: {e}</p><p>BASE_DIR: {BASE_DIR}</p>", 500

@app.route("/api/tailor-resume", methods=["POST"])
def tailor_resume():
    data = request.json
    jd = data.get("jd", "")
    role_type = data.get("roleType", "Business Analyst")
    ai_role = is_ai_role(jd, role_type)
    P = get_active_profile()
    framing = build_product_framing(P)

    prompt = f"""You are an expert ATS-optimised resume writer helping candidates transition into in-house product roles.
{framing}

Rewrite the following candidate's resume to precisely match the job description. Target role: {role_type}.

CANDIDATE PROFILE:
{json.dumps(P, indent=2)}

JOB DESCRIPTION:
{jd}

{"AI ROLE DETECTED: Prominently feature the AI Project section with the live URL: " + P.get('aiProjectUrl','') + ". Lead Skills with AI/LLM skills." if ai_role else ""}

ATS OPTIMISATION RULES:
1. Mirror the exact keywords, phrases and job titles used in the JD — ATS systems do exact-match keyword scanning.
2. Use standard section headers: "Professional Summary", "Core Skills", "Professional Experience", "Education & Certifications".
3. Place the most relevant keywords in the first 1/3 of the resume (summary + skills) where ATS gives highest weight.
4. Include both spelled-out terms AND acronyms (e.g. "Applicant Tracking System (ATS)").
5. Use measurable metrics (%, $, days saved, team size) in every bullet point.
6. Use active verbs that match JD language: Led, Drove, Delivered, Owned, Shipped, Optimised.
7. Do NOT use tables, columns, headers/footers, or images — these break ATS parsers.
8. Keep formatting clean: single column, standard fonts, bullet points with plain text.

Write a complete ATS-optimised resume with:
- Header (name, contact, LinkedIn, {P.get('aiProjectUrl','') if ai_role else ''})
- Professional Summary (keyword-rich, mirrors JD language, product-ownership framing)
- {"AI & Innovation / Projects section (FIRST after summary for AI roles)" if ai_role else ""}
- Core Skills (extracted from JD + candidate's real skills, comma-separated)
- Professional Experience (product language, real metrics, JD keywords woven naturally)
- Education & Certifications

Do not fabricate experience. Use product language, not consulting language. Every bullet must contain a measurable outcome."""

    result = call_claude(prompt)
    return jsonify({"result": result, "isAiRole": ai_role})

@app.route("/api/cover-letter", methods=["POST"])
def cover_letter():
    data = request.json
    jd = data.get("jd", "")
    role_type = data.get("roleType", "Business Analyst")
    company = data.get("company", "the company")
    ai_role = is_ai_role(jd, role_type)

    P = get_active_profile()
    framing = build_product_framing(P)
    # Build achievements from profile experience
    achievements_text = ""
    for exp in P.get('experience', []):
        for ach in exp.get('achievements', []):
            achievements_text += f"- {ach}\n"
    if P.get('certification'):
        achievements_text += f"- Certified: {P['certification']}\n"
    if P.get('aiProjectUrl'):
        achievements_text += f"- Personal Project: {P.get('aiProjectUrl','')}\n"

    prompt = f"""Write a professional 300-350 word cover letter for {P['name']} applying to {role_type} at {company}.
{framing}

KEY ACHIEVEMENTS:
{achievements_text}

JOB DESCRIPTION:
{jd}

{"IMPORTANT — AI ROLE: Mention the project at " + P.get('aiProjectUrl','') + " as proof of hands-on AI product development. Include the URL." if ai_role else ""}

ATS & RECRUITER OPTIMISATION:
1. Mirror the EXACT job title and 5-8 key phrases from the JD in the letter.
2. Use confident product language, not consulting jargon.
3. Include specific metrics (5% value, 30 man-days) for credibility.
4. Reference the company name and role title at least twice.
5. Keep paragraphs short (3-4 sentences max) for easy scanning.

Write a compelling cover letter that:
1. Opens with a confident hook referencing the specific role and company, positioning as a product builder not a service provider
2. Highlights KPMG metrics (5% value, 30 man-days) in context of what JD requires
3. {"Mentions live AI project with URL as key differentiator" if ai_role else "Bridges consulting delivery to product ownership with specific JD alignment"}
4. Shows genuine, specific enthusiasm for {company} — reference what they do
5. Ends with a clear, action-oriented call to action

Exactly 300-350 words. No consulting jargon. Sound like a product person. Weave JD keywords naturally throughout."""

    result = call_claude(prompt)
    return jsonify({"result": result})

@app.route("/api/interview-prep", methods=["POST"])
def interview_prep():
    data = request.json
    company = data.get("company", "the company")
    role_type = data.get("roleType", "Business Analyst")
    jd = data.get("jd", "")

    P = get_active_profile()
    framing = build_product_framing(P)
    # Build candidate summary from profile
    exp_lines = ""
    for exp in P.get('experience', []):
        bullets_preview = '; '.join(exp.get('bullets', [])[:2])
        exp_lines += f"- {exp.get('company','')} ({exp.get('period','')}): {exp.get('role','')}. {bullets_preview}\n"
    skills_str = ', '.join(P.get('skills', [])[:12])
    proj_url = P.get('aiProjectUrl', '')

    prompt = f"""Generate a comprehensive interview prep guide for {P['name']} interviewing at {company} for {role_type}.
{framing}

CANDIDATE:
{exp_lines}
- Certified: {P.get('certification','')}
- Skills: {skills_str}
{('- Project: ' + proj_url) if proj_url else ''}
{"JD: " + jd if jd else ""}

Create prep with these EXACT sections:

## 5 Behavioral Questions with STAR Answers
For each: the question, then full STAR answer using the candidate's real experience with specific metrics.

## 5 Technical Questions for {role_type}
Questions with model answers specific to this role.

## 3 Things to Research About {company}
Specific actionable research areas.

## 5 Smart Questions to Ask the Interviewer
Product-minded questions that signal ownership thinking.

## Salary Negotiation Tip
Specific tip based on the candidate's certifications and experience level."""

    result = call_claude(prompt)
    return jsonify({"result": result})


# ─── INTERACTIVE AI INTERVIEW COACH ─────────────────────────────────────────

# In-memory session store (per-server; for multi-server use Redis/Supabase)
_interview_sessions = {}

def _scrape_company_intel(company):
    """Try to gather company interview intelligence from public sources."""
    intel = {"glassdoor": None, "general": None}
    try:
        import requests as http_req
        # Try Glassdoor-style search via Google
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        queries = [
            f"{company} interview questions glassdoor",
            f"{company} interview process experience",
        ]
        snippets = []
        for q in queries[:1]:  # limit to 1 query to be fast
            try:
                url = f"https://www.google.com/search?q={q.replace(' ', '+')}&num=5"
                r = http_req.get(url, headers=headers, timeout=8)
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(r.text, "html.parser")
                for div in soup.select(".BNeawe.s3v9rd"):
                    text = div.get_text(strip=True)
                    if len(text) > 40:
                        snippets.append(text[:300])
                    if len(snippets) >= 5:
                        break
            except Exception:
                pass
        if snippets:
            intel["glassdoor"] = snippets
    except Exception:
        pass
    return intel


@app.route("/api/interview/start", methods=["POST"])
def interview_start():
    """Start an interactive interview session."""
    data = request.json or {}
    role = data.get("role", "").strip()
    company = data.get("company", "").strip()
    interview_type = data.get("type", "behavioral")
    jd = data.get("jd", "").strip()
    resume_text = data.get("resume", "").strip()

    if not role or not company:
        return jsonify({"error": "Role and company are required"}), 400

    P = get_active_profile()

    # Build candidate context from profile + optional resume
    candidate_info = f"Name: {P.get('name', 'Candidate')}\n"
    if P.get('headline'):
        candidate_info += f"Headline: {P['headline']}\n"
    if P.get('summary'):
        candidate_info += f"Summary: {P['summary'][:300]}\n"
    for exp in P.get('experience', [])[:3]:
        bullets = '; '.join(exp.get('bullets', [])[:2])
        candidate_info += f"- {exp.get('company','')} | {exp.get('role','')} ({exp.get('period','')}): {bullets}\n"
    if resume_text:
        candidate_info += f"\nResume excerpt:\n{resume_text[:800]}\n"

    # Type-specific instruction
    type_instructions = {
        "behavioral": """Focus on behavioral and situational questions using the STAR method.
Ask questions like "Tell me about a time when..." and "How would you handle...".
Cover: leadership, conflict, failure, teamwork, prioritization, stakeholder management.
After each answer, evaluate their STAR structure and probe deeper.""",

        "technical": """Focus on technical and case study questions relevant to the role.
Include: system design, data analysis, technical problem-solving, SQL/analytics scenarios.
Ask follow-up questions to test depth of knowledge.""",

        "product": f"""Focus on product sense, strategy, and case study questions.
Use frameworks from top PM prep (Exponent, PrepLounge style).
Include: product design, metrics/KPIs, go-to-market, prioritization frameworks, estimation.
After each answer, evaluate their structured thinking.""",

        "mixed": """Conduct a realistic full mock interview mixing:
- 2 behavioral/situational questions (STAR method)
- 2 technical/role-specific questions
- 1 product sense or case question
Transition naturally between types like a real interviewer.""",
    }

    # Try to get company intel
    company_intel = _scrape_company_intel(company)
    intel_context = ""
    if company_intel.get("glassdoor"):
        intel_context = f"\nCompany interview intelligence (from web research):\n" + "\n".join(f"- {s}" for s in company_intel["glassdoor"][:3])

    session_id = f"session_{id(data)}_{__import__('time').time()}"

    system_prompt = f"""You are an expert AI interview coach conducting a realistic mock interview.
You are interviewing a candidate for the role of **{role}** at **{company}**.

CANDIDATE PROFILE:
{candidate_info}

{"JOB DESCRIPTION:\n" + jd[:1000] if jd else ""}
{intel_context}

INTERVIEW TYPE: {interview_type}
{type_instructions.get(interview_type, type_instructions['behavioral'])}

RULES:
1. Ask ONE question at a time. Wait for the candidate's answer before continuing.
2. After each answer, provide:
   - A brief score (1-10) with reasoning
   - Specific feedback on what was good and what to improve
   - A follow-up or new question
3. Be encouraging but honest. Point out weak areas constructively.
4. Track which competencies you've covered.
5. If the answer is vague, probe deeper — "Can you be more specific?" or "What was the measurable outcome?"
6. Reference the candidate's actual experience from their profile when asking questions.
7. Vary difficulty — start with a warm-up question, then increase complexity.
8. Format your response as:
   **Score: X/10** [brief reason]
   **Feedback:** [specific feedback]
   **Next Question:** [the next question]
   (For the FIRST message, skip score/feedback and just ask an opening question with a brief welcome.)"""

    # Generate the first question
    first_msg_prompt = f"""{system_prompt}

Start the interview now. Welcome the candidate warmly, mention the role and company, and ask your first question.
Keep the welcome to 2 sentences max, then ask the question."""

    first_response = call_claude(first_msg_prompt)

    # Store session
    _interview_sessions[session_id] = {
        "system_prompt": system_prompt,
        "messages": [
            {"role": "assistant", "content": first_response}
        ],
        "role": role,
        "company": company,
        "type": interview_type,
        "scores": [],
        "started_at": __import__('time').time(),
        "company_intel": company_intel,
    }

    return jsonify({
        "session_id": session_id,
        "message": first_response,
        "company_intel": company_intel,
    })


@app.route("/api/interview/respond", methods=["POST"])
def interview_respond():
    """Process a candidate's answer and generate AI follow-up."""
    data = request.json or {}
    session_id = data.get("session_id", "")
    answer = data.get("answer", "").strip()

    if not session_id or session_id not in _interview_sessions:
        return jsonify({"error": "Invalid or expired session"}), 400
    if not answer:
        return jsonify({"error": "Please provide an answer"}), 400

    session = _interview_sessions[session_id]
    session["messages"].append({"role": "user", "content": answer})

    # Build conversation for Claude
    conversation = session["system_prompt"] + "\n\n"
    conversation += "CONVERSATION SO FAR:\n"
    for msg in session["messages"]:
        prefix = "INTERVIEWER" if msg["role"] == "assistant" else "CANDIDATE"
        conversation += f"\n{prefix}: {msg['content']}\n"

    conversation += "\nINTERVIEWER (now respond with score, feedback, and next question):"

    response = call_claude(conversation)

    session["messages"].append({"role": "assistant", "content": response})

    # Extract score if present
    import re
    score_match = re.search(r'\*?\*?Score:\s*(\d+)/10', response)
    if score_match:
        session["scores"].append(int(score_match.group(1)))

    return jsonify({
        "message": response,
        "question_count": sum(1 for m in session["messages"] if m["role"] == "assistant"),
        "answer_count": sum(1 for m in session["messages"] if m["role"] == "user"),
        "avg_score": round(sum(session["scores"]) / len(session["scores"]), 1) if session["scores"] else None,
    })


@app.route("/api/interview/end", methods=["POST"])
def interview_end():
    """End interview session and generate comprehensive summary."""
    data = request.json or {}
    session_id = data.get("session_id", "")

    if not session_id or session_id not in _interview_sessions:
        return jsonify({"error": "Invalid or expired session"}), 400

    session = _interview_sessions[session_id]

    # Build full transcript
    transcript = ""
    for msg in session["messages"]:
        prefix = "🤖 Interviewer" if msg["role"] == "assistant" else "👤 You"
        transcript += f"\n{prefix}:\n{msg['content']}\n"

    summary_prompt = f"""You conducted a mock interview for {session['role']} at {session['company']}.
Type: {session['type']}

Full transcript:
{transcript}

Provide a comprehensive session summary with:

## Overall Performance Score
Give an overall score out of 10 with detailed reasoning.

## Strengths Demonstrated
List 3-5 specific strengths shown during the interview, with examples from their answers.

## Areas for Improvement
List 3-5 specific areas to improve, with actionable recommendations.

## STAR Method Assessment
Rate their use of the STAR method (Situation, Task, Action, Result) in behavioral answers. Which component was weakest?

## Communication Analysis
Assess: clarity, conciseness, confidence, structure, use of metrics/data.

## Key Recommendations
Top 3 actionable things to practice before the real interview.

## Sample Improved Answer
Take their weakest answer and rewrite it as an ideal response.

Be specific, reference their actual answers, and be constructive."""

    summary = call_claude(summary_prompt)

    # Clean up session
    result = {
        "summary": summary,
        "transcript": transcript,
        "total_questions": sum(1 for m in session["messages"] if m["role"] == "assistant"),
        "total_answers": sum(1 for m in session["messages"] if m["role"] == "user"),
        "avg_score": round(sum(session["scores"]) / len(session["scores"]), 1) if session["scores"] else None,
        "duration_seconds": int(__import__('time').time() - session["started_at"]),
    }

    del _interview_sessions[session_id]
    return jsonify(result)


@app.route("/api/interview/company-intel", methods=["POST"])
def interview_company_intel():
    """Fetch company interview intelligence."""
    data = request.json or {}
    company = data.get("company", "").strip()
    role = data.get("role", "").strip()

    if not company:
        return jsonify({"error": "Company name required"}), 400

    intel = _scrape_company_intel(company)

    # Also ask AI for company-specific insights
    prompt = f"""Provide interview intelligence for {role or 'a candidate'} interviewing at {company}:

## Company Overview
Brief company description, culture, and values (2-3 sentences).

## Interview Process
Typical interview stages and what to expect at {company}.

## Common Interview Questions at {company}
List 5 questions commonly asked at {company} based on known patterns.

## Company-Specific Tips
3 tips specifically for succeeding at a {company} interview.

## Key Values & Culture Fit
What {company} looks for in candidates — culture signals to demonstrate.

## Recent News & Talking Points
2-3 recent developments at {company} worth mentioning in the interview.

Be specific to {company}. If you don't have specific info, provide educated guidance based on the company's industry and size."""

    ai_intel = call_claude(prompt)

    return jsonify({
        "ai_intel": ai_intel,
        "web_snippets": intel.get("glassdoor", []),
    })


@app.route("/api/full-kit", methods=["POST"])
def full_kit():
    data = request.json
    company = data.get("company", "")
    role = data.get("role", "")
    role_type = data.get("roleType", "Business Analyst")
    jd = data.get("jd", "")
    ai_role = is_ai_role(jd, role_type)

    P = get_active_profile()
    framing = build_product_framing(P)
    profile_str = json.dumps({k: v for k, v in P.items()}, indent=2)
    proj_url = P.get('aiProjectUrl', '')

    resume_prompt = f"Write ATS-optimised resume for {P['name']} applying to {role} at {company} ({role_type}). {framing} Profile: {profile_str}. JD: {jd}. {'AI role: feature project ' + proj_url + ' prominently.' if ai_role else ''} ATS rules: mirror exact JD keywords, use standard section headers (Professional Summary, Core Skills, Professional Experience, Education), include metrics in every bullet, single-column format, no tables."
    cover_prompt = f"Write 300-word cover letter for {P['name']} for {role} at {company}. Profile: {profile_str}. {'Mention project: ' + proj_url if ai_role else ''} Mirror key phrases from JD: {jd[:500]}. Product language, no consulting jargon. Reference company name and role at least twice."
    prep_prompt = f"Give top 5 interview questions for {role_type} at {company} with brief model answers for {P['name']}. Profile summary: {P.get('summary','')}. JD context: {jd[:500]}. Include STAR-format answers with real metrics."

    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        r_future = executor.submit(call_claude, resume_prompt)
        c_future = executor.submit(call_claude, cover_prompt)
        p_future = executor.submit(call_claude, prep_prompt)
        resume = r_future.result()
        cover = c_future.result()
        prep = p_future.result()

    return jsonify({"resume": resume, "cover": cover, "prep": prep, "isAiRole": ai_role})

@app.route("/api/follow-up", methods=["POST"])
def follow_up():
    data = request.json
    company = data.get("company", "the company")
    role = data.get("role", "the role")
    days = data.get("days", 7)

    prompt = f"""Write a polite 3-line follow-up email from Amretha Karthikeyan about her application for {role} at {company}, submitted {days} days ago.
Include: subject line, brief message referencing the role, continued interest, offer to provide more info.
Under 80 words. Ready to copy-paste. Professional and confident."""

    result = call_claude(prompt)
    return jsonify({"result": result})

@app.route("/api/speed-kit", methods=["POST"])
def speed_kit():
    data = request.json
    company = data.get("company", "this company")
    role = data.get("role", "this role")

    prompt = f"""Write a genuine 3-sentence "Why do you want to work at {company}?" answer for Amretha Karthikeyan, a SAFe 6.0 PO/Lead BA transitioning from KPMG to an in-house {role} role. Be specific to {company}'s product/market. Sound like a product person who wants to build. No consulting language."""

    result = call_claude(prompt)
    return jsonify({"result": result})


@app.route("/api/generic", methods=["POST"])
def generic():
    data = request.json
    prompt = data.get("prompt", "")
    system = data.get("systemPrompt", "")
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    result = call_claude(full_prompt)
    return jsonify({"result": result})


@app.route("/api/health", methods=["GET"])
def health_check():
    """Debug endpoint to check environment configuration."""
    sb = get_supabase()
    sb_status = "connected" if sb else "NOT configured"
    if sb:
        try:
            res = sb.table("jobs").select("id", count="exact").execute()
            sb_status = f"connected ({res.count or 0} jobs in DB)"
        except Exception as e:
            sb_status = f"connected but query failed: {str(e)[:100]}"
    return jsonify({
        "status": "ok",
        "groq_api_key": "SET" if GROQ_API_KEY else "MISSING",
        "supabase_url": "SET" if SUPABASE_URL else "MISSING",
        "supabase_key": "SET" if SUPABASE_KEY else "MISSING",
        "supabase_key_length": len(SUPABASE_KEY) if SUPABASE_KEY else 0,
        "supabase_key_prefix": (SUPABASE_KEY[:20] + "...") if SUPABASE_KEY else "empty",
        "supabase_status": sb_status,
        "supabase_error": _supabase_error,
        "supabase_url_preview": (SUPABASE_URL[:40] + "...") if SUPABASE_URL else "empty"
    })


@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    """Load all jobs from Supabase."""
    sb = get_supabase()
    if not sb:
        return jsonify({"error": "Supabase not configured", "jobs": []}), 200
    try:
        res = sb.table("jobs").select("*").order("created_at", desc=False).execute()
        return jsonify({"jobs": res.data or []})
    except Exception as e:
        return jsonify({"error": str(e), "jobs": []}), 200


@app.route("/api/jobs/upsert", methods=["POST"])
def upsert_jobs():
    """Save/update jobs to Supabase. Upserts by job id."""
    sb = get_supabase()
    if not sb:
        return jsonify({"error": "Supabase not configured"}), 200
    data = request.json
    jobs = data.get("jobs", [])
    if not jobs:
        return jsonify({"ok": True, "count": 0})
    try:
        # Whitelist all fields we want to persist — everything
        def clean(j):
            return {
                "id":               str(j.get("id", "")),
                "role":             j.get("role", ""),
                "company":          j.get("company", ""),
                "status":           j.get("status", "saved"),
                "url":              j.get("url", ""),
                "linkedInId":       j.get("linkedInId", ""),
                "jd":               (j.get("jd") or "")[:8000],
                "roleType":         j.get("roleType", ""),
                "source":           j.get("source", ""),
                "salary":           j.get("salary", ""),
                "dateApplied":      j.get("dateApplied", ""),
                "aiScore":          j.get("aiScore"),
                "aiLabel":          j.get("aiLabel", ""),
                "aiReason":         j.get("aiReason", ""),
                "aiPriority":       j.get("aiPriority", ""),
                "notes":            j.get("notes", ""),
                "resume_docx_b64":  (j.get("resume_docx_b64") or "")[:500000],
                "cover_docx_b64":   (j.get("cover_docx_b64") or "")[:500000],
                "resume_variant":   j.get("resume_variant", ""),
                "resume_filename":  j.get("resume_filename", ""),
                "cover_filename":   j.get("cover_filename", ""),
                "resume_generated_at": j.get("resume_generated_at", ""),
            }
        cleaned = [clean(j) for j in jobs if j.get("id")]
        res = sb.table("jobs").upsert(cleaned, on_conflict="id").execute()
        return jsonify({"ok": True, "count": len(cleaned)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/jobs/delete", methods=["POST"])
def delete_job():
    """Delete a job from Supabase by id."""
    sb = get_supabase()
    if not sb:
        return jsonify({"error": "Supabase not configured"}), 200
    data = request.json
    job_id = data.get("id")
    if not job_id:
        return jsonify({"error": "No id"}), 400
    try:
        sb.table("jobs").delete().eq("id", job_id).execute()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/jobs/clear-all", methods=["POST"])
def clear_all_jobs():
    """Delete every job from Supabase — fresh start."""
    sb = get_supabase()
    if not sb:
        return jsonify({"error": "Supabase not configured"}), 200
    try:
        # Delete all rows — Supabase requires a filter, use neq on a always-true condition
        sb.table("jobs").delete().neq("id", "___never___").execute()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/generate-docs", methods=["POST"])
def generate_docs():
    """Generate tailored resume + cover letter as .docx files using Node.js script."""
    import subprocess, json as json_lib, tempfile, base64, os

    data = request.json
    role = data.get("role", "").strip()
    company = data.get("company", "").strip()
    jd = data.get("jd", "").strip()
    role_type = data.get("roleType", "").strip()
    is_ai = bool(data.get("isAI", False))

    if not role or not company:
        return jsonify({"error": "role and company are required"}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(BASE_DIR, "gen_docs.js")
        # Pass active profile to gen_docs.js if it's a custom (non-default) profile
        P = get_active_profile()
        is_custom = (P.get("name") != DEFAULT_PROFILE.get("name") or
                     P.get("email") != DEFAULT_PROFILE.get("email"))
        payload = json_lib.dumps({
            "role": role,
            "company": company,
            "jd": jd[:3000] if jd else "",
            "roleType": role_type,
            "outputDir": tmpdir,
            "isAI": is_ai,
            "profile": P if is_custom else None
        })

        try:
            result = subprocess.run(
                ["node", script_path, payload],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                return jsonify({"error": result.stderr or "Node script failed"}), 500

            output = json_lib.loads(result.stdout.strip())
            resume_path = output["resume"]
            cover_path = output["cover"]

            with open(resume_path, "rb") as f:
                resume_b64 = base64.b64encode(f.read()).decode()
            with open(cover_path, "rb") as f:
                cover_b64 = base64.b64encode(f.read()).decode()

            return jsonify({
                "resume_b64": resume_b64,
                "cover_b64": cover_b64,
                "variant": output.get("variant", "BA"),
                "resume_filename": f"Resume_{company.replace(' ','_')}.docx",
                "cover_filename": f"CoverLetter_{company.replace(' ','_')}.docx"
            })
        except subprocess.TimeoutExpired:
            return jsonify({"error": "Document generation timed out"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/api/import-job", methods=["POST"])
def import_job():
    data = request.json
    url = data.get("url", "").strip()
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Detect platform
    is_linkedin = "linkedin.com" in url
    is_indeed = "indeed.com" in url or "sg.indeed.com" in url

    # Headers that mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }

    result = {
        "platform": "linkedin" if is_linkedin else "indeed" if is_indeed else "other",
        "url": url,
        "title": "",
        "company": "",
        "location": "Singapore",
        "description": "",
        "partial": False,
        "message": ""
    }

    try:
        from bs4 import BeautifulSoup

        if is_linkedin:
            # LinkedIn blocks login-walled pages but public job URLs sometimes work
            # Extract job ID from URL for reference
            import re
            job_id_match = re.search(r'/jobs/view/(\d+)', url)
            job_id = job_id_match.group(1) if job_id_match else ""
            
            # Try to extract company from URL slug
            company_match = re.search(r'linkedin\.com/jobs/view/[^/]+-at-([a-z0-9-]+)-\d+', url)
            if company_match:
                result["company"] = company_match.group(1).replace("-", " ").title()

            try:
                resp = http_requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(resp.text, "lxml")

                # Try various LinkedIn selectors
                title_el = (soup.find("h1", {"class": lambda c: c and "job-title" in c}) or
                           soup.find("h1", {"class": lambda c: c and "topcard__title" in c}) or
                           soup.find("h1"))
                if title_el:
                    result["title"] = title_el.get_text(strip=True)

                company_el = (soup.find("a", {"class": lambda c: c and "topcard__org-name" in c}) or
                             soup.find("span", {"class": lambda c: c and "company-name" in c}))
                if company_el:
                    result["company"] = company_el.get_text(strip=True)

                desc_el = (soup.find("div", {"class": lambda c: c and "description__text" in c}) or
                          soup.find("div", {"class": lambda c: c and "job-description" in c}))
                if desc_el:
                    result["description"] = desc_el.get_text(separator="\n", strip=True)[:3000]

                if not result["title"] and not result["description"]:
                    # LinkedIn returned a login wall
                    result["partial"] = True
                    result["message"] = "LinkedIn requires login to view full details. Company name extracted from URL — please paste the job description manually."
                else:
                    result["message"] = "Job details imported from LinkedIn!"

            except Exception:
                result["partial"] = True
                result["message"] = "LinkedIn blocked the request. Company extracted from URL — please paste the job description manually."

        elif is_indeed:
            resp = http_requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "lxml")

            # Indeed selectors
            title_el = (soup.find("h1", {"class": lambda c: c and "jobTitle" in str(c)}) or
                       soup.find("h1", {"data-testid": "jobsearch-JobInfoHeader-title"}) or
                       soup.find("h1"))
            if title_el:
                result["title"] = title_el.get_text(strip=True).replace("- job post", "").strip()

            company_el = (soup.find("div", {"data-testid": "inlineHeader-companyName"}) or
                         soup.find("span", {"class": lambda c: c and "companyName" in str(c)}) or
                         soup.find("a", {"data-tn-element": "companyName"}))
            if company_el:
                result["company"] = company_el.get_text(strip=True)

            location_el = (soup.find("div", {"data-testid": "job-location"}) or
                          soup.find("div", {"class": lambda c: c and "companyLocation" in str(c)}))
            if location_el:
                result["location"] = location_el.get_text(strip=True)

            desc_el = (soup.find("div", {"id": "jobDescriptionText"}) or
                      soup.find("div", {"class": lambda c: c and "jobsearch-jobDescriptionText" in str(c)}))
            if desc_el:
                result["description"] = desc_el.get_text(separator="\n", strip=True)[:3000]

            if result["title"] or result["company"]:
                result["message"] = "Job details imported from Indeed! ✅"
            else:
                result["partial"] = True
                result["message"] = "Could not extract details automatically. Please fill in manually."

        else:
            # Generic scrape attempt
            resp = http_requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "lxml")
            title_el = soup.find("h1")
            if title_el:
                result["title"] = title_el.get_text(strip=True)
            result["partial"] = True
            result["message"] = "Basic details extracted — please verify and fill in any missing fields."

    except Exception as e:
        result["partial"] = True
        result["message"] = f"Could not fetch URL automatically. Please fill in details manually. ({str(e)[:80]})"

    return jsonify(result)


@app.route("/api/rank-jobs", methods=["POST"])
def rank_jobs():
    data = request.json
    jobs = data.get("jobs", [])
    
    if not jobs:
        return jsonify({"error": "No jobs provided"}), 400

    # Build a compact job list for the prompt
    job_list = ""
    for i, j in enumerate(jobs):
        jd_snippet = (j.get("jd", "") or "")[:400]
        job_list += f"""
JOB {i+1}:
  ID: {j.get("id")}
  Title: {j.get("role", "Unknown")}
  Company: {j.get("company", "Unknown")}
  Type: {j.get("roleType", "")}
  JD: {jd_snippet if jd_snippet else "No JD provided"}
---"""

    P = get_active_profile()
    # Build dynamic candidate profile text for scoring
    exp_summary_lines = ""
    for exp in P.get('experience', []):
        achvs = '; '.join(exp.get('achievements', [])[:2])
        exp_summary_lines += f"- {exp.get('company','')}: {exp.get('role','')} ({exp.get('period','')})"
        if achvs:
            exp_summary_lines += f" — {achvs}"
        exp_summary_lines += "\n"
    skills_str = ', '.join(P.get('skills', [])[:12])
    proj_url = P.get('aiProjectUrl', '')

    prompt = f"""You are a career coach expert in the tech and product job market.

CANDIDATE PROFILE:
Name: {P.get('name', 'Unknown')}
Headline: {P.get('headline', '')}
Summary: {P.get('summary', '')}
Experience:
{exp_summary_lines}
Certification: {P.get('certification', '')}
Skills: {skills_str}
{'Personal project: ' + proj_url if proj_url else ''}
Target: In-house product roles (NOT consulting) — PM, PO, BA at fintech/tech companies

JOBS TO EVALUATE:
{job_list}

For each job, return a JSON array with this exact structure:
[
  {{
    "id": <job id number>,
    "score": <integer 1-10>,
    "label": "<one of: 🔥 Strong Match | ✅ Good Fit | 🟡 Possible | ❌ Weak Fit>",
    "reason": "<2 sentences: why she fits + one gap or concern if any>",
    "priority": "<one of: Apply Today | Apply This Week | Lower Priority | Skip>"
  }}
]

Scoring guide:
9-10: Near-perfect fit — in-house product role, fintech/tech domain, Singapore, matches PO/BA background
7-8: Good fit — most criteria match, minor gaps
5-6: Possible — transferable skills apply but some gaps
1-4: Weak fit — significant mismatch in role type, seniority, or domain

COMPANY TYPE WEIGHTING — apply these modifiers BEFORE finalising the score:
+2 points: In-house product companies (Grab, Sea/Shopee, Gojek, Airwallex, Stripe, Revolut, Wise, PropertyGuru, Carousell, Lazada, ByteDance, Razer, DBS Tech, OCBC digital, GovTech, tech startups)
+1 point: Companies with strong internal product teams (large banks with digital arms, insurance tech)
 0 points: Neutral / unclear
-2 points: Consulting or professional services firms (Big 4: KPMG, Deloitte, PwC, EY, Accenture, McKinsey, BCG, Bain, IBM GBS, Wipro, Infosys, TCS, CGI, Cognizant)

Amretha is ACTIVELY LEAVING consulting — a consulting role should score maximum 4/10 regardless of title.
Flag consulting roles clearly in the reason field so she can deprioritise them immediately.

VISA RULE — HARD OVERRIDE:
If the job description contains any of these phrases: "no visa sponsorship", "no sponsorship", "candidates must have right to work", "must be a Singapore citizen or PR", "singaporeans and PRs only", "no work pass sponsorship" — score it 0/10 (zero score), label it ❌ Weak Fit, priority Skip, and reason must say "This role explicitly states no visa sponsorship — not worth applying." regardless of any other fit factors.

Return ONLY the JSON array, no other text."""

    result = call_claude(prompt)
    
    # Parse the JSON response
    import json, re
    try:
        # Clean up response - remove markdown code blocks if present
        clean = re.sub(r'```json|```', '', result).strip()
        rankings = json.loads(clean)
        return jsonify({"rankings": rankings, "raw": result})
    except Exception as e:
        return jsonify({"error": f"Could not parse AI response: {str(e)}", "raw": result}), 500


@app.route("/api/fetch-jd", methods=["POST"])
def fetch_jd():
    """Fetch job description from a LinkedIn or Indeed URL via HTTP scraping."""
    import requests as req
    from bs4 import BeautifulSoup

    data = request.json
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        }
        resp = req.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")

        jd = ""
        title = ""
        company = ""

        if "linkedin.com" in url:
            # LinkedIn job description selectors
            for sel in [
                ".description__text",
                ".show-more-less-html__markup",
                "[class*='description']",
                "section.description",
            ]:
                el = soup.select_one(sel)
                if el and len(el.get_text(strip=True)) > 100:
                    jd = el.get_text(separator="\n", strip=True)[:5000]
                    break

            title_el = soup.select_one("h1.top-card-layout__title, h1[class*='title']")
            if title_el:
                title = title_el.get_text(strip=True)

            company_el = soup.select_one("a.topcard__org-name-link, [class*='company-name']")
            if company_el:
                company = company_el.get_text(strip=True)

        elif "indeed.com" in url:
            for sel in ["#jobDescriptionText", ".jobsearch-jobDescriptionText", "[class*='description']"]:
                el = soup.select_one(sel)
                if el and len(el.get_text(strip=True)) > 100:
                    jd = el.get_text(separator="\n", strip=True)[:5000]
                    break

        elif "mycareersfuture.gov.sg" in url:
            for sel in ["[class*='job-description']", "[class*='description']", "article"]:
                el = soup.select_one(sel)
                if el and len(el.get_text(strip=True)) > 100:
                    jd = el.get_text(separator="\n", strip=True)[:5000]
                    break
        else:
            # Generic fallback
            for tag in soup.find_all(["article", "section", "div"], limit=20):
                text = tag.get_text(strip=True)
                if len(text) > 500 and any(kw in text.lower() for kw in ["responsibilities", "requirements", "qualifications", "experience"]):
                    jd = text[:5000]
                    break

        if not jd:
            return jsonify({"jd": "", "error": "Could not extract JD — LinkedIn may require login"}), 200

        return jsonify({"jd": jd, "title": title, "company": company})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/bookmarklet-add", methods=["POST", "OPTIONS"])
def bookmarklet_add():
    # Handle CORS preflight - bookmarklet calls come from linkedin.com/indeed.com
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response

    data = request.json
    role = data.get("role", "").strip()
    company = data.get("company", "").strip()

    if not role or not company:
        resp = jsonify({"success": False, "error": "Missing job title or company"})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    # Store in a simple JSON file on the server
    import json, os
    jobs_file = os.path.join(BASE_DIR, "bookmarked_jobs.json")
    
    try:
        if os.path.exists(jobs_file):
            with open(jobs_file, "r") as f:
                saved = json.load(f)
        else:
            saved = []

        new_job = {
            "id": int(__import__("time").time() * 1000),
            "role": role,
            "company": company,
            "jd": data.get("jd", ""),
            "location": data.get("location", "Singapore"),
            "url": data.get("url", ""),
            "status": "wishlist",
            "date": __import__("datetime").date.today().strftime("%d/%m/%Y"),
            "notes": "",
            "salary": "",
            "isDemo": False,
            "fromBookmarklet": True
        }

        saved.append(new_job)
        with open(jobs_file, "w") as f:
            json.dump(saved, f)

        resp = jsonify({"success": True, "job": new_job})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp

    except Exception as e:
        resp = jsonify({"success": False, "error": str(e)})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 500


@app.route("/api/pending-count", methods=["GET"])
def pending_count():
    """Returns how many jobs are queued — does NOT clear the file"""
    import json, os
    jobs_file = os.path.join(BASE_DIR, "bookmarked_jobs.json")
    if not os.path.exists(jobs_file):
        return jsonify({"count": 0})
    try:
        saved = json.load(open(jobs_file))
        return jsonify({"count": len(saved)})
    except:
        return jsonify({"count": 0})


@app.route("/api/bookmarklet-jobs", methods=["GET"])
def bookmarklet_jobs():
    """Frontend calls this to pull queued jobs — clears file after sending"""
    import json, os
    jobs_file = os.path.join(BASE_DIR, "bookmarked_jobs.json")
    if not os.path.exists(jobs_file):
        return jsonify({"jobs": []})
    try:
        with open(jobs_file, "r") as f:
            saved = json.load(f)
        with open(jobs_file, "w") as f:
            json.dump([], f)
        return jsonify({"jobs": saved})
    except Exception as e:
        return jsonify({"jobs": [], "error": str(e)})


@app.route("/api/bookmarklet-bulk", methods=["POST", "OPTIONS"])
def bookmarklet_bulk():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response

    data = request.json
    incoming_jobs = data.get("jobs", [])

    if not incoming_jobs:
        resp = jsonify({"success": False, "error": "No jobs provided"})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    import json, os, time
    from datetime import date

    jobs_file = os.path.join(BASE_DIR, "bookmarked_jobs.json")

    try:
        if os.path.exists(jobs_file):
            with open(jobs_file, "r") as f:
                saved = json.load(f)
        else:
            saved = []

        # Avoid duplicates by URL or title+company combo
        seen_urls = set()
        seen_tc   = set()
        for j in saved:
            u = j.get("url","").split("?")[0]
            tc = (j.get("role","").strip().lower() + "|" + j.get("company","").strip().lower())
            if u: seen_urls.add(u)
            seen_tc.add(tc)

        added = 0
        for job in incoming_jobs:
            u  = job.get("url","").split("?")[0]
            tc = (job.get("role","").strip().lower() + "|" + job.get("company","").strip().lower())
            if (u and u in seen_urls) or tc in seen_tc:
                continue
            new_job = {
                "id": int(time.time() * 1000) + added,
                "role": job.get("role", "").strip(),
                "company": job.get("company", "").strip(),
                "jd": job.get("jd", ""),
                "location": job.get("location", "Singapore"),
                "url": job.get("url", ""),
                "status": "wishlist",
                "date": date.today().strftime("%d/%m/%Y"),
                "notes": "",
                "salary": "",
                "isDemo": False,
                "fromBookmarklet": True
            }
            saved.append(new_job)
            if u: seen_urls.add(u)
            seen_tc.add(tc)
            added += 1

        with open(jobs_file, "w") as f:
            json.dump(saved, f)

        resp = jsonify({"success": True, "count": added, "total": len(incoming_jobs)})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp

    except Exception as e:
        resp = jsonify({"success": False, "error": str(e)})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 500


@app.route("/ping")
def ping():
    return "ok", 200


@app.route("/capture")
def capture():
    """Bookmarklet redirects here with job details as URL params"""
    title = request.args.get("title", "").strip()
    company = request.args.get("company", "").strip()
    location = request.args.get("location", "Singapore").strip()
    url = request.args.get("url", "").strip()
    jd = request.args.get("jd", "").strip()

    if not title:
        title = "Unknown Role"
    if not company:
        company = "Unknown Company"

    import json, os, time
    from datetime import date

    jobs_file = os.path.join(BASE_DIR, "bookmarked_jobs.json")
    try:
        existing = json.load(open(jobs_file)) if os.path.exists(jobs_file) else []
    except:
        existing = []

    # Dedup check
    clean_url = url.split("?")[0]
    already = any(j.get("url","").split("?")[0] == clean_url or
                  (j.get("role","") == title and j.get("company","") == company)
                  for j in existing)

    if not already:
        existing.append({
            "id": int(time.time() * 1000),
            "role": title,
            "company": company,
            "location": location,
            "url": url,
            "jd": jd,
            "status": "wishlist",
            "date": date.today().strftime("%d/%m/%Y"),
            "notes": "",
            "salary": "",
            "isDemo": False,
            "fromBookmarklet": True
        })
        with open(jobs_file, "w") as f:
            json.dump(existing, f)
        msg = f"✅ <strong>{title}</strong> at <strong>{company}</strong> added to your Job Tracker!"
        color = "#15803d"
    else:
        msg = f"⚠️ <strong>{title}</strong> at <strong>{company}</strong> is already in your tracker."
        color = "#c2410c"

    app_url = request.host_url.rstrip('/')
    return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Job Saved!</title>
<style>
  body {{ font-family: -apple-system, sans-serif; background: #f8fafc; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }}
  .card {{ background: white; border-radius: 16px; padding: 40px; max-width: 420px; width: 90%; box-shadow: 0 4px 24px rgba(0,0,0,0.1); text-align: center; }}
  h2 {{ color: {color}; margin-bottom: 8px; font-size: 22px; }}
  p {{ color: #64748b; margin-bottom: 24px; font-size: 15px; line-height: 1.5; }}
  .btn {{ display: inline-block; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 15px; cursor: pointer; border: none; margin: 6px; }}
  .btn-primary {{ background: #6366f1; color: white; }}
  .btn-ghost {{ background: #f1f5f9; color: #475569; }}
</style>
</head><body>
<div class="card">
  <div style="font-size:48px;margin-bottom:16px;">{'🎯' if not already else '📌'}</div>
  <h2>{'Job Saved!' if not already else 'Already Saved'}</h2>
  <p>{msg}</p>
  <a href="{app_url}" class="btn btn-primary">Open Job Tracker</a>
  <button onclick="history.back()" class="btn btn-ghost">← Back to LinkedIn</button>
</div>
<script>
  // Auto-close and go back to LinkedIn after 3 seconds if opened in same tab
  setTimeout(function() {{ history.back(); }}, 3000);
</script>
</body></html>"""


@app.route("/capture-bulk", methods=["POST"])
def capture_bulk():
    import json, os, time
    from datetime import date

    raw = request.form.get("jobs", "[]")
    try:
        incoming = json.loads(raw)
    except:
        return "Invalid data", 400

    jobs_file = os.path.join(BASE_DIR, "bookmarked_jobs.json")
    try:
        existing = json.load(open(jobs_file)) if os.path.exists(jobs_file) else []
    except:
        existing = []

    # Build lookup sets for both URL and title+company
    seen_urls = set()
    seen_tc   = set()
    for j in existing:
        u = j.get("url","").split("?")[0]
        tc = (j.get("role","").strip().lower() + "|" + j.get("company","").strip().lower())
        if u: seen_urls.add(u)
        seen_tc.add(tc)

    added = 0
    for job in incoming:
        u  = job.get("url","").split("?")[0]
        tc = (job.get("role","").strip().lower() + "|" + job.get("company","").strip().lower())
        if (u and u in seen_urls) or tc in seen_tc:
            continue
        existing.append({
            "id": int(time.time() * 1000) + added,
            "role": job.get("role","").strip(),
            "company": job.get("company","").strip(),
            "location": job.get("location","Singapore"),
            "url": job.get("url",""),
            "jd": "",
            "status": "wishlist",
            "roleType": job.get("roleType","Business Analyst"),
            "priority": job.get("priority","Medium"),
            "source": "LinkedIn",
            "dateApplied": date.today().isoformat(),
            "notes": "", "salary": "", "isDemo": False,
            "fromBookmarklet": True, "checklist": {}
        })
        if u: seen_urls.add(u)
        seen_tc.add(tc)
        added += 1

    with open(jobs_file, "w") as f:
        json.dump(existing, f)

    # Redirect back to the tracker — user lands there and clicks "Import Pending Jobs"
    return redirect(f"/?imported={added}")


# ═══════════════════════════════════════════════════════════════
# JOB DISCOVERY — Scrape Indeed, JobStreet, Workable
# ═══════════════════════════════════════════════════════════════

import urllib.parse
import re as _re
import datetime as _dt
from concurrent.futures import ThreadPoolExecutor, as_completed


def _scrape_indeed(keywords, location, max_days):
    """Scrape Indeed job listings using the Indeed API-like endpoints."""
    jobs = []
    try:
        query = urllib.parse.quote_plus(keywords)
        loc = urllib.parse.quote_plus(location)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "https://www.google.com/",
        }

        # Try multiple Indeed domains
        domains = [
            f"https://sg.indeed.com/jobs?q={query}&l={loc}&fromage={max_days}&sort=date&limit=25",
            f"https://www.indeed.com/jobs?q={query}&l={loc}&fromage={max_days}&sort=date&limit=25",
        ]

        from bs4 import BeautifulSoup

        for url in domains:
            try:
                resp = http_requests.get(url, headers=headers, timeout=20, allow_redirects=True)
                if resp.status_code != 200:
                    continue
                soup = BeautifulSoup(resp.text, "html.parser")

                # Try to parse embedded JSON data (Indeed stores job data in script tags)
                import json as _json
                for script in soup.find_all("script", type="application/ld+json"):
                    try:
                        ld_data = _json.loads(script.string or "")
                        if isinstance(ld_data, dict) and ld_data.get("@type") == "ItemList":
                            for item in ld_data.get("itemListElement", []):
                                job_posting = item if item.get("@type") == "JobPosting" else item.get("item", {})
                                if job_posting.get("title"):
                                    jobs.append({
                                        "role": job_posting.get("title", ""),
                                        "company": (job_posting.get("hiringOrganization", {}) or {}).get("name", ""),
                                        "url": job_posting.get("url", ""),
                                        "location": (job_posting.get("jobLocation", [{}]) or [{}])[0].get("address", {}).get("addressLocality", location) if isinstance(job_posting.get("jobLocation"), list) else location,
                                        "jd": (job_posting.get("description", "") or "")[:2000],
                                        "platform": "Indeed",
                                        "postedDaysAgo": None,
                                    })
                    except Exception:
                        continue

                # Fallback: Parse HTML cards
                if not jobs:
                    cards = soup.select("div.job_seen_beacon, div.cardOutline, div[class*='result'], td.resultContent")
                    for card in cards[:30]:
                        try:
                            title_el = card.select_one("h2.jobTitle a, h2 a, a[data-jk], span[id*='jobTitle']")
                            if not title_el:
                                title_el = card.select_one("a[class*='title'], h2 span")
                            title = title_el.get_text(strip=True) if title_el else ""
                            href = ""
                            if title_el:
                                if title_el.name == "a" and title_el.get("href"):
                                    href = title_el["href"]
                                    if href.startswith("/"):
                                        href = f"https://sg.indeed.com{href}"
                                elif title_el.get("data-jk"):
                                    href = f"https://sg.indeed.com/viewjob?jk={title_el['data-jk']}"
                                else:
                                    parent_a = title_el.find_parent("a")
                                    if parent_a and parent_a.get("href"):
                                        href = parent_a["href"]
                                        if href.startswith("/"):
                                            href = f"https://sg.indeed.com{href}"

                            company_el = card.select_one("[data-testid='company-name'], span.companyName, span[class*='company']")
                            company = company_el.get_text(strip=True) if company_el else ""

                            loc_el = card.select_one("[data-testid='text-location'], div.companyLocation")
                            job_loc = loc_el.get_text(strip=True) if loc_el else location

                            snippet_el = card.select_one("div.job-snippet, ul[style], div[class*='snippet']")
                            snippet = snippet_el.get_text(strip=True) if snippet_el else ""

                            if title:
                                jobs.append({
                                    "role": title,
                                    "company": company,
                                    "url": href,
                                    "location": job_loc,
                                    "jd": snippet[:2000],
                                    "platform": "Indeed",
                                    "postedDaysAgo": None,
                                })
                        except Exception:
                            continue

                if jobs:
                    break  # Got results from this domain, no need to try next
            except Exception:
                continue

    except Exception as e:
        return jobs, str(e)

    return jobs, None


def _scrape_jobstreet(keywords, location, max_days):
    """Scrape JobStreet using their GraphQL API endpoint."""
    jobs = []
    try:
        query = keywords
        # JobStreet (now part of SEEK) uses a GraphQL API
        api_url = "https://xapi.supercharge-srp.co/job-search/graphql?country=sg&is498=true"

        payload = {
            "query": "query getJobs($keyword: String, $jobFunctions: [Int], $locations: [Int], $salaryType: Int, $salaryRange: [Int], $careerLevels: [Int], $page: Int, $country: String, $sort: String, $dateRange: String) { jobs(keyword: $keyword, jobFunctions: $jobFunctions, locations: $locations, salaryType: $salaryType, salaryRange: $salaryRange, careerLevels: $careerLevels, page: $page, country: $country, sort: $sort, dateRange: $dateRange) { total jobs { id jobTitle company { name } jobLocation { location } salary { min max type currency } jobUrl postedAt descriptions { items { text } } } } }",
            "variables": {
                "keyword": query,
                "country": "sg",
                "page": 1,
                "sort": "date",
                "dateRange": f"{max_days}d"
            }
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://www.jobstreet.com.sg",
            "Referer": "https://www.jobstreet.com.sg/",
        }

        # Try GraphQL API first
        try:
            resp = http_requests.post(api_url, json=payload, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                job_items = data.get("data", {}).get("jobs", {}).get("jobs", [])
                for item in job_items[:30]:
                    title = item.get("jobTitle", "")
                    company = (item.get("company") or {}).get("name", "")
                    loc_info = item.get("jobLocation", {})
                    job_loc = loc_info.get("location", location) if isinstance(loc_info, dict) else location
                    job_url = item.get("jobUrl", "")
                    if job_url and not job_url.startswith("http"):
                        job_url = f"https://www.jobstreet.com.sg{job_url}"
                    desc_items = (item.get("descriptions") or {}).get("items", [])
                    jd = " ".join([d.get("text", "") for d in desc_items])[:2000] if desc_items else ""

                    if title:
                        jobs.append({
                            "role": title,
                            "company": company,
                            "url": job_url,
                            "location": job_loc if isinstance(job_loc, str) else location,
                            "jd": jd,
                            "platform": "JobStreet",
                            "postedDaysAgo": None,
                        })
        except Exception:
            pass

        # Fallback: scrape HTML
        if not jobs:
            from bs4 import BeautifulSoup
            fallback_url = f"https://www.jobstreet.com.sg/{urllib.parse.quote_plus(keywords).replace('+', '-').lower()}-jobs"
            try:
                resp = http_requests.get(fallback_url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                    "Accept": "text/html",
                }, timeout=15, allow_redirects=True)
                soup = BeautifulSoup(resp.text, "html.parser")

                # Try to find JSON-LD structured data
                for script in soup.find_all("script", type="application/ld+json"):
                    try:
                        ld_data = json.loads(script.string or "")
                        if isinstance(ld_data, dict) and ld_data.get("@type") == "ItemList":
                            for item in ld_data.get("itemListElement", []):
                                jp = item if item.get("@type") == "JobPosting" else item.get("item", {})
                                if jp.get("title"):
                                    jobs.append({
                                        "role": jp.get("title", ""),
                                        "company": (jp.get("hiringOrganization", {}) or {}).get("name", ""),
                                        "url": jp.get("url", ""),
                                        "location": location,
                                        "jd": (jp.get("description", "") or "")[:2000],
                                        "platform": "JobStreet",
                                        "postedDaysAgo": None,
                                    })
                    except Exception:
                        continue

                # Fallback: parse links
                if not jobs:
                    all_links = soup.select("a[href*='/job/'], a[href*='/jobs-']")
                    seen = set()
                    for link in all_links[:30]:
                        href = link.get("href", "")
                        if href not in seen:
                            seen.add(href)
                            title_text = link.get_text(strip=True)
                            if 3 < len(title_text) < 200:
                                full_url = href if href.startswith("http") else f"https://www.jobstreet.com.sg{href}"
                                jobs.append({
                                    "role": title_text,
                                    "company": "",
                                    "url": full_url,
                                    "location": location,
                                    "jd": "",
                                    "platform": "JobStreet",
                                    "postedDaysAgo": None,
                                })
            except Exception:
                pass

    except Exception as e:
        return jobs, str(e)

    return jobs, None


def _scrape_workable(keywords, location, max_days):
    """Search Workable job board using their search API."""
    jobs = []
    try:
        # Workable has a search API
        api_url = "https://jobs.workable.com/api/v1/jobs"
        params = {
            "query": keywords,
            "location": location,
            "limit": 30,
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
        }

        try:
            resp = http_requests.get(api_url, params=params, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                job_items = data if isinstance(data, list) else data.get("results", data.get("jobs", []))
                for item in (job_items or [])[:30]:
                    if isinstance(item, dict):
                        title = item.get("title", item.get("name", ""))
                        company = item.get("company", item.get("organization", {}) if isinstance(item.get("organization"), dict) else {})
                        if isinstance(company, dict):
                            company = company.get("name", "")
                        job_url = item.get("url", item.get("application_url", ""))
                        job_loc = item.get("location", location)
                        if isinstance(job_loc, dict):
                            job_loc = job_loc.get("city", location)
                        jd = (item.get("description", "") or "")[:2000]

                        if title:
                            jobs.append({
                                "role": title,
                                "company": company if isinstance(company, str) else "",
                                "url": job_url,
                                "location": job_loc if isinstance(job_loc, str) else location,
                                "jd": jd,
                                "platform": "Workable",
                                "postedDaysAgo": None,
                            })
        except Exception:
            pass

        # Fallback: HTML scraping
        if not jobs:
            from bs4 import BeautifulSoup
            query = urllib.parse.quote_plus(keywords)
            loc = urllib.parse.quote_plus(location)
            url = f"https://jobs.workable.com/?query={query}&location={loc}"
            try:
                resp = http_requests.get(url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                    "Accept": "text/html",
                }, timeout=15)
                soup = BeautifulSoup(resp.text, "html.parser")

                # Try JSON-LD
                for script in soup.find_all("script", type="application/ld+json"):
                    try:
                        ld_data = json.loads(script.string or "")
                        if isinstance(ld_data, list):
                            for jp in ld_data:
                                if jp.get("@type") == "JobPosting" and jp.get("title"):
                                    jobs.append({
                                        "role": jp["title"],
                                        "company": (jp.get("hiringOrganization", {}) or {}).get("name", ""),
                                        "url": jp.get("url", ""),
                                        "location": location,
                                        "jd": (jp.get("description", "") or "")[:2000],
                                        "platform": "Workable",
                                        "postedDaysAgo": None,
                                    })
                    except Exception:
                        continue

                # Try links
                if not jobs:
                    all_links = soup.select("a[href*='/j/'], a[href*='/view/']")
                    seen = set()
                    for link in all_links[:30]:
                        href = link.get("href", "")
                        if href and href not in seen:
                            seen.add(href)
                            title_text = link.get_text(strip=True)
                            if 3 < len(title_text) < 200:
                                full_url = href if href.startswith("http") else f"https://jobs.workable.com{href}"
                                jobs.append({
                                    "role": title_text,
                                    "company": "",
                                    "url": full_url,
                                    "location": location,
                                    "jd": "",
                                    "platform": "Workable",
                                    "postedDaysAgo": None,
                                })
            except Exception:
                pass

    except Exception as e:
        return jobs, str(e)

    return jobs, None


def _scrape_linkedin_public(keywords, location, max_days):
    """Search LinkedIn public job listings (no login required)."""
    jobs = []
    try:
        query = urllib.parse.quote_plus(keywords)
        loc = urllib.parse.quote_plus(location)
        # LinkedIn public jobs search — f_TPR=r2592000 = last 30 days
        time_filter = "r86400" if max_days <= 1 else "r604800" if max_days <= 7 else "r2592000"
        url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location={loc}&f_TPR={time_filter}&position=1&pageNum=0"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        }

        from bs4 import BeautifulSoup
        resp = http_requests.get(url, headers=headers, timeout=20, allow_redirects=True)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            cards = soup.select("div.base-card, li.result-card, div.job-search-card")
            for card in cards[:30]:
                try:
                    title_el = card.select_one("h3.base-search-card__title, h3[class*='title']")
                    title = title_el.get_text(strip=True) if title_el else ""
                    company_el = card.select_one("h4.base-search-card__subtitle, a[class*='company']")
                    company = company_el.get_text(strip=True) if company_el else ""
                    link_el = card.select_one("a.base-card__full-link, a[class*='job-card']")
                    href = link_el.get("href", "") if link_el else ""
                    loc_el = card.select_one("span.job-search-card__location")
                    job_loc = loc_el.get_text(strip=True) if loc_el else location

                    if title:
                        jobs.append({
                            "role": title,
                            "company": company,
                            "url": href.split("?")[0] if href else "",
                            "location": job_loc,
                            "jd": "",
                            "platform": "LinkedIn",
                            "postedDaysAgo": None,
                        })
                except Exception:
                    continue
    except Exception as e:
        return jobs, str(e)

    return jobs, None


def _scrape_glassdoor(keywords, location, max_days):
    """Search Glassdoor job listings."""
    jobs = []
    try:
        query = urllib.parse.quote_plus(keywords)
        url = f"https://www.glassdoor.com/Job/singapore-{query.replace('+', '-').lower()}-jobs-SRCH_IL.0,9_IC3235921_KO10,{10+len(keywords)}.htm?fromAge={max_days}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html",
        }

        from bs4 import BeautifulSoup
        resp = http_requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")

            # Try JSON-LD structured data
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    ld_data = json.loads(script.string or "")
                    if isinstance(ld_data, list):
                        for item in ld_data:
                            if item.get("@type") == "JobPosting":
                                jobs.append({
                                    "role": item.get("title", ""),
                                    "company": (item.get("hiringOrganization", {}) or {}).get("name", ""),
                                    "url": item.get("url", ""),
                                    "location": location,
                                    "jd": (item.get("description", "") or "")[:2000],
                                    "platform": "Glassdoor",
                                    "postedDaysAgo": None,
                                })
                    elif isinstance(ld_data, dict) and ld_data.get("@type") == "JobPosting":
                        jobs.append({
                            "role": ld_data.get("title", ""),
                            "company": (ld_data.get("hiringOrganization", {}) or {}).get("name", ""),
                            "url": ld_data.get("url", ""),
                            "location": location,
                            "jd": (ld_data.get("description", "") or "")[:2000],
                            "platform": "Glassdoor",
                            "postedDaysAgo": None,
                        })
                except Exception:
                    continue

            # Fallback: parse job cards
            if not jobs:
                cards = soup.select("li.react-job-listing, div[data-test='jobListing']")
                for card in cards[:30]:
                    try:
                        title_el = card.select_one("a[data-test='job-link'], a.jobLink")
                        title = title_el.get_text(strip=True) if title_el else ""
                        href = title_el.get("href", "") if title_el else ""
                        if href and not href.startswith("http"):
                            href = f"https://www.glassdoor.com{href}"
                        company_el = card.select_one("div.job-search-key-l2wjgv, span.EmployerProfile")
                        company = company_el.get_text(strip=True) if company_el else ""
                        if title:
                            jobs.append({
                                "role": title,
                                "company": company,
                                "url": href,
                                "location": location,
                                "jd": "",
                                "platform": "Glassdoor",
                                "postedDaysAgo": None,
                            })
                    except Exception:
                        continue

    except Exception as e:
        return jobs, str(e)

    return jobs, None


def _ai_score_discovered_jobs(jobs_list):
    """Score discovered jobs with AI using active profile context."""
    if not jobs_list:
        return jobs_list
    
    # Only score jobs that have some useful text (title/company at minimum)
    to_score = [j for j in jobs_list if j.get("role")]
    if not to_score:
        return jobs_list

    # Get active profile for personalized scoring
    profile = get_active_profile()
    profile_summary = f"{profile.get('name', 'Candidate')} — {profile.get('headline', 'Professional')}. Skills: {', '.join(profile.get('skills', [])[:10])}. {profile.get('summary', '')[:200]}"

    # Build compact job batch for AI
    batch_text = ""
    for i, j in enumerate(to_score[:30]):  # Limit to 30 for API limits
        jd_snippet = (j.get("jd", "") or "")[:200]
        batch_text += f"\nJOB {i+1}: {j.get('role','')} at {j.get('company','')} ({j.get('platform','')}) — {jd_snippet}\n---"

    prompt = f"""You are a career coach for the Singapore job market.

CANDIDATE PROFILE:
{profile_summary}

SCORING RULES:
- Score 1-10 based on fit with the candidate's profile
- +2 for in-house product/tech companies, -2 for consulting firms (max 4/10)
- Score 0 if "no visa sponsorship" detected
- Labels: 🔥 Strong Match (9-10), ✅ Good Fit (7-8), 🟡 Possible (5-6), ❌ Weak Fit (1-4)
- Priority: Apply Today, Apply This Week, Lower Priority, Skip

JOBS:
{batch_text}

Return ONLY a JSON array (no markdown), one object per job:
[{{"idx": 0, "score": 8, "label": "✅ Good Fit", "reason": "Two sentences.", "priority": "Apply This Week"}}]
Score every job listed. Use idx starting from 0."""

    try:
        result = call_claude(prompt)
        clean = _re.sub(r'```json|```', '', result).strip()
        rankings = json.loads(clean)
        for r in rankings:
            idx = r.get("idx", -1)
            if 0 <= idx < len(to_score):
                to_score[idx]["aiScore"] = r.get("score")
                to_score[idx]["aiLabel"] = r.get("label", "")
                to_score[idx]["aiReason"] = r.get("reason", "")
                to_score[idx]["aiPriority"] = r.get("priority", "")
    except Exception as e:
        print(f"[Discovery] AI scoring failed: {e}")

    return jobs_list


@app.route("/api/discover-jobs", methods=["POST"])
def discover_jobs():
    """Search multiple job platforms and return AI-scored results."""
    data = request.json or {}
    keywords = data.get("keywords", "Product Owner")
    location = data.get("location", "Singapore")
    max_days = data.get("maxDays", 30)
    platforms = data.get("platforms", ["indeed", "jobstreet", "workable", "linkedin", "glassdoor"])

    scrapers = {
        "indeed": _scrape_indeed,
        "jobstreet": _scrape_jobstreet,
        "workable": _scrape_workable,
        "linkedin": _scrape_linkedin_public,
        "glassdoor": _scrape_glassdoor,
    }

    all_jobs = []
    details = {}

    # Scrape platforms in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {}
        for platform in platforms:
            if platform in scrapers:
                futures[executor.submit(scrapers[platform], keywords, location, max_days)] = platform

        for future in as_completed(futures):
            platform = futures[future]
            try:
                jobs, err = future.result(timeout=30)
                details[platform] = {"count": len(jobs), "error": err}
                all_jobs.extend(jobs)
            except Exception as e:
                details[platform] = {"count": 0, "error": str(e)}

    # Deduplicate by URL
    seen_urls = set()
    unique_jobs = []
    for j in all_jobs:
        clean_url = (j.get("url") or "").split("?")[0]
        tc = (j.get("role", "").lower() + "|" + j.get("company", "").lower())
        if clean_url and clean_url in seen_urls:
            continue
        if tc in seen_urls:
            continue
        if clean_url:
            seen_urls.add(clean_url)
        seen_urls.add(tc)
        unique_jobs.append(j)

    # Filter old jobs if we have date info
    if max_days:
        filtered = []
        for j in unique_jobs:
            if j.get("postedDaysAgo") is not None:
                if j["postedDaysAgo"] <= max_days:
                    filtered.append(j)
            else:
                # No date info — keep it
                filtered.append(j)
        unique_jobs = filtered

    # AI score the results
    if unique_jobs:
        unique_jobs = _ai_score_discovered_jobs(unique_jobs)

    # Sort by score descending
    unique_jobs.sort(key=lambda j: j.get("aiScore") or 0, reverse=True)

    return jsonify({
        "jobs": unique_jobs,
        "total": len(unique_jobs),
        "details": details
    })


# ═══════════════════════════════════════════════════════════════
# BULK AUTO-APPLY — Generate docs for multiple jobs at once
# ═══════════════════════════════════════════════════════════════

@app.route("/api/bulk-apply", methods=["POST"])
def bulk_apply():
    """
    Bulk auto-apply: for each selected job that has a JD and score >= threshold,
    generate tailored resume + cover letter .docx via gen_docs.js.
    Returns progress updates and final summary.
    """
    import subprocess, tempfile, base64 as b64mod

    data = request.json or {}
    job_ids = data.get("jobIds", [])
    if not job_ids:
        return jsonify({"error": "No jobs selected"}), 400

    # Load jobs from localStorage (sent from frontend)
    incoming_jobs = data.get("jobs", [])
    if not incoming_jobs:
        return jsonify({"error": "No job data provided"}), 400

    results = []
    generated = 0
    skipped = 0
    errors = 0

    for job in incoming_jobs:
        job_id = str(job.get("id", ""))
        if job_id not in [str(jid) for jid in job_ids]:
            continue

        role = job.get("role", "Unknown").strip()
        company = job.get("company", "Unknown").strip()
        jd = (job.get("jd") or "").strip()
        role_type = job.get("roleType", "Business Analyst")

        # Skip if docs already generated
        if job.get("resume_docx_b64"):
            results.append({"id": job_id, "status": "skipped", "reason": "Docs already exist"})
            skipped += 1
            continue

        # Skip if no JD
        if not jd or len(jd) < 50:
            results.append({"id": job_id, "status": "skipped", "reason": "No JD available"})
            skipped += 1
            continue

        try:
            script_path = os.path.join(BASE_DIR, "gen_docs.js")
            ai_role = is_ai_role(jd, role_type)
            payload_str = json.dumps({
                "role": role, "company": company,
                "jd": jd[:3000], "roleType": role_type,
                "outputDir": tempfile.gettempdir(), "isAI": ai_role
            })
            res = subprocess.run(
                ["node", script_path, payload_str],
                capture_output=True, text=True, timeout=30
            )
            if res.returncode == 0:
                out = json.loads(res.stdout.strip())
                with open(out["resume"], "rb") as f:
                    resume_b64 = b64mod.b64encode(f.read()).decode()
                with open(out["cover"], "rb") as f:
                    cover_b64 = b64mod.b64encode(f.read()).decode()

                results.append({
                    "id": job_id,
                    "status": "generated",
                    "resume_docx_b64": resume_b64,
                    "cover_docx_b64": cover_b64,
                    "resume_variant": out.get("variant", "BA"),
                    "resume_filename": f"Resume_{company.replace(' ','_')}.docx",
                    "cover_filename": f"CoverLetter_{company.replace(' ','_')}.docx",
                })
                generated += 1
            else:
                results.append({"id": job_id, "status": "error", "reason": res.stderr[:100]})
                errors += 1
        except subprocess.TimeoutExpired:
            results.append({"id": job_id, "status": "error", "reason": "Timed out"})
            errors += 1
        except Exception as e:
            results.append({"id": job_id, "status": "error", "reason": str(e)[:100]})
            errors += 1

    return jsonify({
        "results": results,
        "generated": generated,
        "skipped": skipped,
        "errors": errors,
        "total": len(job_ids)
    })


# ═══════════════════════════════════════════════════════════════
# AGENT SYSTEM
# ═══════════════════════════════════════════════════════════════

import threading
import datetime

AGENT_CRON_SECRET    = os.environ.get("AGENT_CRON_SECRET", "jobhunt2025")
NOTIFICATION_PHONE   = os.environ.get("NOTIFICATION_PHONE", "")   # e.g. whatsapp:+6590256503
TWILIO_ACCOUNT_SID   = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN    = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM = os.environ.get("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")  # Twilio sandbox

def _get_twilio_sid():   return os.environ.get("TWILIO_ACCOUNT_SID", "") or get_setting("TWILIO_ACCOUNT_SID")
def _get_twilio_token(): return os.environ.get("TWILIO_AUTH_TOKEN", "") or get_setting("TWILIO_AUTH_TOKEN")
def _get_whatsapp_to():  return os.environ.get("NOTIFICATION_PHONE", "") or get_setting("NOTIFICATION_PHONE")


def send_whatsapp(message):
    """Send a WhatsApp message via Twilio API."""
    sid   = _get_twilio_sid()
    token = _get_twilio_token()
    to    = _get_whatsapp_to()
    frm   = TWILIO_WHATSAPP_FROM
    if not sid or not token or not to:
        print("WhatsApp not configured — set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, NOTIFICATION_PHONE")
        return False
    try:
        # Ensure to/from are prefixed with whatsapp:
        if not to.startswith("whatsapp:"): to = f"whatsapp:{to}"
        if not frm.startswith("whatsapp:"): frm = f"whatsapp:{frm}"
        url  = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
        resp = http_requests.post(url, auth=(sid, token), data={"From": frm, "To": to, "Body": message})
        if resp.status_code in (200, 201):
            print(f"[WhatsApp] Sent: {message[:60]}...")
            return True
        else:
            print(f"[WhatsApp] Failed {resp.status_code}: {resp.text[:200]}")
            return False
    except Exception as e:
        print(f"[WhatsApp] Error: {e}")
        return False

# Keep send_email as alias so existing calls still work
def send_email(subject, html_body):
    # Strip HTML tags for WhatsApp plain text
    import re as _re
    text = _re.sub(r'<[^>]+>', '', html_body)
    text = _re.sub(r'\s+', ' ', text).strip()
    msg  = f"*{subject}*\n\n{text[:1000]}"
    return send_whatsapp(msg)


def _send_whatsapp_summary(summary):
    """Send a concise, well-formatted WhatsApp summary after agent run."""
    top = summary.get("top_jobs", [])
    labels = {"import": "Import", "cron": "Daily 9AM", "manual": "Manual"}
    trigger = labels.get(summary.get("trigger", ""), "Run")
    now_str = datetime.datetime.now().strftime("%d %b %H:%M")

    msg = f"🤖 *Job Agent Complete* — {trigger} · {now_str}\n\n"
    msg += f"📊 *{summary['total']}* processed · *{summary['scored']}* scored · *{summary['docs']}* docs ready\n\n"

    if top:
        msg += "🏆 *Top Matches:*\n"
        for j in top[:5]:
            score = j.get("aiScore", "?")
            company = j.get("company", "")
            role = j.get("role", "")
            priority = j.get("aiPriority", "")
            has_docs = "📄" if j.get("resume_docx_b64") else ""
            msg += f"• {score}/10 — {company} · {role} {has_docs}\n"
            if priority:
                msg += f"  → _{priority}_\n"
    else:
        msg += "No scored jobs yet.\n"

    msg += "\n🔗 Open tracker: https://job-hunt-app-r7my.onrender.com"
    return send_whatsapp(msg)


def agent_process_job(job):
    """Full agent pipeline for one job: score → generate docs → save."""
    log     = []
    job_id  = job.get("id")
    role    = job.get("role", "Unknown")
    company = job.get("company", "Unknown")
    jd      = job.get("jd", "") or ""

    log.append(f"Processing: {role} @ {company}")

    # STEP 1: AI Score
    if jd and len(jd) > 50 and job.get("aiScore") is None:
        try:
            P = get_active_profile()
            skills_short = ', '.join(P.get('skills', [])[:8])
            prompt = f"""You are a career coach for the tech job market.

CANDIDATE: {P.get('name','Unknown')} — {P.get('headline','')}
Summary: {P.get('summary','')[:200]}
Skills: {skills_short}
Certification: {P.get('certification','')}
Target: In-house product roles (NOT consulting).

SCORING RULES:
- Score 1-10 based on fit
- +2 for in-house product companies (Grab, Sea, Airwallex, Stripe, GovTech, startups)
- -2 for consulting (KPMG, Deloitte, Accenture, Big4) — max 4/10 for consulting roles
- Score 0 if JD says "no visa sponsorship"
- Labels: 🔥 Strong Match (9-10), ✅ Good Fit (7-8), 🟡 Possible (5-6), ❌ Weak Fit (1-4)
- Priority: Apply Today, Apply This Week, Lower Priority, Skip

JOB:
Title: {role}
Company: {company}
JD: {jd[:500]}

Return ONLY valid JSON, no markdown:
{{"score": 8, "label": "✅ Good Fit", "reason": "Two sentence reason.", "priority": "Apply This Week"}}"""

            result = call_claude(prompt)
            clean  = result.strip().strip("```json").strip("```").strip()
            # Find JSON object in response
            import re
            m = re.search(r'\{.*\}', clean, re.DOTALL)
            if m:
                scored = json.loads(m.group())
                job["aiScore"]    = scored.get("score")
                job["aiLabel"]    = scored.get("label", "")
                job["aiReason"]   = scored.get("reason", "")
                job["aiPriority"] = scored.get("priority", "")
                log.append(f"  Scored: {job['aiLabel']} ({job['aiScore']}/10)")
        except Exception as e:
            log.append(f"  Scoring failed: {e}")
    elif job.get("aiScore") is not None:
        log.append(f"  Already scored: {job.get('aiLabel')} ({job.get('aiScore')}/10)")
    else:
        log.append(f"  No JD — skipping score")

    # STEP 2: Generate docs (score >= 5, no docs yet)
    score = job.get("aiScore") or 0
    if score >= 5 and not job.get("resume_docx_b64"):
        try:
            import subprocess, tempfile, base64 as b64mod
            script_path = os.path.join(BASE_DIR, "gen_docs.js")
            ai_role     = is_ai_role(jd, job.get("roleType", ""))
            # Pass custom profile if applicable
            P_agent = get_active_profile()
            is_custom_agent = (P_agent.get("name") != DEFAULT_PROFILE.get("name") or
                               P_agent.get("email") != DEFAULT_PROFILE.get("email"))
            payload_str = json.dumps({
                "role": role, "company": company,
                "jd": jd[:3000], "roleType": job.get("roleType", "Business Analyst"),
                "outputDir": tempfile.gettempdir(), "isAI": ai_role,
                "profile": P_agent if is_custom_agent else None
            })
            res = subprocess.run(
                ["node", script_path, payload_str],
                capture_output=True, text=True, timeout=30
            )
            if res.returncode == 0:
                out = json.loads(res.stdout.strip())
                with open(out["resume"], "rb") as f:
                    job["resume_docx_b64"]     = b64mod.b64encode(f.read()).decode()
                with open(out["cover"], "rb") as f:
                    job["cover_docx_b64"]      = b64mod.b64encode(f.read()).decode()
                job["resume_variant"]          = out.get("variant", "BA")
                job["resume_filename"]         = out.get("resume", "").split("/")[-1]
                job["cover_filename"]          = out.get("cover", "").split("/")[-1]
                job["resume_generated_at"]     = datetime.datetime.utcnow().isoformat()
                log.append(f"  Docs generated ({job['resume_variant']} template)")
            else:
                log.append(f"  Doc gen failed: {res.stderr[:80]}")
        except Exception as e:
            log.append(f"  Doc gen error: {e}")
    elif score < 5:
        log.append(f"  Score {score}/10 — skipping docs")
    else:
        log.append(f"  Docs already exist")

    # STEP 3: Save to Supabase
    try:
        sb = get_supabase()
        if sb:
            row = {
                "id":                  str(job.get("id", "")),
                "linkedInId":          job.get("linkedInId", ""),
                "role":                role,
                "company":             company,
                "status":              job.get("status", "saved"),
                "url":                 job.get("url", ""),
                "jd":                  jd[:8000],
                "roleType":            job.get("roleType", ""),
                "source":              job.get("source", ""),
                "salary":              job.get("salary", ""),
                "dateApplied":         job.get("dateApplied", ""),
                "aiScore":             job.get("aiScore"),
                "aiLabel":             job.get("aiLabel", ""),
                "aiReason":            job.get("aiReason", ""),
                "aiPriority":          job.get("aiPriority", ""),
                "notes":               job.get("notes", ""),
                "resume_docx_b64":     (job.get("resume_docx_b64") or "")[:500000],
                "cover_docx_b64":      (job.get("cover_docx_b64") or "")[:500000],
                "resume_variant":      job.get("resume_variant", ""),
                "resume_filename":     job.get("resume_filename", ""),
                "cover_filename":      job.get("cover_filename", ""),
                "resume_generated_at": job.get("resume_generated_at", ""),
            }
            sb.table("jobs").upsert(row, on_conflict="id").execute()
            log.append(f"  Saved to Supabase")
    except Exception as e:
        log.append(f"  Supabase save failed: {e}")

    return job, log


def agent_run(jobs_to_process, trigger="manual"):
    """Run agent pipeline over list of jobs, then notify."""
    results  = []
    all_logs = []
    scored   = []
    docs_gen = []

    for job in jobs_to_process:
        enriched, log = agent_process_job(job)
        all_logs.extend(log)
        results.append(enriched)
        if enriched.get("aiScore") is not None:
            scored.append(enriched)
        if enriched.get("resume_docx_b64"):
            docs_gen.append(enriched)

    top_jobs = sorted(scored, key=lambda j: j.get("aiScore", 0), reverse=True)[:5]
    summary  = {
        "trigger":  trigger,
        "total":    len(jobs_to_process),
        "scored":   len(scored),
        "docs":     len(docs_gen),
        "top_jobs": top_jobs,
        "logs":     all_logs,
        "results":  results,
    }
    _send_agent_notifications(summary)
    return summary


def _send_agent_notifications(summary):
    """Send email notification after agent run."""
    top     = summary["top_jobs"]
    labels  = {"import": "📥 Auto (import)", "cron": "⏰ Daily", "manual": "▶ Manual"}
    trigger_label = labels.get(summary["trigger"], "▶ Run")
    now_str = datetime.datetime.now().strftime("%d %b %Y %H:%M")

    # Email only
    rows_html = ""
    for j in top:
        has_docs = "✅ Ready" if j.get("resume_docx_b64") else "—"
        rows_html += (
            f"<tr>"
            f"<td style='padding:10px;border-bottom:1px solid #e5e7eb;'>"
            f"<a href='{j.get('url','#')}' style='font-weight:700;color:#1d4ed8;'>{j.get('company','')}</a><br>"
            f"<span style='font-size:13px;color:#374151;'>{j.get('role','')}</span></td>"
            f"<td style='padding:10px;border-bottom:1px solid #e5e7eb;text-align:center;font-weight:700;'>{j.get('aiScore','?')}/10</td>"
            f"<td style='padding:10px;border-bottom:1px solid #e5e7eb;'>{j.get('aiLabel','')}</td>"
            f"<td style='padding:10px;border-bottom:1px solid #e5e7eb;font-size:12px;color:#6b7280;'>{j.get('aiReason','')}</td>"
            f"<td style='padding:10px;border-bottom:1px solid #e5e7eb;text-align:center;'>{has_docs}</td>"
            f"</tr>"
        )

    html = f"""<html><body style="font-family:-apple-system,sans-serif;background:#f9fafb;padding:20px;">
<div style="max-width:720px;margin:0 auto;background:white;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.1);">
  <div style="background:linear-gradient(135deg,#1d4ed8,#7c3aed);padding:28px 32px;color:white;">
    <h1 style="margin:0;font-size:22px;">🤖 Job Agent Complete</h1>
    <p style="margin:6px 0 0;opacity:.85;">{trigger_label} · {now_str}</p>
  </div>
  <div style="padding:24px 32px;">
    <div style="display:flex;gap:16px;margin-bottom:24px;">
      <div style="flex:1;background:#eff6ff;border-radius:8px;padding:14px;text-align:center;">
        <div style="font-size:28px;font-weight:700;color:#1d4ed8;">{summary['total']}</div>
        <div style="font-size:12px;color:#6b7280;">Processed</div>
      </div>
      <div style="flex:1;background:#f0fdf4;border-radius:8px;padding:14px;text-align:center;">
        <div style="font-size:28px;font-weight:700;color:#16a34a;">{summary['scored']}</div>
        <div style="font-size:12px;color:#6b7280;">Scored</div>
      </div>
      <div style="flex:1;background:#faf5ff;border-radius:8px;padding:14px;text-align:center;">
        <div style="font-size:28px;font-weight:700;color:#7c3aed;">{summary['docs']}</div>
        <div style="font-size:12px;color:#6b7280;">Docs Ready</div>
      </div>
    </div>
    {'<h2 style="font-size:16px;margin-bottom:12px;">🏆 Top Matches</h2><table style="width:100%;border-collapse:collapse;"><thead><tr style="background:#f3f4f6;"><th style="padding:10px;text-align:left;font-size:12px;color:#6b7280;">JOB</th><th style="padding:10px;font-size:12px;color:#6b7280;">SCORE</th><th style="padding:10px;font-size:12px;color:#6b7280;">FIT</th><th style="padding:10px;font-size:12px;color:#6b7280;">REASON</th><th style="padding:10px;font-size:12px;color:#6b7280;">DOCS</th></tr></thead><tbody>' + rows_html + '</tbody></table>' if top else '<p style="color:#6b7280;">No scored jobs yet.</p>'}
  </div>
  <div style="background:#f3f4f6;padding:16px 32px;text-align:center;font-size:13px;color:#6b7280;">
    Open your <a href="https://job-hunt-app.onrender.com" style="color:#1d4ed8;">Job Tracker</a> to download documents
  </div>
</div></body></html>"""

    send_email(
        subject=f"🤖 Agent: {summary['scored']} scored, {summary['docs']} docs ready — {datetime.datetime.now().strftime('%d %b')}",
        html_body=html
    )

    # Also send concise WhatsApp summary
    _send_whatsapp_summary(summary)


# ─── AUTONOMOUS AGENT PIPELINE ───────────────────────────────
def agent_autonomous_pipeline(config=None):
    """
    Fully autonomous agentic workflow:
      Step 1: Discover new jobs from Indeed/JobStreet/Workable
      Step 2: Scrape LinkedIn saved jobs (if credentials available)
      Step 3: Merge & deduplicate all discovered jobs into Supabase
      Step 4: AI-score all unscored jobs
      Step 5: Generate resume + cover letter for top-scoring jobs
      Step 6: Save everything to Supabase
      Step 7: Send WhatsApp + email notification summary
    """
    config = config or {}
    pipeline_log = []
    P = get_active_profile()

    def log(msg):
        pipeline_log.append(msg)
        print(f"[Agent] {msg}")

    log(f"🤖 Starting autonomous pipeline for {P.get('name', 'user')}")

    # ── Step 1: Job Discovery from web scrapers ──
    discovered_jobs = []
    keywords = config.get("keywords", P.get("headline", "Product Manager"))
    location = config.get("location", "Singapore")
    max_days = config.get("max_days", 30)
    platforms = config.get("platforms", ["indeed", "jobstreet", "workable"])

    if platforms:
        from concurrent.futures import ThreadPoolExecutor
        scraper_map = {
            "indeed": _scrape_indeed,
            "jobstreet": _scrape_jobstreet,
            "workable": _scrape_workable,
        }
        log(f"Step 1: Discovering jobs — keywords='{keywords}', location='{location}', platforms={platforms}")
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = {}
            for p_name in platforms:
                fn = scraper_map.get(p_name)
                if fn:
                    futures[p_name] = pool.submit(fn, keywords, location, max_days)
            for p_name, fut in futures.items():
                try:
                    results = fut.result(timeout=60)
                    discovered_jobs.extend(results)
                    log(f"  {p_name}: {len(results)} jobs found")
                except Exception as e:
                    log(f"  {p_name}: error — {str(e)[:60]}")

        # Deduplicate by title+company
        seen = set()
        unique = []
        for j in discovered_jobs:
            key = f"{j.get('role','').lower().strip()}|{j.get('company','').lower().strip()}"
            if key not in seen:
                seen.add(key)
                unique.append(j)
        discovered_jobs = unique
        log(f"  Total unique discovered: {len(discovered_jobs)}")
    else:
        log("Step 1: Skipping discovery (no platforms configured)")

    # ── Step 2: LinkedIn scrape ──
    linkedin_jobs = []
    li_email = _get_linkedin_email()
    li_pw = _get_linkedin_password()
    if li_email and li_pw:
        log("Step 2: Scraping LinkedIn saved jobs...")
        try:
            scraped, err = linkedin_scrape_saved_jobs()
            if err:
                log(f"  LinkedIn error: {err}")
            else:
                linkedin_jobs = scraped
                log(f"  LinkedIn: {len(scraped)} jobs found")
        except Exception as e:
            log(f"  LinkedIn error: {str(e)[:60]}")
    else:
        log("Step 2: Skipping LinkedIn (no credentials)")

    # ── Step 3: Merge & sync to Supabase ──
    all_new_jobs = discovered_jobs + linkedin_jobs
    total_added = 0
    total_skipped = 0

    if all_new_jobs:
        log(f"Step 3: Syncing {len(all_new_jobs)} jobs to Supabase...")
        # Sync LinkedIn jobs
        if linkedin_jobs:
            added, skipped, err = linkedin_sync_to_supabase(linkedin_jobs)
            total_added += added
            total_skipped += skipped
            log(f"  LinkedIn sync: {added} new, {skipped} duplicates")

        # Sync discovered jobs
        if discovered_jobs:
            sb = get_supabase()
            if sb:
                try:
                    existing = sb.table("jobs").select("id,url").execute().data or []
                    existing_urls = {(j.get("url") or "").split("?")[0] for j in existing if j.get("url")}
                    import time as _time
                    to_insert = []
                    for dj in discovered_jobs:
                        clean_url = (dj.get("url") or "").split("?")[0]
                        if clean_url and clean_url in existing_urls:
                            total_skipped += 1
                            continue
                        job_id = str(int(_time.time() * 1000)) + str(len(to_insert))
                        to_insert.append({
                            "id": job_id,
                            "role": dj.get("role", ""),
                            "company": dj.get("company", ""),
                            "url": clean_url,
                            "jd": (dj.get("jd") or "")[:8000],
                            "status": "saved",
                            "source": dj.get("source", "Discovery"),
                            "roleType": "Business Analyst",
                            "dateApplied": datetime.datetime.now().isoformat(),
                        })
                        if clean_url:
                            existing_urls.add(clean_url)
                    if to_insert:
                        sb.table("jobs").upsert(to_insert, on_conflict="id").execute()
                    total_added += len(to_insert)
                    log(f"  Discovery sync: {len(to_insert)} new, {total_skipped} duplicates")
                except Exception as e:
                    log(f"  Discovery sync error: {str(e)[:60]}")
    else:
        log("Step 3: No new jobs to sync")

    log(f"  Summary: {total_added} added, {total_skipped} skipped")

    # ── Step 4 + 5 + 6: Score, generate docs, save (via existing agent_run) ──
    sb = get_supabase()
    agent_summary = None
    if sb:
        try:
            res = sb.table("jobs").select("*").execute()
            jobs = [j for j in (res.data or []) if not j.get("isDemo")]
            to_run = [
                j for j in jobs
                if (j.get("jd") and j.get("aiScore") is None) or
                   (j.get("aiScore", 0) >= 5 and not j.get("resume_docx_b64"))
            ]
            if to_run:
                log(f"Step 4-6: Processing {len(to_run)} jobs (score → docs → save)...")
                agent_summary = agent_run(to_run, trigger="auto")
                log(f"  Done: {agent_summary['scored']} scored, {agent_summary['docs']} docs generated")
            else:
                log("Step 4-6: All jobs already processed")
        except Exception as e:
            log(f"Step 4-6 error: {str(e)[:60]}")

    log("✅ Autonomous pipeline complete")

    return {
        "pipeline_log": pipeline_log,
        "discovered": len(discovered_jobs),
        "linkedin": len(linkedin_jobs),
        "added": total_added,
        "skipped": total_skipped,
        "scored": agent_summary["scored"] if agent_summary else 0,
        "docs": agent_summary["docs"] if agent_summary else 0,
    }


@app.route("/api/agent/autonomous", methods=["POST"])
def agent_autonomous_route():
    """Trigger the fully autonomous agentic pipeline."""
    data = request.json or {}
    config = {
        "keywords": data.get("keywords", ""),
        "location": data.get("location", "Singapore"),
        "max_days": data.get("max_days", 30),
        "platforms": data.get("platforms", ["indeed", "jobstreet", "workable"]),
    }

    def bg():
        with app.app_context():
            agent_autonomous_pipeline(config)

    threading.Thread(target=bg, daemon=True).start()
    return jsonify({"status": "started", "message": "Autonomous agent pipeline running in background"})


# ─── AGENT ROUTES ────────────────────────────────────────────

@app.route("/api/agent/run", methods=["POST"])
def agent_run_route():
    """Manual Run Agent — processes all pending jobs in background."""
    data      = request.json or {}
    force_all = data.get("force_all", False)

    sb = get_supabase()
    if not sb:
        return jsonify({"error": "Supabase not configured"}), 400
    try:
        res      = sb.table("jobs").select("*").execute()
        all_jobs = res.data or []
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if force_all:
        to_run = [j for j in all_jobs if not j.get("isDemo")]
    else:
        to_run = [
            j for j in all_jobs
            if not j.get("isDemo") and (
                (j.get("jd") and j.get("aiScore") is None) or
                (j.get("aiScore", 0) >= 5 and not j.get("resume_docx_b64"))
            )
        ]

    if not to_run:
        return jsonify({"status": "nothing_to_do", "message": "All jobs already processed"})

    def bg():
        with app.app_context():
            agent_run(to_run, trigger="manual")

    threading.Thread(target=bg, daemon=True).start()
    return jsonify({"status": "started", "count": len(to_run),
                    "message": f"Agent processing {len(to_run)} jobs in background"})


@app.route("/api/agent/run-import", methods=["POST"])
def agent_run_import():
    """Auto-triggered after bookmarklet import — processes new jobs immediately."""
    data     = request.json or {}
    new_jobs = data.get("jobs", [])
    if not new_jobs:
        return jsonify({"status": "nothing_to_do"})

    def bg():
        with app.app_context():
            agent_run(new_jobs, trigger="import")

    threading.Thread(target=bg, daemon=True).start()
    return jsonify({"status": "started", "count": len(new_jobs)})


@app.route("/api/config/save", methods=["POST"])
def config_save():
    """Save LinkedIn + email credentials to Supabase config table."""
    sb = get_supabase()
    if not sb:
        return jsonify({"error": "Supabase not configured"}), 400
    data = request.json or {}
    try:
        # Store each key as a row in a simple config table
        for key, val in data.items():
            if val:  # only save non-empty values
                sb.table("config").upsert({"key": key, "value": val}).execute()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/config/load", methods=["GET"])
def config_load():
    """Load config from Supabase. Returns keys without sensitive values (masked)."""
    sb = get_supabase()
    if not sb:
        return jsonify({"error": "Supabase not configured"}), 400
    try:
        rows = sb.table("config").select("key,value").execute().data or []
        result = {}
        for row in rows:
            k, v = row["key"], row.get("value", "")
            # Mask passwords/sensitive values
            if "password" in k.lower() or "secret" in k.lower():
                result[k] = "••••••••" if v else ""
            else:
                result[k] = v
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_config_value(key):
    """Retrieve a single config value from Supabase config table."""
    # First check env vars (env vars take priority)
    env_map = {
        "linkedin_email":    "LINKEDIN_EMAIL",
        "linkedin_password": "LINKEDIN_PASSWORD",
        "twilio_account_sid": "TWILIO_ACCOUNT_SID",
        "twilio_auth_token":  "TWILIO_AUTH_TOKEN",
        "notification_phone": "NOTIFICATION_PHONE",
    }
    env_key = env_map.get(key)
    if env_key:
        val = os.environ.get(env_key, "")
        if val:
            return val
    # Fall back to Supabase config table
    sb = get_supabase()
    if not sb:
        return ""
    try:
        rows = sb.table("config").select("value").eq("key", key).execute().data or []
        return rows[0]["value"] if rows else ""
    except Exception:
        return ""


@app.route("/api/agent/status", methods=["GET"])
def agent_status():
    """Return counts of processed vs pending jobs."""
    empty = {"total": 0, "with_jd": 0, "scored": 0, "with_docs": 0, "pending": 0}
    sb = get_supabase()
    if not sb:
        return jsonify(empty)
    try:
        res  = sb.table("jobs").select("id,aiScore,resume_docx_b64,jd").execute()
        jobs = res.data or []
        return jsonify({
            "total":     len(jobs),
            "with_jd":   sum(1 for j in jobs if (j.get("jd") or "").strip()),
            "scored":    sum(1 for j in jobs if j.get("aiScore") is not None),
            "with_docs": sum(1 for j in jobs if j.get("resume_docx_b64")),
            "pending":   sum(1 for j in jobs if j.get("aiScore") is None),
        })
    except Exception as e:
        return jsonify(empty)



# ─── CREDENTIALS STORE ──────────────────────────────────────────────────────
# Stores LinkedIn + Gmail credentials in Supabase settings table
# so user can enter them via the UI without touching Render env vars.

def get_setting(key):
    """Read a setting from env vars, Supabase, or memory cache."""
    # First try env var (Render dashboard)
    env_val = os.environ.get(key.upper(), "")
    if env_val:
        return env_val
    # Then try in-memory cache
    if key in _settings_cache:
        return _settings_cache[key]
    # Then try Supabase settings table
    try:
        sb = get_supabase()
        if not sb:
            return ""
        if ensure_settings_table():
            res = sb.table("settings").select("value").eq("key", key).execute()
            if res.data:
                val = res.data[0]["value"]
                _settings_cache[key] = val  # Cache for future reads
                return val
    except Exception:
        pass
    return ""

_settings_table_ok = False
_settings_cache = {}  # In-memory fallback cache

def ensure_settings_table():
    """Check if settings table exists. If not, mark as unavailable and use memory/env fallback."""
    global _settings_table_ok
    if _settings_table_ok:
        return True
    sb = get_supabase()
    if not sb:
        return False
    try:
        sb.table("settings").select("key").limit(1).execute()
        _settings_table_ok = True
        return True
    except Exception:
        # Table doesn't exist — try SQL creation via Supabase REST SQL endpoint
        try:
            resp = http_requests.post(
                f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json"
                },
                json={"query": "CREATE TABLE IF NOT EXISTS public.settings (key TEXT PRIMARY KEY, value TEXT NOT NULL, updated_at TIMESTAMPTZ DEFAULT NOW()); ALTER TABLE public.settings ENABLE ROW LEVEL SECURITY; CREATE POLICY IF NOT EXISTS settings_all ON public.settings FOR ALL USING (true);"},
                timeout=10
            )
            if resp.status_code < 300:
                _settings_table_ok = True
                print("[Settings] Created settings table via REST RPC")
                return True
        except Exception:
            pass
        # If we reach here, just use in-memory cache — don't crash
        print("[Settings] Table unavailable — using in-memory + env fallback")
        return False


def upsert_setting(key, value):
    """Save a setting to Supabase settings table, with memory fallback."""
    global _settings_cache
    _settings_cache[key] = value  # Always cache in memory as backup
    try:
        sb = get_supabase()
        if not sb:
            return True  # Saved in memory
        if ensure_settings_table():
            sb.table("settings").upsert({"key": key, "value": value}, on_conflict="key").execute()
            print(f"[Settings] Saved {key} to Supabase")
            return True
        else:
            print(f"[Settings] Saved {key} to memory (Supabase unavailable)")
            return True  # Memory fallback succeeded
    except Exception as e:
        print(f"[Settings] upsert for {key} failed in Supabase, kept in memory: {e}")
        return True  # Memory fallback succeeded

@app.route("/api/settings/save", methods=["POST"])
def save_settings():
    data   = request.json or {}
    secret = data.get("secret", "")
    if secret != AGENT_CRON_SECRET:
        return jsonify({"error": "Unauthorized"}), 401
    saved  = []
    failed = []
    for key in ["LINKEDIN_EMAIL", "LINKEDIN_PASSWORD", "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "NOTIFICATION_PHONE"]:
        val = data.get(key, "").strip()
        if val:
            ok = upsert_setting(key, val)
            (saved if ok else failed).append(key)
    if failed:
        return jsonify({"status": "partial", "saved": saved, "failed": failed,
                        "error": f"Could not save {failed} — make sure the settings table exists in Supabase (run supabase_setup.sql)"})
    return jsonify({"status": "ok", "saved": saved})

@app.route("/api/settings/load", methods=["GET"])
def load_settings():
    """Return non-sensitive settings (mask passwords)."""
    return jsonify({
        "LINKEDIN_EMAIL":     get_setting("LINKEDIN_EMAIL"),
        "TWILIO_ACCOUNT_SID": get_setting("TWILIO_ACCOUNT_SID"),
        "NOTIFICATION_PHONE": get_setting("NOTIFICATION_PHONE"),
        "linkedin_pw_set":    bool(get_setting("LINKEDIN_PASSWORD")),
        "twilio_token_set":   bool(get_setting("TWILIO_AUTH_TOKEN")),
    })


# ─── LINKEDIN SCRAPER (Selenium) ────────────────────────────────────────────

def _get_linkedin_email():    return get_setting("LINKEDIN_EMAIL")
def _get_linkedin_password(): return get_setting("LINKEDIN_PASSWORD")


def _make_selenium_driver():
    """Create a headless Chrome driver that works on Render."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    # Try system Chrome first (Render has it pre-installed), then webdriver-manager
    import shutil
    chrome_path = shutil.which("google-chrome") or shutil.which("google-chrome-stable") or shutil.which("chromium-browser") or shutil.which("chromium")
    if chrome_path:
        opts.binary_location = chrome_path
        try:
            driver = webdriver.Chrome(options=opts)
            return driver
        except Exception:
            pass

    # Fallback: webdriver-manager downloads matching chromedriver
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver  = webdriver.Chrome(service=service, options=opts)
        return driver
    except Exception as e:
        raise RuntimeError(f"Could not start Chrome: {e}")


def linkedin_scrape_saved_jobs():
    """
    Logs into LinkedIn with stored credentials using Selenium (headless Chrome).
    Scrapes saved jobs from /my-items/saved-jobs/ including job descriptions.
    Returns (jobs_list, error_message).
    """
    import re, time, datetime as dt

    LINKEDIN_EMAIL    = _get_linkedin_email()
    LINKEDIN_PASSWORD = _get_linkedin_password()
    if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
        return [], "LinkedIn credentials not set — enter them in the Agent panel"

    try:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
    except ImportError:
        return [], "selenium not installed"

    def _wait(driver, secs=2):
        time.sleep(secs)

    def _scroll_down(driver, steps=8):
        for _ in range(steps):
            driver.execute_script("window.scrollBy(0, 600)")
            time.sleep(0.35)
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(0.5)

    jobs  = []
    error = None
    driver = None

    try:
        driver = _make_selenium_driver()
        wait   = WebDriverWait(driver, 20)

        # ── Step 1: Login ──
        print("[LinkedIn] Navigating to login page...")
        driver.get("https://www.linkedin.com/login")
        wait.until(EC.presence_of_element_located((By.ID, "username")))
        driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
        driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

        # Wait for redirect away from login
        try:
            WebDriverWait(driver, 20).until(lambda d: "linkedin.com/login" not in d.current_url)
        except TimeoutException:
            pass

        cur = driver.current_url
        if "checkpoint" in cur or "challenge" in cur:
            return [], "LinkedIn security checkpoint triggered — log in manually once to clear it"
        if "login" in cur:
            return [], "Login failed — check LINKEDIN_EMAIL and LINKEDIN_PASSWORD env vars"

        print(f"[LinkedIn] Logged in: {cur}")
        _wait(driver, 2)

        # ── Step 2: Navigate to saved jobs ──
        driver.get("https://www.linkedin.com/my-items/saved-jobs/")
        _wait(driver, 3)

        # ── Step 3: Scrape pages ──
        seen_urls = set()
        page_num  = 1

        while page_num <= 30:
            print(f"[LinkedIn] Page {page_num}...")
            _scroll_down(driver)

            # Multi-strategy card detection
            cards = driver.find_elements(By.CSS_SELECTOR, "[data-chameleon-result-urn]")
            if not cards:
                cards = driver.find_elements(By.CSS_SELECTOR,
                    "li.scaffold-layout__list-item, li[class*=jobs-saved-jobs__list-item], li[class*=job-card-container]")
            if not cards:
                all_li = driver.find_elements(By.TAG_NAME, "li")
                cards  = [li for li in all_li if li.find_elements(By.CSS_SELECTOR, "a[href*='/jobs/view/']")]

            for card in cards:
                try:
                    link_el = card.find_element(By.CSS_SELECTOR, "a[href*='/jobs/view/']")
                    href    = link_el.get_attribute("href").split("?")[0].split("#")[0]
                    if not href or href in seen_urls:
                        continue
                    seen_urls.add(href)

                    # Title
                    title = ""
                    for sel in ["[class*=job-card-list__title]","[class*=job-card__title]","strong","h3","h4"]:
                        els = card.find_elements(By.CSS_SELECTOR, sel)
                        for el in els:
                            tx = (el.text or "").strip()
                            if 2 < len(tx) < 200:
                                title = tx
                                break
                        if title:
                            break
                    if not title:
                        lines = [l.strip() for l in (card.text or "").split("\n") if 2 < len(l.strip()) < 150]
                        title = lines[0] if lines else ""

                    # Company
                    company = "Unknown"
                    for sel in ["[class*=job-card-container__primary-description]","[class*=job-card-list__company-name]","[class*=subtitle]","[class*=company]"]:
                        els = card.find_elements(By.CSS_SELECTOR, sel)
                        for el in els:
                            cx = (el.text or "").strip()
                            if 1 < len(cx) < 100 and cx != title:
                                company = cx
                                break
                        if company != "Unknown":
                            break

                    li_m  = re.search(r'/jobs/view/(\d+)', href)
                    li_id = f"li_{li_m.group(1)}" if li_m else ""

                    if title:
                        jobs.append({
                            "role":        title,
                            "company":     company,
                            "url":         href,
                            "linkedInId":  li_id,
                            "source":      "LinkedIn",
                            "status":      "saved",
                            "roleType":    "Business Analyst",
                            "dateApplied": dt.datetime.now().isoformat(),
                            "jd":          "",
                        })
                except Exception:
                    continue

            print(f"[LinkedIn] Page {page_num}: {len(jobs)} total jobs")

            # Next page button
            next_btn = None
            for sel in [
                "button.artdeco-pagination__button--next",
                "button[aria-label*='Next']",
                "button[aria-label*='next']",
            ]:
                btns = driver.find_elements(By.CSS_SELECTOR, sel)
                for b in btns:
                    if b.is_enabled() and b.is_displayed():
                        next_btn = b
                        break
                if next_btn:
                    break

            if not next_btn:
                # Fallback: button text "Next"
                for b in driver.find_elements(By.TAG_NAME, "button"):
                    if b.text.strip().lower() == "next" and b.is_enabled():
                        next_btn = b
                        break

            if not next_btn:
                print("[LinkedIn] No more pages")
                break

            driver.execute_script("arguments[0].click();", next_btn)
            _wait(driver, 3)
            driver.execute_script("window.scrollTo(0, 0)")
            _wait(driver, 1)
            page_num += 1

        # ── Step 4: Fetch JDs ──
        print(f"[LinkedIn] Fetching JDs for {len(jobs)} jobs...")
        for i, job in enumerate(jobs):
            try:
                print(f"[LinkedIn] JD {i+1}/{len(jobs)}: {job['company']}")
                driver.get(job["url"])
                _wait(driver, 2)

                jd_text = ""
                for sel in ["#job-details", "[class*=jobs-description__content]",
                            "[class*=description__content]", "[class*=jobs-box__html-content]"]:
                    els = driver.find_elements(By.CSS_SELECTOR, sel)
                    if els:
                        txt = (els[0].text or "").strip()
                        if len(txt) > 100:
                            jd_text = txt[:4000]
                            break

                if not jd_text:
                    divs = driver.find_elements(By.TAG_NAME, "div")
                    for d in divs:
                        txt = (d.text or "").strip()
                        if len(txt) > 300 and any(k in txt.lower() for k in ["responsibilities","requirements","qualifications"]):
                            jd_text = txt[:4000]
                            break

                jobs[i]["jd"] = jd_text
                _wait(driver, 0.7)
            except Exception as e:
                print(f"[LinkedIn] JD error for {job['url']}: {e}")
                jobs[i]["jd"] = ""

        print(f"[LinkedIn] Done — {len(jobs)} jobs, {sum(1 for j in jobs if j['jd'])} with JD")

    except Exception as e:
        error = f"Selenium error: {str(e)}"
        print(f"[LinkedIn] ERROR: {error}")
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

    return jobs, error


def linkedin_sync_to_supabase(scraped_jobs):
    """Sync scraped LinkedIn jobs to Supabase, deduplicating by URL/linkedInId."""
    sb = get_supabase()
    if not sb:
        return 0, 0, "Supabase not configured"
    try:
        existing = sb.table("jobs").select("id,url,linkedInId").execute().data or []
        existing_urls = {(j.get("url") or "").split("?")[0] for j in existing if j.get("url")}
        existing_li   = {j.get("linkedInId") for j in existing if j.get("linkedInId")}

        to_insert = []
        skipped = 0
        for job in scraped_jobs:
            clean_url = (job.get("url") or "").split("?")[0]
            li_id     = job.get("linkedInId", "")
            if (clean_url and clean_url in existing_urls) or (li_id and li_id in existing_li):
                skipped += 1
                continue
            import time as _time
            to_insert.append({
                "id":          li_id or str(int(_time.time() * 1000)),
                "linkedInId":  li_id,
                "role":        job.get("role", ""),
                "company":     job.get("company", ""),
                "url":         clean_url,
                "jd":          (job.get("jd") or "")[:8000],
                "status":      job.get("status", "saved"),
                "source":      "LinkedIn",
                "roleType":    job.get("roleType", "Business Analyst"),
                "dateApplied": job.get("dateApplied", ""),
                "salary":      "",
                "notes":       "",
            })
            if clean_url: existing_urls.add(clean_url)
            if li_id:     existing_li.add(li_id)

        if to_insert:
            sb.table("jobs").upsert(to_insert, on_conflict="id").execute()

        return len(to_insert), skipped, None
    except Exception as e:
        return 0, 0, str(e)


@app.route("/api/linkedin/scrape", methods=["POST"])
def linkedin_scrape_route():
    """Manual trigger: scrape LinkedIn saved jobs and sync to Supabase."""
    secret = (request.json or {}).get("secret", "")
    if secret != AGENT_CRON_SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    def run_scrape():
        with app.app_context():
            print("[LinkedIn Scrape] Starting...")
            scraped, err = linkedin_scrape_saved_jobs()
            if err:
                print(f"[LinkedIn Scrape] Error: {err}")
                send_email(
                    "⚠️ LinkedIn Scrape Failed",
                    f"<h2>LinkedIn Scrape Error</h2><p>{err}</p>"
                )
                return

            added, skipped, db_err = linkedin_sync_to_supabase(scraped)
            if db_err:
                print(f"[LinkedIn Scrape] DB Error: {db_err}")
                return

            print(f"[LinkedIn Scrape] Done — {added} new, {skipped} skipped")

            # Run the AI agent on newly added jobs
            if added > 0:
                try:
                    sb = get_supabase()
                    if sb:
                        all_jobs = sb.table("jobs").select("*").execute().data or []
                        to_score = [
                            j for j in all_jobs
                            if j.get("jd") and j.get("aiScore") is None and not j.get("isDemo")
                        ]
                        if to_score:
                            agent_run(to_score, trigger="cron")
                except Exception as e:
                    print(f"[LinkedIn Scrape] Agent trigger error: {e}")
            else:
                send_email(
                    "✅ LinkedIn Scrape — No New Jobs",
                    f"<h2>Daily LinkedIn Sync</h2><p>Scraped {len(scraped)} jobs — all {skipped} already in tracker.</p>"
                )

    threading.Thread(target=run_scrape, daemon=True).start()
    return jsonify({"status": "started", "message": "LinkedIn scrape running in background"})



@app.route("/api/agent/full-run", methods=["POST"])
def agent_full_run():
    """
    Button-triggered full pipeline:
      1. Scrape LinkedIn saved jobs (if credentials set)
      2. AI score all unscored jobs
      3. Generate resume + cover letter for scored >= 5
      4. WhatsApp notification to configured phone
    """
    def bg():
        with app.app_context():
            summary = {"scraped": 0, "skipped": 0, "scored": 0, "docs": 0, "error": None}

            # ── Step 1: LinkedIn scrape ──
            li_email = _get_linkedin_email()
            li_pw    = _get_linkedin_password()
            if li_email and li_pw:
                print("[FullRun] Scraping LinkedIn...")
                scraped_jobs, err = linkedin_scrape_saved_jobs()
                if err:
                    summary["error"] = err
                    print(f"[FullRun] Scrape error: {err}")
                    send_email("⚠️ Extract Latest Jobs — Scrape Failed", f"<h2>LinkedIn Scrape Error</h2><p>{err}</p>")
                else:
                    added, skipped, _ = linkedin_sync_to_supabase(scraped_jobs)
                    summary["scraped"] = added
                    summary["skipped"] = skipped
                    print(f"[FullRun] Scraped: {added} new, {skipped} already in tracker")
            else:
                summary["error"] = "no_credentials"
                print("[FullRun] No LinkedIn credentials — skipping scrape")
                send_email(
                    "⚠️ Extract Latest Jobs — No LinkedIn Credentials",
                    "<h2>Setup Required</h2><p>Open the app → click <strong>Extract Latest Jobs</strong> → enter your LinkedIn email and password in the setup form → Save → try again.</p>"
                )
                return

            # ── Step 2 + 3: Score + generate docs ──
            sb = get_supabase()
            if not sb:
                return
            try:
                res  = sb.table("jobs").select("*").execute()
                jobs = [j for j in (res.data or []) if not j.get("isDemo")]
                to_run = [
                    j for j in jobs
                    if (j.get("jd") and j.get("aiScore") is None) or
                       (j.get("aiScore", 0) >= 5 and not j.get("resume_docx_b64"))
                ]
                if to_run:
                    agent_run(to_run, trigger="manual")
                else:
                    # Nothing new to score — still send summary email
                    send_email(
                        f"✅ Extract Latest Jobs — {summary['scraped']} new jobs added",
                        f"""<html><body style="font-family:sans-serif;padding:20px;">
                        <h2>🔍 LinkedIn Sync Complete</h2>
                        <p><strong>{summary['scraped']}</strong> new jobs added to tracker</p>
                        <p><strong>{summary['skipped']}</strong> jobs already in tracker (skipped)</p>
                        <p>All jobs are already scored — no new scoring needed.</p>
                        <p><a href="https://job-hunt-app-r7my.onrender.com">Open your tracker →</a></p>
                        </body></html>"""
                    )
            except Exception as e:
                print(f"[FullRun] Agent error: {e}")

    threading.Thread(target=bg, daemon=True).start()
    return jsonify({"status": "started"})

@app.route("/api/agent/cron", methods=["POST", "GET"])
def agent_cron():
    """Daily cron trigger — scrapes LinkedIn then runs AI agent pipeline."""
    secret = request.args.get("secret") or (request.json or {}).get("secret", "")
    if secret != AGENT_CRON_SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    def bg():
        with app.app_context():
            # Step 1: Scrape LinkedIn saved jobs if credentials are configured
            if _get_linkedin_email() and _get_linkedin_password():
                print("[Cron] Starting LinkedIn scrape...")
                scraped, err = linkedin_scrape_saved_jobs()
                if err:
                    print(f"[Cron] LinkedIn scrape error: {err}")
                    send_email("⚠️ LinkedIn Cron Scrape Failed", f"<h2>Error</h2><p>{err}</p>")
                else:
                    added, skipped, _ = linkedin_sync_to_supabase(scraped)
                    print(f"[Cron] LinkedIn: {added} new jobs, {skipped} skipped")
            else:
                print("[Cron] LinkedIn credentials not set — skipping scrape")

            # Step 2: Run AI agent on all pending jobs
            sb = get_supabase()
            if not sb:
                return
            try:
                res  = sb.table("jobs").select("*").execute()
                jobs = [j for j in (res.data or []) if not j.get("isDemo")]
                to_run = [
                    j for j in jobs
                    if (j.get("jd") and j.get("aiScore") is None) or
                       (j.get("aiScore", 0) >= 5 and not j.get("resume_docx_b64"))
                ]
                if to_run:
                    agent_run(to_run, trigger="cron")
                else:
                    print("[Cron] No jobs to process")
                    send_email("✅ Daily Cron — Nothing to Process",
                               "<h2>Daily Job Agent</h2><p>All jobs already scored and docs generated.</p>")
            except Exception as e:
                print(f"[Cron] Agent error: {e}")

    threading.Thread(target=bg, daemon=True).start()
    return jsonify({"status": "started", "message": "LinkedIn scrape + agent pipeline running"})


@app.route("/api/test-notifications", methods=["POST"])
def test_notifications():
    ok = send_whatsapp("🤖 Job Agent test — WhatsApp connected ✅")
    return jsonify({
        "whatsapp": "✅ sent" if ok else "❌ not configured — check Twilio credentials and NOTIFICATION_PHONE"
    })


if __name__ == "__main__":
    # Ensure settings table exists at startup
    try:
        ensure_settings_table()
    except Exception as e:
        print(f"[Startup] Settings table check: {e}")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
