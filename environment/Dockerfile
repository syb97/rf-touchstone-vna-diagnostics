FROM python:3.11.9-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

RUN python -m pip install --no-cache-dir --upgrade pip==24.0 \
    && python -m pip install --no-cache-dir pytest==8.2.2

COPY . /workspace

CMD ["bash"]
