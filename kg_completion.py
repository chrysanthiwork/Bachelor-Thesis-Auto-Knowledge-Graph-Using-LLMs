from langchain_together import ChatTogether
import re

# ChatTogether object
chat = ChatTogether(
    together_api_key="196466437fae467603e2b0b04c7943e1871be1cc0cd30330d0487c66e74d1dd6",
    model="meta-llama/Llama-3-8b-chat-hf",
    temperature=0.2
)

file_path = 'output.txt'

# List to store all triplets
triplets = []

# Read the input file and extract the triplets
with open(file_path, 'r') as file:
    for line in file:
        # Remove the angle brackets and strip any surrounding whitespace
        line = line.strip()[1:-1]
        
        # Split by comma, limit split to 2 so we get exactly three parts
        parts = [part.strip() for part in line.split(',', 2)]
        
        # Check if we have exactly three parts (subject, predicate, object)
        if len(parts) == 3:
            subject, predicate, object_ = parts
            # Remove any surrounding quotes from object (if present)
            object_ = object_.strip('"')
            # Store each triplet with angle brackets as a formatted string
            triplet_str = f"<{subject}, {predicate}, \"{object_}\">"
            triplets.append(triplet_str)
            # Print each triplet with angle brackets
            print(triplet_str)
        else:
            print(f"Skipping malformed line: {line}")

# Convert the list of triplets to a set to ensure uniqueness
unique_triplets = set(triplets)

# Convert the list of unique triplets back to a string
triplets_str = "\n".join(unique_triplets)

# Prompt for KG completion
prompt = f"""
Here is a list of knowledge graph triples:
{triplets_str}

Based on these existing triples, please generate additional unique triples in the format <subject, predicate, object> to help complete this knowledge graph. I need new triples with new relationships if they exist, in order to complete my knowledge graph.
The new triples must be correct and their relationships must be real.
"""

# Send the prompt to the ChatTogether model
response = chat.invoke(prompt)  
response_text = response.content  # Get the response text from the AIMessage object

# Extract generated triples from the response
new_triplets = re.findall(r'<(.*?)>', response_text)

# Format the extracted triples with angle brackets and quotes around the object
formatted_triplets = [f"<{triplet.strip()}>" for triplet in new_triplets]

# Convert the list of new triplets to a set to ensure uniqueness
unique_new_triplets = set(formatted_triplets)

# Combine the original unique triplets and new unique triplets
all_triplets = unique_triplets.union(unique_new_triplets)

# Write the new unique triplets to a file
with open('new_triples.txt', 'w') as file:
    for triplet in unique_new_triplets:
        file.write(f"{triplet}\n")  # Write each new triple in a new line

# Print the combined unique triples array
print("Completed Knowledge Graph Triples:\n", all_triplets)


