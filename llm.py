from langchain_together import ChatTogether
# ChatTogether object
chat = ChatTogether(
    together_api_key="196466437fae467603e2b0b04c7943e1871be1cc0cd30330d0487c66e74d1dd6",
    model="Qwen/Qwen2.5-Coder-32B-Instruct",
    temperature=0.2
)
#This is the given task
task = "Construct a Knowledge Graph about bribery and corruption in triples format. The format must be <subject, predicate, object>"
# Print the results
for m in chat.stream(task):
    print(m.content, end="", flush=True)

