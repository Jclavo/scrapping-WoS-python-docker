
import pandas as pd
import numpy as np
import time

def filterXlsFile(main_df, log = True):

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

    main_df["Abstract"].fillna("", inplace = True)

    if log :
        print(f'{len(main_df.index)} initial records')

    abstract_source_result = main_df [
        (
            main_df["Abstract"].str.lower().str.contains(sub_main_key_language)
        )
    ]

    if log :
        print(f'{len(abstract_source_result.index)} records filter by abstract')

    source_result = abstract_source_result [
        (
            (
                abstract_source_result["Source Title"].str.lower().str.contains(conferences_key_words) |
                abstract_source_result["Source Title"].str.lower().str.contains(journals_main_key_words_good)
            )
                |
            (
                abstract_source_result["Conference Title"].str.lower().str.contains(conferences_key_words) |
                abstract_source_result["Conference Title"].str.lower().str.contains(journals_main_key_words_good)
            )               
        )
    ]

    if log :
        print(f'{len(source_result.index)} records filter by conferences and papers')

    result = source_result
    result_remainder = pd.concat([abstract_source_result,source_result]).drop_duplicates(keep=False)

    filterFinalResult(result, 'result')
    filterFinalResult(result_remainder, 'result_remainder')


def filterFinalResult(result, fileName):

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

    print(f'> {len(result_DF.index)} {fileName} records')

    result_DF = result_DF[columns]
    result_DF.to_excel(f'/app/code/data/output/{fileName}_{round(time.time() * 1000)}.xls')


def main():

    search_by_TI_DF = pd.read_excel("/app/code/data/search_by_TI.xls")
    
    search_by_AB_DF_I = pd.read_excel("/app/code/data/search_by_AB_I.xls")
    search_by_AB_DF_II = pd.read_excel("/app/code/data/search_by_AB_II.xls")
    search_by_AB_DF = pd.concat([search_by_AB_DF_I, search_by_AB_DF_II], ignore_index=True)

    result_DF = pd.concat([search_by_TI_DF, search_by_AB_DF], ignore_index=True)

    result_DF = result_DF.drop_duplicates(subset=['UT (Unique WOS ID)']).applymap(lambda s:s.lower() if type(s) == str else s)

    result_DF = filterXlsFile(result_DF)

if __name__ == "__main__":
    main()

