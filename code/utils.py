import re
import pandas as pd
import efaqa_corpus_zh

def divide_20k_chats_into_small_files():
    df_label = pd.read_csv('../data/label.csv', sep='\t', dtype=str)
    id_name = {id:f"{id}_{str(eng).lower().replace(' ','_')}" for id, eng in zip(df_label.id, df_label.english)}
    print(id_name)

    data = list(efaqa_corpus_zh.load())

    out = []
    for m in data:
        ti = m['title'].strip()
        following_from_self = ' // '.join([o['value'].strip().replace('\n', ' ') for o in m['chats'] if o['sender']=='owner'])
        following_from_others = ' // '.join([o['value'].strip().replace('\n', ' ') for o in m['chats'] if o['sender']!='owner'])
        ti = re.sub(r'\s+', '、', ti)
        following_from_self = re.sub(r'\s+', '、', following_from_self)
        following_from_others = re.sub(r'\s+', '、', following_from_others)

        s1 = m['label']['s1']
        s2 = m['label']['s2']

        out.append({'s1':s1, 'reviewed':'', 'beginning_description':ti, 'following_from_self': following_from_self, 'following_from_others': following_from_others })
    
    df_out = pd.DataFrame(out)
    df_out.sort_values('s1')

    print(df_out.s1.value_counts())
    print(df_out.iloc[0])

    folder_out = "../data"
    s1_wanted = '1.19 1.3'.split()
    #s1_wanted = '1.19'.split()
    s1_wanted = '1.1 1.2 1.4 1.5 1.6 1.7 1.8 1.9 1.10'.split()
    s1_wanted = '1.11 1.12 1.13 1.14 1.15 1.16 1.17 1.18'.split()
    for s1 in s1_wanted:
        df_ = df_out[df_out.s1 == s1]
        s1_name = id_name[s1]
        
        #if len(df_) < 500:
        if len(df_) < 550:
            fpath_out = f'{folder_out}/{s1_name}.xlsx'
            df_.to_excel(fpath_out, index=False, encoding="utf-8")
        else:
            for i in range(0, len(df_), 500):
                df__ = df_[i:(i+500)]
                fpath_out = f'{folder_out}/{s1_name}__{i}.xlsx'
                df__.to_excel(fpath_out, index=False, encoding="utf-8")



def main():
    divide_20k_chats_into_small_files()

if __name__ == '__main__':
    main()
