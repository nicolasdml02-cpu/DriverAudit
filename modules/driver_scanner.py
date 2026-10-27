import wmi

def escaneia_drivers_sistema():
    """
    Varre o Windows utilizando classes dedicadas do WMI para capturar
    Placas de Vídeo, Rede, Áudio e Controladores de Sistema com alta precisão.
    """
    c = wmi.WMI()
    drivers_detectados = []
    nomes_vistos = set()

    # 1. Buscar Placas de Vídeo (GPU)
    try:
        for gpu in c.Win32_VideoController():
            nome = gpu.Name or "Placa de Vídeo Desconhecida"
            if nome not in nomes_vistos:
                nomes_vistos.add(nome)
                eh_generico = "Microsoft" in (gpu.AdapterCompatibility or "")
                drivers_detectados.append({
                    "nome": nome,
                    "categoria": "Placa de Vídeo",
                    "fabricante": gpu.AdapterCompatibility or "Desconhecido",
                    "versao_instalada": gpu.DriverVersion or "N/A",
                    "data_driver": gpu.DriverDate or "N/A",
                    "eh_generico": eh_generico,
                    "link": f"https://www.google.com/search?q=driver+{nome.replace(' ', '+')}"
                })
    except Exception:
        pass

    # 2. Buscar Adaptadores de Rede Físicos
    try:
        for net in c.Win32_NetworkAdapter(PhysicalAdapter=True):
            nome = net.Name or "Adaptador de Rede"
            if nome not in nomes_vistos and net.DriverVersion:
                nomes_vistos.add(nome)
                eh_generico = "Microsoft" in (net.Manufacturer or "")
                drivers_detectados.append({
                    "nome": nome,
                    "categoria": "Adaptador de Rede",
                    "fabricante": net.Manufacturer or "Desconhecido",
                    "versao_instalada": net.DriverVersion or "N/A",
                    "data_driver": "N/A",
                    "eh_generico": eh_generico,
                    "link": f"https://www.google.com/search?q=driver+{nome.replace(' ', '+')}"
                })
    except Exception:
        pass

    # 3. Buscar Áudio, Chipset e Componentes via PnP
    try:
        for driver in c.Win32_PnPSignedDriver():
            if driver.DeviceName and driver.DeviceClass:
                d_class = driver.DeviceClass.upper()
                if any(cat in d_class for cat in ["MEDIA", "AUDIO", "SOUND", "SYSTEM", "PROCESSOR", "HDC"]):
                    nome = driver.DeviceName
                    if nome not in nomes_vistos:
                        nomes_vistos.add(nome)
                        eh_generico = "Microsoft" in (driver.Manufacturer or "")
                        categoria_nome = "Controlador de Áudio"
                        if "SYSTEM" in d_class or "HDC" in d_class:
                            categoria_nome = "Chipset / Sistema"
                        elif "PROCESSOR" in d_class:
                            categoria_nome = "Processador"
                            
                        drivers_detectados.append({
                            "nome": nome,
                            "categoria": categoria_nome,
                            "fabricante": driver.Manufacturer or "Desconhecido",
                            "versao_instalada": driver.DriverVersion or "N/A",
                            "data_driver": driver.DriverDate or "N/A",
                            "eh_generico": eh_generico,
                            "link": f"https://www.google.com/search?q=driver+{nome.replace(' ', '+')}"
                        })
    except Exception:
        pass

    return drivers_detectados