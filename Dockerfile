FROM apache/airflow:2.7.3

USER airflow
RUN pip install --user --no-cache-dir scikit-learn pandas numpy requests
ENV PATH=/home/airflow/.local/bin:$PATH
