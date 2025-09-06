import json
import os
import datetime

MEMORIA_ARQUIVO = os.path.expanduser("~/mari/memoria.json")

# ---------- Funções de Memória ----------
def carregar_memoria():
    if os.path.exists(MEMORIA_ARQUIVO):
        try:
            with open(MEMORIA_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def salvar_memoria(memoria):
    with open(MEMORIA_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=4)

# ---------- Comandos Fixos ----------
def comando_hora():
    agora = datetime.datetime.now().strftime("%H:%M:%S")
    return f"⏰ Agora são {agora}"

def comando_calcular(expressao):
    try:
        resultado = eval(expressao, {"__builtins__": {}})
        return f"🧮 Resultado: {resultado}"
    except:
        return "Não consegui calcular isso 😅"

def comando_listar(memoria):
    if not memoria:
        return "📂 A memória está vazia."
    resposta = "📖 Memória atual:\n"
    for chave in memoria:
        resposta += f"- {chave} → {memoria[chave]}\n"
    return resposta

def comando_apagar(memoria, chave):
    if chave in memoria:
        del memoria[chave]
        salvar_memoria(memoria)
        return f"❌ Apaguei '{chave}' da memória."
    else:
        return f"Não encontrei '{chave}' na memória."

# ---------- Inicializar memória ----------
memoria = carregar_memoria()

# Dicionário inicial (só adiciona se ainda não existir)
iniciais = {
    "oi": "Oi Conde 👑, em que posso te ajudar hoje?",
    "oi mari": "Oi Conde 👑, eu sou a Mari! Como posso te ajudar?",
    "quem te criou": "Fui criada pelo Marcondes (Conde) 👑",
    "como você está": "Estou bem e pronta para ajudar você 😉",
    "tudo bem": "Sim, tudo ótimo e com você?"
}
for k, v in iniciais.items():
    if k not in memoria:
        memoria[k] = v
salvar_memoria(memoria)

print("🤖 Mari Beta 0.9 iniciada! Digite 'sair' para encerrar.")
print("💡 Dica: use 'listar' para ver o que já ensinei para a Mari")

# ---------- Loop principal ----------
while True:
    entrada = input("Você: ").strip().lower()

    if entrada == "sair":
        print("Mari: Até logo, Conde! 👋")
        break

    elif entrada == "hora":
        print("Mari:", comando_hora())

    elif entrada.startswith("calcular "):
        expressao = entrada.replace("calcular ", "")
        print("Mari:", comando_calcular(expressao))

    elif entrada == "listar":
        print("Mari:", comando_listar(memoria))

    elif entrada.startswith("apagar "):
        chave = entrada.replace("apagar ", "").strip()
        print("Mari:", comando_apagar(memoria, chave))

    elif entrada in memoria:
        print("Mari:", memoria[entrada])

    else:
        print(f"Mari: Não entendi '{entrada}'. Quer me ensinar a resposta? (s/n)")
        escolha = input().strip().lower()
        if escolha == "s":
            resposta = input("Digite a resposta: ")
            memoria[entrada] = resposta
            salvar_memoria(memoria)
            print("Mari: Aprendi algo novo! 🧠✨")
