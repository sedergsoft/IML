# Laboratorio 1 — Variante 1-13

Solución de **Regression outliers and influential points**.

## Contenido
- `data_v1-13.csv`: datos originales de la variante.
- `solve_variant_13.py`: análisis reproducible, diagnósticos OLS y generación de figuras.
- `INFORME_VARIANTE_13.md`: informe, resultados y conclusiones.
- `resultados_modelos.csv`: métricas de los modelos.
- `requirements.txt`: dependencias.

## Ejecución
```bash
pip install -r requirements.txt
python solve_variant_13.py
```

Se usa Holdout 70/30 con semilla 42. Los diagnósticos de influencia se calculan en entrenamiento y el umbral es 3 veces la distancia de Cook media, conforme al enunciado. Las figuras se guardan en `figures/`.