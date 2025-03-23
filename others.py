from __future__ import annotations
from fastapi import APIRouter, HTTPException
from fastapi import FastAPI, Query
import httpx
from psycopg2 import IntegrityError
from pydantic import BaseModel, validator
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Literal 
from sqlalchemy.orm import sessionmaker
import bscript
import models

import json



