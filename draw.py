import networkx as nx
import matplotlib.pyplot as plt

def read_relations(file_path):
    relations = []
    with open(file_path, 'r') as file:
        for line in file:
            # Remove angle brackets and strip whitespace
            line = line.strip().replace('<', '').replace('>', '')
            parts = line.split(',')
            if len(parts) == 3:
                subject = parts[0].strip()
                predicate = parts[1].strip()
                obj = parts[2].strip()
                relations.append((subject, predicate, obj))
    return relations

def draw_knowledge_graph(relations):
    G = nx.DiGraph()

    for subj, pred, obj in relations:
        G.add_node(subj, label=subj)
        G.add_node(obj, label=obj)
        G.add_edge(subj, obj, label=pred)

    pos = nx.spring_layout(G)

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title('Knowledge Graph')
    plt.show()

def main():
    
    output_file_path = 'output.txt'

    # Read the relations from the file
    relations = read_relations(output_file_path)

    # Draw the knowledge graph
    draw_knowledge_graph(relations)

if __name__ == "__main__":
    main()
