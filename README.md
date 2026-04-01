uvicorn main:app --reload

$ curl -X POST "http://127.0.0.1:8000/location" -H "Content-Type: application/json" -d '{
  "carId": "1",
  "lat": 60.00,
  "lon": 40.00,
  "speed": 10,
  "timestamp": 1710000000
}'



  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   190  100    98  100    92   2480   2328 --:--:-- --:--:-- --:--:--  4871{"status":"ok","data":{"carId":"1","lat":55.75,"lon":37.61,"speed":10.0,"timestamp":1710000000.0}}
