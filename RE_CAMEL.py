from langchain.agents import  initialize_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import AgentType
from colorama import Fore
from langchain_together import ChatTogether
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from LC_CAMEL import CAMELAgent
import os,re,time
from duckduckgo_search import exceptions as ddg_exceptions

# Initialize Llama model and tokenizer
chat = ChatTogether(
    together_api_key="196466437fae467603e2b0b04c7943e1871be1cc0cd30330d0487c66e74d1dd6",
    model="Qwen/Qwen2.5-Coder-32B-Instruct",
)


import re

def append_to_file(filename, text):
    # Define the pattern to find all substrings within angle brackets
    pattern = r'<[^<>]+>'
    
    # Find all matches in the text
    matches = re.findall(pattern, str(text))
    
    # Process each match to ensure proper format
    formatted_matches = []
    all_third_elements = set()
    for match in matches:
        parts = match.strip('<>').split(', ')
        if len(parts) < 3:
            continue  # Skip if parts are less than 3
        if len(parts) > 3:
            # Join the third part with remaining parts
            parts[2] = ', '.join(parts[2:])
            parts = parts[:3]
        formatted_matches.append(parts)
        all_third_elements.add(parts[2])
    
    # Check if third element appears as a first element in any triplet
    first_elements = {parts[0] for parts in formatted_matches}
    
    # Read existing content to avoid duplicates
    existing_lines = set()
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            existing_lines = set(line.strip() for line in file.readlines())
    except FileNotFoundError:
        pass  # If the file does not exist, proceed without reading

    # Write each formatted match to the file on a new line if it does not already exist
    with open(filename, 'a', encoding="utf-8") as file:
        for parts in formatted_matches:
            # Apply the rule for quotes
            third_element = parts[2]
            if third_element in first_elements:
                formatted_match = f'<{parts[0]}, {parts[1]}, {third_element}>'
            else:
                formatted_match = f'<{parts[0]}, {parts[1]}, "{third_element}">'
            
            # Check if the formatted match already exists
            if formatted_match not in existing_lines:
                file.write(formatted_match + '\n')
                existing_lines.add(formatted_match)


def Retrieval_Msg(assistant_role_name, user_role_name, task, word_limit):
    retrieval_sys_msg = SystemMessage(content="You are an assistant who can use Google search to gather information")

    retrieval_specifier_prompt = (
    """Here is a task that {assistant_role_name} will help {user_role_name} to complete: constructing a Knowledge Graph based on the {user_role_name}'s instruction and input: {task}.

Suppose you are the {assistant_role_name}.
You are able to perform web searches to gather factual knowledge.
You are never supposed to search for information about methodology questions.
Important: Reply only in the following format and nothing else:
<Subject, Predicate, Object>

For example:
<Miles Morales, livesin, New York City>
<Spongebob, hasPet, Garry>

Please summarize the key information of the task and answer only in this form:

Browsing Question: <YOUR_QUESTION>

<YOUR_QUESTION> should be your browsing question suitable for Google search.
If you think browsing is not necessary, then the answer should be "none".
Be creative and imaginative. Please reply in {word_limit} words or less. Do not add anything else.

Never forget to provide your answers as the examples and the rules that I gave you.
    """
)


    retrieval_specifier_template = HumanMessagePromptTemplate.from_template(template=retrieval_specifier_prompt)
    retrieval_specify_agent = CAMELAgent(retrieval_sys_msg, chat)
    retrieval_specifier_msg = retrieval_specifier_template.format_messages(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        task=task,
        word_limit=word_limit
    )[0]
    specified_retrieval_msg = retrieval_specify_agent.step(retrieval_specifier_msg) #Browsing Question: <>, Instruction
    print(Fore.GREEN + f"Specified retrieval:\n{specified_retrieval_msg.content}")
    specified_retrieval = specified_retrieval_msg.content
    append_to_file("output.txt",specified_retrieval)
   
    response = ""            
    # if "Browsing Question:" in specified_retrieval:
    #     if "Browsing Question: none" in specified_retrieval:
    #         return  response
    #     if "CAMEL_TASK_DONE" in specified_retrieval:
    #         return
    #     else:
    #         specified_retrieval = specified_retrieval.replace("Browsing Question:","")
    #         # ChatTogether
    #         llm = chat
    #          # ddg-search
    #         tools = load_tools(["ddg-search"])
    #         # initialization
    #         agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True)
            
    #         # Loop until the specified retrieval is successful
    #         success = False
    #         while not success:
    #             try:
    #                 # Attempt to run the specified retrieval
    #                 response = agent.run(specified_retrieval)
    #                 # If successful, exit the loop
    #                 success = True
                    
    #             except Exception as e:
    #                 print(f"An error occurred: {e}. Retrying...")
    return response


