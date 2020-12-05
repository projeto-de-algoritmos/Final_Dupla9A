import heapq
import sys

def create_edge(graph, node1, node2, interval):
    if not graph.get(node1):
        graph[node1] = []

    graph[node1].append({
        'city': node2,
        'interval': interval
    })

def dijkstra(graph, start, target, socketio):
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
        socketio.emit('update', {'ids': []})
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


def create_path(start, goal, graph, socketio):
    distances = dijkstra(graph, start, goal,socketio)  
    ids = []

    if not (distances):
        socketio.emit('update', {'ids': []})
        return 'impossivel'
    
    node = distances[goal]['previous_node']
    path = []
    path.append(distances[goal])

    while node:
        path.append(distances[node])
        node = distances[node]['previous_node']

    print(path)

    for i in range(0, len(path)-1):
        print(path[i])
        print(path[i+1])
        if path[i+1]['previous_node'] is not None:
            ids.append(path[i+1]['previous_node']+path[i]['previous_node'])
    
    print(ids)
    socketio.emit('update', {'ids': ids})
    return path

def build_and_solve(graph_data, start, goal, socketio):
    graph = {}
    for edge in graph_data:
        node1 = edge['city1']
        node2 = edge['city2']
        interval = edge['interval']

        create_edge(graph, node1, node2, interval)
        create_edge(graph, node2, node1, interval)

    print(create_path(start, goal, graph, socketio))
