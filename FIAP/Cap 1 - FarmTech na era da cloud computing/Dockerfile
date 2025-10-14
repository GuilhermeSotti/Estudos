FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
COPY models/ models/
EXPOSE 5000
ENV MODEL_PATH=models/rf_model.joblib
ENV SCALER_PATH=models/scaler.joblib
CMD ["gunicorn", "src.serve:app", "--bind", "0.0.0.0:5000", "--workers", "1"]
