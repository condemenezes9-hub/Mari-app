import json
import os

MEMORIA_ARQUIVO = os.path.expanduser("~/mari/memoria.json")

# Função para carregar memória
def carregar_memoria():
    if os.path.exists(MEMORIA_ARQUIVO):
        try:
            with open(MEMORIA_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Erro no arquivo de memória. Criando nova memória...")
            return {"dono": {}, "fatos": {}, "humor": "neutro"}
    return {"dono": {}, "fatos": {}, "humor": "neutro"}

# Função para salvar memória
def salvar_memoria(memoria):
    with open(MEMORIA_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=4, ensure_ascii=False)

# Carregar memória ao iniciar
memoria = carregar_memoria()

# Inicializar informações do dono se não existirem
if "dono" not in memoria or not memoria["dono"]:
    memoria["dono"] = {"nome": "Marcondes", "apelido": "Conde", "local": "Alagoas"}
    salvar_memoria(memoria)

print("🤖 Mari Beta 0.8 iniciada! Digite 'sair' para encerrar.")
print("💡 Dica: use 'listar' para ver o que já ensinei para a Mari.\n")

# Loop principal
while True:
    entrada = input("Você: ").strip().lower()

    if entrada == "sair":
        print(f"Mari: Até logo, {memoria['dono'].get('apelido','amigo')}! 👋")
        break

    elif entrada == "listar":
        print("\n📜 Memória atual da Mari:")
        for pergunta, resposta in memoria["fatos"].items():
            print(f"❓ {pergunta} → 💬 {resposta}")
        print()
        continue

    # Respostas já aprendidas
    if entrada in memoria["fatos"]:
        print("Mari:", memoria["fatos"][entrada])
        continue

    # Respostas padrão / criador
    if entrada in ["oi", "olá", "ei", "eai", "iae"]:
        print(f"Mari: Oi {memoria['dono'].get('apelido','')} 👑, em que posso te ajudar hoje?")
        continue

    if entrada in ["quem é seu criador?", "quem te criou?", "seu dono"]:
        print(f"Mari: Fui criada pelo {memoria['dono'].get('nome','meu criador')} 👑, diretamente de {memoria['dono'].get('local','um lugar especial')} 😉")
        continue

    if entrada in ["tudo bem?", "como você está?", "como vai?"]:
        print("Mari: Estou ótima 😄 e você?")
        continue

    # Caso não saiba
    print(f"Mari: Não entendi '{entrada}'. Quer me ensinar a resposta?")
    ensinar = input("Ensinar (s/n): ").strip().lower()

    if ensinar == "s":
        nova_resposta = input("Digite a resposta: ")
        memoria["fatos"][entrada] = nova_resposta
        salvar_memoria(memoria)
        print("Mari: Aprendi algo novo! 🧠✨")
