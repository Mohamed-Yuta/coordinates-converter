import math ;
from model.cartesien import Cartesien # type: ignore
from model.geographicCord import GeographicCord # type: ignore
class Converter:
    def __init__(self) -> None:
        self.a = 6378137.0  # Semi-major axis (equatorial radius) in meters
        self.b = 6356752.3142  # Semi-minor axis (polar radius) in meters
        self.eSq = 1 - (self.b**2 / self.a**2)  # Square of eccentricityt

    def converterToCartesien(self ,objet : GeographicCord):
        # Convert latitude and longitude from degrees to radians
        latRad = math.radians(objet.latitude)
        lonRad = math.radians(objet.longtitude)

        # Calculate the prime vertical radius of curvature
        N = self.a / math.sqrt(1 - self.eSq * math.sin(latRad)**2)

        # Calculate Cartesian coordinates
        X = (N + objet.altitude) * math.cos(latRad) * math.cos(lonRad)
        Y = (N + objet.altitude) * math.cos(latRad) * math.sin(lonRad)
        Z = ((1 - self.eSq) * N + objet.altitude) * math.sin(latRad)
        print(X )
        print(Y )
        print(Z )
        return X, Y, Z
    
    def converterToGeographic(self, cartesian):
        # Extract X, Y, Z
        X, Y, Z = cartesian.X, cartesian.Y, cartesian.Z

        # Longitude calculation
        longitude = math.atan2(Y, X)

        # Iterative calculation for latitude
        p = math.sqrt(X**2 + Y**2)
        theta = math.atan2(Z * self.a, p * self.b)

        latitude = math.atan2(Z + (self.eSq * self.b * math.sin(theta)**3),
                              p - (self.eSq * self.a * math.cos(theta)**3))

        # Radius of curvature in the prime vertical
        N = self.a / math.sqrt(1 - self.eSq * math.sin(latitude)**2)

        # Altitude calculation
        altitude = (p / math.cos(latitude)) - N

        # Convert radians back to degrees for latitude and longitude
        latitude = math.degrees(latitude)
        longitude = math.degrees(longitude)

        return latitude, longitude, altitude

    def initiaGeographic(self):
        objet = GeographicCord(1.5,1.3,3.5)
        return objet