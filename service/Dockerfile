FROM python:3.12 AS builder

RUN pip3 install -U pip poetry
WORKDIR /app
COPY . .
RUN poetry build


FROM python:3.12

RUN pip3 install -U pip wheel

WORKDIR /app
COPY --from=builder /app/dist/*.whl .

RUN pip install *.whl

EXPOSE 5000
ENTRYPOINT [ "python3", "-m", "structure_comparer" ]
CMD [ "--project-dir", "/app/projects" ]
