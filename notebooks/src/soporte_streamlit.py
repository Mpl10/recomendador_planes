import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity




def planes_similares(plan):
    '''
    Recomendador que devuelve los 3 planes con mayor similitud a un plan dado
    '''
    df_planes= pd.read_csv(f'../data/ENTRENAMIENTO.csv')
    contador_argumento= CountVectorizer(min_df=3)

    argumentos_bag_of_words =(contador_argumento
                              .fit_transform(df_planes["descripcion_conc"])
                              .toarray())

    columnas_descripciones= [tup[0] for tup in sorted(contador_argumento.vocabulary_.items(), key= lambda x: x[1])]

    argumentos_bag_of_words_df= pd.DataFrame(argumentos_bag_of_words, columns=columnas_descripciones, index= df_planes["id"])
    tf_idf= TfidfTransformer()
    tf_idf_planes= tf_idf.fit_transform(argumentos_bag_of_words_df).toarray()
    tf_idf_planes_df= pd.DataFrame(tf_idf_planes, columns=columnas_descripciones, index= df_planes["id"])
    cosine_sim=cosine_similarity(tf_idf_planes_df)
    matriz_simil_planes_df= pd.DataFrame(cosine_sim, columns= df_planes["id"], index= df_planes["id"])

    similares=matriz_simil_planes_df[plan].sort_values(ascending=False).head(4)
    df_similares = similares.to_frame(name='similitud')
    indices = list(set(df_similares.index))
    df_planes_all= pd.read_csv(f'../data/PRINCIPAL.csv')
    df_filtrado = df_planes_all[df_planes_all['id'].isin(indices)]
    df_filtrado = df_filtrado.set_index('id').join(df_similares)
    df_filtrado = df_filtrado.sort_values(by='similitud', ascending=False)
    df_filtrado = df_filtrado[df_filtrado['similitud'] < 0.9999999]

    return df_filtrado