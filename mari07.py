import json
import os

MEMORIA_ARQUIVO = "memoria.json"

# Carregar memória
def carregar_memoria():
    if os.path.exists(MEMORIA_ARQUIVO):
        with open(MEMORIA_ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "saudacoes": {},
            "informacoes": {"dono": {}},
            "curiosidades": {},
            "fatos": {},
            "humor": "neutro",
            "stats": {"interacoes": 0},
            "despedida": {}
        }

# Salvar memória
def salvar_memoria(memoria):
    with open(MEMORIA_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=2)

# Buscar resposta em qualquer categoria
def buscar_resposta(memoria, pergunta):
    for categoria, conteudo in memoria.items():
        if isinstance(conteudo, dict):
            for chave, valor in conteudo.items():
                if isinstance(valor, str) and chave.lower() == pergunta.lower():
                    return valor
                elif isinstance(valor, dict):
                    for sub_chave, sub_valor in valor.items():
                        if sub_chave.lower() == pergunta.lower():
                            return sub_valor
    return None

# Adicionar novo aprendizado
def aprender(memoria, chave, resposta):
    if "curiosidades" not in memoria:
        memoria["curiosidades"] = {}
    memoria["curiosidades"][chave] = resposta
    salvar_memoria(memoria)

# -------------------------
# PROGRAMA PRINCIPAL
# -------------------------
print("🤖 Mari Beta 0.7 iniciada! Digite 'sair' para encerrar.")

memoria = carregar_memoria()

while True:
    entrada = input("Você: ").strip().lower()
    memoria["stats"]["interacoes"] += 1

    if entrada == "sair":
        print("Mari:", memoria["despedida"].get("sair", "Até logo! 👋"))
        salvar_memoria(memoria)
        break

    elif entrada.startswith("ensina:"):
        try:
            partes = entrada.replace("ensina:", "").split("=")
            chave = partes[0].strip()
            resposta = partes[1].strip()
            aprender(memoria, chave, resposta)
            print(f"Mari: Aprendi! Quando você disser '{chave}', vou responder: {resposta}")
        except:
            print("Mari: Formato inválido! Use: ensina: pergunta = resposta")

    elif entrada == "list":
        print("Mari: Coisas que aprendi:")
        for categoria, conteudo in memoria.items():
            if isinstance(conteudo, dict):
                for chave in conteudo:
                    print(f" • {chave}")
        continue

    else:
        resposta = buscar_resposta(memoria, entrada)
        if resposta:
            print("Mari:", resposta)
        else:
            print(f"Mari: Não entendi '{entrada}'. Quer me ensinar a resposta?")
