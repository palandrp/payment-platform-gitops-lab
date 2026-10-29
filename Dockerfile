FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PORT=8080
WORKDIR /app
COPY app/ /app/app/
RUN useradd --uid 10001 --create-home appuser
USER 10001:10001
EXPOSE 8080
CMD ["python", "-m", "app.main"]
