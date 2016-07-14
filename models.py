from django.db import models
from django.contrib.gis.db import models

##################################
# PASSENGER DATA


# Create your models here.
class Passenger(models.Model):
    full_name = models.CharField(blank=False)
    first_name = models.CharField()
    middle_name = models.CharField(blank=True)
    last_name = models.CharField()


class PassengerData(models.Model):
    passenger = models.ForeignKey('Passenger')
    # TODO: document type can be different: passport,
    document_series = models.CharField()
    document_number = models.CharField()
    document_issuer_name = models.CharField()
    document_issue_date = models.CharField()


##################################
# TRAIN AND PLACEMENT DATA

class Train(models.Model):
    type = models.CharField()   # TODO: what types?
    code = models.CharField()


class TrainPlace(models.Model):
    train = models.ForeignKey('Train')
    carriage_number = models.IntegerField()
    place_type = models.CharField(choices=['sitting',
                                           'compartment',
                                           'accomodations'])     # TODO: other types?
    place_code = models.CharField()


##################################
# ROUTE AND SCHEDULE DATA


class Country(models.Model):
    name = models.CharField()
    code = models.CharField()   # some code


class Location(models.Model):
    name = models.CharField()
    code = models.CharField()   # some code
    country = models.ForeignKey('Country')
    type = models.CharField(choices=['city', 'village'])    # TODO: any other types?
    geo_location = models.GeometryField(geography=True)


class Station(models.Model):
    name = models.CharField()
    location = models.ForeignKey('Location')
    geo_location = models.GeometryField(geography=True)


class Route(models.Model):
    start_station = models.ForeignKey('Station')
    end_station = models.ForeignKey('Station')


class RouteElement(models.Model):
    route = models.ForeignKey('Route')
    order = models.IntegerField()
    station = models.ForeignKey('Station')
    time_arrival = models.TimeField()
    time_departure = models.TimeField()
    day_arrival = models.IntegerField(default=1)       # for routes longer than 1 day
    day_departure = models.IntegerField(default=1)


##################################
# TRIP AND TICKET DATA

class Trip(models.Model):
    train = models.ForeignKey('Train')
    route = models.ForeignKey('Route')
    date_departure = models.DateTimeField()
    date_arrival = models.DateTimeField()


class TicketBasePrice(models.Model):
    trip = models.ForeignKey('Trip')
    place = models.ForeignKey('TrainPlace')
    price = models.FloatField()


class TicketOrder(models.Model):
    trip = models.ForeignKey('Trip')
    place = models.ForeignKey('TrainPlace')
    passenger = models.ForeignKey('Passenger')
    price = models.FloatField()
