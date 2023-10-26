import pickle, time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_card import card as card
similarity = pickle.load(open('data/cosine_sim.pkl', 'rb'))
movie_dict = pickle.load(open('data/movie_dict.pkl', 'rb'))
verse_dict = pickle.load(open('data/verses_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
verses = pd.DataFrame(verse_dict)

programme_list=verses['original_title'].to_list()
def recommend(verse):
   try:
      index = programme_list.index(verse)         
      sim_score = list(enumerate(similarity[index])) 
      #pick first six suggestions to display
      sim_score = sorted(sim_score, key= lambda x: x[1], reverse=True)
      #sorts the list of tuples by similarity score in descending order.
      recommend_index = [i[0] for i in sim_score]
      return movies.iloc[recommend_index]
   except Exception as e:
      st.write('ErR. . .an error occurred while generating recommendations:', e)
  
st.set_page_config(page_title='Movie Recommender System', 
                   page_icon=':clapper:', layout = "wide",
                   menu_items={
                       'Get Help': 'https://www.extremelycoolapp.com/help',
                       'Report a bug': "https://www.extremelycoolapp.com/bug",
                       'About': "# This is a header. This is an *extremely* cool app!"
                  })
# st.markdown(f"""
#             <style>
#             .stApp {{background-image: url("https://unsplash.com/photos/AtPWnYNDJnM"); 
#                      background-attachment: fixed;
#                      background-size: cover}}
#          </style>
#          """, unsafe_allow_html=True)


# st.sidebar.title("The Movie Recommender.")
# with st.sidebar.expander("About"):
#    st.write(f"The Movie Recommender uses cosine similarity to suggest "
#             f"movies based on user input. The system "
#             f"is built using TMDB's 5000 movie dataset. Additional "
#             f"Posters are retreived using the TMDB API"
#             f" This project was initiated for a course at my university"
#             f" and is still a work in progress. If you would like to give"
#             f" feedback or contribute, the source code and documentation "
#             f"for the project can be found "
#             f"[here](https://github.com/chibuzordev/BeulahMovies)."
#             f" If you have any suggestions or questions, "
#             f"please don't hesitate to reach out.")
# with st.sidebar.expander("About"):
#    st.write(f"The Movie Recommender uses cosine similarity to suggest ")
#    containee = st.container()
# with st.sidebar.expander("About"):
#     st.write(f"The Movie Recommender uses cosine similarity to suggest ")

st.image("https://images.unsplash.com/photo-1627133805103-ce2d34ccdd37?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80", use_column_width=True)
st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Please select a Verse',
                                   sorted(verses['original_title'].values))
if st.button('Movie recommendations', use_container_width= True):
   try:
      recommendations = recommend(selected_movie_name)
      # four rows each of three columns
      col1, col2, col3, col4 = st.columns(4, gap = "medium")
      col5, col6,  col7, col8 = st.columns(4, gap = "medium")
      col9, col10, col11, col12 = st.columns(4, gap = "medium")
      col13, col14, col15, col16 = st.columns(4, gap = "medium")
      cols = zip(range(12), [col1, col2, col3, col4, col5, col6, col7, col8, 
                             col9, col10, col11, col12, col13, col15, col16])
      for i, column in cols:
          with column:
              movie_data = st.container()
              try:
                 movie_data.image(f"http://image.tmdb.org/t/p/w500{recommendations.iloc[i]['poster_path']}", use_column_width = True)
              except: 
                 movie_data.image("eRr_no_display.png", use_column_width = True)
              movie_data.markdown(f"##### {recommendations.iloc[i]['title']}")
              try:
                 movie_data.text(f'''{
                    (recommendations.iloc[i]['genres']).strip("'").strip("]").strip("[").strip(",")
                 }''')
              except: 
                  movie_data.text("")
                  
              try:
                 movie_data.text(f"{recommendations.iloc[i]['vote_average']}/10")
              except: 
                  movie_data.text("")
                  
              try:
                 movie_data.text(recommendations.iloc[i]['release_date'])    
              except: 
                  movie_data.text("")
                  
              with movie_data.expander("MOVIE PLOT"):
                 try:
                    st.write(f"{recommendations.iloc[i]['overview'][:120]}...")
                 except: 
                    st.text("")
                 st.markdown(f"[https://github.com/streamlit/streamlit/issues/152](hi)")
                  
      st.markdown("## Thank you ! !")   
   except Exception as e:
      st.write('ErR. . .an error occurred while displaying recommendations:', e)
