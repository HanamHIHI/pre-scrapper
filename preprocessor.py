import pandas as pd

for index, _cat2 in enumerate(["A0302"]):
    df_surfing = pd.read_csv("hanam_restaurant_real_url.csv", encoding='cp949')

    def contains_review(row):
        try:
            if("review" in row):
                return True
            else:
                return False
        except:
            return False
        
    df_surfing["contains_review"] = df_surfing["naverURL"].apply(contains_review)
    cond_nonreview = df_surfing["contains_review"] == False

    df_surfing[~cond_nonreview].to_csv("preprocessed_urls_hanam_restaurant_real_url_position.csv", encoding='utf-8')
