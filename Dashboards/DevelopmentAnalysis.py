import os
import pandas as pd
import streamlit as st
cwd = os.path.abspath('')
import re
#%%

st.title('Entwicklung von Suchbegriffen im Vergleich')
st.write('Für folgende Auswertung die Mastertabellen (https://henkelgroup.sharepoint.com/teams/MST-L-LEGEComTeam/Shared%20Documents/Forms/AllItems.aspx?csf=1&web=1&e=snGgkx&OR=Teams%2DHL&CT=1662726602405&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiIyNy8yMjA3MzEwMTAwNSIsIkhhc0ZlZGVyYXRlZFVzZXIiOmZhbHNlfQ%3D%3D&cid=279365d0%2D029a%2D4859%2D8d75%2D8f8ca6400927&RootFolder=%2Fteams%2FMST%2DL%2DLEGEComTeam%2FShared%20Documents%2FGeneral%2F1%5FAmazon%2FTools%204%20Amazon%2FJudith%20Streamlit%20App&FolderCTID=0x012000D6892CF00C98694EBC4249412BCFC103) '
         'um die aktuellen Werte ergänzen, und mit dem ensprechenden Zeistempel '
         'versehen. Aktuelle Reporte stammen aus Vendor Central: https://vendorcentral.amazon.de/analytics/dashboard/searchTerms '
         'Für weitere Hinweise siehe separate Excel Templates. '
         ' '
         'Auswertungsbereich: wöchentlich oder monatlich '
         'Abteilung: Amazon.de')
#%%
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

#########################################################################################################################
# Markenspezifische je Marke untersuchen

    '# Markenspezifische Suchbegriffe'

    col1, col2 = st.columns(2)
    with col1:
        choice1 = st.radio('Wähle eine Henkel Marke',('botclean','Bref','Love Nature','Persil','Perwoll','Pril','Sidolin','Sil','Somat','Spee','Vernel','Weißer Riese','WC Frisch'))
    with col2:
        choice2 = st.radio('Wähle eine Wettbewerbermarke',('Ajax','Ariel','Bissell','Cillit Bang','Coral','Dr. Beckmann','Ecover','Fairy','Finish','Frosch','Lenor','Sagrotan','Vanish','WC Ente'))

    search1 = '\\b(' + choice1 + ')\\b'

    dsi = df.Suchbegriff.str.contains(search1, flags = re.IGNORECASE, regex = True, na = False)
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
    st.line_chart(data=ranking1, x='Periode', y='Suchbegriff 1')

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

    entwicklungppb=entwicklungppb.pivot_table(index='Periode',columns='Produkttitel',values='Klickrate')

    entwicklungppb = entwicklungppb.fillna(0)

    entwicklungppb['Rest']=1-entwicklungppb.sum(numeric_only=True, axis=1)

    '#### Verteilung der TOP 3 geklickten Produkte von Suchbegriff 1'
    st.bar_chart(data=entwicklungppb)

######################

    search2 = '\\b(' + choice2 + ')\\b'

    dsi2 = df.Suchbegriff.str.contains(search2, flags = re.IGNORECASE, regex = True, na = False)
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

    ranking = pd.merge(ranking1, ranking2, on=['Periode'])
    ranking = ranking[['Periode','Suchbegriff 1','Suchbegriff 2']]
    ranking.set_index('Periode')

    '#### Ranking des Suchbegriffs 2'
    st.line_chart(data=ranking2, x='Periode', y='Suchbegriff 2')

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

    entwicklungppb_b=entwicklungppb_b.pivot_table(index='Periode',columns='Produkttitel',values='Klickrate')

    entwicklungppb_b = entwicklungppb_b.fillna(0)

    entwicklungppb_b['Rest']=1-entwicklungppb_b.sum(numeric_only=True, axis=1)

    '#### Verteilung der TOP 3 geklickten Produkte von Suchbegriff 2'
    st.bar_chart(data=entwicklungppb_b)

#########################################################################################################################
# Suchbegriffe im Vergleich

    '#### Ranking der Suchbegriffe 1 und 2 im Vergleich'
    st.line_chart(data=ranking, x='Periode', y=["Suchbegriff 1","Suchbegriff 2"])

#########################################################################################################################
# Suchbegriffe im Vergleich

######### Suchbegriff 1

    '# Suchbegriffe im Vergleich'

    wahl_generisch1=st.text_input('Hier Suchbegriff 1 eintragen')

    df_generisch1= df.loc[(df['Suchbegriff'] == wahl_generisch1)]
    df_generisch1 = df_generisch1.iloc[:, [2,15]]
    df_generisch1.rename(columns={"Suchfrequenz-Rang ": "Suchbegriff 1"},inplace=True)
    df_generisch1['Suchbegriff 1']*= -1

######### Suchbegriff 2

    wahl_generisch2=st.text_input('Hier Suchbegriff 2 eintragen')

    df_generisch2= df.loc[(df['Suchbegriff'] == wahl_generisch2)]
    df_generisch2 = df_generisch2.iloc[:, [2,15]]
    df_generisch2.rename(columns={"Suchfrequenz-Rang ": "Suchbegriff 2"},inplace=True)
    df_generisch2['Suchbegriff 2']*= -1

######### Suchbegriff 1 und 2 im Vergleich
    df_generisch = pd.merge(df_generisch1, df_generisch2, on=['Periode'])
    df_generisch = df_generisch[['Periode','Suchbegriff 1','Suchbegriff 2']]
    df_generisch.set_index('Periode')

    '#### Ranking der Suchbegriffe 1 und 2 im Vergleich'
    st.line_chart(data=df_generisch, x='Periode', y=["Suchbegriff 1","Suchbegriff 2"])
