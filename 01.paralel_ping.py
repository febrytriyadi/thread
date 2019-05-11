# import os, re dan threading
from threading import Thread
import os, re

# import time
import time

received_packages = re.compile(r"Received = (\d)")

# buat kelas ip_check
class ip_check(Thread):
    
    # fungsi __init__; init untuk assign IP dan hasil respons = -1
	def __init__ (self,ip):
		Thread.__init__(self)
		self.ip=ip
		self.status = -1
    
    # fungsi utama yang diekseskusi ketika thread berjalan
	def run(self):
        # lakukan ping dengan perintah ping -n (gunakan os.popen())
	    pingaling = os.popen("ping -n 2 "+self.ip,"r")      	
	    
	    # loop forever
	    while True:
	        # baca hasil respon setiap baris
	        line = pingaling.readline()
	        
	        # break jika tidak ada line lagi
	        if not line:
	        	break
	        # baca hasil per line dan temukan pola Received = x
	        if received_packages.findall(line) :
	            n_received = received_packages.findall(line)

	    print((self.ip , status[int(n_received[0])]))
'''	    if n_received:
	        print((status[int(n_received[0])]))
'''	            
	# fungsi untuk mengetahui status; 0 = tidak ada respon, 1 = hidup tapi ada loss, 2 = hidup
	# def statusku(bom):
	#     # 0 = tidak ada respon
	# 	if (bom == '0'):
	# 		print ("tidak ada respon")
	# 	elif (bom == '1'):
	# 		print (" ada loss")
	#     # 2 = hidup
	# 	elif (bom == '2'):
	# 		print ("hidup")
	# 	elif (bom == '-1'):
	# 		print ("seharusnya tidak terjadi")
# buat regex untuk mengetahui isi dari r"Received = (\d)"
status = ('tidak ada respon', 'ada loss', 'hidup')

# catat waktu awal
start = time.time()

# buat list untuk menampung hasil pengecekan
pinglist = []

# lakukan ping untuk 20 host
for suffix in range(20):
    # tentukan IP host apa saja yang akan di ping
    ip = "192.168.1."+str(suffix+1)
#    print (ip)

    # panggil thread untuk setiap IP
    current = ip_check(ip)
    
    # masukkan setiap IP dalam list
    pinglist.append(current)
    
    # jalankan thread
    current.start()

# untuk setiap IP yang ada di list
for el in pinglist:
    
    # tunggu hingga thread selesai
    el.join()
    
    # dapatkan hasilnya
    

# catat waktu berakhir
end = time.time()

# tampilkan selisih waktu akhir dan awal
print('waktu ping : ',end-start)
