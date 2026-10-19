"""
Laboratorio 1, variante 1-13: Regression outliers and influential points.
Instalación: pip install -r requirements.txt
Ejecución: python solve_variant_13.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from statsmodels.stats.outliers_influence import OLSInfluence

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data_v1-13.csv"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
df = pd.read_csv(DATA)
X_train, X_test, y_train, y_test = train_test_split(
    df[["x"]], df["y"], test_size=0.30, random_state=42
)
def design(x):
    return sm.add_constant(x, has_constant="add")

model = sm.OLS(y_train, design(X_train)).fit()
fit_train, fit_test = model.predict(design(X_train)), model.predict(design(X_test))
infl = OLSInfluence(model)
stdres = infl.resid_studentized_internal
leverage, cooks = infl.hat_matrix_diag, infl.cooks_distance[0]
threshold = 3 * np.mean(cooks)
keep = cooks <= threshold
Xc, yc = X_train.iloc[np.flatnonzero(keep)], y_train.iloc[np.flatnonzero(keep)]
model_c = sm.OLS(yc, design(Xc)).fit()
fit_train_c, fit_test_c = model_c.predict(design(Xc)), model_c.predict(design(X_test))

def save(name):
    plt.tight_layout()
    plt.savefig(OUT / name, dpi=160, bbox_inches="tight")
    plt.close()

plt.figure(figsize=(9,6))
plt.scatter(X_train.x, y_train, label="Entrenamiento", alpha=.75)
plt.scatter(X_test.x, y_test, label="Prueba", marker="^", alpha=.75)
grid = np.linspace(df.x.min(), df.x.max(), 250)
plt.plot(grid, model.params["const"]+model.params["x"]*grid, label="OLS inicial")
plt.plot(grid, model_c.params["const"]+model_c.params["x"]*grid, label="OLS filtrado Cook")
for pos, label in [(np.argmax(np.abs(stdres)), "Mayor |residuo|"),
                   (np.argmax(leverage), "Mayor leverage"), (np.argmax(cooks), "Mayor Cook")]:
    plt.annotate(label, (X_train.x.iloc[pos], y_train.iloc[pos]), xytext=(5,8),
                 textcoords="offset points", fontsize=8, arrowprops={"arrowstyle":"->","lw":.7})
plt.xlabel("x"); plt.ylabel("y"); plt.title("Variante 1-13: OLS y puntos influyentes")
plt.legend(); save("01_regresion_comparada.png")

plt.figure(figsize=(8,5)); plt.scatter(fit_train, stdres, alpha=.8)
plt.axhline(0,ls="--"); plt.axhline(2,ls=":"); plt.axhline(-2,ls=":")
plt.xlabel("Valores ajustados"); plt.ylabel("Residuos estandarizados")
plt.title("Residuos estandarizados vs ajustados"); save("02_residuos_vs_ajustados.png")
plt.figure(figsize=(8,5)); plt.scatter(X_train.x, stdres, alpha=.8)
plt.axhline(0,ls="--"); plt.axhline(2,ls=":"); plt.axhline(-2,ls=":")
plt.xlabel("x"); plt.ylabel("Residuos estandarizados")
plt.title("Residuos estandarizados vs x"); save("03_residuos_vs_x.png")
plt.figure(figsize=(7,5)); plt.boxplot(stdres, tick_labels=["OLS inicial"])
plt.ylabel("Residuos estandarizados"); plt.title("Boxplot de residuos iniciales")
save("04_boxplot_residuos_inicial.png")

for vals, name, ylabel, title in [
    (leverage,"05_leverage_vs_ajustados.png","Leverage","Leverage vs valores ajustados"),
    (cooks,"06_cook_vs_ajustados.png","Distancia de Cook","Cook vs valores ajustados")]:
    plt.figure(figsize=(8,5)); plt.scatter(fit_train, vals, alpha=.8)
    plt.xlabel("Valores ajustados"); plt.ylabel(ylabel); plt.title(title); save(name)
plt.figure(figsize=(8,5)); plt.scatter(X_train.x, leverage, alpha=.8)
plt.xlabel("x"); plt.ylabel("Leverage"); plt.title("Leverage vs x"); save("07_leverage_vs_x.png")
plt.figure(figsize=(8,5)); plt.scatter(X_train.x, cooks, alpha=.8)
plt.axhline(threshold,ls="--",label=f"Umbral={threshold:.4f}")
plt.xlabel("x"); plt.ylabel("Distancia de Cook"); plt.title("Cook vs x"); plt.legend()
save("08_cook_vs_x.png")
plt.figure(figsize=(8,5)); plt.scatter(stdres, cooks, alpha=.8)
plt.axhline(threshold,ls="--",label="Umbral 3 × media")
plt.xlabel("Residuos estandarizados"); plt.ylabel("Distancia de Cook")
plt.title("Cook vs residuos estandarizados"); plt.legend(); save("09_cook_vs_residuos.png")
stdres_c = OLSInfluence(model_c).resid_studentized_internal
plt.figure(figsize=(7,5)); plt.boxplot([stdres,stdres_c],tick_labels=["Inicial","Filtrado"])
plt.ylabel("Residuos estandarizados"); plt.title("Comparación de residuos")
save("10_boxplot_comparacion.png")

summary = pd.DataFrame([
 {"modelo":"Inicial","n_train":len(y_train),"n_test":len(y_test),
  "R2_train":r2_score(y_train,fit_train),"R2_test":r2_score(y_test,fit_test),
  "intercepto":model.params["const"],"pendiente":model.params["x"]},
 {"modelo":"Filtrado Cook","n_train":len(yc),"n_test":len(y_test),
  "R2_train":r2_score(yc,fit_train_c),"R2_test":r2_score(y_test,fit_test_c),
  "intercepto":model_c.params["const"],"pendiente":model_c.params["x"]}
])
summary.to_csv(ROOT/"resultados_modelos.csv",index=False)
print(f"n={len(df)}; train={len(y_train)}; test={len(y_test)}")
print(f"Inicial: y={model.params['const']:.6f}+{model.params['x']:.6f}x; "
      f"R2 train={r2_score(y_train,fit_train):.6f}; R2 test={r2_score(y_test,fit_test):.6f}")
print(f"Umbral Cook={threshold:.6f}; excluidos={sum(~keep)}")
print(f"Filtrado: y={model_c.params['const']:.6f}+{model_c.params['x']:.6f}x; "
      f"R2 train={r2_score(yc,fit_train_c):.6f}; R2 test={r2_score(y_test,fit_test_c):.6f}")
print(f"Max |residuo estandarizado|={np.max(np.abs(stdres)):.6f}; "
      f"max leverage={max(leverage):.6f}; max Cook={max(cooks):.6f}")
print(summary.to_string(index=False))
