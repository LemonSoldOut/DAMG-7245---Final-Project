from fastapi.testclient import TestClient
from src.main import app
import pytest
# from pathlib import Path
# import sys

client = TestClient(app)

def test_search():
    response = client.get("/api/get/stockprice_search_by_date/?compamyabbreviation=goog, startdate=2018,8,8, enddate=2018,8,10")
    assert response.status_code == 200
    assert response.json() == {
  "Date": {
    "0": "2018-08-08T00:00:00",
    "1": "2018-08-09T00:00:00",
    "2": "2018-08-10T00:00:00"
  },
  "High": {
    "0": 62.83,
    "1": 62.78,
    "2": 62.28
  },
  "Low": {
    "0": 61.9,
    "1": 62.3,
    "2": 61.6
  },
  "Open": {
    "0": 62.02,
    "1": 62.49,
    "2": 62.15
  },
  "Close": {
    "0": 62.28,
    "1": 62.46,
    "2": 61.88
  },
  "Volume": {
    "0": 27406000,
    "1": 16972000,
    "2": 22174000
  },
  "Adj Close": {
    "0": 62.28,
    "1": 62.46,
    "2": 61.88
  }
}


def test_search_not_found():
    response = client.get("/api/get/stockprice_search_by_date/?compamyabbreviation=weqweq, startdate=2018,8,8, enddate=2018,8,10")
    assert response.status_code == 200
    assert response.json() == {
  "details": "WEQWEQ is not a valid company stock name!"
}

def test_predict_model_not_found():
    response = client.get("/api/get/predicted_stock_price/?compamyabbreviation=goog")
    assert response.status_code == 200
    assert response.json() == {
  "details": "model not found!"
}

def test_predict_model_not_found():
    response = client.get("/api/get/predicted_stock_price/?compamyabbreviation=goog")
    assert response.status_code == 200
    assert response.json() == {
  "details": "model not found!"
}

if __name__ == '__main__':
  pytest.main()