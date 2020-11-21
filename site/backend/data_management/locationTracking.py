from math import asin, cos, pi, sin, atan2, radians, degrees

rEarth = 20902230.971129  # Earth's average radius in km


def pointRadialDistance(lat1, lon1, bearing, distance):
    rlat1 = radians(lat1)
    rlon1 = radians(lon1)
    rbearing = radians(bearing)
    rdistance = distance / rEarth  # normalize linear distance to radian angle

    rlat = asin(sin(rlat1) * cos(rdistance) + cos(rlat1)
                * sin(rdistance) * cos(rbearing))

    rlon = rlon1 + atan2(sin(rbearing) * sin(rdistance) *
                         cos(rlat1), cos(rdistance) - sin(rlat1) * sin(rlat))

    lat = degrees(rlat)
    lon = degrees(rlon)
    return (lat, lon)


def main():
    print("lat1 \t lon1 \t\t bear \t dist \t\t lat2 \t\t lon2")
    testcases = []
    testcases.append((0, 0, 0, 3280.84))
    testcases.append((0, 0, 90, 3280.84))
    testcases.append((0, 0, 0, 328084))
    testcases.append((0, 0, 90, 328084))
    testcases.append((49.25705, -123.140259, 225, 3280.84))
    testcases.append((49.25705, -123.140259, 225, 328084))
    testcases.append((49.25705, -123.140259, 225, 3280840))
    for lat1, lon1, bear, dist in testcases:
        (lat, lon) = pointRadialDistance(lat1, lon1, bear, dist)
        print("%6.2f \t %6.2f \t %4.1f \t %6.1f \t %6.2f \t %6.2f" %
              (lat1, lon1, bear, dist, lat, lon))


if __name__ == "__main__":
    main()
