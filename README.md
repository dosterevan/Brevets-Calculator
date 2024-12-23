## Brevet time calculator with MongoDB, and a RESTful API!

Evan Doster
dosterevan@gmail.com

# Brevet Time Calculator

### ACP controle Algorithm

This project introduces a web application that utilizes RUSA's online calculator. The algorithm for calculating controle times is described [here](https://rusa.org/pages/acp-brevet-control-times-calculator). Additional background information can be found [here](https://rusa.org/pages/rulesForRiders).

I essentially replace the calculator available [here](https://rusa.org/octime_acp.html). I also use that calculator to clarify requirements and develop test data.

### Outline of Algorithm

Depending on the control location, we can expect the minimum and maximum speed (km/hour) to change as a result of this distance. Refer to the table [here](https://rusa.org/pages/acp-brevet-control-times-calculator).

The open time is calculated by dividing the control distance by the maximum speed. The algorithm can be generalized as follows:
(control distance - previous interval) / (current maximum speed) + (last interval's control distance - previous interval) / (last interval's maximum speed)

Similarly, the close time is calculated by dividing the control distance by the minimum speed. The algorithm can be generalized as follows:
(control distance - previous interval) / (current minimum speed) + (last interval's control distance - previous interval) / (last interval's minimum speed)

Except when the control distance is equal to the brevet distance, which both are equal to 200. This special rule dictates that our close time is 13H30.

## Running the Program

#### Docker

Inside your terminal, navigate to your project-6 folder, then run 'docker compose up'. Once the container is running, you can run the application by searching http://localhost:XXXX on your browser, where XXXX is the port number specified in your docker-compose.yml file.

## Usage

The web interface allows the brevet organizer to enter the brevet distance, start time, and checkpoint locations. As checkpoint distances are entered, the app will automatically calculate and populate the open and close time for each one.

The app provides a Submit button to save these calculated times to a database for later retrieval.

The Display button will fetch the latest saved brevet info and populate the form.

This allows organizers to save and restore the controle times for their events.

The backend uses MongoDB to store the brevet data. Docker Compose is used to run the Flask app and MongoDB containers to run the application.

## Tests

To test if the services run as expected, send a curl request to the API. Run docker compose and be in a directory close to the compose file. Once the three containers are running, run the following command in the terminal:
For POST
```bash
curl -i -X POST -H "Content-Type: application/json" -d '{
  "distance": "200",
  "begin_date": "2021-01-01T00:00",
  "controls": [
    {
      "km": "50",
      "miles": "31.068550",
      "location": "",
      "open_time": "2021-01-01T01:28",   
      "close_time": "2021-01-01T03:20"
    },
    {
      "km": "200",
      "miles": "124.274200",
      "location": "",
      "open_time": "2021-01-01T05:52",   
      "close_time": "2021-01-01T13:30"
    }
  ]
}' http://127.0.0.1:5001/api/brevets
```
For GET 
```bash
curl -X GET http://127.0.0.1:5001/api/brevets
```

For PUT, fill in with your _id
```bash
curl -X PUT -H 'Content-Type: application/json' -d '{"distance": 400.0, "begin_date": "2021-01-01T00:00", "controls": [{"km": 50.0, "miles": 31.06855, "location": "", "open_time": "2021-01-01T01:28", "close_time": "2021-01-01T03:20"}, {"km": 200.0, "miles": 124.2742, "location": "", "open_time": "2021-01-01T05:52", "close_time": "2021-01-01T13:30"}]}' http://127.0.0.1:5001/api/brevet/_id_
```

For GET fill in with your _id
```bash
curl -X GET http://127.0.0.1:5001/api/brevet/_id
```

For DELETE, fill in with your _id
```bash
curl -X DELETE http://127.0.0.1:5001/api/brevet/_id
```
Feel free to customize it further according to your project's needs.

## Authors
Michal Young, Ram Durairajan. Updated by Ali Hassani. Completed by Evan Doster
