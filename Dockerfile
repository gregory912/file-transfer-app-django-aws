FROM python:3.11.0


ENV PYTHONDONTWRITEBYTECODE 1


ENV PYTHONUNBUFERED 1

WORKDIR /webapp

COPY Pipfile Pipfile.lock /webapp/


RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

## copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /webapp/entrypoint.sh
RUN chmod +x /webapp/entrypoint.sh

COPY . /webapp/

## run entrypoint.sh
ENTRYPOINT ["/webapp/entrypoint.sh"]