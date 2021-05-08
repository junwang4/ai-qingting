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
        following = ' // '.join([o['value'].strip().replace('\n', ' ') for o in m['chats'] if o['sender']=='owner'])
        s1 = m['label']['s1']
        s2 = m['label']['s2']
        out.append({'s1':s1, 'title':ti, 'following': following })
    
    df_out = pd.DataFrame(out)
    df_out.sort_values('s1')

    print(df_out.s1.value_counts())
    #print(df_out.head())
    #print(df_out.tail())

    folder_out = "../data"
    for s1 in '1.19 1.3'.split():
        df_ = df_out[df_out.s1 == s1]
        s1_name = id_name[s1]
        if len(df_) < 500:
            fpath_out = f'{folder_out}/{s1_name}.csv'
            df_.to_csv(fpath_out, index=False)
        else:
            for i in range(0, len(df_), 500):
                df__ = df_[i:(i+500)]
                fpath_out = f'{folder_out}/{s1_name}__{i}.csv'
                df__.to_csv(fpath_out, index=False)



def main():
    divide_20k_chats_into_small_files()

if __name__ == '__main__':
    main()
