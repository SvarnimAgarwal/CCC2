FROM python:3

WORKDIR /mastodon_harvestor

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./mastodon_runner.py" ]