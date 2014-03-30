import urllib
import sys
import time
from xml.dom import minidom

if __name__ == "__main__":
    #Pre-define locations (bbox)
    locations = {'RN' : [48.2242, -79.0138, 48.2382, -78.9858]}
    
    #construct call to overpass api to get all nodes inside bbox
    call = "http://overpass-api.de/api/interpreter?data=node("
    try:
        location = locations[sys.argv[1]]
    except:
        print("Location doesn't exist")
    else:
        print("Fetching nodes for "+sys.argv[1])
        filename = "./nodes_"+sys.argv[1]+".xml"
        for i in range(3):
            call = call + str(location[i]) + ","
        call = call + str(location[3])
        call = call + ");out;"
        print(call)
        urllib.urlretrieve(call, filename=filename)

        xmldoc = minidom.parse(filename)
        nodelist = xmldoc.getElementsByTagName('node') 
        print("Location "+sys.argv[1]+" contains "+ str(len(nodelist)) + " nodes")
        i = 0
        user_counts = {}
        for s in nodelist :
            if (i<50) :
                id  = str(s.attributes['id'].value)
                lat = str(s.attributes['lat'].value)
                lon = str(s.attributes['lon'].value)
                print("Node " + id + ": " + lat + ", " + lon)
                opener = urllib.FancyURLopener({})
                call = "http://api.openstreetmap.org/api/0.6/node/" + str(id) + "/history"
                f = opener.open(call)
                print("bing")
                time.sleep(1.0)
                print("bang")
                data = f.read()
                opener.close()
                s_hist_doc  = minidom.parseString(data)
                s_hist_list = s_hist_doc.getElementsByTagName('node')
                for v in s_hist_list :
                    version = str(v.attributes['version'].value)
                    user    = str(v.attributes['user'].value)
                    print("version " + version + " : " + user)
                    if (user_counts.has_key(user)) :
                        user_counts[user]+=1
                    else :
                        user_counts[user] = 1
                i = i + 1
        print(user_counts)
                



#wget -O history.xml "http://api.openstreetmap.org/node/<id>/history"
