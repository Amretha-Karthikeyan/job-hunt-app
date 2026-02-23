import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
CORS(app)

# Configure Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

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
CRITICAL POSITIONING — She is transitioning from CONSULTING to IN-HOUSE PRODUCT roles:
- Reframe "KPMG consultant" → "Product Owner for Loan IQ product squad"
- Reframe "client delivery" → "shipped product features, owned backlog, drove sprint outcomes"
- DO NOT use: consultant, client, engagement, billable, service delivery
- DO USE: product, squad, roadmap, discovery, iteration, user value, outcome, feature, backlog
"""

def is_ai_role(jd, role_type):
    ai_terms = ["ai", "artificial intelligence", "machine learning", "ml", "llm",
                "generative ai", "genai", "nlp", "gpt", "claude", "openai",
                "foundation model", "large language model", "ai product", "data science"]
    text = (jd + " " + role_type).lower()
    return any(t in text for t in ai_terms)

def call_gemini(prompt):
    if not GEMINI_API_KEY:
        return "Error: Gemini API key not configured. Please set GEMINI_API_KEY in Render environment variables."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {str(e)}"

# ─── ROUTES ───────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tailor-resume", methods=["POST"])
def tailor_resume():
    data = request.json
    jd = data.get("jd", "")
    role_type = data.get("roleType", "Business Analyst")
    ai_role = is_ai_role(jd, role_type)

    prompt = f"""You are an expert resume writer helping candidates transition into in-house product roles.
{PRODUCT_FRAMING}

Rewrite the following candidate's resume to match the job description. Target role: {role_type}.

CANDIDATE PROFILE:
{json.dumps(PROFILE, indent=2)}

JOB DESCRIPTION:
{jd}

{"AI ROLE DETECTED: Prominently feature the AI Project section with the live URL: " + PROFILE['aiProjectUrl'] + ". Lead Skills with AI/LLM skills." if ai_role else ""}

Write a complete ATS-optimised resume with:
- Header (name, contact, LinkedIn, {PROFILE['aiProjectUrl'] if ai_role else ''})
- Professional Summary (product-ownership framing, keyword-rich)
- {"AI & Innovation / Projects section (FIRST after summary for AI roles)" if ai_role else ""}
- Core Skills
- Professional Experience (product language throughout, real metrics)
- Education & Certifications

Do not fabricate experience. Use product language, not consulting language."""

    result = call_gemini(prompt)
    return jsonify({"result": result, "isAiRole": ai_role})

@app.route("/api/cover-letter", methods=["POST"])
def cover_letter():
    data = request.json
    jd = data.get("jd", "")
    role_type = data.get("roleType", "Business Analyst")
    company = data.get("company", "the company")
    ai_role = is_ai_role(jd, role_type)

    prompt = f"""Write a professional 300-350 word cover letter for {PROFILE['name']} applying to {role_type} at {company}.
{PRODUCT_FRAMING}

KEY ACHIEVEMENTS:
- At KPMG: drove ~5% business value through product scope decisions
- At KPMG: eliminated 30 man-days through automation feature
- SAFe 6.0 certified Product Owner/Product Manager
- Personal AI Project: Built and deployed live Trade Analysis platform using Claude Opus 4.6 — {PROFILE['aiProjectUrl']}

JOB DESCRIPTION:
{jd}

{"IMPORTANT — AI ROLE: Mention the live Trade Analysis platform (" + PROFILE['aiProjectUrl'] + ") as hard proof she ships AI products. Include the URL." if ai_role else ""}

Write a compelling cover letter that:
1. Opens with a confident hook about building products, not delivering services
2. Highlights KPMG metrics (5% value, 30 man-days)
3. {"Mentions live AI project with URL as key differentiator" if ai_role else "Bridges consulting delivery to product ownership"}
4. Shows genuine enthusiasm for {company}
5. Ends with clear call to action

Exactly 300-350 words. No consulting jargon. Sound like a product person."""

    result = call_gemini(prompt)
    return jsonify({"result": result})

@app.route("/api/interview-prep", methods=["POST"])
def interview_prep():
    data = request.json
    company = data.get("company", "the company")
    role_type = data.get("roleType", "Business Analyst")
    jd = data.get("jd", "")

    prompt = f"""Generate a comprehensive interview prep guide for {PROFILE['name']} interviewing at {company} for {role_type}.
{PRODUCT_FRAMING}

CANDIDATE:
- KPMG Singapore (Feb 2021–Present): De-facto Product Owner for Loan IQ. Drove 5% business value, saved 30 man-days through automation, led sprint-to-SIT delivery
- J.P. Morgan (Oct 2023–Jan 2024): Portfolio KPI analysis, requirement gathering
- Amazon India (Mar 2018–Mar 2019): Power BI dashboards, data products
- SAFe 6.0 certified, Agile, JIRA, SQL, Tableau, Power BI
- Built and deployed live AI Trade Analysis platform: {PROFILE['aiProjectUrl']}
{"JD: " + jd if jd else ""}

Create prep with these EXACT sections:

## 5 Behavioral Questions with STAR Answers
For each: the question, then full STAR answer using her real experience with specific metrics.

## 5 Technical Questions for {role_type}
Questions with model answers specific to this role.

## 3 Things to Research About {company}
Specific actionable research areas.

## 5 Smart Questions to Ask the Interviewer
Product-minded questions that signal ownership thinking.

## Salary Negotiation Tip (Singapore Market)
Specific tip for SAFe-certified PO/BA with 5+ years in Singapore fintech."""

    result = call_gemini(prompt)
    return jsonify({"result": result})

@app.route("/api/full-kit", methods=["POST"])
def full_kit():
    data = request.json
    company = data.get("company", "")
    role = data.get("role", "")
    role_type = data.get("roleType", "Business Analyst")
    jd = data.get("jd", "")
    ai_role = is_ai_role(jd, role_type)

    profile_str = json.dumps({k: v for k, v in PROFILE.items()}, indent=2)

    resume_prompt = f"Write ATS-optimised resume for {PROFILE['name']} applying to {role} at {company} ({role_type}). {PRODUCT_FRAMING} Profile: {profile_str}. JD: {jd}. {'AI role: feature project ' + PROFILE['aiProjectUrl'] + ' prominently.' if ai_role else ''}"
    cover_prompt = f"Write 300-word cover letter for {PROFILE['name']} for {role} at {company}. Highlight: 5% KPMG value, 30 man-days saved, SAFe 6.0. {'Mention live AI project: ' + PROFILE['aiProjectUrl'] if ai_role else ''} Product language, no consulting jargon."
    prep_prompt = f"Give top 5 interview questions for {role_type} at {company} with brief model answers for {PROFILE['name']} (KPMG PO, SAFe 6.0, AI project at {PROFILE['aiProjectUrl']}). Be specific."

    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        r_future = executor.submit(call_gemini, resume_prompt)
        c_future = executor.submit(call_gemini, cover_prompt)
        p_future = executor.submit(call_gemini, prep_prompt)
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

    result = call_gemini(prompt)
    return jsonify({"result": result})

@app.route("/api/speed-kit", methods=["POST"])
def speed_kit():
    data = request.json
    company = data.get("company", "this company")
    role = data.get("role", "this role")

    prompt = f"""Write a genuine 3-sentence "Why do you want to work at {company}?" answer for Amretha Karthikeyan, a SAFe 6.0 PO/Lead BA transitioning from KPMG to an in-house {role} role. Be specific to {company}'s product/market. Sound like a product person who wants to build. No consulting language."""

    result = call_gemini(prompt)
    return jsonify({"result": result})


@app.route("/api/generic", methods=["POST"])
def generic():
    data = request.json
    prompt = data.get("prompt", "")
    system = data.get("systemPrompt", "")
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    result = call_gemini(full_prompt)
    return jsonify({"result": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
