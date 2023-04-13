import pandas as pd

df = pd.read_csv('./domain_text.csv')
with open('./domain_list.txt', 'r', encoding='utf-8') as f:
    domain_list = f.readlines()
domain_list = [x.strip() for x in domain_list]

domain_in_df = df.domain.to_list()
for domain in domain_list:
    if domain not in domain_in_df:
        df.loc[len(df)] = {
            "domain": domain,
            "text": None
        }

df.to_csv('./text.csv', index = False)