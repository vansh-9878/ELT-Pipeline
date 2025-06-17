schema={
    "bsonType":"object",
    "properties":{
        "driverId":{"bsonType": "string"},
        "name":{"bsonType": "string"},
        "dsp":{
            "bsonType": "object",
            "properties": {
                "dspId": {"bsonType": "string"},
                "name": {"bsonType": "string"},
                "region": {"bsonType": "string"},
            }
        },
        "vehicle":{
            "bsonType": "object",
            "properties": {
                "vehicleId": {"bsonType": "string"},
                "make": {"bsonType": "string"},
                "model": {"bsonType": "string"},
                "mileage": {"bsonType": "int"},
            }
        },
        "device":{
            "bsonType": "object",
            "properties": {
                "model": {"bsonType": "string"},
                "osVersion": {"bsonType": "string"}
            }
        },
        "employment":{
            "bsonType": "object",
            "properties": {
                "hireDate": {"bsonType": "date"},
                "status": {"bsonType": "string",
                           "enum": ["active", "on-leave", "terminated", "cancelled"]},
            }
        },
        "weeklyStats": {
            "bsonType": "array",
            "items": {
                "bsonType": "object",
                "properties": {
                    "weekStart": {"bsonType": "date"},
                    "weekEnd": {"bsonType": "date"},
                    "dailyRoutes":{
                        "bsonType" : "array",
                        "items":{
                            "bsonType":"object",
                            "properties":{
                                "date": {"bsonType": "date"},
                                "routeId": {"bsonType": "string"},
                                "shiftStart": {"bsonType": "string"},
                                "shiftEnd": {"bsonType": "string"},
                                "onRoadTimeMin": {"bsonType": "int"},
                                "routeScore": {"bsonType": "double"},
                                "stops": {
                                    "bsonType": "array",
                                    "items":{
                                        "bsonType":"object",
                                        "properties":{
                                            "stopNumber":{"bsonType":"int"},
                                            "address":{"bsonType":"string"},
                                            "coordinates":{
                                                "bsonType":"object",
                                                "properties":{
                                                    "lat":{"bsonType":"double"},
                                                    "lon":{"bsonType":"double"},
                                                }
                                            },
                                            "packages":{
                                                "bsonType":"array",
                                                "items":{
                                                    "bsonType":"object",
                                                    "properties":{
                                                        "trackingId":{"bsonType":"int"},
                                                        "weightKg":{"bsonType":"double"},
                                                        "dimensionsCm":{
                                                            "bsonType":"object",
                                                            "properties":{
                                                                "l":{"bsonType":"int"},
                                                                "w":{"bsonType":"int"},
                                                                "h":{"bsonType":"int"},
                                                            }
                                                        },
                                                        "hazmat":{"bsonType":"bool"}
                                                    }
                                                }
                                            },
                                            "deliveredCount":{"bsonType":"int"},
                                            "attempts":{"bsonType":"int"},
                                            "scanTime":{"bsonType":"string"},
                                        }
                                    }
                                },
                                "deliveries": {"bsonType": "int"},
                                "safety": {
                                    "bsonType": "object",
                                    "properties":{
                                        "seatBeltCompliancePct":{"bsonType":"double"},
                                        "speedingEvents":{"bsonType":"int"},
                                        "harshBrakingEvents":{"bsonType":"int"},
                                    }
                                },
                            }
                        }
                    },
                    "summary":{
                        "bsonType":"object",
                        "properties":{
                            "totalStops":{"bsonType":"int"},
                            "successfulDeliveries":{"bsonType":"int"},
                            "rescans":{"bsonType":"int"},
                            "lateDeliveries":{"bsonType":"int"},
                            "customerFeedback":{
                                "bsonType":"object",
                                "properties":{
                                    "positive":{"bsonType":"int"},
                                    "negative":{"bsonType":"int"},
                                }
                            },
                            "safety":{
                                "bsonType":"object",
                                "properties":{
                                    "avgSeatBeltCompliancePct":{"bsonType":"double"},
                                    "totalSpeedingEvents":{"bsonType":"int"},
                                    "totalHarshBrakingEvents":{"bsonType":"int"},
                                }
                            },
                            "scorecard":{
                                "bsonType":"object",
                                "properties":{
                                    "efficiencyScore":{"bsonType":"int"},
                                    "qualityScore":{"bsonType":"int"},
                                    "onTimeScore":{"bsonType":"int"},
                                    "overallScore":{"bsonType":"double"},
                                }
                            },
                        }
                    }
                }
            }
        }
    }
}


def getSchema():
    return schema