import os
from groq import Groq
from src.sanitization import sanitize_name, sanitize_address
from src.constants import LLM_MODEL, LLM_TEMPERATURE
from src.errors import LLMError

class CloudLLM:
    def __init__(self, api_key: str):
        """Initialize CloudLLM client.
        
        Args:
            api_key: Groq API key
        """
        self.client = Groq(api_key=api_key)
        self.model = LLM_MODEL

    def draft_appeal(self, context, advocate_details):
        """Draft an appeal letter with sanitized inputs to prevent prompt injection.
        
        Args:
            context: The denial context extracted from the PDF
            advocate_details: Dictionary containing name, title, and address
            
        Returns:
            Generated appeal letter text
        """
        # Sanitize all user inputs to prevent prompt injection
        name = sanitize_name(advocate_details.get("name", "[Your Name]"))
        title = sanitize_name(advocate_details.get("title", "Medical Billing Advocate"))
        address = sanitize_address(advocate_details.get("address", "[Your Address]"))
        
        # Use structured prompting with clear XML-style delimiters for security
        prompt = f"""You are a medical billing advocate assistant. Generate a formal insurance appeal letter.

SENDER INFORMATION (Use exactly as provided below):
<sender>
<name>{name}</name>
<title>{title}</title>
<address>{address}</address>
</sender>

DENIAL CONTEXT:
<denial_context>
{context}
</denial_context>

INSTRUCTIONS:
1. HEADER: Start the letter with the sender's details in this exact format:
   {name}
   {title}
   {address}
   Date: (Insert Today's Date)

2. DO NOT include labels like "[Your Name]" or placeholders like "[City, State, ZIP]".
   If information is missing in the address, do not add placeholders.

3. Address the specific denial reason found in the context.

4. Provide medical justification based ONLY on information in the denial context.
   DO NOT invent diagnoses or medical facts.

5. Sign the letter with: {name}

6. Keep the tone professional and formal.
"""
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful medical billing advocate assistant."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=LLM_TEMPERATURE,
            )
            
            return chat_completion.choices[0].message.content
        except Exception as e:
            raise LLMError(f"Failed to generate appeal letter: {str(e)}") from e