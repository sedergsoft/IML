# Informe de laboratorio — Variante 1-13
## Regression outliers and influential points

### 1. Objetivo
Ajustar una regresión lineal simple por mínimos cuadrados ordinarios (OLS), diagnosticar residuos estandarizados, leverage y distancia de Cook, y comparar el modelo inicial con otro entrenado tras retirar observaciones influyentes.

### 2. Datos y procedimiento
- Datos: 110 observaciones, columnas `x` e `y`.
- Holdout 70/30 con `random_state=42`: 77 casos de entrenamiento y 33 de prueba.
- Los diagnósticos se calculan sobre entrenamiento para no usar la prueba al decidir exclusiones.
- Modelo: ŷ = β₀ + β₁x.
- Umbral de filtrado: distancia de Cook > 3 × media de Cook del entrenamiento.

### 3. Modelo inicial
**ŷ = -0.311776 + 0.936361 x**

| Métrica | Resultado |
|---|---:|
| R² entrenamiento | 0.290399 |
| R² prueba | -0.935444 |
| Máximo valor absoluto del residuo estandarizado | 2.513206 |
| Máximo leverage | 0.097313 |
| Máxima distancia de Cook | 0.125413 |
| Umbral de Cook (3 × media) | 0.053161 |

El máximo residuo estandarizado absoluto es aproximadamente 2.51; con la referencia visual habitual de ±3 no hay un residuo que supere ese límite. Este criterio no sustituye una evaluación conjunta de influencia.

### 4. Observaciones influyentes
Aplicando el umbral indicado, se excluyeron 10 observaciones del conjunto de entrenamiento. La distancia de Cook combina información sobre el residuo y el leverage; un leverage alto por sí solo no implica necesariamente un valor atípico en la respuesta.

### 5. Modelo tras filtrar por Cook
**ŷ = 0.465597 + 0.186327 x**

| Métrica | Modelo inicial | Modelo filtrado |
|---|---:|---:|
| Casos usados para entrenar | 77 | 67 |
| R² entrenamiento | 0.290399 | 0.067465 |
| R² prueba (mismos 33 casos) | -0.935444 | -0.376683 |
| Intercepto | -0.311776 | 0.465597 |
| Pendiente | 0.936361 | 0.186327 |

El R² de prueba mejora (es menos negativo), pero continúa por debajo de cero. Un R² negativo significa que el modelo predice peor que una referencia que siempre usa la media de `y` de la prueba. El R² de entrenamiento antes y después se calcula sobre conjuntos distintos (77 frente a 67 casos), por lo que esa comparación debe interpretarse con cautela.

### 6. Conclusiones
1. La regresión OLS inicial explica una fracción limitada de la variabilidad del entrenamiento y generaliza mal en esta partición.
2. Residuos estandarizados, leverage y distancia de Cook son diagnósticos complementarios; no debe identificarse influencia basándose en un solo indicador.
3. Al filtrar los casos con Cook por encima del umbral, la pendiente cambia notablemente, señal de que esos casos influyen en la recta.
4. El R² de prueba mejora de -0.935 a -0.377, aunque el resultado sigue siendo insatisfactorio.
5. No se deben eliminar observaciones automáticamente: hay que comprobar si son errores de medición o casos legítimos. Conviene inspeccionar la relación x–y y, si procede, estudiar modelos no lineales o robustos.

### 7. Figuras
El script genera dispersión con ambas rectas y marcadores diagnósticos; residuos estandarizados frente a ajustados y x; boxplots; leverage y distancia de Cook frente a ajustados, x y residuos.

### 8. Reproducción
```bash
pip install -r requirements.txt
python solve_variant_13.py
```
Las métricas se guardan en `resultados_modelos.csv`; las figuras se generan en `figures/`.