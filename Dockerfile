# 1. Base Python image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy everything from your local project into the container
COPY . .

# 4. Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose the default Streamlit port
EXPOSE 8501

# 6. Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
