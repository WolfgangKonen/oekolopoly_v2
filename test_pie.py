import matplotlib.pyplot as plt
import pandas as pd

labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]

df = pd.DataFrame({'done_reason':labels, 'cnt': sizes})
df.loc[df.cnt<20,['done_reason']] = "Other"
df_grouped = df.groupby('done_reason').sum().sort_values('cnt', ascending=False)
sizes = df_grouped.cnt.values
labels = df_grouped.index
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.show()