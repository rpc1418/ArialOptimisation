# **Arial Optimisation - Analyzes and visualizes optimal flight routing and data rates.**

![GitHub repo size](https://img.shields.io/github/repo-size/rpc1418/ArialOptimisation) ![License](https://img.shields.io/github/license/rpc1418/ArialOptimisation) ![Contributors](https://img.shields.io/github/contributors/rpc1418/ArialOptimisation)


# Flight Path Optimization and Visualization

## Overview

This Python script performs various operations related to flight path optimization, including calculating distances between flights, finding the shortest routing paths, and visualizing data. It uses several libraries such as `pandas`, `plotly`, and built-in Python modules to achieve these functionalities.

## Features

- **CSV Data Extraction:** Reads flight data from a CSV file.
- **Shortest Path Calculation:** Computes the shortest path between flights using a priority queue-based algorithm.
- **Distance and Data Rate Calculation:** Uses the Haversine formula to calculate distances and determines data rates based on distance.
- **Path Analysis:** Determines the optimal routing path and calculates data transmission rates and latencies.
- **Visualization:** Plots flight paths and locations using Plotly.

## Requirements

Ensure the required packages are installed. The script will attempt to install them if they are missing:

- `math`
- `csv`
- `pandas`
- `collections`
- `heapq`
- `plotly`

## Usage

1. **Prepare the Dataset:**

   Place your dataset in a file named `dataset.CSV` in the same directory as the script. The CSV should contain columns for flight names, latitude, and longitude.

2. **Run the Script:**

   Execute the script using Python:

   ```bash
   python script_name.py
   ```
   The script will:
    - Read flight data from dataset.CSV.
    - Calculate distances between flights.
    - Find the shortest routing paths.
    - Calculate data transmission rates and latencies.
    - Save results to CSV files.
    - Plot flight paths and locations.
## Functions

### `csvtolistofdict_file_extractor(location)`

Extracts flight data from a CSV file and returns a list of dictionaries.

**Parameters:**
- `location` (str): The file path of the CSV file.

**Returns:**
- List[Dict[str, str]]: A list of dictionaries containing flight data.

---

### `shortestPath(edges, source, sink)`

Finds the shortest path between two nodes using a priority queue-based approach.

**Parameters:**
- `edges` (List[Tuple[str, str, int]]): A list of edges in the form (source, destination, cost).
- `source` (str): The starting node.
- `sink` (str): The destination node.

**Returns:**
- Tuple[int, List[str]]: The cost and path from the source to the sink.

---

### `calculate_distance(coord1, coord2)`

Calculates the distance between two geographical coordinates using the Haversine formula.

**Parameters:**
- `coord1` (Dict[str, str]): The latitude and longitude of the first point.
- `coord2` (Dict[str, str]): The latitude and longitude of the second point.

**Returns:**
- float: The distance between the two coordinates in kilometers.

---

### `calculate_data_rate(distance)`

Determines the data transmission rate based on distance.

**Parameters:**
- `distance` (float): The distance between two points in kilometers.

**Returns:**
- float: The data transmission rate in Mbps.

---

### `find_all_routing_path()`

Finds all possible routing paths between flights.

**Returns:**
- List[Tuple[str, str, int]]: A list of tuples representing edges with their distances.

---

### `shortest_routing_path()`

Finds the shortest routing path for each flight to either Newark Liberty or Heathrow.

**Returns:**
- List[Tuple[str, List[str]]]: A list of tuples containing the shortest path for each flight.

---

### `transmission_rate()`

Calculates the end-to-end data rate and latency for each flight's routing path.

**Returns:**
- List[Tuple[str, List[Tuple[str, float]], str, float, int]]: A list of tuples containing the source flight, routing path with data rates, nearest ground station, end-to-end data rate, and latency.

---

### `tocheck()`

Allows user input to check the routing path, data rate, and latency for a specific flight.

**Usage:**
- Prompts the user to enter a flight name and displays its routing path, data rate, and latency.

---

### `plot()`

Visualizes the flight paths and locations using Plotly.

**Usage:**
- Plots the flight paths and nodes on a map using Plotly's `scatter_mapbox` and `line_mapbox` functions.

## Output Files

- **`all_Paths_Available.csv`**: Contains all possible routing paths between flights.
- **`Final_result.csv`**: Contains the end-to-end data rates and latencies for each flight.
- **`ptogs.csv`**: Contains the shortest path for each flight to the nearest ground station.

---

## Example

The script visualizes the flight paths and locations. Here’s a sample visualization of how the data might look:

![Example Visualization](path_to_image)

---

## License

This project is licensed under the MIT License.
