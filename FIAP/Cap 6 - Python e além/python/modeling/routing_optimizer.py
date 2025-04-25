from ortools.constraint_solver import pywrapcp, routing_enums_pb2

def optimize_routes(distance_matrix: list, num_vehicles: int, depot: int = 0):
    """
    Roteirização otimizada via OR-Tools.
    :param distance_matrix: matriz de distâncias NxN
    :param num_vehicles: número de veículos disponíveis
    :param depot: índice do depósito
    """
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, depot)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(i, j):
        return distance_matrix[manager.IndexToNode(i)][manager.IndexToNode(j)]
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_params)
    routes = []
    if solution:
        for v in range(num_vehicles):
            idx = routing.Start(v)
            route = []
            while not routing.IsEnd(idx):
                route.append(manager.IndexToNode(idx))
                idx = solution.Value(routing.NextVar(idx))
            route.append(manager.IndexToNode(idx))
            routes.append(route)
    return routes
