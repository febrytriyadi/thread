import os
import requests
import threading
import urllib.request, urllib.error, urllib.parse
import time
#import threading dan lainnnya
url = "https://apod.nasa.gov/apod/image/1901/LOmbradellaTerraFinazzi.jpg" #link gambar yang akan di download


def buildRange(value, numsplits):
    lst = []
    for i in range(numsplits):
        if i == 0:
            lst.append('%s-%s' % (i, int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
            #menambahkan elemen pada array lst
        else:
            lst.append('%s-%s' % (int(round(1 + i * value/(numsplits*1.0),0)), int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
    return lst

class SplitBufferThreads(threading.Thread):
    """ Splits the buffer to ny number of threads
        thereby, concurrently downloading through
        ny number of threads.
    """
    def __init__(self, url, byteRange):
        super(SplitBufferThreads, self).__init__()
        self.__url = url
        self.__byteRange = byteRange
        self.req = None
        #memisahkan buffer setiap thread dengan byte range tertentu
    def run(self):
        self.req = urllib.request.Request(self.__url,  headers={'Range': 'bytes=%s' % self.__byteRange})

    def getFileData(self):
        return urllib.request.urlopen(self.req).read()


def main(url=None, splitBy=3):
    start_time = time.time()#dimulai merekord waktu 
    if not url:#terminate url jika url belum ada
        print("Please Enter some url to begin download.")
        return

    fileName = url.split('/')[-1]#membagi nama file berdasarkan / nya nama file dari path url posisi paling akhir
    sizeInBytes = requests.head(url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)#mengukur besar file yang didownload
    print("%s bytes to download." % sizeInBytes)#output besar file
    if not sizeInBytes:#jika isi dalam byte kosong maka program akan selesai
        print("Size cannot be determined.")
        return

    dataLst = []#deklarasi list
    for idx in range(splitBy):#perulangan sejumlah splitby
        byteRange = buildRange(int(sizeInBytes), splitBy)[idx]#membagi byte data sesuai dengan splitby 
        bufTh = SplitBufferThreads(url, byteRange)#assign thread dengan job sesuai dari pembagian yang dilakukan pada byterange
        bufTh.start()#mulai perkejaan penguploadan
        bufTh.join()#mainthread menunggu pekerjaan childthread selesai untuk dapat mengeksekusi perkejaan lainnya
        dataLst.append(bufTh.getFileData())#append data yang sudah diunggah kedalam list

    content = b''.join(dataLst)#menggabungkan isi datalst 

    if dataLst:#jika datalst berhasil terisi maka
        if os.path.exists(fileName): #jika dalam folder memiliki nama file yang sama
            os.remove(fileName) #hapus file
        print("--- %s seconds ---" % str(time.time() - start_time))#output waktu pekerjaan
        with open(fileName, 'wb') as fh:
            fh.write(content) #penulisan konten file
        print("Finished Writing file %s" % fileName) #output selesai

if __name__ == '__main__':
main(url)#menjalankan program utama