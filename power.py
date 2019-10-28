import serial, time

def send_receive(ser, text):
	ser.write((text + '\r\n').encode())
	out = ''
	# let's wait 1/2 a second before reading output (let's give device time to answer)
	time.sleep(0.5)
	while ser.inWaiting() > 0:
		out += ser.read(1).decode("utf-8")
		
	return out

def start(ser):
	ser.write('start\r\n'.encode())
	response = ''

	#looking for ack or err
	temp_2 = ''
	temp_1 = ''
	temp = '' 
	while 'ack' not in (temp_2 + temp_1 + temp) and 'err' not in (temp_2 + temp_1 + temp):
		temp_2 = temp_1
		temp_1 = temp
		temp = ser.read(1).decode("utf-8")
		response += temp

	return response

def results_parser(results):
	results = results.replace('start', '')
	results = results.replace('\r', '')
	list_of_data_strings = results.split('\n') #splits on any whitespace and returns a list of the data formatted like '1204-07'
	list_of_data_floats = []
	temp_list = []
	temp_float = 0.0
	list_of_data_strings.pop(0)#first two items are ususally blank
	list_of_data_strings.pop(0)
	list_of_data_strings.pop()#last item is usually invalid
	for data in list_of_data_strings:
		if 'TimeStamp' in data:
			continue
		temp_list = data.split('-')
		temp_float = float(temp_list[0].replace('\x00', '')) * 10 ** (float(temp_list[1]) * -1)
		list_of_data_floats.append(temp_float)

	return list_of_data_floats

def get_averages_from_parsed_data(parsed_results):
	num_measurements = 0.0
	cur_sum =0.0
	for cur in parsed_results:
		num_measurements += 1.0
		cur_sum += cur
	avg_cur = cur_sum / num_measurements
	avg_power = avg_cur * 3.3
	return avg_cur, avg_power


#Function to benchmark the power of the target board
#Uses serial connection with ST PowerShield to measure power
#returns a string and the Serial object
#Check interface commands for more detail:
#https://www.st.com/content/ccc/resource/technical/document/user_manual/group0/cc/53/da/bf/54/f4/48/ee/DM00418905/files/DM00418905.pdf/jcr:content/translations/en.DM00418905.pdf
def init_power_benchmark(port = '/dev/tty.usbmodemFFFFFFFEFFFF1', #port needs to be changed depending on machine and virtual com port
					volt = 'volt 3300m', #voltage in volts, Default: 3.3 V
					freq = 'freq 100',	#frequency in Hz, Default: 100 Hz
					acq_time = 'acqtime inf', #aquisiton time in seconds, Default: infinite
					output = 'output energy', #output type, either instantaneous current or integrated energy over sample
					trig_delay = 'trigdelay 1m' #delay between target power-up and measurement start, Default: 1 ms
					):


	ser = serial.Serial()

	#serial connection configuration for the st PowerShield
	ser.port=port
	ser.baudrate=3686400 #will likely default to max baudrate of the virtual com port
	ser.parity=serial.PARITY_NONE
	ser.stopbits=serial.STOPBITS_ONE
	ser.bytesize=serial.EIGHTBITS

	#initialization and configuration parameters for the PowerShield
	paramaters = [volt, freq, acq_time, output, trig_delay]

	try:
		ser.open()
	except Exception as e:
		return "Error: error opening serial port: " + str(e), None
		#code to attempt another connection if the first path failed in case it changes
		# ser.port = 'usbmodemFFFFFFFEFFFF'
		# try:
		# 	ser.open()
		# except Exception as e:
		# 	print "error open serial port: " + str(e)
		# 	exit()

	if ser.isOpen():
		sanity_check = send_receive(ser, 'echo test')

		if not 'echo test' in sanity_check:
			ser.close()
			return 'Error: did not pass sanity check. recieved:' + sanity_check, None

		have_control = send_receive(ser, 'htc')

		if 'ack htc' in have_control:
			for param in paramaters:
				response = send_receive(ser, param)
				if 'error' in response:
					return 'Error: error recieved when sending: ' + param + ', response: ' + response, None
			results = send_receive(ser, 'start')
			
		else:
			return 'Error: take control failed, recieved: ' + have_control, None

		start_response = start(ser)
		if 'error' in start_response:
			return 'Failed to start. start_response: ' + start_response, None

		return 'start response: ' + start_response, ser


#read data from ser (serial power) for num_sec (seconds)
#returns the raw data read
def read_data(ser, num_sec):
	results = ''
	timeout = time.time() + num_sec
	while time.time() < timeout:
		results += ser.read(1).decode("utf-8") 
		
	return results

#stop data aquisition
def stop(ser):
	stop_response = send_receive(ser, 'stop') #should just be "ack stop"
	return stop_response


def main():
	print('start main')
	init_response, ser = init_power_benchmark()
	print('init finished')
	if ser is None:
		print('init response: '+ init_response)
		return
	results = read_data(ser, 10)
	print('read data complete')
	stop_response = stop(ser)
	print('stop complete')
	parsed_results = results_parser(results)
	avg_cur, avg_power = get_averages_from_parsed_data(parsed_results)
	print ('Avergae Current (Amps): ' + str(avg_cur))
	print ('Avergae Power (Watts): ' + str(avg_power))

	return

if __name__ == '__main__':
	main()