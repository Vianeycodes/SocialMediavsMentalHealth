import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['figure.figsize'] = (10, 5)

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'social_media_mental_health 2.csv')
df = pd.read_csv(CSV_PATH)

df.columns = df.columns.str.lower()
df.rename(columns={
    'gad_7_score':    'gad7_score',
    'gad_7_severity': 'gad7_severity',
    'phq_9_score':    'phq9_score',
    'phq_9_severity': 'phq9_severity',
}, inplace=True)

print(f'Loaded {len(df):,} rows x {df.shape[1]} columns')
print(df.head())

df['late_night_usage']          = df['late_night_usage'].astype(bool)
df['social_comparison_trigger'] = df['social_comparison_trigger'].astype(bool)

gad7_order = ['Minimal', 'Mild', 'Moderate', 'Severe']
phq9_order = ['None-Minimal', 'Mild', 'Moderate', 'Moderately Severe', 'Severe']
df['gad7_severity'] = pd.Categorical(df['gad7_severity'], categories=gad7_order, ordered=True)
df['phq9_severity'] = pd.Categorical(df['phq9_severity'], categories=phq9_order, ordered=True)

print(df.dtypes)
print(df.describe())

# RQ1 — Screen time vs GAD-7 (Quartile + ANOVA)
df['screen_time_quartile'] = pd.qcut(
    df['daily_screen_time_hours'], q=4,
    labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)']
)

quartile_stats = df.groupby('screen_time_quartile', observed=True)['gad7_score'].agg(
    mean='mean', std='std', count='count'
).round(2)
print('GAD-7 by screen-time quartile:')
print(quartile_stats)

groups  = [g['gad7_score'].values for _, g in df.groupby('screen_time_quartile', observed=True)]
f_stat, p_val = stats.f_oneway(*groups)
print(f'\nANOVA - F={f_stat:.3f}, p={p_val:.4f}')
print('Significant (p<0.05):', p_val < 0.05)

r, p = stats.pearsonr(df['daily_screen_time_hours'], df['gad7_score'])
print(f'Pearson r={r:.3f}, p={p:.4f}')

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.boxplot(data=df, x='screen_time_quartile', y='gad7_score', ax=axes[0])
axes[0].set_title('GAD-7 Score by Screen Time Quartile')
axes[0].set_xlabel('Screen Time Quartile')
axes[0].set_ylabel('GAD-7 Score')

sns.regplot(data=df, x='daily_screen_time_hours', y='gad7_score',
            scatter_kws={'alpha': 0.1}, ax=axes[1])
axes[1].set_title(f'Screen Time vs GAD-7 (r={r:.2f})')
axes[1].set_xlabel('Daily Screen Time (hours)')
axes[1].set_ylabel('GAD-7 Score')
plt.tight_layout()
plt.savefig('rq1_screen_time_vs_anxiety.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved rq1_screen_time_vs_anxiety.png')

# RQ2 — Late-night usage vs sleep duration (T-Test)
late    = df[df['late_night_usage']]['sleep_duration_hours']
no_late = df[~df['late_night_usage']]['sleep_duration_hours']

print(f'Late-night users - n={len(late):,}, mean sleep={late.mean():.2f} h, sd={late.std():.2f}')
print(f'No late-night    - n={len(no_late):,}, mean sleep={no_late.mean():.2f} h, sd={no_late.std():.2f}')

t_stat, p_val = stats.ttest_ind(late, no_late)
print(f'\nT-Test - t={t_stat:.3f}, p={p_val:.4f}')
print('Significant (p<0.05):', p_val < 0.05)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.boxplot(data=df, x='late_night_usage', y='sleep_duration_hours', ax=axes[0])
axes[0].set_title('Sleep Duration vs Late-Night Usage')
axes[0].set_xticklabels(['No Late-Night', 'Late-Night'])
axes[0].set_ylabel('Sleep Duration (hours)')

sns.histplot(data=df, x='sleep_duration_hours', hue='late_night_usage',
             kde=True, bins=30, ax=axes[1])
axes[1].set_title('Sleep Duration Distribution by Late-Night Usage')
axes[1].set_xlabel('Sleep Duration (hours)')
plt.tight_layout()
plt.savefig('rq2_sleep_vs_late_night.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved rq2_sleep_vs_late_night.png')

# Dashboard
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Social Media & Mental Health - Dashboard', fontsize=16, fontweight='bold')

gad7_counts = df['gad7_severity'].value_counts().reindex(gad7_order)
axes[0, 0].pie(gad7_counts, labels=gad7_order, autopct='%1.1f%%', startangle=90,
               colors=sns.color_palette('YlOrRd', 4))
axes[0, 0].set_title('GAD-7 Anxiety Severity')

phq9_counts = df['phq9_severity'].value_counts().reindex(phq9_order)
axes[0, 1].pie(phq9_counts, labels=phq9_order, autopct='%1.1f%%', startangle=90,
               colors=sns.color_palette('Blues', 5))
axes[0, 1].set_title('PHQ-9 Depression Severity')

sns.histplot(df['daily_screen_time_hours'], bins=30, kde=True, ax=axes[0, 2], color='teal')
axes[0, 2].set_title('Daily Screen Time Distribution')
axes[0, 2].set_xlabel('Hours per Day')

sns.boxplot(data=df, x='user_archetype', y='gad7_score', ax=axes[1, 0])
axes[1, 0].set_title('GAD-7 by User Archetype')
axes[1, 0].tick_params(axis='x', rotation=30)

sns.boxplot(data=df, x='primary_platform', y='phq9_score', ax=axes[1, 1])
axes[1, 1].set_title('PHQ-9 by Platform')
axes[1, 1].tick_params(axis='x', rotation=30)

numeric_cols = ['age', 'daily_screen_time_hours', 'sleep_duration_hours', 'gad7_score', 'phq9_score']
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=axes[1, 2], vmin=-1, vmax=1)
axes[1, 2].set_title('Correlation Matrix')

plt.tight_layout()
plt.savefig('mental_health_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print('Dashboard saved to mental_health_dashboard.png')

# Key Findings
print('\n=== KEY FINDINGS ===')
print(f"Total participants: {len(df):,}")
print(f"Age range: {df['age'].min()}-{df['age'].max()} years")
print(f"Avg daily screen time: {df['daily_screen_time_hours'].mean():.2f} h")
print(f"Avg sleep duration:    {df['sleep_duration_hours'].mean():.2f} h")
print(f"Avg GAD-7 score:       {df['gad7_score'].mean():.2f} / 21")
print(f"Avg PHQ-9 score:       {df['phq9_score'].mean():.2f} / 27")
print()
pct_severe_gad7 = (df['gad7_severity'] >= 'Moderate').mean() * 100
pct_severe_phq9 = (df['phq9_severity'] >= 'Moderate').mean() * 100
print(f"% with Moderate+ anxiety (GAD-7):    {pct_severe_gad7:.1f}%")
print(f"% with Moderate+ depression (PHQ-9): {pct_severe_phq9:.1f}%")
print()
top_risk     = df.groupby('user_archetype')['gad7_score'].mean().idxmax()
top_platform = df.groupby('primary_platform')['phq9_score'].mean().idxmax()
print(f"Highest-risk archetype (GAD-7): {top_risk}")
print(f"Highest-risk platform (PHQ-9):  {top_platform}")
