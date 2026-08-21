FROM python:3.12.13-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build
COPY packaging/oci-requirements.txt /tmp/oci-requirements.txt
RUN python -m venv /opt/venv \
    && /opt/venv/bin/python -m pip install --upgrade -r /tmp/oci-requirements.txt

COPY pyproject.toml README.md ./
COPY src ./src
RUN /opt/venv/bin/python -m pip install --no-deps --no-build-isolation . \
    && /opt/venv/bin/python -c "import cogniprint"

FROM python:3.12.13-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de AS runtime

ENV PATH=/opt/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/home/cogniprint

RUN groupadd --gid 10001 cogniprint \
    && useradd --uid 10001 --gid 10001 --create-home --home-dir /home/cogniprint --shell /usr/sbin/nologin cogniprint \
    && mkdir -p /workspace \
    && chown 10001:10001 /workspace

COPY --from=builder /opt/venv /opt/venv

WORKDIR /workspace
USER 10001:10001
ENTRYPOINT ["cogniprint"]
CMD ["--help"]
