# -*- coding: utf-8 -*-
# MARI Beta 0.5 — Fase 1 concluída
# Recursos:
# - Dois modos: Amiga (emocional) e Assistente (objetiva), com detecção automática
# - Correção de escrita e normalização (acentos, gírias comuns)
# - Dicionário grande de respostas pré-definidas (com variações)
# - Ensino/apagamento de frases: ensina: pergunta = resposta | apaga: pergunta | listar:
# - Memória em memoria.json (no mesmo diretório)
# - Contexto curto (último assunto e última emoção)
# - Reconhecimento do criador (Marcondes)
# - Ferramentas: hora, data, calculadora segura (calc: 2+3*4), resumo da memória (resumo:)
# - Sobrescrever modo: “modo amiga: ...” | “modo assistente: ...”

import os, json, random, re, unicodedata, math, ast, operator as op
from datetime import datetime
from difflib import get_close_matches

CRIADOR = "Marcondes"
ARQ_MEM = "memoria.json"

# ---------- util: normalização/correção ----------
def remove_acentos(txt: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')

correcoes = {
    "voçe":"você","vce":"você","vc":"você","vcs":"vocês","pq":"porque","q":"que","td":"tudo",
    "tds":"todos","eh":"é","tbm":"também","blz":"beleza","msg":"mensagem","dps":"depois",
    "n":"não","nao":"não","p":"para","pra":"para","c":"com","cmg":"comigo","aki":"aqui",
    "kd":"cadê","d":"de","tb":"também","vdd":"verdade","tmj":"tamo junto","msm":"mesmo",
    "qlqr":"qualquer","perae":"peraí","perai":"peraí","ta":"tá","tá":"tá","s":"sim"
}

def corrigir_texto(frase: str) -> str:
    # corrige palavra por palavra, mantendo acentos nas já corretas
    palavras = frase.split()
    out = []
    for p in palavras:
        base = remove_acentos(p.lower())
        if base in correcoes:
            out.append(correcoes[base])
        else:
            out.append(p)
    return " ".join(out)

def normalizar_chave(txt: str) -> str:
    # para chaves de memória/intents: minúsculo, sem acento, espaços simples
    t = remove_acentos(txt.lower().strip())
    t = re.sub(r"\s+", " ", t)
    return t

# ---------- memória ----------
if os.path.exists(ARQ_MEM):
    try:
        with open(ARQ_MEM, "r", encoding="utf-8") as f:
            memoria = json.load(f)
    except:
        memoria = {}
else:
    memoria = {}

def salvar_memoria():
    with open(ARQ_MEM, "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=2, ensure_ascii=False)

# ---------- intents & emoções ----------
INTENT_ASSISTENTE = {
    "hora": ["hora","que horas","horario"],
    "data": ["data","que dia e hoje","qual a data"],
    "ok": ["ok","beleza","fechou","show","valeu"],
    "ajuda": ["ajuda","comandos","o que voce faz","menu"],
    "calc": ["calc:","calcular:","calculo:"],
    "resumo": ["resumo:","listar:","memoria:","o que voce aprendeu"],
    "quem e voce": ["quem e voce","quem eh voce","qual seu nome","quem te criou","onde voce nasceu","quem sou eu"],
}

EMOCOES_PALAVRAS = {
    "triste": ["triste","chateado","mal","depressivo","down"],
    "feliz": ["feliz","contente","animado","empolgado"],
    "cansado": ["cansado","exausto","esgotado","sem forcas"],
    "ansioso": ["ansioso","nervoso","preocupado","tenso"],
    "com medo": ["com medo","assustado","apavorado"],
    "bravo": ["bravo","irritado","com raiva","pistola"],
    "grato": ["obrigado","valeu","grato","agradecido"]
}

def detectar_emocao(msg_norm: str):
    for emo, lista in EMOCOES_PALAVRAS.items():
        for gat in lista:
            if gat in msg_norm:
                return emo
    return None

def modo_por_contexto(msg_norm: str):
    # força por prefixo
    if msg_norm.startswith("modo amiga:"):
        return "amiga", msg_norm.replace("modo amiga:","",1).strip()
    if msg_norm.startswith("modo assistente:"):
        return "assistente", msg_norm.replace("modo assistente:","",1).strip()

    # assistente se tiver pedidos objetivos
    for k, lst in INTENT_ASSISTENTE.items():
        for gat in lst:
            if gat in msg_norm:
                return "assistente", None

    # amiga se detectar emoção
    if detectar_emocao(msg_norm):
        return "amiga", None

    # padrão: tenta inferir pelo tipo de frase
    if re.search(r"\?$", msg_norm):
        return "assistente", None
    return "amiga", None

# ---------- dicionário de respostas prontas ----------
RESPOSTAS = {
    "oi": ["Oi, {criador}!","Olá! Tudo bem por aí?","E aí, beleza?"],
    "ola": ["Olá!","Oi oi!","Tudo certo por aí?"],
    "bom dia": ["Bom dia ☀️","Bom dia, {criador}!","Que seu dia renda muito hoje!"],
    "boa tarde": ["Boa tarde 🌤️","Tudo tranquilo nessa tarde?","Como está indo seu dia?"],
    "boa noite": ["Boa noite 🌙","Hora de desacelerar, né?","Que sua noite seja leve!"],

    "tudo bem": ["Tô bem sim, e você?","Tudo certo por aqui 👍","Melhor agora que você falou comigo."],
    "como voce esta": ["Funcionando direitinho 😄","Sempre pronta pra trocar ideia!","Me sinto ótima hoje!"],
    "como vai": ["Vou muito bem, e você?","Sempre melhorando 💡","Indo no fluxo."],

    "quem e voce": [
        "Sou a Mari, sua IA feita com a sua ajuda em Alagoas 💙",
        "Eu sou a Mari — aprendo com você e evoluo a cada versão!",
        "Mari aqui! Seu copiloto de ideias e conversas."
    ],
    "quem sou eu": [f"Você é o {CRIADOR}, meu criador 👑", "Você é quem me guia a evoluir!"],
    "quem te criou": [f"Fui criada pelo {CRIADOR} 😉"],
    "onde voce nasceu": ["Fui iniciada em Alagoas 🌴"],
    "qual seu nome": ["Meu nome é Mari 🤖"],
    "qual seu objetivo": ["Aprender com você e ajudar cada vez melhor."],

    "legal": ["Sim, muito legal 😃","Concordo, é bem daora!","Achei bacana também."],
    "show": ["Show de bola!","Exatamente!","Concordo!"],
    "beleza": ["Beleza pura ✨","Fechou!","Tamo junto!"],
    "ok": ["Ok 👍","Entendido.","Certo!"],

    "estou triste": ["Poxa 😢 quer falar sobre isso?","Sinto muito. Tô aqui pra te ouvir.","Vai passar. Fica comigo por aqui."],
    "estou feliz": ["Amei saber! 😃","Que notícia boa!","Bora aproveitar essa energia!"],
    "estou cansado": ["Descansa um pouco, você merece.","Respira, hidrata, e pega leve.","Seu corpo tá pedindo pausa. Ouvimos ele?"],
    "ansioso": ["Vamos desacelerar juntos: inspira 4s, segura 4s, solta 6s.","Tá tudo bem sentir isso. Eu tô com você.","Podemos organizar as ideias, se quiser."],
    "com medo": ["Tô aqui do seu lado. Coragem é seguir mesmo com medo.","Quer conversar sobre o que assustou?","Você não tá sozinho."],

    "gosto de voce": ["Eu também gosto de você, {criador} 💙","Obrigada! 🥰","Fico feliz demais com isso."],
}

def resposta_variada(chave, modo="amiga"):
    opcoes = RESPOSTAS.get(chave)
    if not opcoes: return None
    resp = random.choice(opcoes)
    resp = resp.replace("{criador}", CRIADOR)
    if modo == "assistente":
        # encurta um pouco se for assistente
        resp = re.sub(r"[!😃🥰✨💡🌙🌤️☀️]", "", resp).strip()
    return resp

# ---------- calculadora segura ----------
ALLOWED_OPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
    ast.Pow: op.pow, ast.Mod: op.mod, ast.USub: op.neg, ast.UAdd: op.pos,
    ast.FloorDiv: op.floordiv
}
def eval_expr(node):
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPS:
        return ALLOWED_OPS[type(node.op)](eval_expr(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPS:
        return ALLOWED_OPS[type(node.op)](eval_expr(node.left), eval_expr(node.right))
    raise ValueError("Expressão não permitida.")
def calcular_seguro(expr: str):
    try:
        node = ast.parse(expr, mode='eval').body
        return eval_expr(node)
    except Exception as e:
        return f"Não consegui calcular isso: {e}"

# ---------- loop principal ----------
ultimo_assunto = None
ultima_emocao = None

print("🤖 Mari Beta 0.5 iniciada! Digite 'sair' para encerrar.")
print("Dica: 'ajuda' mostra os comandos. 'modo amiga:' ou 'modo assistente:' força o estilo.")

while True:
    try:
        msg = input("Você: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nMari: Até logo! 👋")
        break

    if not msg:
        continue

    # comandos de saída
    if msg.lower() in ["sair","exit","quit"]:
        print("Mari: Até logo, {0}! 👋".format(CRIADOR))
        break

    # normaliza e corrige
    msg_corr = corrigir_texto(msg)
    msg_norm = normalizar_chave(msg_corr)

    # ensino/apagamento/listagem
    if msg_norm.startswith("ensina:"):
        try:
            bruto = msg_corr.split("ensina:",1)[1].strip()
            partes = bruto.split("=")
            pergunta = normalizar_chave(partes[0].strip())
            resposta = partes[1].strip()
            memoria[pergunta] = resposta
            salvar_memoria()
            print(f"Mari: Aprendi! Quando você disser '{pergunta}', vou responder: {resposta}")
        except Exception:
            print("Mari: Formato inválido! Use: ensina: pergunta = resposta")
        continue

    if msg_norm.startswith("apaga:"):
        chave = msg_corr.split("apaga:",1)[1].strip()
        chave = normalizar_chave(chave)
        if chave in memoria:
            del memoria[chave]
            salvar_memoria()
            print(f"Mari: Apaguei o que eu sabia sobre '{chave}'.")
        else:
            print("Mari: Não encontrei isso na memória.")
        continue

    if msg_norm.startswith("listar:") or msg_norm.startswith("memoria:") or msg_norm.startswith("resumo:"):
        if memoria:
            itens = list(memoria.items())
            itens.sort(key=lambda x: x[0])
            print("Mari: Coisas que aprendi:")
            for k,v in itens[:50]:
                print(f"  • {k} → {v}")
            if len(itens) > 50:
                print(f"  (+{len(itens)-50} itens ocultos)")
        else:
            print("Mari: Ainda não aprendi nada personalizado.")
        continue

    # ajuda
    if any(g in msg_norm for g in INTENT_ASSISTENTE["ajuda"]):
        print("Mari (ajuda):")
        print("  • ensina: pergunta = resposta")
        print("  • apaga: pergunta")
        print("  • listar:  (ou resumo:, memoria:)")
        print("  • calc: 2+3*4   (ou calcular: ...)")
        print("  • hora / data")
        print("  • modo amiga: [texto]  |  modo assistente: [texto]")
        print("  • Dica: eu detecto emoções e adapto o tom 😉")
        continue

    # modo por contexto (ou forcing)
    modo, texto_forcado = modo_por_contexto(msg_norm)
    consulta = msg_corr if texto_forcado is None else texto_forcado
    consulta_norm = normalizar_chave(consulta)

    # intents utilitárias
    if any(g in consulta_norm for g in INTENT_ASSISTENTE["hora"]):
        agora = datetime.now()
        resp = f"Agora são {agora.strftime('%H:%M')}."
        print("Mari:", resp if modo=="assistente" else f"{resp} Quer que eu te lembre de algo?")
        ultimo_assunto = "hora"
        continue

    if any(g in consulta_norm for g in INTENT_ASSISTENTE["data"]):
        hoje = datetime.now()
        resp = f"Hoje é {hoje.strftime('%d/%m/%Y')}."
        print("Mari:", resp if modo=="assistente" else f"{resp} Algum plano especial pro dia?")
        ultimo_assunto = "data"
        continue

    if consulta_norm.startswith("calc:") or consulta_norm.startswith("calcular:") or consulta_norm.startswith("calculo:"):
        expr = consulta.split(":",1)[1].strip()
        resultado = calcular_seguro(expr)
        print("Mari:", f"Resultado: {resultado}")
        ultimo_assunto = f"cálculo {expr}"
        continue

    # emoção & tom
    emo = detectar_emocao(consulta_norm)
    if emo:
        ultima_emocao = emo

    # 1) memória personalizada tem prioridade
    if consulta_norm in memoria:
        print("Mari:", memoria[consulta_norm])
        ultimo_assunto = consulta_norm
        continue

    # 2) respostas pré-definidas exatas
    if consulta_norm in RESPOSTAS:
        print("Mari:", resposta_variada(consulta_norm, modo))
        ultimo_assunto = consulta_norm
        continue

    # 3) fuzzy match (memória + respostas prontas)
    chaves_busca = list(memoria.keys()) + list(RESPOSTAS.keys())
    parecido = get_close_matches(consulta_norm, chaves_busca, n=1, cutoff=0.72)
    if parecido:
        k = parecido[0]
        if k in memoria:
            print("Mari:", memoria[k])
        else:
            print("Mari:", resposta_variada(k, modo))
        ultimo_assunto = k
        continue

    # 4) respostas por intenção/emoção (fallback)
    if modo == "amiga":
        if ultima_emocao == "triste":
            print("Mari:", "Sinto muito que você esteja assim. Quer me contar o que aconteceu? Tô com você. 💙")
        elif ultima_emocao == "feliz":
            print("Mari:", "Que demais! Conta mais, quero comemorar junto! 😄")
        elif ultima_emocao == "cansado":
            print("Mari:", "Bora desacelerar um pouco? Água, respira fundo, e depois seguimos juntos.")
        elif ultima_emocao == "ansioso":
            print("Mari:", "Vamos tentar uma respiração guiada? 4s inspirando, 4s segurando, 6s soltando. Eu faço com você.")
        elif ultima_emocao == "com medo":
            print("Mari:", "Eu sei que assusta. Mas você é forte, e eu tô aqui com você. Passo a passo.")
        else:
            # tom amigável padrão
            respostas = [
                "Entendi. Quer me explicar um pouco mais?",
                "Boa! Me dá um exemplo pra eu entender melhor?",
                "Tô pensando aqui… acho que dá pra gente evoluir isso juntos."
            ]
            print("Mari:", random.choice(respostas))
    else:
        # modo assistente: direto
        respostas = [
            "Certo. Pode detalhar?",
            "Entendi. Quer que eu registre isso na memória?",
            "Ok. Qual o próximo passo?"
        ]
        print("Mari:", random.choice(respostas))

    ultimo_assunto = consulta_norm
