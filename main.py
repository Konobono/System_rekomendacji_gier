import streamlit as st
import pandas as pd
import numpy as np
import pickle

#moduł pickle do obsługi pliku similarity.pkl, ktory powstał z funkcji similarity z pliku 'cos_similarity'
#moduł streamlit do stworzenia UI

st.set_page_config(page_title='System rekomendacji gier steam',
                   page_icon='🎮',
                   layout="wide")

# Zbiory danych

l_data = pd.read_csv('data/data3.csv')
l_data.drop(['Unnamed: 0','Unnamed: 0.1'],axis=1)

similarity = pickle.load(open('data/similarity.pkl','rb'))



# Strona glowna

st.title('🎮 System rekomendacji gier')

st.write("Szukasz nowych gier? Po prostu wpisz tytuły swoich ulubionych gier, a aplikacja ci w tym pomoże.")


# Rekomendacje

st.write("<h4>Wpisz tytuł/y gier poniżej</h4>", unsafe_allow_html=True)

games = st.multiselect('', l_data['name'], [], key='games')
#pozwala wybrać wiele tytułów

recommend = st.button('Rekomenduj')
col1,col2 = st.columns(2)

if recommend:
    top_recommendations = []

    for game in games:
        index = l_data[l_data['name'] == game].index[0]
        top_six = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])[1:7]
        top_recommendations.extend([top_six[i][0] for i in range(len(top_six))])

    top_recommendations = list(set(top_recommendations))[:6]

    for i, k in enumerate(top_recommendations):
        if i % 2 == 0:
            with col1:
                st.markdown("""
                            <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                            <a href="{link}" target="_blank"><img src="{image}" style="width:500px;height:250px; margin-bottom: 10px;"></a>
                            <div style="text-align: center;">
                                <p style="margin: 0; font-size: 20px;"><b>Title: </b>{name}</p>
                                <p style="margin: 0; font-size: 20px;"><b>Developer: </b>{developer}</p>
                            </div>
                            </div>
                            """.format(link=l_data["Steam Page"][k], image=l_data["header_image"][k], name=l_data["name"][k], developer=l_data['developer'][k]), unsafe_allow_html=True)
        else:
            with col2:
                st.markdown("""
                            <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
                            <a href="{link}" target="_blank"><img src="{image}" style="width:500px;height:250px; margin-bottom: 10px;"></a>
                            <div style="text-align: center;">
                                <p style="margin: 0; font-size: 20px;"><b>Title: </b>{name}</p>
                                <p style="margin: 0; font-size: 20px;"><b>Developer: </b>{developer}</p>
                            </div>
                            </div>
                            """.format(link=l_data["Steam Page"][k], image=l_data["header_image"][k], name=l_data["name"][k], developer=l_data['developer'][k]), unsafe_allow_html=True)



# Pasek boczny

st.sidebar.header("Instrukcje:")

st.sidebar.markdown("1. Wybierz grę z rozwijanego menu.")
st.sidebar.markdown("2. Wciśnij przycisk 'Rekomenduj'.")
st.sidebar.markdown("3. Zobacz wyniki.")
st.sidebar.markdown("4. Najedź na obrazek, jeśli chcesz odwiedzić stronę z grą. ")

st.sidebar.markdown('---')

# wyswietlanie tagow
for game in games:
    selected_game_categories = l_data.loc[l_data['name'] == game, 'Tags'].iloc[0]

    if selected_game_categories:
        st.sidebar.subheader(f"Gra '{game}' posiada tagi:")
        categories_list = selected_game_categories.split(',')
        for category in categories_list:
            st.sidebar.write(f"- {category.strip()}")


st.markdown('---')

trending = st.subheader('Filler')

st.write("----------------------------------------------------------------------------------------------------Zapychacz----------------------------------------------------------------------------------------------------")



