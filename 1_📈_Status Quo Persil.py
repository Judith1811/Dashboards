import streamlit as st
import pandas as pd
#import plotly.express as px
import re
import numpy as np
import plotly.graph_objs as go

st.set_page_config(page_title='Amazon Suchvolumen Persil')
st.title('Amazon Suchvolumen Persil')
st.write('Für folgende Auswertung den aktuellen Report aus Vendor Central (https://vendorcentral.amazon.de/analytics/dashboard/searchTerms) herunterladen. '
         'Auswertungsbereich frei wählbar und Abteilung "Amazon.de" oder "Drugstore" möglich.')

uploaded_file = st.file_uploader('Report aus Vendor Central hier hochladen:', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    df.rename(columns=df.iloc[0])
    df.drop(df.index[1])

    st.write('Auswertung der Suchbegriffe erfolgt auf der Ebene', df.iloc[0]['Abteilung'],'.')

    #Hilfestellungen###################################################################################
    dsi = df.Suchbegriff.str.contains('persil |persil$', flags = re.IGNORECASE, regex = True, na = False)
    toppersil = df[dsi]
    toppersil = toppersil.dropna()

    dsi = df.Suchbegriff.str.contains('ariel |ariel$', flags = re.IGNORECASE, regex = True, na = False)
    topariel = df[dsi]
    topariel = topariel.dropna()
    ###################################################################################################

    col1, col2 = st.columns(2)

    with col1:
        "####  Ranking Suchbegriffe rund um Persil:"
        dropdown_persil = toppersil['Suchbegriff'].values.tolist()
        optionpersil = st.selectbox('Wähle einen Suchbegriff',dropdown_persil)
        persil = df.loc[(df['Suchbegriff'] == optionpersil)]
        persil.reset_index(drop=True,inplace=True)
        st.write('Der Suchbegriff',optionpersil, 'belegt im Ranking Platz', persil.loc[0]['Suchfrequenz-Rang '],'von',df['Suchfrequenz-Rang '].iat[-1])

    with col2:
        "####  Ranking Suchbegriffe rund um Ariel:"
        dropdown_ariel = topariel['Suchbegriff'].values.tolist()
        optionariel = st.selectbox('Wähle einen Suchbegriff',dropdown_ariel)
        ariel = df.loc[(df['Suchbegriff'] == optionariel)]
        ariel.reset_index(drop=True,inplace=True)
        st.write('Der Suchbegriff',optionariel, 'belegt im Ranking Platz', ariel.loc[0]['Suchfrequenz-Rang '],'von',df['Suchfrequenz-Rang '].iat[-1])

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label=optionpersil, value=persil.loc[0]['Suchfrequenz-Rang '], delta=ariel.loc[0]['Suchfrequenz-Rang ']-persil.loc[0]['Suchfrequenz-Rang '])

    with col2:
        st.metric(label=optionariel, value=ariel.loc[0]['Suchfrequenz-Rang '], delta=persil.loc[0]['Suchfrequenz-Rang ']-ariel.loc[0]['Suchfrequenz-Rang '])

    '#### TOP Suchbegriffe rund um Persil:'
    st.dataframe(toppersil)

    '#### TOP Suchbegriffe rund um Ariel:'
    st.dataframe(topariel)

    '#### TOP Suchbegriffe rund um Persil und Ariel:'
    dsi = df.Suchbegriff.str.contains('ariel |persil |persil$|ariel$', flags = re.IGNORECASE, regex = True, na = False)
    toppersilariel = df[dsi]
    toppersilariel = toppersilariel.dropna()
    st.dataframe(toppersilariel)

    '#### Persil Produkte unter den TOP 3 der angeklickten ASINs:'
    df.rename(columns={"Produkttitel #1": "col1","Produkttitel #2": "col2","Produkttitel #3": "col3"},inplace=True)
    ids_persil = df.col1.str.contains('persil |persil$', flags = re.IGNORECASE, regex = True, na = False)
    product1_persil = df[ids_persil]
    ids_persil = df.col2.str.contains('persil |persil$', flags = re.IGNORECASE, regex = True, na = False)
    product2_persil = df[ids_persil]
    ids_persil = df.col3.str.contains('persil |persil$', flags = re.IGNORECASE, regex = True, na = False)
    product3_persil = df[ids_persil]
    products_persil = pd.concat([product1_persil,product2_persil,product3_persil]).drop_duplicates().reset_index(drop=True)
    products_persil = products_persil.dropna()
    st.dataframe(products_persil)

    '#### Ariel Produkte unter den TOP 3 der angeklickten ASINs:'
    ids_ariel = df.col1.str.contains('ariel |ariel$', flags = re.IGNORECASE, regex = True, na = False)
    product1_ariel = df[ids_ariel]
    ids_ariel = df.col2.str.contains('ariel ariel$', flags = re.IGNORECASE, regex = True, na = False)
    product2_ariel = df[ids_ariel]
    ids_ariel = df.col3.str.contains('ariel ariel$', flags = re.IGNORECASE, regex = True, na = False)
    product3_ariel = df[ids_ariel]
    products_ariel = pd.concat([product1_ariel,product2_ariel,product3_ariel]).drop_duplicates().reset_index(drop=True)
    products_ariel = products_ariel.dropna()
    st.dataframe(products_ariel)

    col1, col2 = st.columns(2)

    with col1:
        st.caption('Generische Suchbegriffe, bei denen unter den TOP 3 geklickten Produkten nur Persil auftaucht und kein Ariel')
        vergleich_persil = products_persil.iloc[: , [1]]
        vergleich_persil['Marke'] = 'Persil'
        vergleich_persil = vergleich_persil[~vergleich_persil.Suchbegriff.str.contains("persil ")]
        vergleich_persil = vergleich_persil[~vergleich_persil.Suchbegriff.str.contains(" persil")]
        vergleich_persil = vergleich_persil[vergleich_persil.Suchbegriff != 'persil']
        vergleich_persil.reset_index(inplace=True, drop=True)
        vergleich_persil

    with col2:
        st.caption('Generische Suchbegriffe, bei denen unter den TOP 3 geklickten Produkten nur Ariel auftaucht und kein Persil')
        vergleich_ariel = products_ariel.iloc[: , [1]]
        vergleich_ariel['Marke'] = 'Ariel'
        vergleich_ariel = vergleich_ariel[~vergleich_ariel.Suchbegriff.str.contains("ariel ")]
        vergleich_ariel = vergleich_ariel[~vergleich_ariel.Suchbegriff.str.contains(" ariel")]
        vergleich_ariel = vergleich_ariel[vergleich_ariel.Suchbegriff != 'ariel']
        vergleich_ariel.reset_index(inplace=True, drop=True)
        vergleich_ariel

    title = st.text_input('Suchbegriff', 'Trage hier den gewünschten Suchbegriff ein')
    '#### TOP 3 Klickrate des Suchbegriffs'
    waschmittelpods = df.loc[(df['Suchbegriff'] == title)]
    waschmittelpods1 = waschmittelpods[['col1','Klickrate #1']]
    waschmittelpods1.rename(columns={'col1':'Produktname','Klickrate #1':'Klickrate'},inplace=True)
    waschmittelpods2 = waschmittelpods[['col2','Klickrate #2']]
    waschmittelpods2.rename(columns={'col2':'Produktname','Klickrate #2':'Klickrate'},inplace=True)
    waschmittelpods3 = waschmittelpods[['col3','Klickrate #3']]
    waschmittelpods3.rename(columns={'col3':'Produktname','Klickrate #3':'Klickrate'},inplace=True)
    waschmittelpodssum = pd.concat([waschmittelpods1, waschmittelpods2, waschmittelpods3]).drop_duplicates().reset_index(drop=True)
    waschmittelpodssum['Produkt'] = waschmittelpodssum['Produktname'].str.split().str[:4].str.join(sep=" ")
    waschmittelpodssum = waschmittelpodssum.drop('Produktname',axis=1)
    waschmittelpodssum['Klickrate']=pd.to_numeric(waschmittelpodssum['Klickrate'])
    waschmittelpodssum.loc['sum']=1-waschmittelpodssum.sum(numeric_only=True, axis=0)
    waschmittelpodssum.replace(np.nan,'Others',inplace=True)
    labels = waschmittelpodssum['Produkt'].value_counts().index
    values = waschmittelpodssum['Klickrate'].values
    fig = go.Figure(
        go.Pie(
            labels = labels,
            values = values,
            hoverinfo = "label+percent",
            textinfo = "percent"
        ))
    st.plotly_chart(fig)















#%%


#%%

#%%
