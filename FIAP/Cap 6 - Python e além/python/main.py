import os
import argparse
import pandas as pd
import subprocess
from ingestion.faostat_ingest import ingest_faostat
from ingestion.comexstat_ingest import ingest_comexstat
from ingestion.utils import get_engine
from preprocessing.clean_data import drop_missing, fill_defaults
from preprocessing.transform_data import normalize_numeric
from modeling.yield_prediction import train_yield_model
from modeling.harvest_loss import train_harvest_loss

def process_and_train(df: pd.DataFrame, stg_table: str):    
    rename_map = {
        'stg_insumos': {
            'Domain': 'cultura',
            'Area': 'pais',
            'Value': 'quantidade',
            'Unit': 'unidade',
            'Year': 'ano'
        },
        'stg_producao': {
            'coSITCBasicHeading': 'codigo_categoria_basica',
            'SITCBasicHeading': 'categoria_basica',
            'coSITCSubGroup': 'codigo_subgrupo',
            'SITCSubGroup': 'subgrupo',
            'coSITCGroup': 'codigo_grupo',
            'SITCGroup': 'grupo',
            'coSITCDivision': 'codigo_divisao',
            'SITCDivision': 'divisao',
            'coSITCSection': 'codigo_secao',
            'SITCSection': 'secao'
        }
    }

    selected_cols = {
        'stg_insumos': ['cultura', 'pais', 'quantidade', 'unidade', 'ano'],
        'stg_producao': [
            'codigo_categoria_basica', 'categoria_basica', 'codigo_subgrupo',
            'subgrupo', 'codigo_grupo', 'grupo', 'codigo_divisao', 'divisao',
            'codigo_secao', 'secao'
        ]
    }

    features_map = {
        'stg_insumos': ['quantidade'],
        'stg_producao': ['codigo_divisao']
    }

    target_map = {
        'stg_insumos': 'quantidade',
        'stg_producao': 'codigo_secao'
    }

    df = df.rename(columns=rename_map[stg_table])[selected_cols[stg_table]]
    df = drop_missing(df, thresh=0.8)
    df = fill_defaults(df, defaults={'quantidade': 0, 'codigo_secao': 0})

    num_cols = df.select_dtypes(include='number').columns.tolist()
    df = normalize_numeric(df, cols=num_cols)

    engine = get_engine()
    df.to_sql(stg_table, con=engine, schema='staging', if_exists='append', index=False, chunksize=1000)

    df_stage = pd.read_sql_table(stg_table, con=engine, schema='staging')

    features = features_map[stg_table]
    target = target_map[stg_table]

    train_yield_model(df_stage, features=features, target=target, out_path=f"artefacts/{stg_table}_yield_model.pkl")

    if stg_table == 'stg_insumos':
        col = features[0]
        df_stage[col] = pd.to_numeric(df_stage[col], errors='coerce')
        median_loss = df_stage[col].median()
        df_stage['loss_flag'] = (df_stage[col] > median_loss).astype(int)

        train_harvest_loss(df_stage, features=features, target='loss_flag', out_path=f"artefacts/{stg_table}_loss_model.pkl")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2023)
    parser.add_argument("--faostat_ds", type=str, default="QCL")
    args = parser.parse_args()

    os.makedirs('artefacts', exist_ok=True)

    process_and_train(ingest_faostat(args.faostat_ds, args.year), 'stg_insumos')
    process_and_train(ingest_comexstat("1006", args.year, flow="Export"), 'stg_producao')

if __name__ == "__main__":
    main()
