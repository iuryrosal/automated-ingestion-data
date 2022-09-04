from flask import request

def get_query_params() -> dict:
  '''
    Get query parameters in request
  '''
  args_dict = {}
  args = ["region", "datasource", "date", "limit",
          "origin_coord_point_x", "origin_coord_point_y",
          "destination_coord_point_x", "destination_coord_point_y"]
  for arg in args:
    args_dict[arg] = request.args.get(arg)
  return args_dict

def build_where_expr(query_str: str, query_params: str) -> str:
  '''
    Append WHERE SQL expression in query script following query parameters
  '''
  where_expr = []

  if query_params["region"]:
    where_expr.append(f"region = '{query_params['region']}'")
  if query_params["datasource"]:
    where_expr.append(f"datasource = '{query_params['datasource']}'")
  if query_params["origin_coord_point_x"]:
    where_expr.append(f"origin_coord_point_x LIKE '{str(query_params['origin_coord_point_x'])}%%'")
  if query_params["origin_coord_point_y"]:
    where_expr.append(f"origin_coord_point_y LIKE '{str(query_params['origin_coord_point_y'])}%%'")
  if query_params["destination_coord_point_x"]:
    where_expr.append(f"destination_coord_point_x LIKE '{str(query_params['destination_coord_point_x'])}%%'")
  if query_params["destination_coord_point_y"]:
    where_expr.append(f"destination_coord_point_y LIKE '{str(query_params['destination_coord_point_y'])}%%'")
  if query_params["date"]:
    where_expr.append(f"datetime::TIMESTAMP::DATE = '{str(query_params['date'])}%%'")

  if len(where_expr) > 0:  # There is where expression
    count = 0
    while count < len(where_expr):
      if count == 0:  # first where condition 
        query_str = query_str + (f" WHERE {where_expr[count]}")        
      else:
        query_str = query_str + (f" AND {where_expr[count]}")
      count += 1
  
  return query_str

def build_limit_expr(query_str: str, query_params: str) -> str:
  '''
    Append LIMIT SQL expression in query script
  '''
  if query_params["limit"]:
    query_str = query_str + (f" LIMIT {query_params['limit']}")
  else:
    query_str = query_str + (" LIMIT 10")
  return query_str
