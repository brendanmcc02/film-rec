def convertRuntimeToHoursMinutes(runtimeInMinutes):
    hours = int(runtimeInMinutes / 60)
    minutes = runtimeInMinutes % 60

    if hours > 0:
        hours = f"{hours}h"
    else:
        hours = ""

    if minutes > 0:
        minutes = f"{minutes}m"
    else:
        minutes = ""

    return f"{hours}{minutes}"