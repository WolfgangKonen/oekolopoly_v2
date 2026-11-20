import matplotlib.pyplot as plt
import pandas as pd

labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]

df = pd.DataFrame({'done_reason':labels, 'cnt': sizes})
# All categories which have less than 20% of all counts are overwritten with done_reason = 'Other'.
# Then the 2nd line groups all 'Other' categories together to one row.
df.loc[df.cnt<0.2*sum(df['cnt']),['done_reason']] = "Other"
df_grouped = df.groupby('done_reason').sum().sort_values('cnt', ascending=False)
fig, ax = plt.subplots()
ax.pie(df_grouped.cnt.values,
       labels=df_grouped.index,
       autopct='%1.1f%%')
plt.show()