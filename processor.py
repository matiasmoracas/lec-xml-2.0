import xml.etree.ElementTree as ET

SII_NS = {'sii': 'http://www.sii.cl/SiiDte'}

DTE_TIPOS = {
    "33": "Factura electrónica",
    "34": "Factura exenta electrónica",
    "39": "Boleta electrónica",
    "41": "Boleta exenta electrónica",
    "52": "Guía de despacho electrónica",
    "56": "Nota de débito electrónica",
    "61": "Nota de crédito electrónica"
}

def detectar_tipo_xml(root):
    tag = root.tag.lower()
    if 'enviodte' in tag:
        return 'EnvioDTE'
    elif 'respuestadte' in tag:
        return 'RespuestaDTE'
    elif 'dte' in tag:
        return 'DTE directo'
    return 'Desconocido'

def procesar_enviodte(root):
    datos = []
    try:
        dtes = root.findall('.//sii:DTE', SII_NS)
        for dte in dtes:
            doc = dte.find('.//sii:Documento', SII_NS)
            encabezado = doc.find('.//sii:Encabezado', SII_NS)
            detalles = doc.findall('.//sii:Detalle', SII_NS)

            tipo_dte = encabezado.findtext('sii:IdDoc/sii:TipoDTE', '', SII_NS)
            descripcion_dte = DTE_TIPOS.get(tipo_dte, "Desconocido")

            base_info = {
                "Tipo XML": "Factura (EnvioDTE)",
                "Tipo DTE": tipo_dte,
                "Descripción DTE": descripcion_dte,
                "Folio": encabezado.findtext('sii:IdDoc/sii:Folio', '', SII_NS),
                "Fecha Emisión": encabezado.findtext('sii:IdDoc/sii:FchEmis', '', SII_NS),
                "Fecha Vencimiento": encabezado.findtext('sii:IdDoc/sii:FchVenc', '', SII_NS),
                "RUT Emisor": encabezado.findtext('sii:Emisor/sii:RUTEmisor', '', SII_NS),
                "Razón Social Emisor": encabezado.findtext('sii:Emisor/sii:RznSoc', '', SII_NS),
                "Dirección Emisor": encabezado.findtext('sii:Emisor/sii:DirOrigen', '', SII_NS),
                "RUT Receptor": encabezado.findtext('sii:Receptor/sii:RUTRecep', '', SII_NS),
                "Razón Social Receptor": encabezado.findtext('sii:Receptor/sii:RznSocRecep', '', SII_NS),
                "Dirección Receptor": encabezado.findtext('sii:Receptor/sii:DirRecep', '', SII_NS),
                "Monto Exento": encabezado.findtext('sii:Totales/sii:MntExe', '', SII_NS),
                "Monto Total": encabezado.findtext('sii:Totales/sii:MntTotal', '', SII_NS),
            }

            for detalle in detalles:
                item = {
                    "Descripción Item": detalle.findtext('sii:NmbItem', '', SII_NS),
                    "Cantidad": detalle.findtext('sii:QtyItem', '', SII_NS),
                    "Precio Unitario": detalle.findtext('sii:PrcItem', '', SII_NS),
                    "Monto Item": detalle.findtext('sii:MontoItem', '', SII_NS)
                }
                datos.append({**base_info, **item})
    except Exception as e:
        datos.append({"Tipo XML": "Factura (EnvioDTE)", "Error": str(e)})
    return datos

def procesar_respuestadte(root):
    datos = []
    try:
        resultados = root.findall('.//sii:ResultadoDTE', SII_NS)
        for resultado in resultados:
            datos.append({
                "Tipo XML": "RespuestaDTE",
                "RUT Receptor": resultado.findtext('sii:RutRecep', '', SII_NS),
                "RUT Emisor": resultado.findtext('sii:RutEmisor', '', SII_NS),
                "Tipo DTE": resultado.findtext('sii:TipoDTE', '', SII_NS),
                "Folio": resultado.findtext('sii:Folio', '', SII_NS),
                "Estado Recepción": resultado.findtext('sii:EstadoRecepDTE', '', SII_NS),
                "Glosa Estado": resultado.findtext('sii:GlosaRecepDTE', '', SII_NS)
            })
    except Exception as e:
        datos.append({"Tipo XML": "RespuestaDTE", "Error": str(e)})
    return datos

def procesar_archivos_xml(uploaded_files):
    resultados = []
    if not uploaded_files:
        return []

    for archivo in uploaded_files:
        try:
            content = archivo.read()
            root = ET.fromstring(content)
            tipo = detectar_tipo_xml(root)
            if tipo == 'EnvioDTE':
                resultados.extend(procesar_enviodte(root))
            elif tipo == 'RespuestaDTE':
                resultados.extend(procesar_respuestadte(root))
            else:
                resultados.append({"Tipo XML": tipo, "Error": "Formato no reconocido", "Archivo": archivo.name})
        except Exception as e:
            resultados.append({"Tipo XML": "Error", "Error": str(e), "Archivo": archivo.name})

    return resultados
