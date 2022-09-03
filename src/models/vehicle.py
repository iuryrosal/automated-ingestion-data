from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class Vehicle(database.Model):
  __tablename__ = "vehicles_records"
  id = database.Column(database.Integer, primary_key=True)
  region = database.Column(database.String(100))
  origin_coord_point = database.Column(database.String(100))
  destination_coord_point = database.Column(database.String(100))
  datetime = database.Column(database.DateTime())
  datasource = database.Column(database.String(100))

  def __init__(self, region, origin_coord_point, destination_coord_point, datetime, datasource):
    self.region = region
    self.origin_coord_point = origin_coord_point
    self.destination_coord_point = destination_coord_point
    self.datetime = datetime
    self.datasource = datasource
