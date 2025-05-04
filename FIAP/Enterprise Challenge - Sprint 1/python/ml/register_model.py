import os
import logging
import subprocess
from config.settings import MODEL_REGISTRY_URI
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("register_model")

def build_and_push_docker(model_path="models/rf_model.pkl", 
                          image_name="rf_inference", 
                          tag="latest"):
    # Dockerfile deve copiar o modelo e expor endpoint
    image_uri = f"{MODEL_REGISTRY_URI}/{image_name}:{tag}"
    cmd_build = ["docker", "build", "-t", image_uri, "."]
    cmd_push  = ["docker", "push", image_uri]
    try:
        subprocess.check_call(cmd_build)
        logger.info(f"Imagem Docker construída: {image_uri}")
        subprocess.check_call(cmd_push)
        logger.info(f"Imagem Docker enviada para {MODEL_REGISTRY_URI}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao build/push Docker: {e}")
        raise
    return image_uri

if __name__ == "__main__":
    build_and_push_docker()
