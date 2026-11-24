"""Análise simples de atendimentos com dados simulados."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PASTA = Path(__file__).resolve().parent
df = pd.read_csv(PASTA / "dados" / "atendimentos.csv", parse_dates=["data"])
df = df.drop_duplicates(subset=["id_atendimento"])
df["tempo_horas"] = pd.to_numeric(df["tempo_horas"], errors="coerce")
df = df.dropna(subset=["data", "status", "tempo_horas"])
df = df[df["tempo_horas"] >= 0]

total = len(df)
resolvidos = (df["status"] == "Resolvido").sum()
taxa = 100 * resolvidos / total if total else 0
media = df["tempo_horas"].mean()
por_mes = df.groupby(df["data"].dt.strftime("%Y-%m")).size()
por_status = df["status"].value_counts()

print(f"Atendimentos: {total}")
print(f"Resolvidos: {resolvidos} ({taxa:.1f}%)")
print(f"Tempo médio: {media:.1f} horas")

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].bar(por_mes.index, por_mes.values)
axes[0].set_title("Atendimentos por mês")
axes[0].set_ylabel("Quantidade")
axes[0].tick_params(axis="x", rotation=35)
axes[1].bar(por_status.index, por_status.values)
axes[1].set_title("Atendimentos por status")
axes[1].tick_params(axis="x", rotation=20)
fig.suptitle("Indicadores operacionais (dados fictícios)")
fig.tight_layout()
(PASTA / "imagens").mkdir(exist_ok=True)
fig.savefig(PASTA / "imagens" / "indicadores.png", dpi=160)
print("Gráfico criado em imagens/indicadores.png")
