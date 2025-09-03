def process_quiz_answers(answers):
    """
    Processa as respostas do quiz para gerar um perfil de aprendizagem simplificado.
    """
    profile = {
        "estilo_aprendizagem": "",
        "interesses_principais": [],
        "preferencia_dificuldade": "",
        "motivacao": []
    }

    # Lógica simplificada para determinar o estilo de aprendizagem
    if answers.get("q1_learning_preference") == "pratico":
        profile["estilo_aprendizagem"] = "Cinestésico (Prático)"
    elif answers.get("q1_learning_preference") == "visual":
        profile["estilo_aprendizagem"] = "Visual"
    elif answers.get("q1_learning_preference") == "auditivo":
        profile["estilo_aprendizagem"] = "Auditivo"
    else:
        profile["estilo_aprendizagem"] = "Leitura/Escrita"

    # Lógica para interesses principais (exemplo com base em matérias)
    if "matematica" in answers.get("q2_favorite_subjects", []):
        profile["interesses_principais"].append("Matemática/Lógica")
    if "robotica" in answers.get("q2_favorite_subjects", []):
        profile["interesses_principais"].append("Robótica/Programação")
    if "ciencias" in answers.get("q2_favorite_subjects", []):
        profile["interesses_principais"].append("Ciências/Experimentação")
    if "arte" in answers.get("q2_favorite_subjects", []):
        profile["interesses_principais"].append("Arte/Criatividade")

    # Preferência de dificuldade
    profile["preferencia_dificuldade"] = answers.get("q3_challenge_preference", "medio")

    # Motivação
    if "desafios" in answers.get("q4_motivation", []):
        profile["motivacao"].append("Gostar de desafios")
    if "recompensas" in answers.get("q4_motivation", []):
        profile["motivacao"].append("Recompensas e reconhecimento")
    if "aprender_novo" in answers.get("q4_motivation", []):
        profile["motivacao"].append("Aprender coisas novas")

    return profile

# --- Simulação de Respostas do Quiz ---
# Estas respostas simulam o que um aluno poderia escolher no quiz.
# Você pode alterar esses valores para ver como o perfil muda.

simulated_answers = {
    "q1_learning_preference": "pratico", # opções: "visual", "auditivo", "pratico", "leitura_escrita"
    "q2_favorite_subjects": ["matematica", "robotica", "ciencias"], # opções: "matematica", "ciencias", "portugues", "ingles", "historia", "geografia", "arte", "educacao_fisica", "robotica", "programacao"
    "q3_challenge_preference": "dificil", # opções: "facil", "medio", "dificil"
    "q4_motivation": ["desafios", "recompensas"] # opções: "pontos", "competicao", "colaboracao", "descoberta", "criacao", "reconhecimento", "diversao", "conquista"
}

# Processa as respostas simuladas
learning_profile = process_quiz_answers(simulated_answers)

# Imprime o perfil de aprendizagem gerado
print("--- Perfil de Aprendizagem Gerado ---")
for key, value in learning_profile.items():
    print(f"{key.replace("_", " ").title()}: {value}")

print("\nEste é um exemplo simplificado da lógica de IA do aplicativo.")
print("Você pode copiar este código e colá-lo no mycompiler.io para testar.")
print("Altere os valores em 'simulated_answers' para ver diferentes perfis!")


