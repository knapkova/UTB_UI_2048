import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv('results.csv', delimiter=';')

# Group data by Type and Category, and calculate the average score and moves
grouped_data = data.groupby(['Type', 'Category']).agg({'Score': 'mean', 'Moves': 'mean'}).reset_index()

# Plot average score by Type and Category
plt.figure(figsize=(12, 8))
for category in grouped_data['Category'].unique():
    subset = grouped_data[grouped_data['Category'] == category]
    plt.bar(subset['Type'], subset['Score'], label=category)
plt.xlabel('Type')
plt.ylabel('Average Score')
plt.title('Average Score by Type and Category')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('average_score_by_type_and_category.png')
plt.show()

# Plot average moves by Type and Category
plt.figure(figsize=(12, 8))
for category in grouped_data['Category'].unique():
    subset = grouped_data[grouped_data['Category'] == category]
    plt.bar(subset['Type'], subset['Moves'], label=category)
plt.xlabel('Type')
plt.ylabel('Average Moves')
plt.title('Average Moves by Type and Category')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('average_moves_by_type_and_category.png')
plt.show()

# Plot score distribution for each Type and Category
plt.figure(figsize=(12, 8))
for category in data['Category'].unique():
    subset = data[data['Category'] == category]
    plt.hist(subset['Score'], bins=20, alpha=0.5, label=category)
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.title('Score Distribution by Type and Category')
plt.legend()
plt.tight_layout()
plt.savefig('score_distribution_by_type_and_category.png')
plt.show()