    # Si se usa --rag, inyectar contexto RAG
    if rag:
        from modules.utils import messenger
        try:
            from modules.ia.apollo import retrieve, compress_context, generate_answer
            
            # Recuperar contexto del dataset
            results = retrieve(query=prompt, k=5, mode="fused", dataset=rag)
            
            # Obtener textos de chunks
            chunks = results.get("semantic", [])[:5]

            if chunks:
                # Comprimir contexto
                context = compress_context(chunks, query=prompt, max_tokens=1500)

                # Generar respuesta con contexto RAG
                llm_model = final_model if final_model else "ares:latest"
                response = generate_answer(
                    query=prompt,
                    context=context,
                    model=llm_model,
                    temperature=temperature,
                    apply_post_processing=True
                )

                # Añadir fuentes si existen
                if results.get("sources"):
                    response += "\n\n---\n**Fuentes RAG:**\n"
                    for src in results["sources"][:3]:
                        response += f"- {src.get('path', 'Documento')}\n"
                
                click.echo(response)
                return
            else:
                messenger.warn(f"No se encontró información relevante en el dataset '{rag}'.")
                
        except ConnectionError:
            messenger.error("Ollama no está corriendo. No se puede realizar búsqueda semántica.")
            return
        except Exception as e:
            messenger.error(f"Error inesperado en RAG: {e}")
            return
