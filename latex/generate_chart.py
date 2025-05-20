#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

# Data from the results
metrics = ['Entropy H', 'Expected Length E[L]', 'Realized Length L̄']
k1_values = [2.4058, 2.4500, 2.4450]
k2_values = [4.8116, 4.8456, 4.8420]

# Normalize k=2 values by dividing by 2 for fair comparison
k2_normalized = [v/2 for v in k2_values]

# Set up the bar chart
fig, ax = plt.subplots(figsize=(8, 5))

x = np.arange(len(metrics))  # the label locations
width = 0.35  # the width of the bars

rects1 = ax.bar(x - width/2, k1_values, width, label='k=1', color='skyblue')
rects2 = ax.bar(x + width/2, k2_normalized, width, label='k=2 (normalized)', color='lightcoral')

# Add fixed-length coding reference line (log₂6 ≈ 2.585)
ax.axhline(y=2.585, color='black', linestyle='--', alpha=0.7)
ax.text(len(metrics)-1, 2.615, 'Fixed-length (log₂6 ≈ 2.585)', va='bottom', ha='right', fontsize=9)

# Add some text for labels, title and custom x-axis tick labels
ax.set_ylabel('Bits')
ax.set_title('Comparison of Huffman Coding Metrics')
ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.legend()

# Add value annotations on top of each bar
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.4f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

# Add a note about k=2 normalization
plt.figtext(0.5, 0.01, 
           "Note: k=2 values are normalized (divided by 2) for direct comparison", 
           ha="center", fontsize=9, style='italic')

# Save the figure
plt.savefig('fig_results.pdf')
plt.savefig('fig_results.png', dpi=300)
print("Charts saved as fig_results.pdf and fig_results.png") 