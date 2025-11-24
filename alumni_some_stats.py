#open an excel file 
import pandas as pd
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
df_esse3 = pd.read_excel('2025.09.01-ESSE3.xlsx')
df_iscritti = pd.read_excel('2025.10.01-ISCRITTI.xlsx')
#print the number of rows in the excel file
print("Studenti laureati che hanno risposto al questionario:", len(df_esse3))
#create a subsample of all the entries where the value in the column "Cognome" starts with the letter "B"
df_esse3_privacy_yes = df_esse3[df_esse3['ANA_PRIVACY'].str.startswith('SI')]
print(f"Studenti che YES hanno dato il consenso ad essere contattati da ALUMNI: {len(df_esse3_privacy_yes)} ({len(df_esse3_privacy_yes)/len(df_esse3)*100:.1f}%)")
df_esse3_privacy_no = df_esse3[df_esse3['ANA_PRIVACY'].str.startswith('NO')]
print(f"Studenti che NON hanno dato il consenso ad essere contattati da ALUMNI: {len(df_esse3_privacy_no)} ({len(df_esse3_privacy_no)/len(df_esse3)*100:.1f}%)")
# Create a subsample of df_esse3_privacy_yes for the students that answered YES to the questionaire
df_esse3_contact_si = df_esse3_privacy_yes[df_esse3_privacy_yes['RISP_DES'].str.startswith('S')]
df_esse3_contact_no = df_esse3_privacy_yes[df_esse3_privacy_yes['RISP_DES'].str.startswith('N')]

print(f"Studenti che NON vogliono iscriversi: {len(df_esse3_contact_no)} ({len(df_esse3_contact_no)/len(df_esse3_privacy_yes)*100:.1f}%)")
print(f"Studenti che YES vogliono iscriversi: {len(df_esse3_contact_si)} ({len(df_esse3_contact_si)/len(df_esse3_privacy_yes)*100:.1f}%)")

# Create a dataframe with students who want to enroll AND are already registered
df_already_registered = df_esse3_contact_si[df_esse3_contact_si['COD_FIS'].isin(df_iscritti['INA_CF'])]
print(f"Studenti che vogliono iscriversi e sono già iscritti: {len(df_already_registered)} ({len(df_already_registered)/len(df_esse3_contact_si)*100:.1f}%)")
   
# Create a dataframe with students who want to enroll AND are NOT already registered
df_not_registered = df_esse3_contact_si[~df_esse3_contact_si['COD_FIS'].isin(df_iscritti['INA_CF'])]
print(f"Studenti che vogliono iscriversi e NON sono ancora iscritti: {len(df_not_registered)} ({len(df_not_registered)/len(df_esse3_contact_si)*100:.1f}%)")

#Print the following values for the are already registered students (COGNOME, NOME, EMAIL, COD_FIS)
print("\nStudenti che vogliono iscriversi e sono già iscritti:")
for index, row in df_already_registered.iterrows():
    cognome = row['COGNOME']
    if len(cognome) <= 3:
        masked_cognome = cognome[0] + '*' * (len(cognome) - 1)
    else:
        masked_cognome = cognome[:3] + '*' * (len(cognome) - 3)
    
    nome = row['NOME']
    if len(nome) <= 3:
        masked_nome = nome[0] + '*' * (len(nome) - 1)
    else:
        masked_nome = nome[:3] + '*' * (len(nome) - 3)
    
    cod_fis = row['COD_FIS']
    if len(cod_fis) <= 8:
        masked_cod_fis = cod_fis[0] + '*' * (len(cod_fis) - 1)
    else:
        masked_cod_fis = cod_fis[:8] + '*' * (len(cod_fis) - 8)
    
    print(f"{masked_cognome}, {masked_nome}, {masked_cod_fis}")

#Save the following values for the NOT registered students to a file (COGNOME, NOME, EMAIL, COD_FIS)
with open('da_contattare.txt', 'w', encoding='utf-8') as f:
    f.write("Studenti che vogliono iscriversi e NON sono ancora iscritti:\n")
    for index, row in df_not_registered.iterrows():
        cognome = row['COGNOME']
        if len(cognome) <= 3:
            masked_cognome = cognome[0] + '*' * (len(cognome) - 1)
        else:
            masked_cognome = cognome[:3] + '*' * (len(cognome) - 3)
        
        nome = row['NOME']
        if len(nome) <= 3:
            masked_nome = nome[0] + '*' * (len(nome) - 1)
        else:
            masked_nome = nome[:3] + '*' * (len(nome) - 3)
        
        cod_fis = row['COD_FIS']
        if len(cod_fis) <= 8:
            masked_cod_fis = cod_fis[0] + '*' * (len(cod_fis) - 1)
        else:
            masked_cod_fis = cod_fis[:8] + '*' * (len(cod_fis) - 8)

        email = row['EMAIL']

        f.write(f"{masked_cognome}, {masked_nome}, {masked_cod_fis}, {email}\n")

print(f"\nLista salvata in 'da_contattare.txt' ({len(df_not_registered)} studenti)")
