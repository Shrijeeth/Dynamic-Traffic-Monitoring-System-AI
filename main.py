"""
Main module
"""

import logging

from fastapi import FastAPI
from lifespan import lifespan_init

app = FastAPI(lifespan=lifespan_init)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
