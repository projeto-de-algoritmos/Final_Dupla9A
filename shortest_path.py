import heapq
import sys

def create_edge(graph, node1, node2, interval):
  if not graph.get(node1):
    graph[node1] = []

  graph[node1].append({
    'city': node2,
    'interval': interval
  })

def dijkstra(graph, start, target):
  distances = {}
  visited = {}

  for node in graph:
    distances[node] = {
      'distance': sys.maxsize,
      'previous_node': None
    }
  
  try:
    distances[start]['distance'] = 0
  except KeyError:
    # socketio.emit('update', {'ids': []})
    return []

  for node in graph:
    visited[node] = False

  queue = []
  heapq.heappush(queue, (0, start))

  while queue:
    node = heapq.heappop(queue)[1]

    if visited[node]:
      continue
      
    if node == target:
      return distances

    for edge in graph[node]:
      possibility = distances[node]['distance'] + edge['interval']
      current_weight = distances[edge['city']]['distance']

      if possibility < current_weight:
        distances[edge['city']]['distance'] = possibility
        distances[edge['city']]['previous_node'] = node

        heapq.heappush(queue, (possibility, edge['city']))


def create_path(start, goal, graph):
  distances = dijkstra(graph, start, goal)  
  ids = []

  if not (distances):
    # socketio.emit('update', {'ids': []})
    return 'impossivel'
  
  node = distances[goal]['previous_node']
  path = []
  path.append(distances[goal])

  while node:
    path.append(distances[node])
    node = distances[node]['previous_node']

#   for distance in path:
#     if distance['word']:
#       id = distance['word']
#       ids.append(id)
  
#   socketio.emit('update', {'ids': ids})
  return path

def main():
    graph = {}
    graph_data = [
        {
            'city1': 'bsb',
            'city2': 'sp',
            'interval': 800
        },
        {
            'city1': 'sp',
            'city2': 'rj',
            'interval': 200
        },
        {
            'city1': 'bsb',
            'city2': 'rj',
            'interval': 1100
        },
    ]

    for edge in graph_data:
        node1 = edge['city1']
        node2 = edge['city2']
        interval = edge['interval']

        create_edge(graph, node1, node2, interval)
        create_edge(graph, node2, node1, interval)

    print(create_path('bsb', 'rj', graph))



if __name__ == "__main__":
    main()