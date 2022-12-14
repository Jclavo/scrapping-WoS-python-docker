
import pandas as pd
import numpy as np
import time

def filterXlsFile(filePath, log = False):

    df = pd.read_excel(filePath)

    #print(f'{filePath} > {len(df.index)} initial records')

    main_key_words_good = [
    "taint analysis",
    "tainted analysis",
    "information flow",
    "information-flow",
    "data flow",
    "data-flow"
    ]
    main_key_words_good = '|'.join(main_key_words_good)

    sub_main_key_language = [
        "java",
        "android"
    ]
    sub_main_key_language = '|'.join(sub_main_key_language)

    sub_main_key_taint = [
        "taint",
        "tainted"
    ]
    sub_main_key_taint = '|'.join(sub_main_key_taint)

    conferences_key_words = [
        "conference on programming language design and implementation", "PLDI",
        "symposium on principles of programming languages", "POPL",
        "conference on object oriented programming systems languages and applications", "OOPSLA",
        "european conference on object-oriented programming", "ECOOP",
        "european symposium on programming", "ESOP",
        "automated software engineering conference", "ASE",
        "european software engineering conference", "ESEC",
        "symposium on the foundations of software engineering", "FSE",
        "international conference on software engineering", "ICSE",
        "virtual reality software and technology", "VRST",
        "foundations of software science and computational structures", "FOSSACS",
        "international conference on evaluation and assessment in software engineering", "EASE",
        "international conference on software testing, verification and validation", "ICST",
        "international symposium on empirical software engineering and measurement", "ESEM",
        "international symposium on software reliability engineering", "ISSRE",
        "international symposium on software testing and analysis", "ISSTA",
        "symposium on software reusability", "SSR",
        "international conference on software analysis, evolution and reengineering", "SANER",
        "conference on computer and communications security", "CCS",
        "symposium on security and privacy", "SP",
        "usenix security symposium", "USENIX-Security",
        "asia conference on information, computer and communications security", "AsiaCCS",
        "computer security foundations symposium", "CSF",
        "european symposium on research in computer security", "ESORICS",
        "computer security foundations workshop", "CSFW",
        "international symposium on software reliability engineering", "ISSRE"
    ]
    conferences_key_words = '|'.join(conferences_key_words)


    journals_main_key_words_good = [
        "transactions on programming languages and systems",
        "science of computer programming",
        "transactions on software engineering",
        "journal of systems and software",
        "information and software technology",
        "transactions on privacy and security",
        "transactions on information and system security",
        "automated software engineering",
        "transactions on software engineering and methodology"
    ]
    journals_main_key_words_good = '|'.join(journals_main_key_words_good)

    main_result = df [
            (
                (
                    df["Article Title"].str.lower().str.contains(main_key_words_good)
                )
            ) 
                | 
            (
                (
                    df["Abstract"].str.lower().str.contains(main_key_words_good)
                ) 
                    &
                (
                    (
                        df["Abstract"].str.lower().str.contains("static")
                    )
                        &
                    (
                        df["Abstract"].str.lower().str.contains(sub_main_key_taint)
                    )
                        &
                    (
                        df["Abstract"].str.lower().str.contains(sub_main_key_language)
                    )
                )
            )
        ]
    
    if log :
        print('main_result', len(main_result.index))

    source_result = df [
            (
                (
                    df["Source Title"].str.lower().str.contains(conferences_key_words) |
                    df["Source Title"].str.lower().str.contains(journals_main_key_words_good)
                )
                |
                (
                    df["Conference Title"].str.lower().str.contains(conferences_key_words) |
                    df["Conference Title"].str.lower().str.contains(journals_main_key_words_good)
                )               
            )
        ]
    
    if log :
        print('source_result', len(source_result.index))

    result = pd.merge(main_result, source_result)
    print(f'{filePath} > {len(result.index)} records')
    return result

def filterFinalResult(result):

    result_DF = pd.DataFrame(result).drop_duplicates(subset=['UT (Unique WOS ID)']).applymap(lambda s:s.lower() if type(s) == str else s)

    columns = [
        'Article Title',
        'Abstract',
        'Publication Type',
        'Source Title',
        'Document Type',
        'Conference Title',
        'Conference Location',
        'Times Cited, All Databases',
        'Publication Year',
        'UT (Unique WOS ID)',
    ]

    return result_DF[columns]


def main():

    search_by_TI_DF = filterXlsFile("/app/code/data/search_by_TI.xls")
    
    # search_by_AB_DF_I = filterXlsFile("/app/code/data/search_by_AB_I.xls")
    # search_by_AB_DF_II = filterXlsFile("/app/code/data/search_by_AB_II.xls")
    # search_by_AB_DF = pd.concat([search_by_AB_DF_I, search_by_AB_DF_II])
    search_by_AB_DF = filterXlsFile("/app/code/data/search_by_AB.xls")

    result_DF = pd.concat([search_by_TI_DF, search_by_AB_DF])

    result_DF = filterFinalResult(result_DF)

    print(f'> {len(result_DF.index)} records')

    result_DF.to_excel(f'/app/code/data/output/result_{round(time.time() * 1000)}.xls')

if __name__ == "__main__":
    main()

