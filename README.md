# 🧠 Bachelor Thesis: Auto Knowledge Graph Creation Using LLMs

This thesis explores the **automated generation of knowledge graphs** using **Large Language Models (LLMs)**. Knowledge graphs provide a structured and interconnected representation of information, enabling more effective data access and reasoning.

Leveraging the capabilities of state-of-the-art LLMs, such as **Meta’s LLaMA-3**, this work demonstrates how unstructured data (e.g., text, articles, or databases) can be transformed into structured knowledge through a **multi-agent system**. Each agent is responsible for a specific role, and through cooperation, they build accurate and complete knowledge graphs in real time.

---

## 📌 Abstract

LLMs significantly improve natural language understanding, enabling the extraction of entities and the creation of meaningful relations between them. This thesis proposes a **multi-agent architecture** that generates knowledge graphs automatically, utilizing both LLM capabilities and **external knowledge sources** such as:

- Knowledge bases  
- Pre-existing knowledge graphs  
- Web/network resources  

The results show that LLM-generated graphs are highly accurate and rich in information. The approach unlocks new potential for **automated knowledge management**, graph completion, and reasoning.

---

## 🛠️ How It Works

1. **Setup**
   - Clone the repository.
   - Install dependencies:  
     ```bash
     pip install -r requirements.txt
     ```
   - Add your **API Key** (e.g., for OpenAI or HuggingFace).
     > ⚠️ Note: A free trial API key may have limitations.

2. **Define Your Task**
   - Open `autokg.py`.
   - Edit the `"task"` variable to describe the goal (e.g., “Extract a knowledge graph about renewable energy”).

3. **Run the Graph Generator**
   - Run `autokg.py`.
   - Output: A file called `output.txt` containing the knowledge triples.

4. **Visualize the Knowledge Graph**
   - Use `draw.py` to generate a graphical visualization of the output:
     ```bash
     python draw.py
     ```

5. **Graph Completion**
   - Run `kg_completion.py` to enhance your graph with additional relationships:
     ```bash
     python kg_completion.py
     ```
   - Output: `new_triples.txt` with extended knowledge triples.

6. **Evaluate Your Graph**
   - Use the following scripts to assess graph quality:
     - `WCS.py` – Whole-graph Comparison Score  
     - `TWCS.py` – Triple-level Comparison Score

---

## 📚 Reference

This project is inspired by the work:

> Zhu, Yuqi et al.  
> *LLMs for Knowledge Graph Construction and Reasoning: Recent Capabilities and Future Opportunities*  
> [arXiv:2305.13168](https://arxiv.org/abs/2305.13168)  
> GitHub: [zjunlp/AutoKG](https://github.com/zjunlp/AutoKG)




