# content_check.py
from openai import OpenAI
import re
import json

class Translator:
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
        self.language_list = ['Afrikaans', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Azerbaijani', 'Basque', 'Belarusian', 'Bengali',
 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chinese (Simplified)', 'Chinese (Traditional)',
 'Corsican', 'Croatian', 'Czech', 'Danish', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Finnish', 'French',
 'Frisian', 'Galician', 'Georgian', 'German', 'Greek', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian',
 'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese',
 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin',
 'Latvian', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Maori',
 'Marathi', 'Mongolian', 'Nepali', 'Norwegian', 'Nyanja', 'Odia', 'Pashto', 'Persian', 'Polish', 'Portuguese',
 'Punjabi', 'Romanian', 'Russian', 'Samoan', 'Scots Gaelic', 'Serbian', 'Sesotho', 'Shona', 'Sindhi', 'Sinhala',
 'Slovak', 'Slovenian', 'Somali', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tagalog', 'Tajik', 'Tamil',
 'Tatar', 'Telugu', 'Thai', 'Tigrinya', 'Tsonga', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek',
 'Vietnamese', 'Welsh', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']


    def translate_content(self, content: str, translated_language: str = "thai"):
        """
        Sends a request to the OpenAI API with the specified content and the system prompt.

        Parameters:
        - content: The text content to check.

        Returns:
        - The response from the OpenAI API as a JSON string.
        """
        # Define the system prompt
        system_prompt = f"""
        You are a highly skilled translator proficient in translating content accurately and contextually. 
        Translate the following text from English to {translated_language}, while maintaining the original meaning, tone, and style. Ensure that cultural nuances and expressions are appropriately adapted to fit the context of the target language.
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
                                "text": system_prompt
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
            )

            llm_response = response.choices[0].message.content

            return llm_response
        except Exception as e:
            return f"Error: {str(e)}"



if __name__ == '__main__':
    content = '''Where the extra $4.7 billion in gender-based violence funding is going

Australians fleeing domestic violence will soon receive additional support as Prime Minister Anthony Albanese announced a $4.7 billion boost in funding.

Albanese met with premiers and chief ministers on Friday morning to discuss what he's repeatedly labelled a "national crisis", and reassert his government's commitment to end family, domestic and sexual violence "in a generation".

Forty-seven women have been violently killed in Australia since the start of the year, according to the advocacy group Destroy the Joint's project Counting Dead Women.

The prime minister said it was crucial to have an "all hands on deck" approach, with collaboration between states, territories, and the federal government essential.'''
    translator_obj = Translator()
    llm_output = translator_obj.translate_content(content, 'Norwegian')
    print(llm_output)


