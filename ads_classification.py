from google.cloud import language_v1
from google.oauth2 import service_account
import os
import pandas as pd

os.environ["http_proxy"] = "http://127.0.0.1:10809"
os.environ["https_proxy"] = "http://127.0.0.1:10809"


def my_classify_text(client, text_content):
    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT
    document = {"content": text_content, "type_": type_}
    content_categories_version = (
        language_v1.ClassificationModelOptions.V2Model.ContentCategoriesVersion.V2
    )
    response = client.classify_text(
        request={
            "document": document,
            "classification_model_options": {
                "v2_model": {"content_categories_version": content_categories_version}
            },
        }
    )

    for category in response.categories:
        print("Category name: {}".format(category.name))
        print("Confidence: {}".format(category.confidence))

    return response


if __name__ == '__main__':
    credentials = service_account.Credentials.from_service_account_file('./key/numeric-haven-254117-83c7437851af.json')
    client = language_v1.LanguageServiceClient(credentials=credentials)
    df = pd.read_csv('text.csv')
    df = df.reindex(columns=df.columns.to_list() + ['results'])
    for i in range(len(df)):
        print("Processing {0} :".format(df.loc[i, 'domain']))
        text_content = df.loc[i, 'text']
        if text_content == text_content:
            response = my_classify_text(client=client, text_content=text_content)
            df.loc[i, 'results'] = response
        print('---')
    df.to_csv('domain_with_category.csv', index=False)
