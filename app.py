import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Netflix Dashboard", layout="wide")
st.title("🎬 Netflix Content Analysis and Popularity Predictor")

# Upload CSV
uploaded_file = st.file_uploader("Upload your Netflix dataset (.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")

    # --- Preprocessing ---
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month

    # --- Filters ---
    st.sidebar.header("Filters")
    type_options = df['type'].dropna().unique()
    country_options = df['country'].dropna().unique()

    selected_type = st.sidebar.multiselect("Select Type", options=type_options, default=list(type_options))
    selected_country = st.sidebar.multiselect("Select Country", options=country_options, default=['United States', 'India'])

    filtered_df = df[df['type'].isin(selected_type)]
    if selected_country:
        filtered_df = filtered_df[filtered_df['country'].isin(selected_country)]

    # --- Type Distribution ---
    st.subheader("📊 Content Type Distribution")
    st.bar_chart(filtered_df['type'].value_counts())

    # --- Year-wise Content ---
    st.subheader("📅 Content Added by Year")
    if 'year_added' in filtered_df.columns:
        year_counts = filtered_df['year_added'].value_counts().sort_index()
        st.line_chart(year_counts)

    # --- Rating Distribution ---
    st.subheader("🔢 Rating Distribution")
    st.bar_chart(filtered_df['rating'].value_counts().head(10))

    # --- Top Genres ---
    st.subheader("🎭 Top Genres")
    genre_series = filtered_df['listed_in'].dropna().str.split(', ').explode()
    st.bar_chart(genre_series.value_counts().head(10))

    # --- Country Distribution ---
    st.subheader("🌍 Content Count by Country")
    st.bar_chart(filtered_df['country'].value_counts().head(10))

    # --- Simulated Popularity Prediction ---
    st.subheader("🌟 Simulated Popularity Prediction")

    # Top 10 Genres (Expanded)
    st.subheader("🎭 Top 10 Genres on Netflix")
    genres_expanded = filtered_df['listed_in'].dropna().str.split(', ').explode()
    top_genres = genres_expanded.value_counts().head(10)

    fig, ax = plt.subplots()
    sns.barplot(x=top_genres.values, y=top_genres.index, ax=ax)
    ax.set_title("Top 10 Genres")
    ax.set_xlabel("Count")
    ax.set_ylabel("Genre")
    st.pyplot(fig)

    # Country-wise Content Contribution
    st.subheader("🌍 Top Countries by Content Count")
    top_countries = filtered_df['country'].value_counts().head(10)

    fig, ax = plt.subplots()
    sns.barplot(x=top_countries.values, y=top_countries.index, ax=ax)
    ax.set_title("Top Countries with Most Content")
    ax.set_xlabel("Count")
    ax.set_ylabel("Country")
    st.pyplot(fig)

    # Top 10 Directors
    st.subheader("🎬 Top 10 Directors")
    top_directors = filtered_df['director'].dropna().value_counts().head(10)

    fig, ax = plt.subplots()
    sns.barplot(x=top_directors.values, y=top_directors.index, ax=ax)
    ax.set_title("Top 10 Directors by Content")
    ax.set_xlabel("Count")
    ax.set_ylabel("Director")
    st.pyplot(fig)

    # Year-wise Content Release Trend
    st.subheader("📈 Content Release Trend by Year")
    if 'release_year' in filtered_df.columns:
        year_trend = filtered_df['release_year'].value_counts().sort_index()

        fig, ax = plt.subplots()
        sns.lineplot(x=year_trend.index, y=year_trend.values, marker="o", ax=ax)
        ax.set_title("Content Released by Year")
        ax.set_xlabel("Release Year")
        ax.set_ylabel("Number of Titles")
        st.pyplot(fig)


    def is_popular(row):
        try:
            duration = int(str(row['duration']).split(' ')[0])
        except:
            duration = 0
        return (
            row['release_year'] >= 2018 and
            'Drama' in str(row['listed_in']) and
            duration >= 90
        )

    filtered_df['is_popular'] = filtered_df.apply(is_popular, axis=1)
    popular_df = filtered_df[filtered_df['is_popular'] == True]

    st.write(f"📈 Number of simulated popular titles: {popular_df.shape[0]}")
    st.dataframe(popular_df[['title', 'type', 'release_year', 'duration', 'listed_in']].head(10))

    # --- Popular Titles by Year ---
    st.subheader("📆 Popular Titles by Release Year")
    st.bar_chart(popular_df['release_year'].value_counts().sort_index())

else:
    st.info("Please upload a Netflix dataset to begin.")
