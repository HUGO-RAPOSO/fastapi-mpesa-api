#!/usr/bin/env bash

# Comando de inicialização
uvicorn index:app --host 0.0.0.0 --port $PORT