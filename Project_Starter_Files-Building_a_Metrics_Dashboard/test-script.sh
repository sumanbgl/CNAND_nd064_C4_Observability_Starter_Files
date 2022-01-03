for i in 0 1 2 3 4 5 6 7 8 9
do
  curl http://localhost:8081/
  curl http://localhost:8081/api
  curl POST http://localhost:8081/star
  curl http://localhost:8081/403
  curl http://localhost:8081/404
  curl http://localhost:8081/500
  curl http://localhost:8081/503
  
  curl http://localhost:8080/  
  curl http://localhost:8080/403
  curl http://localhost:8080/404
  curl http://localhost:8080/500
  curl http://localhost:8080/503
done
