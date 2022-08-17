from fastapi.testclient import TestClient
from src.main import app
import pytest
# from pathlib import Path
# import sys

client = TestClient(app)

def test_inputInfoFilterRequest():
    response = client.get("/api/get/infoFilter/?filename=0cd99a9ee135c7618006540f5b6d9b1b")
    assert response.status_code == 200
    assert response.json() == {
        "53": {
    "filename": "0cd99a9ee135c7618006540f5b6d9b1b",
    "width": "1079",
    "height": "1600",
    "class": "F16",
    "xmin": "77",
    "ymin": "263",
    "xmax": "950",
    "ymax": "658"
  }
    }

def test_aircraftClassAndFileNameRequest():
    response = client.get("/api/get/fileNameAndClass/?className=F16")
    assert response.status_code == 200

def test_no_found_aircraftClassAndFileNameRequest():
    response = client.get("/api/get/fileNameAndClass/?className=F10")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Item not found'}

def test_no_found_imgSzieRangeRequest():
    response = client.get("/api/get/imgSizeRange/?width=500&height=500")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Item not found'}

def test_incorrect_input_imgSzieRangeRequest():
    response = client.get("/api/get/imgSizeRange/?width=abc&height=500")
    assert response.status_code == 422

def test_imgSzieRangeRequest():
    response = client.get("/api/get/imgSizeRange/?width=600&height=600")
    assert response.status_code == 200
    assert response.json() == {
  "69": {
    "filename": "0dc3f3e32533d1909ec496e32a3f916c",
    "width": "512",
    "height": "303",
    "class": "SR71",
    "xmin": "178",
    "ymin": "121",
    "xmax": "331",
    "ymax": "209"
  },
  "186": {
    "filename": "2cf1ec46ef1a6534a784b25ce1d07978",
    "width": "512",
    "height": "341",
    "class": "Su57",
    "xmin": "28",
    "ymin": "162",
    "xmax": "236",
    "ymax": "282"
  },
  "187": {
    "filename": "2cf1ec46ef1a6534a784b25ce1d07978",
    "width": "512",
    "height": "341",
    "class": "Su57",
    "xmin": "115",
    "ymin": "43",
    "xmax": "483",
    "ymax": "172"
  },
  "201": {
    "filename": "2ebe35e67880d4f9609c9fa07b6f5f9e",
    "width": "590",
    "height": "369",
    "class": "C17",
    "xmin": "15",
    "ymin": "116",
    "xmax": "492",
    "ymax": "358"
  },
  "202": {
    "filename": "2ebe35e67880d4f9609c9fa07b6f5f9e",
    "width": "590",
    "height": "369",
    "class": "F15",
    "xmin": "329",
    "ymin": "50",
    "xmax": "486",
    "ymax": "101"
  },
  "203": {
    "filename": "2ebe35e67880d4f9609c9fa07b6f5f9e",
    "width": "590",
    "height": "369",
    "class": "F15",
    "xmin": "446",
    "ymin": "11",
    "xmax": "589",
    "ymax": "56"
  },
  "410": {
    "filename": "7aabb72565dae3f2544267ee1ce3f1b4",
    "width": "564",
    "height": "564",
    "class": "F117",
    "xmin": "4",
    "ymin": "153",
    "xmax": "561",
    "ymax": "484"
  },
  "411": {
    "filename": "7aabb72565dae3f2544267ee1ce3f1b4",
    "width": "564",
    "height": "564",
    "class": "F117",
    "xmin": "228",
    "ymin": "419",
    "xmax": "471",
    "ymax": "483"
  }
}

def test_numAndClassFiteredInfoRequest():
    response = client.get("/api/get/aircraftNumandClass/?num=5&className=F16")
    assert response.status_code == 200
    assert response.json() == {
        "133": {
    "filename": "4a042db1cef213a1ed865422e6355f76",
    "class": "F16",
    "count": 5
  }
    }

def test_aircraftPositionRequest():
    response = client.get("/api/get/aircraftPositionRange/?xmin=500&ymin=500&xmax=900&ymax=900")
    assert response.status_code == 200
    assert response.json() == {
        "131": {
    "filename": "1deecbebb637c7cfcb1ed6ef993243c1",
    "width": "1500",
    "height": "969",
    "class": "JAS39",
    "xmin": "616",
    "ymin": "672",
    "xmax": "704",
    "ymax": "731"
  },
  "175": {
    "filename": "2cc2da26e5c852e86339633fdffccbba",
    "width": "1600",
    "height": "1596",
    "class": "Rafale",
    "xmin": "509",
    "ymin": "713",
    "xmax": "630",
    "ymax": "856"
  },
  "299": {
    "filename": "4ef3fc177420d40c4a714f74fc370d41",
    "width": "2048",
    "height": "1365",
    "class": "V22",
    "xmin": "594",
    "ymin": "616",
    "xmax": "699",
    "ymax": "668"
  }
    }

if __name__ == '__main__':
  pytest.main()