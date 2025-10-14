# Uso:
#   make build        # constrói a imagem do serviço http_ingest (docker build)
#   make up           # sobe postgres, mosquitto, pgadmin, e opcional ingest-http (via docker-compose)
#   make down         # derruba os containers
#   make seed         # executa db/seed.sql no container postgres (útil se postgres já estiver up)
#   make gen-sample   # exporta measurements para db/sample_measurements.csv
#   make run-ml       # executa o script de treino (local)
#   make run-dashboard# executa Streamlit (local)
#   make run-replay   # executa utils/replay.py (pub MQTT) (local)
#   make logs         # mostra logs do docker-compose (follow)
#   make clean        # remove volumes e imagens construídas (cuidado)
#

.PHONY: build up down seed gen-sample run-ml run-dashboard run-replay logs clean

IMAGE_NAME := fh_http_ingest:latest

build:
	docker build -t $(IMAGE_NAME) .

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

seed:
	docker exec -i fh_postgres psql -U postgres -d factorydb -f /docker-entrypoint-initdb.d/seed.sql

gen-sample:
	mkdir -p db
	docker exec -i fh_postgres psql -U postgres -d factorydb -c "\COPY (SELECT ts, device_id, temperature_c, humidity FROM measurements ORDER BY ts) TO STDOUT WITH CSV HEADER" > db/sample_measurements.csv
	@echo "Arquivo gerado: db/sample_measurements.csv"

run-ml:
	python ml/train_eval.py

run-dashboard:
	streamlit run dashboard/app.py

run-replay:
	# Executa publisher MQTT local (assume utils/replay.py existe)
	python utils/replay.py

clean:
	# Remove volumes e imagens (use com cuidado)
	docker-compose down -v
	docker image rm $(IMAGE_NAME) || true
	@echo "Containers e volumes removidos (se existiam)."
