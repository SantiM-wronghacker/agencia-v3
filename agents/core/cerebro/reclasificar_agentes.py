import json, shutil
from collections import defaultdict

areas = {"FINANZAS": ["analisis_estados_financieros","control_presupuesto_mensual","calculo_depreciacion_activos","analisis_punto_equilibrio","simulador_inversion_cetes","calculo_rendimiento_fondos","analizador_deuda_empresarial","proyector_flujo_caja_3_anos","calculo_capital_trabajo","comparador_instrumentos_inversion","calculo_nomina_mensual_mexico","analizador_razones_financieras","estimador_valor_empresa","calculadora_afore_retiro","calculo_impuesto_sobre_renta_mensual","simulador_fondo_emergencia"],"REAL ESTATE": ["comparador_zonas_inversion_cdmx","calculadora_renta_justa_m2","reporte_avaluo_basico","detector_oportunidades_compra","analizador_tendencias_mercado_inmobiliario","calculadora_retorno_desarrollo_obra","simulador_crowdfunding_inmobiliario","evaluador_credito_puente","plan_comercializacion_propiedad","calculadora_gastos_escrituracion","analizador_cartera_propiedades","estimador_costos_remodelacion","calculadora_ocupacion_renta","comparador_hipotecas_bancos_mexico"],"CEREBRO": ["orquestador_agentes_industria","router_consultas_complejidad","agente_memoria_contextual","generador_prompts_optimizados","coordinador_pipeline_datos","monitor_performance_agentes","agente_resumen_ejecutivo","clasificador_intencion_usuario","dispatcher_multiagente","agente_validacion_resultados"],"HERRAMIENTAS": ["generador_reportes_csv","scheduler_tareas_programadas","validador_datos_entrada","compresor_archivador_logs","monitor_uso_apis","generador_backups_automaticos","parser_archivos_configuracion","monitor_salud_sistema","notificador_alertas_consola","limpiador_archivos_temporales","generador_hash_verificacion","conversor_formatos_datos"],"LEGAL": ["generador_carta_poder","checklist_requisitos_notariales","convenio_prestacion_servicios","analizador_clausulas_riesgo","guia_constitucion_empresa_mexico","generador_finiquito_laboral","calculadora_indemnizacion_imss","checklist_cumplimiento_sat","generador_acta_acuerdos","template_contrato_servicios_profesionales"],"MARKETING": ["generador_plan_contenidos","analizador_buyer_persona","calculadora_presupuesto_publicitario","generador_propuesta_valor","analizador_funnel_ventas","generador_copy_facebook_ads","calculadora_cac_ltv","generador_estrategia_referidos","analizador_metricas_campana","generador_calendario_editorial","generador_bio_redes_sociales","analizador_hashtags_instagram"],"VENTAS": ["calculadora_pipeline_ventas","generador_propuesta_comercial","analizador_objeciones","tracker_seguimiento_prospectos","calculadora_forecast_mensual","generador_argumentario_ventas","analizador_ciclo_venta","script_cierre_ventas","calculadora_descuentos_margen","generador_email_cotizacion"],"OPERACIONES": ["gestor_inventario_basico","calculadora_costo_operacion","generador_procedimientos_sop","analizador_kpis_operativos","calculadora_capacidad_instalada","gestor_ordenes_trabajo","analizador_cuellos_botella","calculadora_eficiencia_operativa","generador_checklist_procesos","calculadora_tiempo_produccion"],"RECURSOS HUMANOS": ["calculadora_costo_empleado_mexico","generador_descripcion_puesto","calculadora_prestaciones_ley","generador_evaluacion_desempenio","calculadora_liquidacion_laboral","analizador_clima_organizacional","generador_plan_onboarding","calculadora_horas_extra","generador_encuesta_satisfaccion","calculadora_rotacion_personal"],"TECNOLOGIA": ["calculadora_costo_infraestructura_cloud","generador_especificaciones_tecnicas","analizador_stack_tecnologico","calculadora_roi_automatizacion","plan_migracion_cloud","analizador_deuda_tecnica","calculadora_sla_uptime","generador_documentacion_api","calculadora_licencias_software","analizador_seguridad_basica"],"SALUD": ["calculadora_imc_riesgo","generador_plan_nutricional","calculadora_calorias_actividad","analizador_costos_seguro_medico","checklist_consulta_medica","calculadora_dosis_medicamento","generador_recordatorio_medicamentos","analizador_habitos_saludables"],"EDUCACION": ["generador_plan_estudio","calculadora_costo_carrera_mexico","generador_ejercicios_practica","analizador_tecnicas_aprendizaje","calculadora_roi_educativo","generador_rubrica_evaluacion","generador_temario_curso","calculadora_becas_disponibles"],"LOGISTICA": ["calculadora_costo_envio_mexico","optimizador_ruta_entregas","calculadora_tiempo_transito","analizador_costo_ultima_milla","generador_manifiesto_carga","calculadora_capacidad_almacen","tracker_pedidos_basico","calculadora_costo_importacion"],"TURISMO": ["calculadora_presupuesto_viaje","generador_itinerario_viaje","comparador_hospedaje","calculadora_roi_renta_vacacional","analizador_temporadas","generador_paquete_turistico"],"RESTAURANTES": ["calculadora_costo_platillo","generador_menu_precios","calculadora_punto_equilibrio_restaurante","analizador_merma_desperdicio","generador_receta_estandarizada","calculadora_precio_venta_platillo"],"BIENES RAICES COMERCIALES": ["calculadora_renta_oficina_cdmx","analizador_local_comercial","calculadora_roi_bodega_industrial","comparador_zonas_comerciales","estimador_aforo_local","calculadora_contrato_arrendamiento_comercial"],"SEGUROS": ["calculadora_seguro_vida_mexico","comparador_seguros_auto","analizador_cobertura_gastos_medicos","calculadora_prima_seguro","generador_reporte_siniestro","checklist_contratacion_seguro"],"CONTABILIDAD": ["calculadora_iva_desglosado","generador_factura_conceptos","calculadora_ptu_empleados","analizador_deducciones_fiscales","calculadora_regimen_fiscal_adecuado","generador_balance_general_simple"],"MICRO_TAREAS": ["formateador_moneda_mx","validador_rfc_mexico","validador_curp_mexico","calculadora_iva_rapida","parseador_fecha_espanol","formateador_telefono_mx","extractor_numeros_texto","calculadora_isr_mensual_rapido","normalizador_nombre_persona","generador_folio_consecutivo","calculadora_descuento_precio","calculadora_diferencia_fechas","detector_tipo_contribuyente","calculadora_comision_rapida","validador_clabe_bancaria","calculadora_imss_empleado","parseador_monto_texto","formateador_numero_palabras_mx","generador_clave_producto","calculadora_plazo_vencimiento"]}
kw_rules = [(["rfc","curp","sat","fiscal","impuesto","isr","iva","factura","cfdi","regimen","deduccion","declaracion","contable","balance","ptu","razon_social"],"CONTABILIDAD"),(["contrato","legal","juridico","carta_poder","notarial","clausula","finiquito","liquidacion_laboral","indemnizacion","ley_federal","acta","convenio","demanda","juicio"],"LEGAL"),(["marketing","contenido","publicidad","redes_sociales","facebook","instagram","hashtag","buyer","funnel","cac","ltv","calendario_editorial","copy","campana"],"MARKETING"),(["venta","pipeline","prospecto","cotizacion","propuesta_comercial","objecion","cierre","argumentario","forecast","vendedor"],"VENTAS"),(["inventario","operacion","sop","kpi","capacidad","orden_trabajo","cuello","eficiencia","checklist_proceso","produccion"],"OPERACIONES"),(["empleado","nomina","prestacion","rh","recursos_humanos","onboarding","desempeno","clima_org","rotacion","horas_extra"],"RECURSOS HUMANOS"),(["cloud","software","infraestructura","tecnologia","stack","migracion","sla","uptime","api","seguridad","licencia","documentacion_tecnica","deuda_tecnica"],"TECNOLOGIA"),(["salud","imc","calorias","nutricional","medico","medicamento","dosis","habito_saludable","seguro_medico","consulta"],"SALUD"),(["educacion","estudio","aprendizaje","carrera","beca","rubrica","temario","curso","roi_educativo"],"EDUCACION"),(["envio","logistica","transporte","ruta","carga","almacen","pedido","importacion","ultima_milla","transito"],"LOGISTICA"),(["viaje","turismo","hospedaje","hotel","itinerario","paquete_turistico","vacacional","temporada","destino"],"TURISMO"),(["restaurante","platillo","menu","receta","merma","precio_venta_platillo","costo_platillo"],"RESTAURANTES"),(["oficina","local_comercial","bodega","arrendamiento_comercial","aforo","zona_comercial"],"BIENES RAICES COMERCIALES"),(["seguro_vida","seguro_auto","prima_seguro","siniestro","cobertura","aseguradora"],"SEGUROS"),(["inmobiliario","propiedad","hipoteca","avaluo","m2","renta_justa","desarrollo_obra","crowdfunding_inmob","escrituracion","remodelacion","ocupacion_renta","zonas_inversion"],"REAL ESTATE"),(["flujo_caja","estado_financiero","depreciacion","punto_equilibrio","cetes","rendimiento_fondo","deuda_empresarial","capital_trabajo","instrumento_inversion","razones_financieras","valor_empresa","afore","retiro","fondo_emergencia","presupuesto_mensual"],"FINANZAS"),(["formateador","validador","parseador","normalizador","extractor_numeros","calculadora_iva_rapida","folio","clave_producto","plazo_vencimiento","diferencia_fechas","tipo_contribuyente","comision_rapida","clabe","imss_empleado","monto_texto","palabras_mx","moneda_mx","telefono_mx","isr_mensual_rapido"],"MICRO_TAREAS"),(["orquestador","router","memoria","prompt","pipeline","dispatcher","clasificador_intencion","validacion_resultado","monitor_performance","resumen_ejecutivo"],"CEREBRO"),(["reporte_csv","scheduler","validador_dato","logs","backup","parser_config","salud_sistema","alerta","temporal","hash","conversor_formato"],"HERRAMIENTAS")]

agent2cat = {}
for cat, agents in areas.items():
    for a in agents:
        agent2cat[a] = cat

def classify_kw(name):
    n = name.lower()
    for kws, cat in kw_rules:
        for kw in kws:
            if kw in n:
                return cat
    return None

hp = r"C:\Users\Santi\agentes-local\habilidades.json"
tp = hp + ".tmp"
with open(hp, "r", encoding="utf-8") as f:
    data = json.load(f)

before = defaultdict(int)
after = defaultdict(int)
changes = []

for fn, info in data.items():
    name = fn[:-3] if fn.endswith(".py") else fn
    old = info.get("categoria", "DESCONOCIDA")
    before[old] += 1
    new = agent2cat.get(name) or classify_kw(name) or old
    after[new] += 1
    if new != old:
        changes.append((fn, old, new))
        info["categoria"] = new

with open(tp, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
shutil.move(tp, hp)

sep = "=" * 70
print(sep)
print("RECLASSIFICATION COMPLETE")
print(f"Total agents processed: {len(data)}")
print(f"Agents reclassified:    {len(changes)}")
print(sep)
print("")
print("--- CHANGES ---")
for fn, old, new in sorted(changes):
    print(f"  {fn:<55} {old} -> {new}")
print("")
print("--- CATEGORY COUNTS (before -> after) ---")
all_cats = sorted(set(list(before.keys()) + list(after.keys())))
for cat in all_cats:
    b = before.get(cat, 0)
    a = after.get(cat, 0)
    d = a - b
    ds = f"({chr(43) if d>=0 else chr(45)}{d})" if d != 0 else "(no change)"
    print(f"  {cat:<35} {b:>4} -> {a:>4}  {ds}")
