import logging
from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

plane = []
single = True
distress = []
runway = []

@app.route('/airtrafficcontroller', methods=['POST'])
def airtraffic():
  data = request.get_json()
  logging.info("data sent for evaluation{}".format(data))
  plane, single, distress, runway, ret = readin(data)
  output = []
  if single and len(distress) == 0:
    output = single_runway(plane, ret)
  elif len(distress) == 0:
    output = multiple_runways(plane, runway, ret)
  else:
    output = distressed(plane, distress, runway, ret)

  return jsonify({"Flights":output})

def test(data):
  plane, single, distress, runway, ret = readin(data)
  output = []
  if single and len(distress) == 0:
    output = single_runway(plane, ret)
  elif len(distress) == 0:
    output = multiple_runways(plane, runway, ret)
  else:
    output = distressed(plane, distress, runway, ret)

  print(output)


def readin(data):
  # Initialization
  plane = []
  single = True
  distress = []
  runway = []

  flights = data["Flights"] # an array of dictionary
  static = data["Static"] # a dictionry
  ret = float(static["ReserveTime"]) / 60 # reserve time in minute

  if "Runways" in static:
    runway = static["Runways"]
    if len(runway) == 1:
      single = True
    else:
      single = False
  
  for flight in flights:
    Id = flight["PlaneId"]
    ts = flight["Time"]
    time = int(ts[0:2]) * 60 + int(ts[2:4]) # time string to integer
    dis = "false"
    if "Distressed" in flight:
      dis = flight["Distressed"]
      distress.append({"Id":Id, "Time":time})

    plane.append({"Id":Id, "Time":time, "Dis":dis})

  return plane, single, distress, runway, ret



def single_runway(plane, ret):
  new = sorted(plane, key=lambda k: (k["Time"], k["Id"]))
  output = []

  t = new[0]["Time"] - ret # last time
  for p in new:
    if t + ret > p["Time"]:
      # need to wait
      time = t + ret
      t += ret
    else:
      # land immediately
      time = p["Time"]
      t = p["Time"]

    temp = {}
    temp["PlaneId"] = p["Id"]
    temp["Time"] = min_to_time(time)
    output.append(temp.copy())

  return output


def multiple_runways(plane, runway, ret):
  new = sorted(plane, key=lambda k: (k["Time"], k["Id"]))
  rws = []
  output = []
  for r in runway:
    temp = {}
    temp['name'] = r
    temp["Time"] = -10
    rws.append(temp.copy())
  
  rws = sorted(rws, key = lambda k:(k['name']))
  for p in new:
      time = p["Time"]
      temp = {}
      temp["PlaneId"] = p["Id"]
      rw = min(rws, key = lambda k:k['Time'])
      if rw['Time'] + ret <= time:
          for x in rws:
              if x["Time"] + ret <= time:
                  temp["Runway"] = x['name']
                  x["Time"] = time
                  break
      else:
        rw["Time"] += ret   
        time = rw["Time"]
        temp["Runway"] = rw["name"]
        
      temp["Time"] = min_to_time(time)
      output.append(temp.copy())
  
  return sorted(output, key=lambda k: (k["Time"], k["PlaneId"]))



def distressed(plane, distress, runway, ret):
  output = []
  new = sorted(plane, key=lambda k: (k["Time"], k["Id"]))
  used = []
  rws = []
  for r in runway:
    temp = {}
    temp['name'] = r
    temp["Time"] = -10
    rws.append(temp.copy())
  rws = sorted(rws, key = lambda k:(k['name']))

  while new:
      p = new.pop(0)
      time = p["Time"]
      temp = {}
      temp["PlaneId"] = p["Id"]
      rw = min(rws, key = lambda k:k['Time'])
      if rw['Time'] + ret <= time:
        for x in rws:
          if x["Time"] + ret <= time:
            temp["Runway"] = x["name"]
            x["Time"] = time
            break
      else:
        if p["Dis"] == "true":
          # pop plane that block it and redo for them
          while used and used[0]["Time"] > p["Time"] - ret:
            p1 = output.pop()
            for rw in rws:
              if rw["name"] == p1["Runway"]:
                rw["Time"] = p["Time"] - ret
            new.insert(0, used.pop())
            # print(new)
          
          new.insert(0, p)
          continue
        else:
          rw["Time"] += ret   
          time = rw["Time"]
          temp["Runway"] = rw["name"]
        
      temp["Time"] = min_to_time(time)
      output.append(temp.copy())
      used.append(p)
      # print("new", new)
      # print("used", used)
  
    
  return sorted(output, key=lambda k: (k["Time"], k["PlaneId"]))
 


def min_to_time(time):
  a = int(time/60)
  b = int(round(time - a*60))
  return format(a, '02d') + format(b, '02d')