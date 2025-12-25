import json
import os
import base64


def lambda_handler(event, context):
    """
    AWS Lambda entry via HTTP API (API Gateway v2).
    Supports:
      GET  /health
      POST /generate  { "denial_text": "...", "advocate_details": {...} }
    """
    try:
        # Determine path and method (HTTP API v2)
        path = event.get("rawPath") or event.get("path", "/")
        # Strip stage prefix (e.g., /prod, /dev) if present
        if path.startswith("/prod"):
            path = path[5:] or "/"
        if path.startswith("/dev"):
            path = path[4:] or "/"
        method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

        # ---- Health endpoint ----
        if path == "/health" and method == "GET":
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "message": "MediSync API Handler Ready",
                    "status": "active",
                    "runtime": "python3.12"
                }),
            }

        # ---- Generate endpoint ----
        if path == "/generate" and method == "POST":
            # Import Groq directly (no pytesseract dependency)
            from groq import Groq

            api_key = os.environ.get("GROQ_API_KEY")
            if not api_key:
                return {
                    "statusCode": 500,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "GROQ_API_KEY not set in environment"}),
                }

            # Decode request body
            raw_body = event.get("body") or "{}"
            if event.get("isBase64Encoded"):
                raw_body = base64.b64decode(raw_body).decode("utf-8")
            data = json.loads(raw_body)

            denial_text = data.get("denial_text", "").strip()
            if not denial_text:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "denial_text is required"}),
                }

            # Get advocate details (optional)
            advocate_details = data.get("advocate_details", {})
            name = advocate_details.get("name", "[Your Name]")
            title = advocate_details.get("title", "Medical Billing Advocate")
            address = advocate_details.get("address", "[Your Address]")

            # Build the prompt
            prompt = f"""
            You are {name}, a {title}. Write a formal insurance appeal letter.
            
            YOUR DETAILS (The Sender):
            Name: {name}
            Title: {title}
            Address: {address}
            
            DENIAL CONTEXT:
            {denial_text[:6000]}
            
            RULES:
            1. HEADER: Start the letter with your details exactly as provided above.
               Format:
               {name}
               {title}
               {address}
               Date: (Insert Today's Date)

            2. DO NOT include labels like "[Your Name]" or placeholders like "[City, State, ZIP]". 
               If a piece of information (like City/State) is missing in the Address provided, do not fake it or add a placeholder.
            3. Argue specifically against the denial reason found in the text.
            4. Do not invent diagnoses (No Hallucinations).
            5. Sign the letter with {name}.
            """

            # Call Groq API
            client = Groq(api_key=api_key)
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful medical assistant."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.1-8b-instant",
                temperature=0.1,
            )

            appeal_text = chat_completion.choices[0].message.content

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"appeal": appeal_text}),
            }

        # ---- Fallback: unknown route ----
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": f"Route {method} {path} not found"}),
        }

    except Exception as e:
        import traceback
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": str(e),
                "stack": traceback.format_exc(),
            }),
        }
