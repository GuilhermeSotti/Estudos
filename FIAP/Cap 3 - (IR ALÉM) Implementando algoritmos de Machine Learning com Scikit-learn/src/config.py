import yaml
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class PreprocessingConfig:
    outlier_strategy: str
    outlier_method: Optional[str] = None
    outlier_iqr_factor: Optional[float] = None
    outlier_contamination: Optional[float] = None
    impute_strategy: Optional[str] = None

@dataclass
class DataConfig:
    raw_path: str
    processed_dir: str
    test_size: float
    random_state: int
    stratify: bool

@dataclass
class FeaturesConfig:
    use_compactness: bool
    use_ratio_length_width: bool
    use_pca: bool
    pca_n_components: int

@dataclass
class ModelCandidateConfig:
    name: str
    type: str
    params: Dict[str, Any]

@dataclass
class ModelConfig:
    candidates: list
    cv_n_splits: int
    cv_shuffle: bool
    random_state: int
    scoring: list
    optimize: bool
    optimization_method: str
    optimization_n_iter: int

@dataclass
class OutputConfig:
    model_dir: str
    report_dir: str
    log_dir: str

@dataclass
class APIConfig:
    host: str
    port: int

@dataclass
class AppConfig:
    data: DataConfig
    features: FeaturesConfig
    model: ModelConfig
    preprocessing: PreprocessingConfig
    output: OutputConfig
    logging: Dict[str, Any]
    api: APIConfig

def load_config(path: str) -> AppConfig:
    with open(path, 'r', encoding='utf-8') as f:
        cfg_dict = yaml.safe_load(f)
    data_cfg = DataConfig(**cfg_dict['data'])
    feat_cfg = FeaturesConfig(**cfg_dict['features'])
    model_candidates = [ModelCandidateConfig(**mc) for mc in cfg_dict['model']['candidates']]
    model_cfg = ModelConfig(
        candidates=model_candidates,
        cv_n_splits=cfg_dict['model']['cv']['n_splits'],
        cv_shuffle=cfg_dict['model']['cv']['shuffle'],
        random_state=cfg_dict['data']['random_state'],
        scoring=cfg_dict['model']['scoring'],
        optimize=cfg_dict['model']['optimize'],
        optimization_method=cfg_dict['model']['optimization']['method'],
        optimization_n_iter=cfg_dict['model']['optimization'].get('n_iter', 10)
    )
    preproc_cfg = PreprocessingConfig(**cfg_dict.get('preprocessing', {}))
    output_cfg = OutputConfig(**cfg_dict['output'])
    api_cfg = APIConfig(**cfg_dict['api'])
    return AppConfig(
        data=data_cfg,
        features=feat_cfg,
        preprocessing=preproc_cfg,
        model=model_cfg,
        output=output_cfg,
        logging=cfg_dict.get('logging', {}),
        api=api_cfg
    )
