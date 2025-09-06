# MARI 2.2 — FASE 1 CONCLUÍDA
# Autor: Marcondes (criador) | Assistente: GPT
# Recursos:
# - Memória persistente (memoria.json) + dicionário base mesclado
# - Dicionário expandido: saudações, abreviações, gírias, sentimentos, variações
# - Aprendizado: ensina: pergunta = resposta  | apaga: chave
# - Listar memórias: listar
# - Hora/data: hora | data | hoje | agora
# - Cálculo: calc: <expressão>
# - Ajuda: ajuda (básica) / ajuda+ (avançada destravada)
# - Segurança por sessão: autenticar 2411  (desbloqueia comandos críticos)
# - Backup: 2411@backup  | Restauração: 2411@restaura <arquivo>.json
# - Auto-destruição (memória): 2411# (apaga memoria.json)
# - Geração de respostas quando não souber (heurística simples + dicionário)
# - Perfil do dono (Marcondes) embutido

import os, json, re, time, math, random, datetime
from difflib import get_close_matches

ARQ_MEM = "memoria.json"
PASTA_BACKUP = "backups"
os.makedirs(PASTA_BACKUP, exist_ok=True)

# ---------------------------
# DICIONÁRIO BASE (MESCLÁVEL)
# ---------------------------
DIC_BASE = {
    "perfil": {
        "dono_nome": "Marcondes",
        "assistant_nome": "Mari",
        "origem": "Iniciada em Alagoas",
        "criador": "Marcondes",
        "personalidade": "amigavel"  # amigavel | neutra | seria
    },
    "saudacoes": [
        "oi", "olá", "ola", "e ai", "eae", "salve", "bom dia", "boa tarde", "boa noite"
    ],
    "abreviacoes": {
        "vc": "você", "vcs": "vocês", "tb": "também", "tbm": "também", "q": "que",
        "pq": "porque", "pqp": "poxa", "obg": "obrigado", "pfv": "por favor",
        "blz": "beleza", "td": "tudo", "msg": "mensagem", "pra": "para",
        "p": "para", "dps": "depois", "vlw": "valeu", "n": "não", "sim?": "sim?"
    },
    "giras": {
        "mano":"amigo","mina":"mulher","daora":"legal","massa":"legal","show":"ótimo",
        "pode crer":"sim","demorou":"ok","ta ligado":"entende","bora":"vamos",
        "top":"excelente","brabo":"muito bom","suave":"tranquilo","de boa":"tranquilo",
        "sinistro":"assustador","trevoso":"assustador","macabro":"assustador"
    },
    "sentimentos": {
        "feliz":["feliz","contente","animado","alegre"],
        "triste":["triste","chateado","down","pra baixo"],
        "com medo":["com medo","assustado","apreensivo","tenso"],
        "zangado":["zangado","irritado","pistola"],
        "cansado":["cansado","exausto","acabado"]
    },
    "ortografia": {
        "voce":"você","pra":"para","aq":"aqui","aki":"aqui","ta":"tá","to":"tô",
        "quero":"quero","vc":"você","os":"os","as":"as","ja":"já","tbm":"também"
    },
    "sinonimos": {
        "legal":["massa","daora","show","top","maneiro","bacana","bom"],
        "ruim":["péssimo","fraco","chato","triste","negativo"],
        "assustador":["sinistro","macabro","trevoso","medonho"],
        "ajuda":["suporte","socorro","apoio","auxílio"],
        "rapido":["veloz","ligeiro","pronto"],
        "devagar":["lento","calmo","tranquilo"]
    },
    "conhecimento_curto": {
        "quem criou você?":"Fui criada por Marcondes, com ajuda de IAs, em Alagoas.",
        "qual seu nome?":"Eu sou a Mari. Prazer! ☺",
        "quem é seu dono?":"Meu dono/autor é o Marcondes.",
        "de onde você é?":"Fui iniciada em Alagoas, com muito carinho."
    }
}

# ---------------------------
# CARGA DA MEMÓRIA + MERGE
# ---------------------------
def carregar_memoria():
    if os.path.exists(ARQ_MEM):
        try:
            with open(ARQ_MEM, "r", encoding="utf-8") as f:
                mem = json.load(f)
            # mescla chaves ausentes do DIC_BASE
            for k,v in DIC_BASE.items():
                if k not in mem:
                    mem[k] = v
            return mem
        except:
            pass
    # se não existe, inicia com base
    with open(ARQ_MEM, "w", encoding="utf-8") as f:
        json.dump(DIC_BASE, f, ensure_ascii=False, indent=2)
    return json.loads(json.dumps(DIC_BASE))

memoria = carregar_memoria()

def salvar_memoria():
    with open(ARQ_MEM, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=2)

# ---------------------------
# UTILS
# ---------------------------
ACENTOS = str.maketrans(
    "áàãâäéèêëíìîïóòõôöúùûüçñ",
    "aaaaaeeeeiiiiooooouuuucn"
)
def normalizar(txt: str) -> str:
    return re.sub(r"\s+", " ", txt.lower().translate(ACENTOS)).strip()

def agora():
    return datetime.datetime.now()

def timestamp():
    return agora().strftime("%Y%m%d_%H%M%S")

def resposta_personalidade(txt):
    estilo = memoria.get("perfil",{}).get("personalidade","amigavel")
    if estilo == "amigavel":
        suffix = random.choice(["🙂","😉","😄","✨","👍"])
        return f"{txt} {suffix}"
    elif estilo == "seria":
        return txt
    else:
        return txt

def formatar_lista(lst):
    return ", ".join(lst) if isinstance(lst, list) else str(lst)

# ---------------------------
# SEGURANÇA DE SESSÃO
# ---------------------------
AUTENTICADO = False
CODIGO = "2411"  # seu código secreto

def autenticar(cod):
    global AUTENTICADO
    if cod.strip() == CODIGO:
        AUTENTICADO = True
        return "Acesso liberado para comandos avançados. 🔐"
    return "Código incorreto."

def exigir_auth():
    return AUTENTICADO

# ---------------------------
# BACKUP / RESTAURAÇÃO / AUTODESTRUIÇÃO
# ---------------------------
def cmd_backup():
    if not exigir_auth():
        return "Bloqueado. Use: autenticar 2411"
    nome = f"memoria_{timestamp()}.json"
    path = os.path.join(PASTA_BACKUP, nome)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=2)
    return f"Backup criado: {path}"

def cmd_restaura(nome):
    if not exigir_auth():
        return "Bloqueado. Use: autenticar 2411"
    path = os.path.join(PASTA_BACKUP, nome)
    if not os.path.exists(path):
        return "Arquivo de backup não encontrado."
    try:
        with open(path, "r", encoding="utf-8") as f:
            dados = json.load(f)
        # valida estrutura mínima
        if not isinstance(dados, dict):
            return "Backup inválido."
        # substitui memória
        for k in list(memoria.keys()):
            del memoria[k]
        for k,v in dados.items():
            memoria[k] = v
        salvar_memoria()
        return f"Memória restaurada de {nome}."
    except Exception as e:
        return f"Falha ao restaurar: {e}"

def cmd_autodestruicao():
    if not exigir_auth():
        return "Bloqueado. Use: autenticar 2411"
    try:
        if os.path.exists(ARQ_MEM):
            os.remove(ARQ_MEM)
        # recria memória limpa com base
        novo = json.loads(json.dumps(DIC_BASE))
        with open(ARQ_MEM, "w", encoding="utf-8") as f:
            json.dump(novo, f, ensure_ascii=False, indent=2)
        for k in list(memoria.keys()):
            del memoria[k]
        for k,v in novo.items():
            memoria[k] = v
        return "Memória zerada com sucesso. ♻️"
    except Exception as e:
        return f"Erro ao zerar: {e}"

# ---------------------------
# LÓGICA DE INTENÇÕES BÁSICAS
# ---------------------------
def eh_saudacao(msg_n):
    for s in memoria.get("saudacoes", []):
        if s in msg_n:
            return True
    return False

def responder_saudacao():
    nome = memoria.get("perfil",{}).get("dono_nome","")
    opcoes = [
        f"Oi! Eu sou a {memoria.get('perfil',{}).get('assistant_nome','Mari')}.",
        "Olá! Como posso te ajudar hoje?",
        f"E aí, {nome}! Tudo certo?",
        "Salve! Pronta pra ajudar. 😉"
    ]
    return resposta_personalidade(random.choice(opcoes))

def corrigir_abrevs_ortografia(msg_n):
    tokens = msg_n.split()
    abrv = memoria.get("abreviacoes", {})
    orto = memoria.get("ortografia", {})
    corr = []
    for t in tokens:
        t2 = abrv.get(t, t)
        t3 = orto.get(t2, t2)
        corr.append(t3)
    return " ".join(corr)

def sinonimo_basico(palavra):
    for base, lista in memoria.get("sinonimos",{}).items():
        if palavra == base or palavra in lista:
            return base
    return palavra

def heuristica_resposta(msg):
    # tenta responder com base em sentimentos / sinônimos / conhecimento curto
    msg_n = normalizar(msg)
    kc = memoria.get("conhecimento_curto", {})
    if msg_n in kc:
        return kc[msg_n]

    # sentimento
    for sentimento, termos in memoria.get("sentimentos", {}).items():
        for t in termos:
            if t in msg_n:
                if sentimento == "feliz":
                    return "Fico feliz por você! ✨ Quer aproveitar esse momento pra construir algo legal?"
                if sentimento == "triste":
                    return "Sinto muito que esteja assim. Posso ouvir e tentar ajudar. 💛"
                if sentimento == "com medo":
                    return "Respira fundo. Você não está sozinho, eu tô aqui com você. 👀"
                if sentimento == "zangado":
                    return "Compreendo sua raiva. Quer desabafar um pouco?"
                if sentimento == "cansado":
                    return "Descansar também é progresso. Que tal uma pausa curta?"

    # pergunta simples "o que é X" ou "significado de X"
    m = re.search(r"(o que e|o que é|significado de)\s+(.+)", msg_n)
    if m:
        termo = m.group(2).strip()
        termo = termo.split("?")[0].strip()
        base = sinonimo_basico(termo)
        if base in memoria.get("sinonimos", {}):
            defs = [f"• {base}: {', '.join(memoria['sinonimos'][base])}"]
            return "Aqui vai uma noção geral:\n" + "\n".join(defs)
        return f"{termo.title()} pode ter vários sentidos. Me dá um contexto que explico melhor. 😉"

    # fallback
    respostas = [
        "Entendi. Quer me ensinar como você quer que eu responda? Use: ensina: pergunta = resposta",
        "Posso aprender isso agora! Me diga: ensina: <pergunta> = <resposta>",
        "Ainda não sei essa, mas topo aprender. 😉"
    ]
    return random.choice(respostas)

# ---------------------------
# COMANDOS
# ---------------------------
def cmd_ajuda(basica=True):
    if basica and not AUTENTICADO:
        return (
            "Comandos básicos:\n"
            "• ensina: pergunta = resposta\n"
            "• apaga: <pergunta>\n"
            "• listar\n"
            "• hora | data | hoje | agora\n"
            "• calc: 2+2*3\n"
            "• autenticar 2411  (desbloqueia avançados)\n"
            "Dica: digite 'ajuda+' após autenticar para ver tudo."
        )
    else:
        return (
            "Comandos avançados (desbloqueados):\n"
            "• 2411@backup        → cria backup da memória\n"
            "• 2411@restaura <arquivo>.json  → restaura memória de backup\n"
            "• 2411#              → ZERA a memória (cuidado!)\n"
            "• perfil             → mostra perfil atual\n"
            "• set perfil: chave = valor  → ex: set perfil: personalidade = seria\n"
            "• set dicionario: chave = valor  → ex: set dicionario: legal = ótimo\n"
            "• ajuda               → ajuda básica\n"
            "• ajuda+              → esta tela\n"
        )

def cmd_listar():
    chaves = [k for k in memoria.keys() if k not in ["perfil","saudacoes","abreviacoes","giras","sentimentos","ortografia","sinonimos","conhecimento_curto"]]
    # inclui pares ensinados pelo usuário (guardados como memoria["aprendizados"])
    aprend = memoria.get("aprendizados", {})
    info = []
    if aprend:
        info.append(f"Aprendizados ({len(aprend)}): " + ", ".join(sorted(aprend.keys())))
    if chaves:
        info.append("Outras chaves: " + ", ".join(sorted(chaves)))
    if not info:
        return "Ainda não há itens listáveis além do dicionário base."
    return "\n".join(info)

def cmd_calc(expr):
    # aceita apenas dígitos, espaço e operadores básicos
    expr = expr.replace(",", ".")
    if not re.fullmatch(r"[0-9\.\s\+\-\*\/\(\)%]+", expr):
        return "Expressão inválida."
    try:
        val = eval(expr, {"__builtins__":None}, {"math":math})
        return f"Resultado: {val}"
    except Exception as e:
        return f"Erro no cálculo: {e}"

def cmd_hora_data(tipo):
    now = agora()
    if tipo in ("hora","agora"):
        return now.strftime("São %H:%M:%S.")
    return now.strftime("Hoje é %d/%m/%Y.")

def cmd_perfil():
    p = memoria.get("perfil", {})
    linhas = [f"{k}: {v}" for k,v in p.items()]
    return "Perfil atual:\n" + "\n".join(linhas)

def cmd_set_perfil(chave, valor):
    if not exigir_auth():
        return "Bloqueado. Use: autenticar 2411"
    memoria.setdefault("perfil", {})[normalizar(chave)] = valor.strip()
    salvar_memoria()
    return f"Perfil atualizado: {chave} = {valor}"

def cmd_set_dic(chave, valor):
    if not exigir_auth():
        return "Bloqueado. Use: autenticar 2411"
    memoria.setdefault("conhecimento_curto", {})[normalizar(chave)] = valor.strip()
    salvar_memoria()
    return f"Dicionário atualizado: {chave} = {valor}"

# ---------------------------
# LOOP PRINCIPAL
# ---------------------------
print("🤖 Mari 2.2 iniciada! Digite 'ajuda' ou 'autenticar 2411'. (Digite 'sair' para encerrar.)")

while True:
    try:
        msg = input("Você: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nMari: Até logo! 👋")
        break

    if not msg:
        continue

    msg_n = normalizar(msg)

    # sair
    if msg_n == "sair":
        print("Mari: Até logo! 👋")
        break

    # autenticar
    m_auth = re.match(r"^autenticar\s+(\S+)$", msg_n)
    if m_auth:
        print("Mari:", autenticar(m_auth.group(1)))
        continue

    # ajuda / ajuda+
    if msg_n == "ajuda":
        print("Mari:", cmd_ajuda(basica=True))
        continue
    if msg_n == "ajuda+":
        if AUTENTICADO:
            print("Mari:", cmd_ajuda(basica=False))
        else:
            print("Mari:", "Bloqueado. Use: autenticar 2411")
        continue

    # backup / restaura / autodestruição
    if msg_n == "2411@backup":
        print("Mari:", cmd_backup())
        continue

    m_res = re.match(r"^2411@restaura\s+(.+\.json)$", msg.strip())
    if m_res:
        print("Mari:", cmd_restaura(m_res.group(1)))
        continue

    if msg_n == "2411#":
        print("Mari:", cmd_autodestruicao())
        continue

    # listar
    if msg_n == "listar":
        print("Mari:", cmd_listar())
        continue

    # hora / data
    if msg_n in ("hora","agora","data","hoje"):
        t = "hora" if msg_n in ("hora","agora") else "data"
        print("Mari:", cmd_hora_data(t))
        continue

    # calc
    m_calc = re.match(r"^calc:\s*(.+)$", msg, flags=re.IGNORECASE)
    if m_calc:
        print("Mari:", cmd_calc(m_calc.group(1)))
        continue

    # set perfil
    m_setp = re.match(r"^set\s+perfil:\s*([^=]+)=(.+)$", msg, flags=re.IGNORECASE)
    if m_setp:
        print("Mari:", cmd_set_perfil(m_setp.group(1).strip(), m_setp.group(2).strip()))
        continue

    # set dicionario (conhecimento curto)
    m_setd = re.match(r"^set\s+dicionario:\s*([^=]+)=(.+)$", msg, flags=re.IGNORECASE)
    if m_setd:
        print("Mari:", cmd_set_dic(m_setd.group(1).strip(), m_setd.group(2).strip()))
        continue

    # ensina
    if msg_n.startswith("ensina:"):
        try:
            partes = msg.split(":", 1)[1].strip()
            p, r = partes.split("=", 1)
            pergunta = normalizar(p.strip())
            resposta = r.strip()
            memoria.setdefault("aprendizados", {})[pergunta] = resposta
            salvar_memoria()
            print(f"Mari: Aprendi! Quando você disser '{pergunta}', vou responder '{resposta}'.")
        except:
            print("Mari: Formato inválido! Use: ensina: pergunta = resposta")
        continue

    # apaga
    if msg_n.startswith("apaga:"):
        chave = normalizar(msg.split(":",1)[1].strip())
        if "aprendizados" in memoria and chave in memoria["aprendizados"]:
            del memoria["aprendizados"][chave]
            salvar_memoria()
            print(f"Mari: Apaguei o que eu sabia sobre '{chave}'.")
        else:
            print("Mari: Não encontrei isso na memória.")
        continue

    # respostas ensinadas (exata / aproximada)
    aprend = memoria.get("aprendizados", {})
    if msg_n in aprend:
        print("Mari:", resposta_personalidade(aprend[msg_n]))
        continue
    parecido = get_close_matches(msg_n, aprend.keys(), n=1, cutoff=0.78)
    if parecido:
        print("Mari:", resposta_personalidade(aprend[parecido[0]]))
        continue

    # saudações
    if eh_saudacao(msg_n):
        print("Mari:", responder_saudacao())
        continue

    # normalizar texto para tentar melhorar entendimento
    msg_corr = corrigir_abrevs_ortografia(msg_n)

    # conhecimento curto direto
    kc = memoria.get("conhecimento_curto", {})
    if msg_corr in kc:
        print("Mari:", resposta_personalidade(kc[msg_corr]))
        continue

    # heurística final
    resposta = heuristica_resposta(msg_corr)
    print("Mari:", resposta_personalidade(resposta))
