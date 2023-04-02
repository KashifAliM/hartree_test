import os
import pandas

from helpers import common


def load_data_from_csv(file_name: str) -> pandas.DataFrame:
    """Take the csv file as input and load data into pandas data frame"""
    ret_dataset = pandas.read_csv(
        file_name,
        skiprows=0,
        low_memory=False,
    )
    return ret_dataset


def prepare_data(
    df_dataset1: pandas.DataFrame, df_dataset2: pandas.DataFrame
) -> pandas.DataFrame:
    """Take the data sets (in pandas DataFrame) and prepare the final dataframe to use for processing"""

    ret_dataframe = pandas.merge(
        df_dataset1, df_dataset2, how="left", on="counter_party"
    )
    # change the data format
    ret_dataframe = pandas.pivot_table(
        ret_dataframe,
        values="value",
        index=["legal_entity", "counter_party", "tier", "rating"],
        columns=["status"],
        aggfunc="sum",
    ).reset_index()

    return ret_dataframe


def aggregate_data(df_dataset, groupby_cols, agg_dict) -> pandas.DataFrame:
    """Aggregate the data based on the provided parameters"""

    ret_df_dataset = (
        df_dataset.groupby(groupby_cols).agg(agg_dict).reset_index()
    )

    return ret_df_dataset


def prepare_output_data(
    df_dataset: pandas.DataFrame, dict_rename_col: dict
) -> pandas.DataFrame:
    """Take the data set and rename the columns"""
    df_dataset.rename(columns=dict_rename_col, inplace=True)

    return df_dataset


def save_to_csf_file(file_name: str, df_data: pandas.DataFrame):
    try:
        df_data.to_csv(file_name, index=False)
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    # Load the data from CSV files
    df_dataset1 = load_data_from_csv(
        os.path.join(common.get_root_dir(), r"input_data", r"dataset1.csv")
    )
    df_dataset2 = load_data_from_csv(
        os.path.join(common.get_root_dir(), r"input_data", r"dataset2.csv")
    )

    # Prepare the the data before processing
    df_for_precessing = prepare_data(
        df_dataset1=df_dataset1, df_dataset2=df_dataset2
    )

    # process the data
    """
        Pipe 1 >>> Calculation
        1- Maximum rating by counter_party
        2. Sum of ARAP and ACCR 
    """
    df_for_precessing = aggregate_data(
        df_for_precessing,
        ["legal_entity", "counter_party", "tier"],
        {"rating": "max", "ACCR": "sum", "ARAP": "sum"},
    )

    """
        Pipe 2 >>> Calculation based on grouping by [legal entity]
    """
    df_grp_legal_entity = aggregate_data(
        df_for_precessing,
        ["legal_entity"],
        {
            "counter_party": "count",
            "tier": "count",
            "rating": "max",
            "ACCR": "sum",
            "ARAP": "sum",
        },
    )

    """
        Pipe 3 >>> Calculation based on grouping by [legal entity , counter_party]
    """
    df_grp_legal_entity_and_counter_party = aggregate_data(
        df_for_precessing,
        ["legal_entity", "counter_party"],
        {"tier": "count", "rating": "max", "ACCR": "sum", "ARAP": "sum"},
    )

    """
        Pipe 4 >>> Calculation based on grouping by [tier]
    """
    df_grp_tier = aggregate_data(
        df_for_precessing,
        ["tier"],
        {
            "legal_entity": "count",
            "counter_party": "count",
            "rating": "max",
            "ACCR": "sum",
            "ARAP": "sum",
        },
    )

    """
        concatinate all data sets
    """
    df_final = pandas.concat(
        [
            df_for_precessing,
            df_grp_legal_entity,
            df_grp_legal_entity_and_counter_party,
            df_grp_tier,
        ]
    )

    """
        Prepare the data for output
    """
    df_output = prepare_output_data(
        df_final,
        {
            "rating": "max_rating_by_counterparty",
            "ARAP": "sum_arap",
            "ACCR": "sum_accr",
        },
    )

    """
        Save the data into a csv file
    """
    save_to_csf_file(
        file_name=os.path.join(
            common.get_root_dir(), r"output_data", r"result.csv"
        ),
        df_data=df_output,
    )
