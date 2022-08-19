from fastapi.testclient import TestClient
from src.main import app
import pytest
# from pathlib import Path
# import sys

client = TestClient(app)

def test_search():
    response = client.get("/api/get/stockprice_search_by_date/?compamyabbreviation=goog&startdate=2018%2C8%2C10&enddate=2018%2C8%2C13")
    assert response.status_code == 200
    assert response.json() == {
  "Date": {
    "0": "2018-08-10T00:00:00",
    "1": "2018-08-13T00:00:00"
  },
  "High": {
    "0": 62.28,
    "1": 62.46
  },
  "Low": {
    "0": 61.6,
    "1": 61.68
  },
  "Open": {
    "0": 62.15,
    "1": 61.85
  },
  "Close": {
    "0": 61.88,
    "1": 61.75
  },
  "Volume": {
    "0": 22174000,
    "1": 19946000
  },
  "Adj Close": {
    "0": 61.88,
    "1": 61.75
  }
}


def test_search_not_found():
    response = client.get("/api/get/stockprice_search_by_date/?compamyabbreviation=weqweq&startdate=2018%2C8%2C10&enddate=2018%2C8%2C13")
    assert response.status_code == 200
    assert response.json() == {
  "details": "WEQWEQ is not a valid company stock name!"
}

def test_predict_model_not_found():
    response = client.get("/api/get/predicted_stock_price/?compamyabbreviation=weqwewq")
    assert response.status_code == 200
    assert response.json() == {
  "details": "model not found!"
}

def test_save_stock_price():
    response = client.get("/api/get/save_stock_price/?compamyabbreviation=goog")
    assert response.status_code == 200
    assert response.json() == {
  "details": "GOOG Table created! Saving success!"
}

def test_save_stock_price_not_found():
    response = client.get("/api/get/save_stock_price/?compamyabbreviation=weqweq")
    assert response.status_code == 200
    assert response.json() == {
  "details": "WEQWEQ is not a valid company stock name!"
}



if __name__ == '__main__':
  pytest.main()