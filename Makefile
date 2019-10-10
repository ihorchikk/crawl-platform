test:
	docker-compose -f docker-compose.test.yml -p wb-qa-service-test build test
	docker-compose -f docker-compose.test.yml -p wb-qa-service-test up test
	docker-compose -f docker-compose.test.yml -p wb-qa-service-test down
	docker system prune -f
install:
	docker-compose down
	git pull
	docker-compose up --build -d
	docker system prune -f

