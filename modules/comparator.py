import json
import os

def carregar_base_referencia():
    """Carrega o banco de dados local de versões de drivers."""
    caminho_db = os.path.join("data", "drivers_db.json")
    if os.path.exists(caminho_db):
        try:
            with open(caminho_db, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def analisar_drivers(drivers_detectados):
    """
    Cruza os drivers detectados com a base de referência e define o status de cada um:
    - Atualizado (Verde)
    - Desatualizado (Vermelho)
    - Genérico MS (Amarelo/Alerta)
    """
    base_ref = carregar_base_referencia()
    drivers_analisados = []

    for d in drivers_detectados:
        nome = d["nome"]
        versao_atual = d["versao_instalada"]
        eh_generico = d["eh_generico"]
        
        status = "Atualizado"
        status_cor = "🟢"
        versao_sugerida = versao_atual
        link_download = "https://www.google.com/search?q=driver+" + nome.replace(" ", "+")

        # Verifica se existe na nossa base de referência
        if nome in base_ref:
            info_ref = base_ref[nome]
            versao_sugerida = info_ref.get("versao_recente", versao_atual)
            link_download = info_ref.get("site_oficial", link_download)
            
            # Comparação simples de versão (string)
            if versao_atual < versao_sugerida:
                status = "Desatualizado"
                status_cor = "🔴"
        elif eh_generico:
            status = "Genérico MS"
            status_cor = "⚠️"

        d_copia = d.copy()
        d_copia["status"] = status
        d_copia["status_cor"] = status_cor
        d_copia["versao_sugerida"] = versao_sugerida
        d_copia["link"] = link_download
        
        drivers_analisados.append(d_copia)

    return drivers_analisados