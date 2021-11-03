import numpy as np
import pandas as pd
# look up smiles in csv and put all of those descriptors into
# takes a list of actives and inactives and generates and appends chemical attributes to
df_attributes = pd.read_csv('./dsets/rdkit.csv')

#takes in an identifier(aeid or name) for the assay and returns 2 data frames for each active and inactive chemicals
def query_toxcast(assay_identifier : str):
    df = pd.read_csv('./dsets/toxcast.csv')
    id = ''
    if(assay_identifier.isdigit()):
        id = 'ASSAY_ID'
    else:
        id = 'ASSAY_NAME'
    df = df[[id, 'SMILES', 'HIT_CALL']]

    df_active = df.where(df['HIT_CALL'] == 1).dropna()
    df_inactive = df.where(df['HIT_CALL'] == 0).dropna()

    return df_active, df_inactive


# produces attributes for a smiles string
def produce_attributes(sm: str):
    return ((df_attributes.where(df_attributes['SMILES']==sm).dropna(how='all').iloc[0:,1:209]).values.tolist())[0]

# takes in a list of file names for which we need to generate chemical attributes for
def generate(curr_df: pd.DataFrame, filename: str):
    # open each file in the list to generate attributes
    deliverable = pd.DataFrame()
    for sm in curr_df['SMILES']:
        print('Sending: %s' %sm )
        chem_desc = produce_attributes(sm)
        deliverable = deliverable.append(pd.Series(chem_desc), ignore_index = True)
        result = pd.concat([curr_df, deliverable], axis=1)
    try:
        result.to_csv('./new_%s.csv' %filename)
        print('./assays/new_%s.csv was created' %filename)
    except:
        print('./assays/new_%s.csv has already been created' %filename)


def send_to_csv(fileName: str, df: pd.DataFrame):
    df.to_csv('./%s' %fileName)
    print('%s has been created' %fileName)

#general flow which we put assays into
def assay_workflow(assay_identifier: str):
    df_active, df_inactive = query_toxcast(assay_identifier)
    generate(df_active, assay_identifier)

#generate the csvs by inputting assays
assay = input('Input assay: ')
assay_workflow(assay)