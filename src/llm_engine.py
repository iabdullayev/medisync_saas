import os
from groq import Groq

class CloudLLM:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"

    def draft_appeal(self, context, advocate_details):
        # Unpack the details with defaults just in case
        name = advocate_details.get("name", "[Your Name]")
        title = advocate_details.get("title", "Medical Billing Advocate")
        address = advocate_details.get("address", "[Your Address]")

        prompt = f"""
        You are {name}, a {title}. Write a formal insurance appeal letter.
        
        YOUR DETAILS (The Sender):
        Name: {name}
        Title: {title}
        Address: {address}
        
        DENIAL CONTEXT:
        {context}
        
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
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": prompt}
            ],
            model=self.model,
            temperature=0.1,
        )
        
        return chat_completion.choices[0].message.content