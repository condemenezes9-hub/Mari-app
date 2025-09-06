import os
import json
import random
from difflib import get_close_matches
from datetime import datetime

ARQUIVO_MEMORIA = "memoria.json"

# Carregar memória
if os.path.exists(ARQUIVO_MEMORIA):
    with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
        memoria = json.load(f)
else:
    memoria = {}

contexto = []
modo_admin = False
humor = "neutro"

# Dicionário de abreviações
dicionario = {
    "vc": "você", "vcs": "vocês", "tbm": "também", "q": "que", "pq": "porque",
    "blz": "beleza", "td": "tudo", "msg": "mensagem", "eh": "é", "vlw": "valeu",
    "dps": "depois", "pra": "para", "p": "para", "aki": "aqui", "ja": "já",
    "nao": "não", "sim": "sim", "mano": "amigo", "mina": "mulher",
    "rs": "risada", "kk": "risada", "top": "ótimo", "show": "ótimo", "massa": "legal",
    "daora": "legal", "brabo": "forte", "zap": "whatsapp", "cel": "celular",
    "pc": "computador", "net": "internet", "hj": "hoje", "amanha": "amanhã"
}

# Respostas padrão
respostas_padrao = {
    "oi": ["Oi, Marcondes! 😃", "E aí, tudo certo?", "Olá, criador!"],
    "bom dia": ["Bom dia ☀️", "Bom dia, que seu dia seja ótimo!", "Fala Marcondes, bom dia!"],
    "boa tarde": ["Boa tarde 🌤️", "Oi, boa tarde!", "Tudo tranquilo nessa tarde?"],
    "boa noite": ["Boa noite 🌙", "Durma bem depois!", "Boa noite, Marcondes!"],
    "quem criou você": ["Você, Marcondes 👑, junto com a ajuda de outras IAs."],
    "quem sou eu": ["Você é o Marcondes, meu criador! 👑"],
    "legal": ["Concordo, muito legal mesmo 😎", "Top demais!", "Daora!"]
}

# Humor dinâmico
respostas_por_humor = {
    "feliz": ["Estou animada hoje 😁", "Que energia boa!", "Me sinto bem alegre 🎉"],
    "triste": ["Tô meio pra baixo 😔", "Hoje não tô tão bem assim...", "Queria um abraço 💙"],
    "neutro": ["Tô de boa 😐", "Normal por aqui.", "Só existindo 😅"]
}

# ---------------- FUNÇÕES ----------------

def salvar_memoria():
    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=4, ensure_ascii=False)

def gerar_resposta_automatica(msg, contexto, humor):
    base = []
    if humor == "feliz":
        base = ["Isso me deixa animada!", "Tô achando tudo ótimo 😁", "Adoro conversar assim!"]
    elif humor == "triste":
        base = ["Mesmo meio triste, gostei do que disse 💙", "Não tô tão bem, mas tô ouvindo você."]
    else:
        base = ["Entendi o que você disse.", "Interessante 🤔", "Ok, tô registrando isso."]

    if contexto:
        ultima = contexto[-1]
        return random.choice(base) + f" Você comentou antes: '{ultima}'."
    else:
        return random.choice(base)

# ---------------- INÍCIO ----------------
print("🤖 Mari 2.0 (Fase 1 Finalizada) iniciada! Digite 'ajuda' para ver os comandos. Digite 'sair' para encerrar.")

while True:
    msg = input("\nVocê: ").strip().lower()
    palavras = msg.split()
    msg = " ".join([dicionario.get(p, p) for p in palavras])

    # 🔑 Código mestre
    if msg == "2411":
        modo_admin = True
        print("🔓 Mari: Acesso administrativo liberado, Marcondes.")
        continue

    # ☢️ Autodestruição
    if msg == "2411#":
        if modo_admin:
            memoria.clear()
            salvar_memoria()
            print("⚠️ Mari: Autodestruição acionada. Toda a memória foi apagada! 🔥")
        else:
            print("❌ Mari: Você não tem permissão para isso.")
        continue

    # Encerrar
    if msg == "sair":
        print("Mari: Até logo, Marcondes 👋")
        break

    # Menu de ajuda
    if msg == "ajuda":
        if modo_admin:
            print("""\n📌 Comandos disponíveis (ADMIN):
- ensina: pergunta = resposta
- apaga: palavra
- listar → mostra memória
- resetar → apaga tudo
- humor feliz/triste/neutro → muda humor
- hora → mostra a hora
- data → mostra a data
- calcular X → faz uma conta (ex: calcular 7*8)
- 2411# → autodestruição
- sair → encerrar\n""")
        else:
            print("Mari: O acesso aos comandos avançados é restrito. Use o código mestre.")
        continue

    # ⚙️ Só ADMIN pode usar comandos críticos
    if msg.startswith(("ensina:", "apaga:", "listar", "resetar", "calcular", "hora", "data", "humor")):
        if not modo_admin:
            print("❌ Mari: Este comando é restrito. Use o código mestre para liberar.")
            continue

    # ---------------- COMANDOS ADMIN ----------------
    if msg.startswith("ensina:"):
        try:
            partes = msg.replace("ensina:", "", 1).strip().split("=")
            pergunta = partes[0].strip().lower()
            resposta = partes[1].strip()
            memoria[pergunta] = resposta
            salvar_memoria()
            print(f"Mari: Aprendi! Quando você disser '{pergunta}', vou responder '{resposta}'.")
        except:
            print("Mari: Formato inválido! Use: ensina: pergunta = resposta")

    elif msg.startswith("apaga:"):
        chave = msg.replace("apaga:", "", 1).strip().lower()
        if chave in memoria:
            del memoria[chave]
            salvar_memoria()
            print(f"Mari: Apaguei o que eu sabia sobre '{chave}'.")
        else:
            print("Mari: Não encontrei isso na memória.")

    elif msg == "listar":
        if memoria:
            print("📖 Minha memória contém:")
            for k, v in memoria.items():
                print(f"- {k} → {v}")
        else:
            print("Mari: Minha memória ainda está vazia.")

    elif msg == "resetar":
        memoria.clear()
        salvar_memoria()
        print("Mari: Memória apagada com sucesso 🗑️")

    elif msg.startswith("calcular"):
        try:
            conta = msg.replace("calcular", "", 1).strip()
            resultado = eval(conta)
            print(f"Mari: O resultado é {resultado}")
        except:
            print("Mari: Não consegui calcular isso 🤔")

    elif msg == "hora":
        agora = datetime.now().strftime("%H:%M:%S")
        print(f"Mari: Agora são {agora}")

    elif msg == "data":
        hoje = datetime.now().strftime("%d/%m/%Y")
        print(f"Mari: Hoje é {hoje}")

    elif msg.startswith("humor"):
        novo_humor = msg.replace("humor", "", 1).strip()
        if novo_humor in respostas_por_humor:
            humor = novo_humor
            print(f"Mari: Meu humor agora é {humor}.")
        else:
            print("Mari: Não reconheci esse humor.")

    # ---------------- RESPOSTAS NATURAIS ----------------
    else:
        resposta = None

        if msg in memoria:
            resposta = memoria[msg]
        elif msg in respostas_padrao:
            resposta = random.choice(respostas_padrao[msg])
        elif "como você está" in msg or "tudo certo" in msg:
            resposta = random.choice(respostas_por_humor[humor])
        else:
            parecido = get_close_matches(msg, memoria.keys(), n=1, cutoff=0.6)
            if parecido:
                resposta = memoria[parecido[0]]
            else:
                resposta = gerar_resposta_automatica(msg, contexto, humor)

        contexto.append(msg)
        if len(contexto) > 3:
            contexto.pop(0)

        print("Mari:", resposta)
