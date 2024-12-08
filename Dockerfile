FROM python:3.12
RUN addgroup seatsniper
RUN useradd -d /home/seatsniper -m -s /bin/bash seatsniper -g seatsniper
WORKDIR /app
RUN pip install wheel==0.37.1
COPY --chown=seatsniper ./requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
USER seatsniper
COPY --chown=seatsniper . .
EXPOSE 8000
