import os
from datetime import datetime

def exportar_relatorio_html(drivers_auditados):
    """Gera um relatório detalhado em formato HTML com o resultado da auditoria."""
    pasta_relatorios = "relatorios"
    if not os.path.exists(pasta_relatorios):
        os.makedirs(pasta_relatorios)
        
    data_hora_arquivo = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    caminho_arquivo = os.path.join(pasta_relatorios, f"auditoria_drivers_{data_hora_arquivo}.html")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>DriverPulse - Relatório de Auditoria</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0b0f19; color: #f1f5f9; padding: 20px; }}
            h1 {{ color: #38bdf8; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #0f172a; border-radius: 6px; overflow: hidden; }}
            th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #1e293b; }}
            th {{ background-color: #1e293b; color: #38bdf8; }}
            tr:hover {{ background-color: #1a243b; }}
            .status-atualizado {{ color: #34d399; font-weight: bold; }}
            .status-desatualizado {{ color: #f87171; font-weight: bold; }}
            .status-generico {{ color: #fbbf24; font-weight: bold; }}
            a {{ color: #38bdf8; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>🚗 Relatório de Auditoria de Drivers - DriverPulse</h1>
        <p><strong>Data da Análise:</strong> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
        <p><strong>Total de Dispositivos Mapeados:</strong> {len(drivers_auditados)}</p>
        <table>
            <thead>
                <tr>
                    <th>Status</th>
                    <th>Categoria</th>
                    <th>Dispositivo</th>
                    <th>Versão Atual</th>
                    <th>Versão Recomendada</th>
                    <th>Link Oficial</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for d in drivers_auditados:
        classe_status = "status-atualizado"
        if d['status'] == 'Desatualizado':
            classe_status = "status-desatualizado"
        elif d['status'] == 'Genérico MS':
            classe_status = "status-generico"
            
        html_content += f"""
                <tr>
                    <td class="{classe_status}">{d['status_cor']} {d['status']}</td>
                    <td>{d['categoria']}</td>
                    <td>{d['nome']}</td>
                    <td>{d['versao_instalada']}</td>
                    <td>{d['versao_sugerida']}</td>
                    <td><a href="{d['link']}" target="_blank">Aceder ao Fabricante</a></td>
                </tr>
        """
        
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    return os.path.abspath(caminho_arquivo)