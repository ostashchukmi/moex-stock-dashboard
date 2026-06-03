from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class ClustersDesc(Base):
    __tablename__ = "clusters_desc"

    ticker: Mapped[str] = mapped_column(String, primary_key=True)
    mean_return: Mapped[float | None] = mapped_column(Float, nullable=True)
    volatility: Mapped[float | None] = mapped_column(Float, nullable=True)
    mean_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    mean_value_log: Mapped[float | None] = mapped_column(Float, nullable=True)
    cluster: Mapped[int] = mapped_column(Integer)
    pca1: Mapped[float | None] = mapped_column(Float, nullable=True)
    pca2: Mapped[float | None] = mapped_column(Float, nullable=True)
    return_scaled: Mapped[float | None] = mapped_column(Float, nullable=True)
    volatility_scaled: Mapped[float | None] = mapped_column(Float, nullable=True)
    liquidity_scaled: Mapped[float | None] = mapped_column(Float, nullable=True)
    isin: Mapped[str | None] = mapped_column(String, nullable=True)
    sector: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class ClustersHeatmap(Base):
    __tablename__ = "clusters_heatmap"

    cluster: Mapped[int] = mapped_column(Integer, primary_key=True)
    mean_return: Mapped[float | None] = mapped_column(Float, nullable=True)
    volatility: Mapped[float | None] = mapped_column(Float, nullable=True)
    mean_value_log: Mapped[float | None] = mapped_column(Float, nullable=True)


class ClustersSectors(Base):
    __tablename__ = "clusters_sectors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sector: Mapped[str | None] = mapped_column(String, nullable=True)
    cluster: Mapped[int | None] = mapped_column(Integer, nullable=True)
    count: Mapped[int | None] = mapped_column(Integer, nullable=True)
