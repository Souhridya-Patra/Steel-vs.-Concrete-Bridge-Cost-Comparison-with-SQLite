import matplotlib.pyplot as plt

def plot_costs(costs_steel, costs_concrete):
    components = list(costs_steel.keys())
    values_steel = list(costs_steel.values())
    values_concrete = list(costs_concrete.values())

    fig, ax = plt.subplots(figsize=(8, 6))
    x = range(len(components))

    ax.barh(x, values_steel, height=0.3, label="Steel", align="center")
    ax.barh([p + 0.3 for p in x], values_concrete, height=0.3, label="Concrete", align="center")

    ax.set_yticks([p + 0.15 for p in x])
    ax.set_yticklabels(components, rotation=0, ha="right")
    ax.set_xlabel("Cost")
    ax.set_title("Cost Comparison (Rotated)")

    ax.legend()
    fig.tight_layout()
    return fig