import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from utils.models import ClustersHeatmap, ClustersSectors, ClustersDesc
import pandas as pd

load_dotenv()

DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_NAME = os.getenv('POSTGRES_DB')
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def load_clusters_desc():
    query = select(ClustersDesc)

    with SessionLocal() as session:
        result = session.scalars(query).all()

        clust_desc = pd.DataFrame([
                {"ticker": r.ticker,
                 "mean_return": r.mean_return,
                 "volatility": r.volatility,
                 "mean_value": r.mean_value,
                 "mean_value_log": r.mean_value_log,
                 "cluster": r.cluster,
                 "pca1": r.pca1,
                 "pca2": r.pca2,
                 "return_scaled": r.return_scaled,
                 "volatility_scaled": r.volatility_scaled,
                 "liquidity_scaled": r.liquidity_scaled,
                 "isin": r.isin,
                 "sector": r.sector,
                 "description": r.description
                 }
        for r in result
        ])
        return clust_desc
    
def load_clusters_heatmap():
    query = select(ClustersHeatmap)

    with SessionLocal() as session:
        result = session.scalars(query).all()

        clust_heatmap = pd.DataFrame([
                {"cluster": r.cluster,
                 "mean_return": r.mean_return,
                 "volatility": r.volatility,
                 "mean_value_log": r.mean_value_log
                 }
        for r in result
        ])
        return clust_heatmap
    
def load_clusters_sectors():
    query = select(ClustersSectors)

    with SessionLocal() as session:
        result = session.scalars(query).all()

        clust_sectors = pd.DataFrame([
                {"id": r.id,
                 "sector": r.sector,
                 "cluster": r.cluster,
                 "count": r.count
                 }
        for r in result
        ])
        return clust_sectors
