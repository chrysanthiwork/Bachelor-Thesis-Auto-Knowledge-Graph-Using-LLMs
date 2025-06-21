from colorama import Fore
from LC_CAMEL  import starting_convo,get_sys_msgs,CAMELAgent
from RE_CAMEL import Retrieval_Msg
from langchain.schema import HumanMessage
from langchain_together import ChatTogether
from RE_CAMEL import append_to_file
import re
word_limit = 50  # word limit for task brainstorming
#ChatTogether object
chat = ChatTogether(
    together_api_key="196466437fae467603e2b0b04c7943e1871be1cc0cd30330d0487c66e74d1dd6",
    model="Qwen/Qwen2.5-Coder-32B-Instruct",
    temperature=0.2
)

import re

def apply_correction_rules(filename):
    try:
        # Διαβάζουμε το περιεχόμενο του αρχείου
        with open(filename, 'r', encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Το αρχείο {filename} δεν βρέθηκε.")
        return
    except Exception as e:
        print(f"Παρουσιάστηκε σφάλμα κατά την ανάγνωση του αρχείου: {e}")
        return

    # Σύνολο για να αποθηκεύσουμε τις μοναδικές τριπλέτες
    triplets_set = set()
    
    # Αναλύουμε τις γραμμές και αποθηκεύουμε τις τριπλέτες
    for line in lines:
        match = re.match(r'<([^,]+), ([^,]+), "([^"]+)">', line.strip())
        if match:
            triplet = (match.group(1), match.group(2), match.group(3))
            triplets_set.add(triplet)
        else:
            match = re.match(r'<([^,]+), ([^,]+), ([^>]+)>', line.strip())
            if match:
                triplet = (match.group(1), match.group(2), match.group(3))
                triplets_set.add(triplet)
    
    if not triplets_set:
        print("Δεν βρέθηκαν τριπλέτες στο αρχείο.")
        return

    # Εύρεση όλων των πρώτων και τρίτων μελών
    first_elements = {triplet[0] for triplet in triplets_set}
    
    print(f"Πρώτα στοιχεία: {first_elements}")
    
    # Δημιουργία των τελικών τριπλετών με εφαρμογή του κανόνα
    corrected_triplets_set = set()
    for triplet in triplets_set:
        first, relation, third = triplet
        if third in first_elements:
            corrected_triplet = f'<{first}, {relation}, {third}>'
        else:
            corrected_triplet = f'<{first}, {relation}, "{third}">'
        corrected_triplets_set.add(corrected_triplet)
    
    # Μετατροπή του συνόλου σε λίστα για εγγραφή στο αρχείο
    corrected_triplets = list(corrected_triplets_set)
    
    # Γράψιμο των διορθωμένων τριπλετών στο αρχείο
    try:
        with open(filename, 'w', encoding="utf-8") as file:
            for triplet in corrected_triplets:
                file.write(triplet + '\n')
        print(f"Οι διορθωμένες τριπλέτες αποθηκεύτηκαν στο αρχείο {filename}.")
    except Exception as e:
        print(f"Παρουσιάστηκε σφάλμα κατά την εγγραφή στο αρχείο: {e}")

      
def main() ->None:
    #main roles
    assistant_role_name = "Consultant"
    user_role_name = "Knowledge Graph Domain Expert"
    #main task
    task = "Construct a Knowledge Graph about the Cybercrime from the perspective of law enforcement authorities."

    specified_task, assistant_inception_prompt, user_inception_prompt = starting_convo(assistant_role_name, user_role_name, task, word_limit)
    assistant_sys_msg, user_sys_msg = get_sys_msgs(assistant_role_name, user_role_name, specified_task, assistant_inception_prompt, user_inception_prompt)
    assistant_agent = CAMELAgent(assistant_sys_msg, chat)
    user_agent = CAMELAgent(user_sys_msg, chat)

    # Reset agents
    assistant_agent.reset()
    user_agent.reset()

    # Initialize chats
    assistant_msg = HumanMessage(
        content=(f"{user_sys_msg.content}. "
                 "Now start to give me introductions one by one. "
                 "Only reply with Instruction and Input."))

    user_msg = HumanMessage(content=f"{assistant_sys_msg.content}")
    user_msg = assistant_agent.step(user_msg) 
   

    print(Fore.RED+f"Original task prompt:\n{task}\n")
    print(Fore.GREEN+f"Specified task prompt:\n{specified_task}\n")

    chat_turn_limit, n = 10, 0
    while n < chat_turn_limit:
        n += 1
        user_ai_msg = user_agent.step(assistant_msg)
        user_msg = HumanMessage(content=user_ai_msg.content)
        
        print(Fore.BLUE+f"AI User ({user_role_name}):\n\n{user_msg.content}\n\n")

        Supplement_info = Retrieval_Msg(assistant_role_name, user_role_name, user_msg.content, 20) # η απάντηση του search engine
       
        if Supplement_info != "" or "Agent Stoped" not in Supplement_info:
            Supplement_info_new = user_msg.content + "\n Additional information for the Instruction: " + Supplement_info
            Supplement_info_new = HumanMessage(content=Supplement_info_new) 
            assistant_ai_msg = assistant_agent.step(Supplement_info_new) 
            assistant_msg = HumanMessage(content=assistant_ai_msg.content)
           
            append_to_file("output.txt", assistant_msg)
            print(Fore.YELLOW + f"AI Assistant With Tool ({assistant_role_name}):\n\n{assistant_msg.content}\n\n")

        else:
            assistant_ai_msg = assistant_agent.step(user_msg)
            assistant_msg = HumanMessage(content=assistant_ai_msg.content) 
            append_to_file("output.txt", assistant_msg)
          
            print(Fore.CYAN+f"AI Assistant ({assistant_role_name}):\n\n{assistant_msg.content}\n\n")

        if "CAMEL_TASK_DONE" in user_msg.content:
            break



if __name__ == "__main__":
    main()
    apply_correction_rules('output.txt')