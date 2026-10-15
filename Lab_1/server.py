# first of all import the socket library
import socket
import pandas as pd # in case of error, install pnadas using: pip install pandas
# Create an empty Pandas DataFrame
df = pd.DataFrame(columns=['Temp', 'Humd', 'Label']) # Label: 1 means valid, 0 means invalid
# next create a socket object
s = socket.socket()
print ("Socket successfully created")
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print ("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)
print ("socket is listening")
# Establish connection with client.
c, addr = s.accept()
print ('Got connection from', addr)
# a forever loop until we interrupt it or
# an error occurs
i = 10 # only 10 reading will be taken. Increase it to higher according to you plan.
while i>=0:
#receive data from client
    client = c.recv(1024)
    data = client.decode()
    temp = data.split(" ")[0]
    hum = data.split(" ")[1]
    new_data = {
        'Temp': temp,
        'Humd': hum,
        'Label': 1
    }
    df = df._append(new_data, ignore_index=True)
    #print it
    print(data)
    i = i - 1
    
# Close the connection with the client
c.close()
#Export data to CSV
df.to_csv('data.csv', index=False)