FROM python:3.11-slim
WORKDIR /opt/sbac
COPY sbac.py core.py utils.py ./
WORKDIR /workspace
ENTRYPOINT ["python", "/opt/sbac/sbac.py"]