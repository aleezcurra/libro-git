import fitz 
import os
import pandas as pd
import re

# Ruta completa del documento PDF
#pdf_path = '/Users/aleezcurra/Desktop/pruebas/2019913075.pdf'

# Ruta de la carpeta que contiene los archivos
carpeta = '/Users/aleezcurra/Desktop/Informes'

# Obtén la lista de nombres de archivos en la carpeta
archivos_en_carpeta = os.listdir(carpeta)

nombre_archivo =[]
s_ref = []
n_ref = []
vehiculo_implicado = []
tipo_siniestro = []
asegurado = []
compania_seguros =[]
responsabilidad_terceros =[]
marca_maquina=[]
modelo_maquina = []
año_fabricacion_maq = []
causa = []
fechas= []
siniestro_total=[]
valoracion_daños = []
naturaleza_daños = []
capital_asegurado = []


# Iterar sobre cada archivo en la carpeta
for nombre_archivo_actual in archivos_en_carpeta:
    # Ruta completa del documento PDF
    pdf_path = os.path.join(carpeta, nombre_archivo_actual)

    # Obtener el nombre del archivo sin la ruta y la extensión
    file_name = os.path.splitext(nombre_archivo_actual)[0]+'.pdf'

    nombre_archivo.append(file_name)

    # Abrir el archivo en modo de lectura binaria
    with fitz.open(pdf_path) as pdf_document:

        # Obtener el objeto de la primera página
        first_page = pdf_document[0]

        # Extraer el texto de la primera página
        first_page_text = first_page.get_text()

        s_ref_matches = re.findall(r'S\s*/\s*Ref\.\s*:?[\s\n]*([^\n]+)', first_page_text)

        # Agregar resultados a las listas correspondientes
        s_ref.append(s_ref_matches[0] if s_ref_matches else None)


        n_ref_matches = re.findall(r'N\s*/\s*Ref\.\s*:?([^F]+)Fecha', first_page_text)

        # Eliminar los caracteres de nueva línea en los resultados de N/Ref.
        n_ref_matches = [match.replace('\n', '').strip() for match in n_ref_matches]

        # Agregar resultados a las listas correspondientes
        n_ref.append(n_ref_matches[0] if n_ref_matches else None)

        # Buscar 'Tipo de siniestro' en la primera página
        tipo_siniestro_matches = 'Responsabilidad civil' if re.search(r'Responsabilidad civil', 
                                                                      first_page_text, re.IGNORECASE) else 'Daños materiales'

        # Agregar resultado a la lista correspondiente
        tipo_siniestro.append(tipo_siniestro_matches)


        if re.search(r'Plataforma', first_page_text): 
            vehiculo_implicado_matches = 'Plataforma'
            vehiculo_implicado.append(vehiculo_implicado_matches)
            asegurado.append("None")
            valoracion_daños.append("None")
            compania_seguros.append("None")
            causa.append("None")
            responsabilidad_terceros.append("None")
            siniestro_total.append("None")
            marca_maquina.append("None")
            modelo_maquina.append("None")
            año_fabricacion_maq.append("None")
            naturaleza_daños.append("None")
        
        else: 
            vehiculo_implicado_matches = 'Grúa'
            vehiculo_implicado.append(vehiculo_implicado_matches)

            # Utilizar expresiones regulares para buscar el Asegurado en la primera página
            asegurado_matches = re.findall(r'ASEGURADO:\s*([\s\S]+?)\n', 
                                           first_page_text, re.IGNORECASE)

            # Agregar resultado a la lista correspondiente
            asegurado.append(asegurado_matches[0] if asegurado_matches else None)

            # Expresión regular para la valoración de daños
            match_valoracion = re.search(r'VALORACIÓN[^\n]*\n*:?[\n\s]*([\d\.,]+)', first_page_text, re.IGNORECASE)

            # Verificar si se encontró la valoración
            if tipo_siniestro_matches != 'Responsabilidad civil':
                if match_valoracion:
                    valoracion_daños_matches = match_valoracion.group(1)
                    
                    # Limpiar el valor
                    valoracion_daños_matches = re.sub(r'[^\d.,]', '', valoracion_daños_matches)
                    
                    # Agregar el símbolo de euro al resultado
                    valoracion_daños_matches = f"{valoracion_daños_matches} €" if valoracion_daños_matches is not None else 'None'
                else:
                    valoracion_daños_matches = None
            else:
                valoracion_daños_matches = 'None'

            # Agregar resultado a la lista correspondiente
            valoracion_daños.append(valoracion_daños_matches)


            compania_seguros_matches = ('GENERALI ESPAÑA S.A.' if re.search(r'GENERALI|Estrella|grupo vitalicio|VITALICIO SEGUROS', 
                                                                            first_page_text,re.IGNORECASE) 
                                        else 'Allianz Seguros' if re.search(r'Allianz', first_page_text,re.IGNORECASE) 
                                        else 'Mapfre' if re.search(r'Mapfre', first_page_text,re.IGNORECASE)
                                        else 'Helvetia' if re.search(r'Helvetia', first_page_text,re.IGNORECASE)
                                        else 'REALE' if re.search(r'Reale', first_page_text,re.IGNORECASE) 
                                        else 'AXA' if re.search(r'AXA', first_page_text,re.IGNORECASE) 
                                        else 'Zurich' if re.search(r'Zurich', first_page_text,re.IGNORECASE) 
                                        else 'FIATC' if re.search(r'FIATC', first_page_text,re.IGNORECASE) 
                                        else 'Fidelidade' if re.search(r'Fidelidade', first_page_text,re.IGNORECASE)
                                        else 'CHUBB' if re.search(r'CHUBB', first_page_text,re.IGNORECASE) 
                                        else 'Catalana Occidente' if re.search(r'Catalana Occidente', first_page_text,re.IGNORECASE) 
                                        else 'Plus Ultra' if re.search(r'Plus Ultra', first_page_text,re.IGNORECASE) 
                                        else 'ATS' if re.search(r'ATS', first_page_text,re.IGNORECASE) 
                                        else 'NHA' if re.search(r'NHA', first_page_text,re.IGNORECASE) else None)

            # Agregar resultado a la lista correspondiente
            compania_seguros.append(compania_seguros_matches)

            causa_matches = ('Error/Negligencia' if re.search(r'error|negligencia', first_page_text,re.IGNORECASE) 
                            else 'Defecto fabricación' if re.search(r'defecto fabricacion', first_page_text, re.IGNORECASE)
                            else 'Robo' if re.search(r'robo', first_page_text, re.IGNORECASE) 
                            else 'Avería' if re.search(r'averia', first_page_text, re.IGNORECASE) 
                            else 'Incendio' if re.search(r'incendio', first_page_text, re.IGNORECASE) 
                            else 'Hundimiento calzada' if re.search(r'hundimiento', first_page_text, re.IGNORECASE) and 
                            re.search(r'calzada', first_page_text, re.IGNORECASE) 
                            else 'Hundimiento terreno' if re.search(r'hundimiento', first_page_text, re.IGNORECASE) and 
                            re.search(r'terreno', first_page_text, re.IGNORECASE)
                            else 'Impacto' if re.search(r'impacto', first_page_text, re.IGNORECASE)
                            else 'Colisión' if re.search(r'colision', first_page_text, re.IGNORECASE)
                            else 'Estrincón' if re.search(r'enganche|estrincon|traba', first_page_text, re.IGNORECASE)
                            else 'Sobreesfuerzo' if re.search(r'sobreesfuerzo|sobre-esfuerzo', first_page_text, re.IGNORECASE)
                            else None)

            causa.append(causa_matches)
            
            # Inicializar el texto completo del documento
            full_document_text = ""

            # Iterar sobre todas las páginas y concatenar el texto
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                full_document_text += page.get_text()

            # Buscar 'RESPONSABILIDAD DE TERCEROS' o 'RECOBRO' en todo el texto
            responsabilidad_terceros_matches = 'Si' if re.search(r'RESPONSABILIDAD DE TERCEROS|POSIBILIDAD DE RECOBRO', 
                                                                 full_document_text) else 'No'

            # Agregar resultado a la lista correspondiente
            responsabilidad_terceros.append(responsabilidad_terceros_matches)

            # Buscar 'SINIESTRO TOTAL' o 'PERDIDA TOTAL' en todo el texto
            if tipo_siniestro_matches != 'Responsabilidad civil':
                siniestro_total_matches = 'Si' if re.search(r'siniestro total|perdida total', 
                                                            full_document_text) else 'No'
            else:
                siniestro_total_matches = 'None'

            # Agregar resultado a la lista correspondiente
            siniestro_total.append(siniestro_total_matches)


            # Buscar la marca de la máquina
            marca_maquina_matches = re.findall(r'marca\s+(\S+)', full_document_text, re.IGNORECASE)

            # Inicializar la variable para almacenar el resultado
            marca_maquina_value = None

            # Verificar si se encontraron coincidencias
            if marca_maquina_matches:
                marca_maquina_value = marca_maquina_matches[0].rstrip(',')
            else:
                # Si no se encontró la marca, buscar "equipo dañado" y tomar la palabra siguiente
                equipo_danado_matches = re.findall(r'equipo dañado\s+(\S+)', full_document_text, re.IGNORECASE)

                # Verificar si se encontraron coincidencias
                if equipo_danado_matches:
                    marca_maquina_value = equipo_danado_matches[0]

            # Agregar el resultado a la lista correspondiente
            marca_maquina.append(marca_maquina_value if marca_maquina_value else None)
            
            modelo_maquina_matches = re.findall(r'modelo\s*([\w\d]+(?:\/[\w\d]+)?)', full_document_text, re.IGNORECASE)

            if not modelo_maquina_matches:
                modelo_maquina_matches = re.findall(r'modelo\s*([\w\d\/\-]+)', full_document_text, re.IGNORECASE)

            if modelo_maquina_matches:
                modelo_maquina.append(modelo_maquina_matches[0])
            else: 
                modelo_maquina.append(None)

            # Expresión regular para el año de fabricación
            año_fabricacion_maq_matches = re.findall(r'(?:Año|Fecha)[^\n]*\n*\s*de[^\n]*\n*\s*fabricación:\s*([\d\.,\n]+)', 
                                                     full_document_text, re.IGNORECASE)

            # Verificar si se encontraron coincidencias
            if año_fabricacion_maq_matches:
                # Unir los caracteres numéricos
                año_fabricacion_unido = ''.join(año_fabricacion_maq_matches)
                
                # Eliminar puntos, comas y espacios
                año_fabricacion_unido = re.sub(r'[.,\s\n]', '', año_fabricacion_unido)

                # Tomar solo los primeros 4 dígitos
                año_fabricacion_unido = año_fabricacion_unido[:4]

                # Asignar el resultado
                año_fabricacion_maq_matches = año_fabricacion_unido
            else:
                año_fabricacion_maq_matches =None

            año_fabricacion_maq.append(año_fabricacion_maq_matches)


            # Lista de palabras clave a buscar
            palabras_clave = ['pluma', 'plumin', 'superestructura', 'chasis', 'motor', 
                              'corona','caja de cambio', 'estabilizadores', 'cilindro telescopico', 
                              'cilindro elevacion', 'cabina']

            # Buscar cada palabra clave en el texto
            palabras_encontradas = [palabra.title() for palabra in palabras_clave if re.search(palabra, 
                                                                                               full_document_text, re.IGNORECASE)]

            # Convertir la lista de palabras encontradas a una cadena
            naturaleza_daños_str = ', '.join(palabras_encontradas) 

            # Convertir la lista de palabras encontradas a una cadena
            naturaleza_daños_str = ', '.join(palabras_encontradas) if tipo_siniestro_matches != 'Responsabilidad civil' else 'None'

            # Agregar la cadena a la lista
            naturaleza_daños.append(naturaleza_daños_str)

            # Expresión regular para buscar el capital asegurado
            capital_asegurado_matches = re.findall(r'Capital\s*Asegurado[^\d]*([\d\.,]+)', full_document_text, re.IGNORECASE)

            # Verificar si se encontraron coincidencias
            if capital_asegurado_matches:
                # Tomar solo el primer valor encontrado
                capital_asegurado_value = capital_asegurado_matches[0]

                # Agregar '€' al final del valor
                capital_asegurado_value = capital_asegurado_value + ' €'

                # Agregar el valor a la lista correspondiente
                capital_asegurado.append(capital_asegurado_value)
            else:
                capital_asegurado.append(None)
        
            # Expresión regular para buscar líneas con información de fecha
            # Expresión regular para buscar líneas con información de fecha
            fecha_line_matches = re.findall(r'\b(\d{1,2})\s*(?:de)?\s*([a-zA-Z]+)(?: de)?\s*(\d{4})\b', first_page_text)

            # Verificar si se encontraron coincidencias
            if fecha_line_matches:
                # Tomar solo la primera fecha encontrada
                dia, mes, ano = fecha_line_matches[0]

                # Transformar el mes a número
                meses_dict = {
                    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
                    'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
                }
                mes_numero = meses_dict.get(mes.lower(), 0)
                # Crear la fecha en el formato deseado
                fecha = f"{dia}/{mes_numero}/{ano}"

                # Almacenar la fecha en la lista
                fechas.append(fecha)

                # Imprimir el resultado
                #print("Fecha:", fechas)
            else:
                fechas.append(None)

                

            #print("Valoracion daños:", valoracion_daños)

# Imprimir la longitud de todas las listas
print("Longitud nombre archivo: ",len(nombre_archivo))
print("Longitud de s_ref:", len(s_ref))
print("Longitud de n_ref:", len(n_ref))
print("Vehiculo implicado: ", len(vehiculo_implicado))
print("Longitud de tipo_siniestro:", len(tipo_siniestro))
print("Longitud de causa:", len(causa))
print("Longitud de responsabilidad_terceros:", len(responsabilidad_terceros))
print("Longitud de marca_maquina:", len(marca_maquina))
print("Longitud de modelo_maquina:", len(modelo_maquina))
print("Longitud de año_fabricacion_maq:", len(año_fabricacion_maq))
print("Longitud de naturaleza_daños:", len(naturaleza_daños))
print("Longitud de siniestro_total:", len(siniestro_total))
print("Longitud de asegurado:", len(asegurado))
print("Longitud de compania_seguros:", len(compania_seguros))
print("Longitud del capital asegurado:", len(capital_asegurado))
print("Longitud de fecha:", len(fechas))
print("Longitud de valoracion_daños:", len(valoracion_daños))


    # Crear un diccionario con las listas
data2 = {
    'Nombre del archivo': nombre_archivo,
    'S/Ref.': s_ref,
    'N/Ref.': n_ref,
    "Vehículo implicado": vehiculo_implicado,
    'Tipo de siniestro': tipo_siniestro,
    'Causa': causa,
    'Responsabilidad de terceros': responsabilidad_terceros,
    'Marca máquina': marca_maquina,
    'Modelo máquina': modelo_maquina,
    'Año fabricación': año_fabricacion_maq,
    'Naturaleza y alcance de los daños': naturaleza_daños,
    'Siniestro total': siniestro_total,
    'Asegurado': asegurado,
    'Compañía de seguros': compania_seguros,
    'Valoración daños': valoracion_daños
    }
try:
    # Crear un DataFrame de pandas
    df2 = pd.DataFrame(data2)
    # Guardar el DataFrame como un archivo CSV
    df2.to_csv('datos_informes.csv', index=False)
except Exception as e:
    print(f"Error: {e}")

# Especifica la ruta del archivo CSV
csv_path = '/Users/aleezcurra/Desktop/informes4.csv'
# Exporta el DataFrame a un archivo CSV
df2.to_csv(csv_path, index=False)

print(f"DataFrame exportado a: {csv_path}")
