# api_request.py
from dotenv import load_dotenv
import os
import requests
from typing import List, Optional, Union, Dict, Any

# Загрузка переменных окружения из файла .env
load_dotenv()

RAPIDAPI_KEY: Optional[str] = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST: Optional[str] = os.getenv("RAPIDAPI_HOST")

url: str = "https://moviesdatabase.p.rapidapi.com/actors"

headers: Dict[str, Optional[str]] = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}


def get_actors(num_actors_to_display: int, reverse: Optional[bool] = True) -> Optional[List[Dict[str, Any]]]:
    """
    Получение информации об актерах из API.

    :return: Список словарей, представляющих информацию об актерах.
    """
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data: Dict[str, Any] = response.json()
        sorted_actors: List[Dict[str, Any]] = sorted(data["results"], key=lambda x: x["birthYear"], reverse=reverse)

        return sorted_actors[:num_actors_to_display]
    else:
        return None


def get_actors_custom_years(start_year: int, end_year: int) -> Optional[List[Dict[str, Any]]]:
    """
    Получение информации об актерах, родившихся в заданном временном диапазоне, из API.

    :return: Список словарей, представляющих информацию об актерах родившихся в диапазоне.
    """
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data: Dict[str, Any] = response.json()
        actors_info: List[Dict[str, Any]] = [actor for actor in data["results"] if start_year <= actor["birthYear"] <= end_year]
        return actors_info
    else:
        return None
