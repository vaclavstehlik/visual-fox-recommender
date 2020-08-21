import argparse
import json
from models import dataset_analysis_result as da
import numpy as np
import pandas as pd


def main(path):
    df = pd.read_csv(path)

    # Analyze dataset
    dataset_analysis = da.DatasetAnalysisResult()
    df = remove_id_column(df)

    dataset_analysis.numeric = test_numerical_data(df)
    dataset_analysis.categoric = test_categorical_data(df)
    dataset_analysis.mixed_categoric_numeric = test_mixed_num_cat(df)
    dataset_analysis.geospatial = test_geo_coordinates(df)
    dataset_analysis.temporal = test_temporal_data(df)
    dataset_analysis.one_ts = test_one_time_series(df)
    dataset_analysis.multiple_ts = test_multiple_time_series(df)
    dataset_analysis.negative_values = test_negative_values(df)

    # Response
    response = {
        "Features": {
            "numeric": dataset_analysis.numeric,
            "categoric": dataset_analysis.categoric,
            "mixed_categoric_numeric": dataset_analysis.mixed_categoric_numeric,
            "geospatial": dataset_analysis.geospatial,
            "temporal": dataset_analysis.temporal,
            "one_ts": dataset_analysis.one_ts,
            "multiple_ts": dataset_analysis.multiple_ts,
            "negative_values": dataset_analysis.negative_values
        }
    }

    return response


def remove_id_column(df):
    id_names = ["id", "_id," "guid", "_guid"]
    return df.loc[:, ~df.columns.isin(id_names)]


def test_negative_values(df):
    if True in (df.select_dtypes(include=[np.number]) < 0).any():
        return True
    else:
        return False


def test_numerical_data(df):
    if len((df.select_dtypes(include=np.number)).columns) > 0:
        return True
    else:
        return False


def test_categorical_data(df):
    if len((df.select_dtypes(include=["number", "bool_", "object_"])).columns) > 0:
        return True
    else:
        return False


def test_mixed_num_cat(df):
    if test_numerical_data(df) and test_categorical_data(df):
        return True
    else:
        return False


def test_temporal_data(df):
    if get_time_series_count(df) > 0:
        return True
    else:
        return False


def test_one_time_series(df):
    if get_time_series_count(df) == 1:
        return True
    else:
        return False


def test_multiple_time_series(df):
    if get_time_series_count(df) > 1:
        return True
    else:
        return False


def get_time_series_count(df):
    return len((df.select_dtypes(include=["datetime64", "timedelta"])).columns)


def test_geo_coordinates(df):
    latitude_names = ["lat", "Lat", "latitude", "Longitude"]
    longitude_names = ["long", "Long", "longitude", "Longitude"]

    latitude_columns = (df.loc[:, df.columns.isin(latitude_names)]).columns
    longitude_columns = (df.loc[:, df.columns.isin(longitude_names)]).columns

    if len(latitude_columns) > 0 and len(longitude_columns) > 0:
        return True
    else:
        return False


if __name__ == '__main__':
    main()
