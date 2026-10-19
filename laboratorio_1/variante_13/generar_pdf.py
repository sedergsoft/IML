from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import os
from pathlib import Path

# --- Configuración ---
NOMBRE = "Oniel Serguey Gutierres Reyes"
GRUPO = "M26-534"
VARIANTE = "1-13"
CARPETA_FIGS = Path(r"D:\maestria\I semestre\Введение в машинное обучение\lab Регрессионные модели диагностика\IML\laboratorio_1\variante_13\figures")
# Asegúrate de que las imágenes estén aquí

# --- Textos por idioma ---
TEXTOS = {
    "es": {
        "titulo": "Informe de Laboratorio: Regresión Lineal y Valores Atípicos",
        "subtitulo": f"Variante {VARIANTE}",
        "autor": f"Estudiante: {NOMBRE}",
        "grupo": f"Grupo: {GRUPO}",
        "curso": "Curso: Introducción al Aprendizaje Automático",
        "sec1": "1. Datos de Partida",
        "sec1_texto": "El conjunto de datos consta de 110 observaciones con dos variables: x (entrada) e y (salida). Se realizó una división Holdout 70/30 (random_state=42), resultando en 77 casos para entrenamiento y 33 para prueba. La relación es aproximadamente lineal, pero se observa un grupo de puntos extremos en la parte superior derecha (x≈3–4.5, y≈7–8.5).",
        "sec2": "2. Metodología",
        "sec2_texto": "Se ajustó un modelo de regresión lineal simple por Mínimos Cuadrados Ordinarios (OLS). Se calcularon los residuos estandarizados, el leverage (apalancamiento) y la distancia de Cook. El umbral para identificar observaciones influyentes se fijó en 3 veces la media de la distancia de Cook.",
        "sec3": "3. Resultados del Modelo Inicial",
        "sec3_texto": "La ecuación del modelo inicial es: ŷ = -0.311776 + 0.936361·x. El R² en entrenamiento es 0.2904, mientras que en prueba es -0.9354 (lo que indica un mal desempeño predictivo). El residuo estandarizado máximo absoluto es 2.51, el leverage máximo es 0.0973 y la distancia de Cook máxima es 0.1254. El umbral de Cook calculado es 0.0532.",
        "sec4": "4. Detección y Filtrado de Observaciones Influyentes",
        "sec4_texto": "Se identificaron 10 observaciones en el conjunto de entrenamiento que superaban el umbral de Cook. Tras eliminarlas, se reentrenó el modelo, obteniendo la ecuación: ŷ = 0.465597 + 0.186327·x. El R² en entrenamiento bajó a 0.0675, pero el R² en prueba mejoró a -0.3767 (sigue siendo negativo, pero menos). La pendiente cambió drásticamente, demostrando la gran influencia de esos puntos.",
        "sec5": "5. Comparación de Residuos",
        "sec5_texto": "Al comparar los boxplots de los residuos estandarizados del modelo inicial y el filtrado, se observa que el modelo filtrado elimina los valores atípicos extremos que sesgaban la distribución inicial. Sin embargo, la dispersión general de los residuos sigue siendo alta.",
        "sec6": "6. Conclusiones",
        "sec6_texto": "1. La regresión OLS inicial tiene un poder predictivo muy bajo (R² de prueba negativo).\n2. Los diagnósticos (residuos, leverage, Cook) son herramientas complementarias; no se debe confiar en un solo indicador.\n3. La distancia de Cook detectó eficazmente un grupo de 10 puntos que influían desproporcionadamente en la recta.\n4. Al eliminarlos, el R² de prueba mejora, pero el modelo sigue siendo insatisfactorio.\n5. No se deben eliminar datos automáticamente; se debe investigar si son errores o datos legítimos, y considerar modelos no lineales o robustos.",
        "figs": ["01_regresion_comparada.png", "02_residuos_vs_ajustados.png", "03_residuos_vs_x.png", "04_boxplot_residuos_inicial.png", "05_leverage_vs_ajustados.png", "06_cook_vs_ajustados.png", "07_leverage_vs_x.png", "08_cook_vs_x.png", "09_cook_vs_residuos.png", "10_boxplot_comparacion.png"]
    },
    "ru": {
        "titulo": "Лабораторный отчет: Линейная регрессия и выбросы",
        "subtitulo": f"Вариант {VARIANTE}",
        "autor": f"Студент: {NOMBRE}",
        "grupo": f"Группа: {GRUPO}",
        "curso": "Курс: Введение в машинное обучение",
        "sec1": "1. Исходные данные",
        "sec1_texto": "Набор данных состоит из 110 наблюдений с двумя переменными: x (вход) и y (выход). Было выполнено разбиение Holdout 70/30 (random_state=42), в результате чего получено 77 обучающих и 33 тестовых примера. Связь приблизительно линейная, но наблюдается группа экстремальных точек в правом верхнем углу (x≈3–4.5, y≈7–8.5).",
        "sec2": "2. Методология",
        "sec2_texto": "Была построена модель простой линейной регрессии методом наименьших квадратов (OLS). Рассчитаны стандартизованные остатки, leverage (рычаг) и расстояние Кука. Порог для выявления влиятельных наблюдений был установлен на уровне 3-кратного среднего значения расстояния Кука.",
        "sec3": "3. Результаты начальной модели",
        "sec3_texto": "Уравнение начальной модели: ŷ = -0.311776 + 0.936361·x. R² на обучении = 0.2904, R² на тесте = -0.9354 (что указывает на плохую предсказательную способность). Максимальный абсолютный стандартизованный остаток = 2.51, максимальный leverage = 0.0973, максимальное расстояние Кука = 0.1254. Рассчитанный порог Кука = 0.0532.",
        "sec4": "4. Обнаружение и фильтрация влиятельных наблюдений",
        "sec4_texto": "В обучающей выборке было выявлено 10 наблюдений, превышающих порог Кука. После их удаления модель была переобучена, получено уравнение: ŷ = 0.465597 + 0.186327·x. R² на обучении снизился до 0.0675, но R² на тесте улучшился до -0.3767 (остается отрицательным, но меньшим по модулю). Наклон изменился кардинально, что демонстрирует сильное влияние этих точек.",
        "sec5": "5. Сравнение остатков",
        "sec5_texto": "При сравнении boxplot стандартизованных остатков начальной и отфильтрованной моделей видно, что отфильтрованная модель устраняет экстремальные выбросы, которые искажали начальное распределение. Однако общий разброс остатков остается высоким.",
        "sec6": "6. Выводы",
        "sec6_texto": "1. Начальная OLS-регрессия обладает очень низкой предсказательной способностью (отрицательный R² на тесте).\n2. Диагностики (остатки, leverage, Кук) являются взаимодополняющими инструментами; нельзя полагаться на один показатель.\n3. Расстояние Кука эффективно выявило группу из 10 точек, оказывающих непропорционально большое влияние на прямую.\n4. После их удаления R² на тесте улучшается, но модель остается неудовлетворительной.\n5. Не следует автоматически удалять данные; необходимо выяснить, являются ли они ошибками или законными наблюдениями, и рассмотреть нелинейные или робастные модели.",
        "figs": ["01_regresion_comparada.png", "02_residuos_vs_ajustados.png", "03_residuos_vs_x.png", "04_boxplot_residuos_inicial.png", "05_leverage_vs_ajustados.png", "06_cook_vs_ajustados.png", "07_leverage_vs_x.png", "08_cook_vs_x.png", "09_cook_vs_residuos.png", "10_boxplot_comparacion.png"]
    }
}

# --- Función para crear el PDF ---
def crear_pdf(lang):
    t = TEXTOS[lang]
    doc = SimpleDocTemplate(f"Otchetold_{VARIANTE}_{GRUPO}_{lang}.pdf", pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    style_titulo = ParagraphStyle('Titulo', parent=styles['Heading1'], alignment=1, fontSize=18, spaceAfter=20)
    style_subtitulo = ParagraphStyle('Subtitulo', parent=styles['Heading2'], alignment=1, fontSize=14, spaceAfter=10)
    style_autor = ParagraphStyle('Autor', parent=styles['Normal'], alignment=1, fontSize=12, spaceAfter=5)
    style_seccion = ParagraphStyle('Seccion', parent=styles['Heading2'], fontSize=14, spaceBefore=15, spaceAfter=10)
    style_texto = ParagraphStyle('Texto', parent=styles['Normal'], fontSize=11, leading=14, spaceAfter=10)
    
    # Portada
    story.append(Paragraph(t["titulo"], style_titulo))
    story.append(Paragraph(t["subtitulo"], style_subtitulo))
    story.append(Spacer(1, 20))
    story.append(Paragraph(t["curso"], style_autor))
    story.append(Paragraph(t["autor"], style_autor))
    story.append(Paragraph(t["grupo"], style_autor))
    story.append(PageBreak())
    
    # Contenido
    secciones = [
        ("sec1", "sec1_texto", None),
        ("sec2", "sec2_texto", None),
        ("sec3", "sec3_texto", [0]),  # Insertar primera imagen
        ("sec4", "sec4_texto", [7]),  # Insertar imagen de Cook vs x
        ("sec5", "sec5_texto", [9]),  # Insertar comparación de boxplots
        ("sec6", "sec6_texto", None),
    ]
    
    for key_titulo, key_texto, img_indices in secciones:
        story.append(Paragraph(t[key_titulo], style_seccion))
        # Reemplazar saltos de línea por <br/> para reportlab
        texto = t[key_texto].replace('\n', '<br/>')
        story.append(Paragraph(texto, style_texto))
        
        if img_indices:
            for idx in img_indices:
                img_path = os.path.join(CARPETA_FIGS, t["figs"][idx])
                if os.path.exists(img_path):
                    img = Image(img_path, width=6*inch, height=4*inch) # Ajustar tamaño
                    story.append(Spacer(1, 10))
                    story.append(img)
                    story.append(Spacer(1, 10))
                else:
                    story.append(Paragraph(f"[Imagen no encontrada: {img_path}]", style_texto))
        story.append(Spacer(1, 10))

    doc.build(story)
    print(f"PDF generado: Otchetold_{VARIANTE}_{GRUPO}_{lang}.pdf")

# --- Ejecución ---
if __name__ == "__main__":
    crear_pdf("es")
    crear_pdf("ru")