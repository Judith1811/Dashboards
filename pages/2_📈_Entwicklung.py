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
@st.cache(allow_output_mutation=True)
def load_data(file):
    df = pd.read_excel(file)
    return df
uploaded_file2 = st.file_uploader('Report aus Vendor Central hier hochladen:', type='xlsx')
if uploaded_file2 is not None:
    st.markdown('---')
    df=load_data(uploaded_file2)
    df = pd.read_excel(uploaded_file2, engine='openpyxl')
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    df.rename(columns=df.iloc[0])
    df.drop(df.index[1])

    df['Suchfrequenz-Rang ']=pd.to_numeric(df['Suchfrequenz-Rang '])
    df['Suchfrequenz-Rang ']=df['Suchfrequenz-Rang '].astype(int)

    '# Markenspezifische Suchbegriffe'

    col1, col2 = st.columns(2)

    with col1:
        choice1 = st.radio('Wähle eine Henkel Marke',('botclean','Bref','Love Nature','Persil','Perwoll','Pril','Sidolin','Sil','Somat','Spee','Vernel','Weißer Riese','WC Frisch'))

    with col2:
        choice2 = st.radio('Wähle eine Wettbewerbermarke',('Ajax','Ariel','Bissell','Cillit Bang','Coral','Dr. Beckmann','Ecover','Fairy','Finish','Frosch','Lenor','Sagrotan','Vanish','WC Ente'))

    choice1dollar = choice1+'$'
    choice1dollar2 = '$'+choice1
    choice1space = choice1+ ' '
    choice1space2 = ' '+choice1
    choice1combined = [choice1, choice1dollar, choice1dollar2, choice1space, choice1space2]
    c1= '|'.join(choice1combined)
    c1 = '"'+c1+'"'

    dsi = df.Suchbegriff.str.contains(c1, flags = re.IGNORECASE, regex = True, na = False)
    df1 = df[dsi]

    dropdown_persil = df1['Suchbegriff'].values.tolist()
    temp_list = []
    for i in dropdown_persil:
        if i not in temp_list:
            temp_list.append(i)
    dropdown_persil = temp_list

    '#### Wähle einen Suchbegriff 1 rund um die Henkel Marke'
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

    choice2dollar = choice2+'$'
    choice2dollar2 = '$'+choice2
    choice2space = choice2+ ' '
    choice2space2 = ' '+choice2
    choice2combined = [choice2, choice2dollar, choice2dollar2, choice2space, choice2space2]
    c2= '|'.join(choice2combined)
    c2 = '"'+c2+'"'

    dsi2 = df.Suchbegriff.str.contains(c2, flags = re.IGNORECASE, regex = True, na = False)
    df12 = df[dsi2]

    dropdown_persil = df12['Suchbegriff'].values.tolist()
    temp_list = []
    for i in dropdown_persil:
        if i not in temp_list:
            temp_list.append(i)
    dropdown_persil2 = temp_list

    '#### Wähle einen Suchbegriff 2 rund um die Wettbewerbermarke'
    optionpersil2 = st.selectbox('Suchbegriff 2:',dropdown_persil2)
    persilpowerbar2= df12.loc[(df12['Suchbegriff'] == optionpersil2)]

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

#########################################################################################################################
# Generische Suchbegriffe

######### Suchbegriff 1

    '# Generische Suchbegriffe im Vergleich'

    wahl_generisch_=st.text_input('Hier Suchbegriff 1 eintragen')
    generisch_ = df.Suchbegriff.str.contains(wahl_generisch_, flags = re.IGNORECASE, regex = True, na = False)
    df_generisch_ = df[generisch_]


    #dropdown_generisch_ = df_generisch_['Suchbegriff'].values.tolist()
    #temp_list = []
    #for i in dropdown_generisch_:
        #if i not in temp_list:
            #temp_list.append(i)
    #dropdown_generisch_ = temp_list

    #wahl_generisch_=st.selectbox('Generischer Suchbegriff 1 Waschen:',dropdown_generisch_)

    #wahl_generisch_=st.text_input('Hier Suchbegriff 1 eintragen')

    df_generisch__deep_a= df_generisch_.loc[(df_generisch_['Suchbegriff'] == wahl_generisch_)]


    df_generisch__deep_a = df_generisch__deep_a.iloc[:, [2,15]]
    df_generisch__deep_a.rename(columns={"Suchfrequenz-Rang ": "Suchbegriff 1"},inplace=True)
    df_generisch__deep_a['Suchbegriff 1']*= -1

    #'#### Ranking des Suchbegriffs 1'
    #st.line_chart(data=df_generisch__deep_a, x='Woche', y='Suchbegriff Waschen 1')
######### Suchbegriff 2
    #dropdown_generisch_ = df_generisch_['Suchbegriff'].values.tolist()
    #temp_list = []
    #for i in dropdown_generisch_:
        #if i not in temp_list:
           # temp_list.append(i)
    #dropdown_generisch_ = temp_list

    wahl_generisch_=st.text_input('Hier Suchbegriff 2 eintragen')


    df_generisch__deep_b= df_generisch_.loc[(df_generisch_['Suchbegriff'] == wahl_generisch_)]

    df_generisch__deep_b = df_generisch__deep_b.iloc[:, [2,15]]
    df_generisch__deep_b.rename(columns={"Suchfrequenz-Rang ": "Suchbegriff 2"},inplace=True)
    df_generisch__deep_b['Suchbegriff 2']*= -1


    #'#### Ranking des Suchbegriffs 2'
    #st.line_chart(data=df_generisch__deep_b, x='Woche', y='Suchbegriff Waschen 2')
######### Suchbegriff 1 und 2 im Vergleich
    df_generisch__deep = pd.merge(df_generisch__deep_a, df_generisch__deep_b, on=['Woche'])
    df_generisch__deep = df_generisch__deep[['Woche','Suchbegriff 1','Suchbegriff 2']]
    df_generisch__deep.set_index('Woche')


    '#### Ranking der Suchbegriffe 1 und 2 im Vergleich'
    st.line_chart(data=df_generisch__deep, x='Woche', y=["Suchbegriff 1","Suchbegriff 2"])
