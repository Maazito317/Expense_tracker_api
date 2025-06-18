FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app

# 1) Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copy code
COPY . .

# 3) Document the listen port
EXPOSE 8000

# 4) Use bash -lc so command overrides still work
ENTRYPOINT ["bash", "-lc"]

# 5) Default to launching Uvicorn for production
CMD ["uvicorn app.main:app --host 0.0.0.0 --port 8000"]
