import os
import pandas as pd
import streamlit as st
#import numpy as np
#import plotly.express as px
cwd = os.path.abspath('')
import re
import altair as alt
#%%
st.set_page_config(page_title='Entwicklung von Suchbegriffen im Vergleich')
st.title('Entwicklung von Suchbegriffen im Vergleich')
st.write('Für folgende Auswertung die Mastertabelle (...) um die ersten 50.000 Zeilen der aktuellen KW ergänzen, und mit dem ensprechenden Zeistempel '
         'ergänzen. Aktuelle Reporte stammen aus Vendor Central: https://vendorcentral.amazon.de/analytics/dashboard/searchTerms '
         ''
         'Auswertungsbereich: '
         'wöchentlich, Abteilung: Amazon.de')
#%%
uploaded_file = st.file_uploader('Report aus Vendor Central hier hochladen:', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    df.rename(columns=df.iloc[0])
    df.drop(df.index[1])

    df['Suchfrequenz-Rang ']=pd.to_numeric(df['Suchfrequenz-Rang '])
    df['Suchfrequenz-Rang ']=df['Suchfrequenz-Rang '].astype(int)

    dsi = df.Suchbegriff.str.contains('persil |persil$', flags = re.IGNORECASE, regex = True, na = False)
    df1 = df[dsi]

    dropdown_persil = df1['Suchbegriff'].values.tolist()
    temp_list = []
    for i in dropdown_persil:
        if i not in temp_list:
            temp_list.append(i)
    dropdown_persil = temp_list

    '#### Wähle einen Suchbegriff 1'
    optionpersil = st.selectbox('Suchbegriff 1:',dropdown_persil)
    persilpowerbar= df1.loc[(df1['Suchbegriff'] == optionpersil)]
    #%%
    ranking1 = persilpowerbar.iloc[:, [2,15]]
    ranking1.rename(columns={"Suchfrequenz-Rang ": "Suchbegriff 1"},inplace=True)
    ranking1['Suchbegriff 1']*= -1

    '#### Ranking des Suchbegriffs 1'
    st.line_chart(data=ranking1, x='Woche', y='Suchbegriff 1')

######################
    entwicklungppb1 = persilpowerbar.iloc[:, [4,5,15]]
    entwicklungppb1.rename(columns={"Produkttitel #1": "Produkttitel","Klickrate #1": "Klickrate"},inplace=True)

    entwicklungppb2 = persilpowerbar.iloc[:, [8,9,15]]
    entwicklungppb2.rename(columns={"Produkttitel #2": "Produkttitel","Klickrate #2": "Klickrate"},inplace=True)

    entwicklungppb3 = persilpowerbar.iloc[:, [12,13,15]]
    entwicklungppb3.rename(columns={"Produkttitel #3": "Produkttitel","Klickrate #3": "Klickrate"},inplace=True)

    entwicklungppb = pd.concat([entwicklungppb1, entwicklungppb2, entwicklungppb3]).drop_duplicates().reset_index(drop=True)
    entwicklungppb = entwicklungppb.dropna()
    entwicklungppb['Produkttitel'] = entwicklungppb['Produkttitel'].str.split(',').str[0]

    entwicklungppb=entwicklungppb.pivot(index='Woche',columns='Produkttitel',values='Klickrate')

    entwicklungppb = entwicklungppb.fillna(0)

    entwicklungppb['Rest']=1-entwicklungppb.sum(numeric_only=True, axis=1)

    '#### Verteilung der TOP 3 geklickten Produkte von Suchbegriff 1'
    st.bar_chart(data=entwicklungppb)

######################

    dropdown_persil2 = dropdown_persil

    '#### Wähle einen Suchbegriff 2'
    optionpersil2 = st.selectbox('Suchbegriff 2:',dropdown_persil2)
    persilpowerbar2= df1.loc[(df1['Suchbegriff'] == optionpersil2)]

    ranking2 = persilpowerbar2.iloc[:, [2,15]]
    ranking2.rename(columns={"Suchfrequenz-Rang ": "Suchbegriff 2"},inplace=True)
    ranking2['Suchbegriff 2']*= -1

    ranking = pd.merge(ranking1, ranking2, on=['Woche'])
    ranking = ranking[['Woche','Suchbegriff 1','Suchbegriff 2']]
    ranking.set_index('Woche')

    '#### Ranking des Suchbegriffs 2'
    st.line_chart(data=ranking2, x='Woche', y='Suchbegriff 2')

######################

    entwicklungppb1b = persilpowerbar2.iloc[:, [4,5,15]]
    entwicklungppb1b.rename(columns={"Produkttitel #1": "Produkttitel","Klickrate #1": "Klickrate"},inplace=True)

    entwicklungppb2b = persilpowerbar2.iloc[:, [8,9,15]]
    entwicklungppb2b.rename(columns={"Produkttitel #2": "Produkttitel","Klickrate #2": "Klickrate"},inplace=True)

    entwicklungppb3b = persilpowerbar2.iloc[:, [12,13,15]]
    entwicklungppb3b.rename(columns={"Produkttitel #3": "Produkttitel","Klickrate #3": "Klickrate"},inplace=True)

    entwicklungppb_b = pd.concat([entwicklungppb1b, entwicklungppb2b, entwicklungppb3b]).drop_duplicates().reset_index(drop=True)
    entwicklungppb_b = entwicklungppb_b.dropna()
    entwicklungppb_b['Produkttitel'] = entwicklungppb_b['Produkttitel'].str.split(',').str[0]

    entwicklungppb_b=entwicklungppb_b.pivot(index='Woche',columns='Produkttitel',values='Klickrate')

    entwicklungppb_b = entwicklungppb_b.fillna(0)

    entwicklungppb_b['Rest']=1-entwicklungppb_b.sum(numeric_only=True, axis=1)

    '#### Verteilung der TOP 3 geklickten Produkte von Suchbegriff 2'
    st.bar_chart(data=entwicklungppb_b)

######################

    '#### Ranking der Suchbegriffe 1 und 2 im Vergleich'
    st.line_chart(data=ranking, x='Woche', y=["Suchbegriff 1","Suchbegriff 2"])

######################