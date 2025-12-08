// Task 3: Create the Run function
function Run() {
    // Get the data array from theJSON object loaded via script tag
    var data = theJSON.data;

    // Task 5: Call functions to find the corners
    var topLeftPoint = findTopLeft(data);
    var topRightPoint = findTopRight(data);
    var bottomLeftPoint = findBottomLeft(data);
    var bottomRightPoint = findBottomRight(data);

    // Task 6: Create an output object containing the corner points
    var boundingBox = {
        topLeft: topLeftPoint,
        topRight: topRightPoint,
        bottomLeft: bottomLeftPoint,
        bottomRight: bottomRightPoint
    };

    // Task 7: Print out the result with email
    console.log("Bounding box computed for person@tamu.edu: ");
    console.log(boundingBox);
}

// Task 4: Functions to calculate the bounding box

// Find Top Left point (Max Lat and Min Lon)
function findTopLeft(data) {
    var maxLat = null;
    var minLon = null;

    // First pass: find the max lat and min lon values
    data.forEach(element => {
        if (maxLat == null || element.lat > maxLat) {
            maxLat = element.lat;
        }
        if (minLon == null || element.lon < minLon) {
            minLon = element.lon;
        }
    });

    // Return object with the corner coordinates
    return {
        lat: maxLat,
        lon: minLon
    };
}

// Find Top Right point (Max Lat and Max Lon)
function findTopRight(data) {
    var maxLat = null;
    var maxLon = null;

    data.forEach(element => {
        if (maxLat == null || element.lat > maxLat) {
            maxLat = element.lat;
        }
        if (maxLon == null || element.lon > maxLon) {
            maxLon = element.lon;
        }
    });

    return {
        lat: maxLat,
        lon: maxLon
    };
}

// Find Bottom Left point (Min Lat and Min Lon)
function findBottomLeft(data) {
    var minLat = null;
    var minLon = null;

    data.forEach(element => {
        if (minLat == null || element.lat < minLat) {
            minLat = element.lat;
        }
        if (minLon == null || element.lon < minLon) {
            minLon = element.lon;
        }
    });

    return {
        lat: minLat,
        lon: minLon
    };
}

// Find Bottom Right point (Min Lat and Max Lon)
function findBottomRight(data) {
    var minLat = null;
    var maxLon = null;

    data.forEach(element => {
        if (minLat == null || element.lat < minLat) {
            minLat = element.lat;
        }
        if (maxLon == null || element.lon > maxLon) {
            maxLon = element.lon;
        }
    });

    return {
        lat: minLat,
        lon: maxLon
    };
}
