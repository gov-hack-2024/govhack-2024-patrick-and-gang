# content_check.py
from openai import OpenAI
import re
import json
from pydantic import BaseModel

# class ContentModel(BaseModel):
#     mistake: str
#     suggestion: str
#     mistake_type: list[str]
#     explanation : str
#
# class ContentListModel(BaseModel):
#     response : list[ContentModel]

class ContentCheck:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0, max_tokens: int = 5000):
        """
        Initializes the ContentCheck class with the API key, model, temperature, and max_tokens.

        Parameters:
        - api_key: Your OpenAI API key.
        - model: The OpenAI model you want to use (default is "gpt-4").
        - temperature: The level of randomness in the output (default is 0.7).
        - max_tokens: Maximum number of tokens in the output (default is 500).
        """
        self.client = OpenAI()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Define the system prompt
        self.system_prompt = """
        Role: You are an Australian content moderator responsible for reviewing and improving government communications for public dissemination.

        Objective: Thoroughly evaluate the provided government content and enhance it based on the following key guidelines:

        Guidelines:
        1. Writing Style
        - Use plain language with short, clear, and active-voice sentences.
        - Ensure the content is user-friendly, concise, and follows best practices in content design (user-focused, SEO-optimized, easy to read).

        2. Accessibility
        - Simplify language to a Year 7 reading level for better accessibility.
        - Follow WCAG principles to ensure the content is perceivable, operable, understandable, and robust for all users.

        3. Inclusivity
        - Use culturally appropriate language, mindful of Australia’s diverse population.
        - Align with the Australian Government's inclusion principles to promote equity in communication.

        4. Grammar, Punctuation, and Conventions
        - Use Australian English consistently.
        - Minimize punctuation to improve readability.
        - Ensure spelling, grammar, and punctuation meet Australian standards.
        - Follow specific conventions for numbers (e.g., use numerals for 2 and above, write 'zero' and 'one' in words).
        - Follow official rules on the use of numbers in content, including exceptions for fractions, proper nouns, and measurements.

        Output Format: Provide your feedback in structured JSON format. Each entry should include:
        - Mistake: The exact sentence from the content.
        - Suggestion: A revised version of the sentence.
        - Mistake Type: One or more categories that describe the issue (e.g., "Writing Style," "Grammar and Punctuation," "Accessibility," "Inclusivity").
        - Explanation: A brief explanation detailing why the revision improves the content.

        [
          {
            "mistake": "Exact sentence from the content",
            "suggestion": "Improved version of the sentence",
            "mistake_type": ["Writing Style", "Grammar and Punctuation"],
            "explanation": "Explanation of how the revision improves clarity and readability"
          }
        ]
        """

    def check_content(self, content: str):
        """
        Sends a request to the OpenAI API with the specified content and the system prompt.

        Parameters:
        - content: The text content to check.

        Returns:
        - The response from the OpenAI API as a JSON string.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": self.system_prompt
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": content
                            }
                        ]
                    },

                ],
                temperature=0,
                max_tokens= self.max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                # response_format= ContentListModel
            )

            llm_response = response.choices[0].message.content
            # Using re.findall to extract list items
            parse_response = re.findall(r'(\[.*\])', llm_response, re.DOTALL)
            parse_response = parse_response[0]

            return parse_response
        except Exception as e:
            return f"Error: {str(e)}"


# This function can be called from the Streamlit frontend
def check_content(content: str):
    """
    Wrapper function for the Streamlit frontend to call the content checking functionality.

    Parameters:
    - api_key: Your OpenAI API key.
    - content: The content to check.

    Returns:
    - The result of the content check.
    """
    content_checker = ContentCheck()
    # Using re.findall to extract list items
    return json.loads(content_checker.check_content(content))

if __name__ == '__main__':
    content = '''Where the extra $4.7 billion in gender-based violence funding is going

Australians fleeing domestic violence will soon receive additional support as Prime Minister Anthony Albanese announced a $4.7 billion boost in funding.

Albanese met with premiers and chief ministers on Friday morning to discuss what he's repeatedly labelled a "national crisis", and reassert his government's commitment to end family, domestic and sexual violence "in a generation".

Forty-seven women have been violently killed in Australia since the start of the year, according to the advocacy group Destroy the Joint's project Counting Dead Women.

The prime minister said it was crucial to have an "all hands on deck" approach, with collaboration between states, territories, and the federal government essential.'''
    llm_output = check_content(content)
    print(llm_output)


