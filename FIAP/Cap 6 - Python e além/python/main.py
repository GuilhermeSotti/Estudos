# main.py
import argparse
import pandas as pd

from ingestion.faostat_ingest import ingest_faostat
from ingestion.comexstat_ingest import ingest_comexstat
from ingestion.utils import get_engine

from preprocessing.clean_data import drop_missing, fill_defaults
from preprocessing.transform_data import normalize_numeric, encode_categorical

from modeling.yield_prediction import train_yield_model
from modeling.harvest_loss import train_harvest_loss

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2023)
    parser.add_argument("--faostat_ds", type=str, default="QCL")
    args = parser.parse_args()

    # Processa FAOSTAT → stg_insumos
    df_fao = ingest_faostat(args.faostat_ds, args.year)
    process_and_train(df_fao, 'stg_insumos')

    # Processa COMEXSTAT → stg_producao
    # = ingest_comexstat("1006", args.year, flow="Export")
    #process_and_train(df_comex, 'stg_producao')

def process_and_train(df: pd.DataFrame, stg_table: str):
    """
    Seleciona/renomeia colunas conforme tabela de destino,
    aplica limpeza, normalização, encoding e grava no SQL.
    """
    if stg_table == 'stg_insumos':
        df = (
            df
            .rename(columns={
                'Domain':  'cultura',
                'Area':    'pais',
                'Value':   'quantidade',
                'Unit':    'unidade',
                'Year':    'ano'
            })
            [['cultura', 'pais', 'quantidade', 'unidade', 'ano']]
        )
    else:
        df = (
            df
            .rename(columns={
                'Area':       'produtor',
                'Item':       'cultura',
                'Value':      'producao_t',
                'Year':       'ano'
            })
            [['produtor', 'cultura', 'producao_t', 'ano']]
        )

    df = drop_missing(df, thresh=0.8)
    df = fill_defaults(df, defaults={'quantidade': 0, 'producao_t': 0})

    num_cols = df.select_dtypes(include='number').columns.tolist()
    df = normalize_numeric(df, cols=num_cols)
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    df = encode_categorical(df, cols=cat_cols)

    engine = get_engine()
    df.to_sql(
        name=stg_table,
        con=engine,
        schema='staging',
        if_exists='append',
        index=False
    ) 

    df_stage = pd.read_sql_table(stg_table, con=engine, schema='staging')

    train_yield_model(
        df_stage,
        features=['quantidade'] if stg_table=='stg_insumos' else ['producao_t'],
        target='yield' if stg_table=='stg_insumos' else 'producao_t',
        out_path=f"artefacts/{stg_table}_yield_model.pkl"
    )
    train_harvest_loss(
        df_stage,
        features=['quantidade'] if stg_table=='stg_insumos' else ['producao_t'],
        target='loss_flag',
        out_path=f"artefacts/{stg_table}_loss_model.pkl"
    )

if __name__ == "__main__":
    main()
