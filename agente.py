import json

class AdaptiveTutorAgent:
    def __init__(self, llm_model, rag_vector_store, mcp_client):
        self.llm = llm_model  # Ex: Família Llama local (ex: Llama 3)
        self.rag = rag_vector_store  # Base de conhecimento vetorizada
        self.mcp = mcp_client  # Model Context Protocol para segurança

    def process_student_query(self, student_id, query_text, code_context, emotional_indicators):
        # Passo 1: Padronização e encapsulamento do contexto via MCP
        context_payload = self.mcp.standardize_context(
            student_id=student_id,
            query=query_text,
            code=code_context,
            metrics=emotional_indicators
        )

        # Passo 2: Recuperação de contexto fático e pedagógico via RAG
        retrieved_docs = self.rag.similarity_search(
            query=query_text,
            k=3
        )
        pedagogical_guidelines = [doc.text for doc in retrieved_docs]

        # Passo 3: Montagem do Prompt Aumentado (Llama + Contexto + Scaffolding)
        system_prompt = (
            "Você é um tutor inteligente empático e adaptativo. "
            "Seu objetivo é reduzir a sobrecarga cognitiva do estudante. "
            "NÃO forneça o código pronto. Utilize a técnica de scaffolding (microfases), "
            "dividindo o problema conceitual e oferecendo suporte gradual."
        )
        
        augmented_prompt = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Contexto Institucional: {json.dumps(pedagogical_guidelines)}\n\n"
                                        f"Estado do Aluno (MCP): {json.dumps(context_payload)}\n\n"
                                        f"Dúvida: {query_text}"}
        ]

        # Passo 4: Geração de Resposta Local via Llama
        response = self.llm.generate(augmented_prompt)
        return response