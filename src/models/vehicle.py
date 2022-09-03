from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class Vehicle(database.Model):
  __tablename__ = "vehicles_records"
  id = database.Column(database.Integer, primary_key=True)
  region = database.Column(database.String(100))
  origin_coord_point_x = database.Column(database.String(100))
  origin_coord_point_y = database.Column(database.String(100))
  destination_coord_point_x = database.Column(database.String(100))
  destination_coord_point_y = database.Column(database.String(100))
  datetime = database.Column(database.DateTime())
  datasource = database.Column(database.String(100))

  def __init__(self, region, origin_coord_point_x, origin_coord_point_y, 
                destination_coord_point_x, destination_coord_point_y,
                datetime, datasource):
    self.region = region
    self.origin_coord_point_x = origin_coord_point_x
    self.origin_coord_point_y = origin_coord_point_y
    self.destination_coord_point_x = destination_coord_point_x
    self.destination_coord_point_y = destination_coord_point_y
    self.datetime = datetime
    self.datasource = datasource
