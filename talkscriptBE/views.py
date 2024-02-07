from django.shortcuts import render 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from rest_framework.views import APIView


from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)

os.environ["OPENAI_API_KEY"] = "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"

OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

chat = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL)

def extract_code_from_markdown(md_content):
    # Look for the start and end of the code block
    start_code = md_content.find("```") + 3  # Skip the ```
    end_code = md_content.find("```", start_code)

    # Extract the content between the backticks
    code_block = md_content[start_code:end_code].strip()

    # Find the first newline, which should end the language identifier
    first_newline = code_block.find('\n')

    # Remove the language identifier
    code_without_language = code_block[first_newline+1:] if first_newline != -1 else code_block

    return code_without_language

@api_view(['GET'])
def openai_api_call(request):
    # Get the value of the COMMAND_PROMPT from the query parameters
    command_prompt = request.GET.get('COMMAND_PROMPT', '')
     # context = request.GET.get('CONTEXT', '')
    # final_prompt = context + command_prompt
    
    # Use the command_prompt to generate the response using OpenAI
    instruction="""Just do what the command tells you to do. It'll mostly be to generate code so just do that, dont explain to me what it does. Just give me the code snippet in the ```code``` blocks. THATS ALL. Assume information if needed, try not ask user again for input. try not to do anything extra. And try to remember earlier generations you gave on the previous prompts since you might have to work with them."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(instruction)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, command_prompt])

    response = chat(chat_prompt.format_prompt().to_messages())
    code_output = extract_code_from_markdown(response.content.strip())

    # Return the code_output as a JSON response
    return Response({'code_output': code_output})





# from rest_framework.renderers import JSONRenderer
# from rest_framework.response import Response
# from rest_framework.views import APIView

# class OPENAIAPICALL(APIView):
#     """
#     A view that returns the count of active users in JSON.
#     """
#     renderer_classes = [JSONRenderer]

#     def get(self, request):
#         # Get the value of the COMMAND_PROMPT from the query parameters
#         command_prompt = request.GET.get('COMMAND_PROMPT', '')
#         # context = request.GET.get('CONTEXT', '')
#         # final_prompt = context + command_prompt
        
#         # Use the command_prompt to generate the response using OpenAI
#         instruction="""Just do what the command tells you to do. It'll mostly be to generate code so just do that, dont explain to me what it does. just give me the code snippet. THATS ALL. Assume information if needed, try not ask user again for input. try not to do anything extra. And try to remember earlier generations you gave on the previous prompts since you might have to work with them."""
#         system_message_prompt = SystemMessagePromptTemplate.from_template(instruction)
#         chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, command_prompt])

#         response = chat(chat_prompt.format_prompt().to_messages())
#         code_output = response.content.strip()

#         # Return the code_output as a JSON response
#         return Response({'code_output': code_output})




