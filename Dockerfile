FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv
COPY pyproject.toml ./

# Install all dependencies using uv
RUN uv pip install --system \
    agent-framework>=1.0.0b251120 \
    azure-ai-inference>=1.0.0b9 \
    fastapi[standard]>=0.121.3 \
    semantic-kernel>=1.38.0 \
    gradio>=5.50.0 \
    fastmcp>=2.13.1 \
    pandas \
    python-dotenv \
    requests

COPY . .

RUN mkdir -p /var/log/supervisor

RUN echo '[supervisord]\n\
nodaemon=true\n\
logfile=/var/log/supervisor/supervisord.log\n\
pidfile=/var/run/supervisord.pid\n\
\n\
[program:backend]\n\
command=python src/backend/app.py\n\
directory=/app\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/supervisor/backend.err.log\n\
stdout_logfile=/var/log/supervisor/backend.out.log\n\
\n\
[program:frontend]\n\
command=python src/frontend/app.py\n\
directory=/app\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/supervisor/frontend.err.log\n\
stdout_logfile=/var/log/supervisor/frontend.out.log' > /etc/supervisor/conf.d/supervisord.conf

EXPOSE 7860 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
