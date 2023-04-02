import os
from helpers import common
import apache_beam as beam

def start_processing():
    
    with beam.Pipeline() as pipeline:  # DataflowRunner(), InteractiveRunner()
        # Read data from csv files.
        df_dataset1 = pipeline | "Read Dataset1" >> beam.dataframe.io.read_csv(
            os.path.join(common.get_root_dir(), r"input_data", r"dataset1.csv")
        )
        df_dataset2 = pipeline | "Read Dataset2" >> beam.dataframe.io.read_csv(
            os.path.join(common.get_root_dir(), r"input_data", r"dataset2.csv")
        )

        # Prepare the dataset before processing
        df_for_processing = (
            pipeline
            | "Merge Datasets"
            >> df_dataset1.merge(
                df_dataset2.set_index("counter_party").counter_party,
                right_index=True,
                left_on="counter_party",
                how="left",
            )
            | "Pivot the status column"
            >> beam.Map(
                print
            )  # beam.Map() is just a place holder, it woulkd be replace with a method to pivot the meged dataset based on the status ARAP, ACCR
        )

        # Apply the aggregate function
        df_aggregated = (
            df_for_processing.groupby(
                ["legal_entity", "counter_party", "tier"]
            )
            .agg({"rating": "max", "ACCR": "sum", "ARAP": "sum"})
            .reset_index()
        )
        df_grp_legal_entity = (
            df_aggregated.groupby(["legal_entity"])
            .agg(
                {
                    "counter_party": "count",
                    "tier": "count",
                    "rating": "max",
                    "ACCR": "sum",
                    "ARAP": "sum",
                }
            )
            .reset_index()
        )
        df_grp_legal_entity_and_counter_party = (
            df_aggregated.groupby(["legal_entity", "counter_party"])
            .agg(
                {
                    "tier": "count",
                    "rating": "max",
                    "ACCR": "sum",
                    "ARAP": "sum",
                }
            )
            .reset_index()
        )
        df_grp_tier = (
            df_aggregated.groupby(["tier"])
            .agg(
                {
                    "legal_entity": "count",
                    "counter_party": "count",
                    "rating": "max",
                    "ACCR": "sum",
                    "ARAP": "sum",
                }
            )
            .reset_index()
        )

        # concatinate all the above datasets
        df_aggregated = pipeline | df_aggregated.append(df_grp_legal_entity, ignore_index=True)
        df_aggregated = pipeline | df_aggregated(df_grp_legal_entity_and_counter_party, ignore_index=True)
        df_aggregated = pipeline | df_aggregated(df_grp_tier, ignore_index=True)

        # store the final dataset into a csv file
        df_aggregated.to_csv(
            os.path.join(
                common.get_root_dir(), r"output_data", r"result_usingab.csv"
            )
        )


if __name__ == "__main__":
    start_processing()
