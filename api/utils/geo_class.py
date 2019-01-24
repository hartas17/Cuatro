from math import sin, cos, asin, atan2, degrees, radians, sqrt, pow, pi

"""Module to do geographic calculations.
Most of the formulas in this module where taken from
http://www.movable-type.co.uk/scripts/latlong.html
"""


def latlng_from_degrees(lat, lng):
    return LatLng(lat, lng)

def latlng_from_radians(lat, lng):
    return LatLng(degrees(lat), degrees(lng))

# 6,371 km
EARTH_RADIUS = 6371000.0

class LatLng:
    """Class that represents a point on earth by its latitude and
    longitude.
    Quantities are represented in degrees , and must be represented
    with floating points. They are transformed to radians for most
    operations.
    """
    def __init__(self, lat, lng):
        """Creates a new point using degrees"""
        self.lat = float(lat)
        self.lng = float(lng)

    def __repr__(self):
        return "LatLng(%s, %s)" % (self.lat, self.lng)

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.lat == other.lat and self.lng == other.lng)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __cmp__(self, other):
        """Compare first by latitude then by longitude"""
        dif = self.lat - other.lat
        if dif == 0.0:
            dif = self.lng - other.lng
        return dif

    def lat_r(self):
        """Returns the latitude in radians"""
        return radians(self.lat)

    def lng_r(self):
        """Return the longitude in radians"""
        return radians(self.lng)

    def distance_to(self, other):
        """Returns the distance in meters between LatLng self and LatLng
        other
        """

        a = (pow(sin((other.lat_r() - self.lat_r()) / 2), 2)
             +
             (cos(self.lat_r()) *
              cos(other.lat_r()) *
              pow(sin((other.lng_r() - self.lng_r()) / 2) , 2)))

        # c is the angle between the 2 points
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        d = EARTH_RADIUS * c
        return d


    def destination_point(self, bearing_deg, meters):
        return self.destination_point_radians(radians(bearing_deg), meters)

    def destination_point_radians(self, bearing, meters):
        """Returns a new point that lies n meters away from self if
        you start walking with the given bearing
        bearing -- initial bearing, angle in radians clockwise from
        north
        meters -- distance to move from the initial point
        """

        # bearing in radians
        theta = float(bearing)
        # angular distance in radians
        delta = float(meters) / EARTH_RADIUS

        # lat2 in radians
        lat2 = asin((sin(self.lat_r()) * cos(delta))
                    +
                    (cos(self.lat_r()) * sin(delta) * cos(theta)))

        lng2 = self.lng_r() + atan2(sin(theta) * sin(delta) * cos(self.lat_r()),
                                    cos(delta) - (sin(self.lat_r()) * sin(lat2)))

        # normalize to (-180, 180)         (-pi, +pi)
        # lng2 = (lng2 + 540) % 360 - 180
        if lng2 > pi :
            lng2 -= 2 * pi

        if lng2 < -pi:
            lng2 += 2 * pi

        return latlng_from_radians(lat2, lng2)

    def destination_point_north(self, meters):
        """Returns a new point that is meters meters north from this
        point"""
        return self.destination_point_radians(0, meters)

    def destination_point_east(self, meters):
        """Returns a new point that is meters meters east from this
        point"""
        return self.destination_point_radians((pi/2.0), meters)

    def destination_point_south(self, meters):
        """Returns a new point that is meters meters south from this
        point"""
        return self.destination_point_radians(pi, meters)

    def destination_point_west(self, meters):
        """Returns a new point that is meters meters west from this
        point"""
        return self.destination_point_radians((pi*3.0/2.0), meters)


    def distance_to_functor(self):
        """Returns a functor that receives a point and returns the
        distance to that point.
        f = point1.distance_to_functor()
        dist = f(point2)
        It may be usefull to sort points according to their distance
        to one reference point.
        """
        return lambda other: self.distance_to(other)
