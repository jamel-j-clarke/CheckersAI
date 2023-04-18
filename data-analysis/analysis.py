import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS

DATA_FN = './responses.csv'
OUT_DIR = './figures/'

def load_data(filename):
    df = pd.read_csv(filename)
    return df

def plot_difficulty_vs_fun(df):
    plot = sns.scatterplot(df, x='Difficulty', y='Fun')
    fig = plot.get_figure()
    fig.savefig(OUT_DIR + "difficulty_vs_fun.png")
    plt.clf()

def plot_ai_difficulties(df):
    plot = sns.barplot(df, x='AI Type', y='Difficulty')
    fig = plot.get_figure()
    fig.savefig(OUT_DIR + "AI_difficulties.png")
    plt.clf()

def plot_ai_fun(df):
    plot = sns.barplot(df, x='AI Type', y='Fun')
    fig = plot.get_figure()
    fig.savefig(OUT_DIR + "AI_fun.png")
    plt.clf()

def plot_ai_humanlike(df):
    plot = sns.barplot(df, x='AI Type', y='Humanlike')
    fig = plot.get_figure()
    fig.savefig(OUT_DIR + "AI_humanlike.png")
    plt.clf()

def plot_ai_outcomes(df):
    plot = sns.countplot(
        data=df,
        x="AI Type", hue="Outcome"
    )
    fig = plot.get_figure()
    fig.savefig(OUT_DIR + "AI_outcomes.png")
    plt.clf()

def wordcloud(df):
    """ Generates wordcloud from the emotions and highlights participants wrote for each AI. """
    standard_wordbank = ''
    custom_wordbank = ''
    avg_wordbank = ''

    for index, row in df.iterrows():
        if row['AI Type'] == 'Standard':
            standard_wordbank += row['Emotions'] + ' ' + row['Highlight']
        if row['AI Type'] == 'Custom':
            custom_wordbank += row['Emotions'] + ' ' + row['Highlight']
        if row['AI Type'] == 'Average':
            avg_wordbank += row['Emotions'] + ' ' + row['Highlight']

    stopwords = set(STOPWORDS)
    standard_wordcloud = WordCloud(width=800, height=400, stopwords=stopwords, background_color="white").generate(standard_wordbank)
    plt.figure( figsize=(20,10))
    plt.imshow(standard_wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(OUT_DIR + 'standard_wordcloud.png')
    plt.clf()

    custom_wordcloud = WordCloud(width=800, height=400, stopwords=stopwords, background_color="white").generate(standard_wordbank)
    plt.figure( figsize=(20,10))
    plt.imshow(custom_wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(OUT_DIR + 'custom_wordcloud.png')
    plt.clf()

    avg_wordcloud = WordCloud(width=800, height=400, stopwords=stopwords, background_color="white").generate(standard_wordbank)
    plt.figure( figsize=(20,10))
    plt.imshow(avg_wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(OUT_DIR + 'avg_wordcloud.png')
    plt.clf()

def generate_plots(df):
    plot_difficulty_vs_fun(df)
    plot_ai_difficulties(df)
    plot_ai_fun(df)
    plot_ai_humanlike(df)
    plot_ai_outcomes(df)
    wordcloud(df)

def main():
    df = load_data(DATA_FN)
    generate_plots(df)

if __name__ == '__main__':
    main()