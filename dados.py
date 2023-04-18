# Importando bibliotecas necessárias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from bs4 import BeautifulSoup
import requests

# SElecionando os dados da wikipedia de NAruto
url = 'https://naruto.fandom.com/wiki/Narutopedia'
html = requests.get(url).content
soup = BeautifulSoup(html, 'html.parser')

# Find all episode titles and descriptions
episode_titles = soup.find_all('td', {'class': 't-name'})
episode_descriptions = soup.find_all('td', {'class': 't-summary'})

# Clean the data
cleaned_titles = []
cleaned_descriptions = []
for i in range(len(episode_titles)):
    title = episode_titles[i].text.strip()
    description = episode_descriptions[i].text.strip()
    if title not in cleaned_titles and description not in cleaned_descriptions:
        cleaned_titles.append(title)
        cleaned_descriptions.append(description)
        
# Create a Pandas DataFrame
data = {'Title': cleaned_titles, 'Description': cleaned_descriptions}
df = pd.DataFrame(data)


# Define a function to extract character names from the episode descriptions
def extract_characters(description):
    words = description.split()
    characters = []
    for i in range(len(words)):
        if words[i] == 'featuring' or words[i] == 'introducing':
            character = ' '.join(words[i+1:i+3])
            characters.append(character)
        elif words[i] == 'starring':
            character = ' '.join(words[i+1:i+4])
            characters.append(character)
    return characters

# Extract character names and add to DataFrame
df['Characters'] = df['Description'].apply(extract_characters)

# Create a new DataFrame with one row per character
characters = []
for i in range(len(df)):
    for character in df.loc[i, 'Characters']:
        characters.append({'Title': df.loc[i, 'Title'], 'Character': character})
df_characters = pd.DataFrame(characters)

# Perform analysis

# Which are the most popular episodes of Naruto?
df_ratings = pd.read_csv('naruto_ratings.csv')  # Ratings data obtained from another source
df_popular = df_ratings.merge(df, on='Title')
df_popular = df_popular.sort_values(by='Rating', ascending=False).head(10)
plt.bar(df_popular['Title'], df_popular['Rating'])
plt.xticks(rotation=90)
plt.xlabel('Episode Title')
plt.ylabel('Rating')
plt.title('Top 10 Most Popular Episodes of Naruto')
plt.show()

# Which characters appear most frequently in Naruto?
df_characters = df_characters['Character'].value_counts().head(10)
plt.bar(df_characters.index, df_characters.values)
plt.xticks(rotation=90)
plt.xlabel('Character')
plt.ylabel('Number of Appearances')
plt.title('Top 10 Characters with the Most Appearances in Naruto')
plt.show()

# Which are the most common themes or storylines in Naruto?
stopwords = set(STOPWORDS)
stopwords.update(['Naruto', 'episode', 'Ninja', 'Battles', 'battle', 'Konohagakure', 'Sasuke', 'Jiraiya'])
wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=stopwords, min_font_size=10).generate(' '.join(df['Description']))
plt.figure(figsize=(8,8))
plt.imshow(wordcloud)
plt.axis('off')
plt.title('Word Cloud of Common Themes in Naruto')
plt.show()
