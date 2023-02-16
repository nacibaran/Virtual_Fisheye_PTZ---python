import time



# Sanal PTZ Acrop


# YAPILACAKLAR.


#  RE_BUİLD Fonksiyonunu overloading işlemi altına al ve değerlerden örneğin beta geldiyse sadece beta işlemiyapılsın diğer parametreler zaten sabit olduğu için 5 hesaplama yerine tek hesaplamada işlemden kurtulmuş oluruz.

#  RE_BUİLD İşlemi sonrası Tuş soruglarının içine re build fonksiyonunu ekle while her çalıştığında haritayı tekrar güncellemesin sadece sağ sola kaymaş işleminden sonra .


## Click metodları sonrası ekrandaki donma tercih sebebi şuan kamera çıkış parametresi 1080 * 1920   bu değer 720 *720 ye düşürülür ise gecikme süresi 4 e bölünür. Pixel oranımız ne kadar azalırsa click metodlarımızın da gecikmesi aynı oranda düşer.

# Kalite ve hız arasındaki seçim sonrası Manuel olarak giriş değelerini değiştirebilirz. 
# HATA ALINIRSA DVR ŞİFRESİİ EXLXEXKX


import numpy as np
import cv2
import glob
cap=cv2.VideoCapture("rtsp://192.168.1.10:554/user=admin&password=EXLXEXKX&channel=1&stream=0.sdp")
#cap=cv2.VideoCapture(0)


# Görüntü Testi için Yapılacak adımlar 
# 1.Adım 
#      Rtsp yayın üzerinden RTSP_Foto_Cek.py Çalıştırılıp fisheye fotoğraf kayıt edilcek 
#      Kaydedilen görüntü glop glop Kullanılarak Realtime verilmek yerine tek görüntü üzerinden Sanal Ptz kontrol edilcek.
#      Gerekli kütüphaneler import edilmiştir.
#      Fotoğraf üzerine yapılan işlem başarılı ise Kamera ile uyumludur. 

help_Text = '''
  'r' ve 'f' Yakınlaştırma uzaklaştirma . 
  'g' ve 't' rotasyon 
  'h' ve 'y'  Sag - Sol Kaydirma islemi
  'j' ve 'u' rotasyon
  's' Screeen Shot almak icin 

    '''


    
#images = glob.glob('C:/Users/ASUS/Desktop/fisheye_window-master/fisheye_window-master/cpp/*.png')       # Çekilen fotoğrafı koda yüklemek .

class FishEyeWindow(object):
  
    def __init__(self,):
        # Boyut parametreleri
        
        self._srcW = 1920
        self._srcH = 1280       # Görüntü boyutu 
        self._destW = 290   # 290 dan çekildi. 
        self._destH = 850                     # pencere size ayarları 
        self._al = 0
        self._be = 0
        self._th = 0
        self._R  = 960
        self._zoom = 0.5
        




    def setmap(self,beta):
        self._mapY = np.loadtxt("Betay"     +        str(beta)      +        ".txt", delimiter=",",       dtype=np.float32)
        self._mapX = np.loadtxt("BetaX"     +        str(beta)      +        ".txt", delimiter=",",       dtype=np.float32)

    def buildMap(self, alpha=None, beta=None, theta=None, R=None, zoom=None):
        # Data atamaları .
        start=time.time()
        self.setmap(beta)

        end=time.time()
        print(end-start)
    
        

    def getImage(self, img):

        output = cv2.remap(img, self._mapX, self._mapY, cv2.INTER_CUBIC) 
     
        return output

def main():
    
    ret,src_img=cap.read()
    src_size=src_img.shape[:2]

    print("Goruntuleme Oranı :",src_size)
    framespersecond= int(cap.get(cv2.CAP_PROP_FPS))   # Kameramızın Fps değerini alıyoruz ve alt satırda program çalışmadan önce print ediyoruz.

    print("FPS :{0}".format(framespersecond))



    fe = FishEyeWindow()     
    print(src_size[1],src_size[0])
    alpha = -270
    beta = 0
    theta = 270
    zoom = 0.55

    if(not(ret)):
        print("ACROP'Tan goruntu alinamiyor !!")



    fe.buildMap(alpha=alpha, beta=beta, theta=theta, zoom=zoom)     ## Gecikmeyi sağlayan arkadaş bu 

    while cap.open:          ## Görüntümüz varken döngü içine girecek.
        
        ret, src_img= cap.read()    


        if ret:
                
            src_img=cv2.resize(src_img,(1920,1080))
            result_img = fe.getImage(src_img)


            print("------------------")
            print(result_img.shape[0],result_img.shape[1])
            print("-------------------")

            
            cv2.imshow('ACROP_Panel', result_img)
            cv2.imshow('Duzelmemis',src_img)


            # Mod 3 e göre multi thread ataması yapılcak re build fonksiyonunu 3 işlemci çekirdeği aynanda çalışacak ekrana basıaln görüntü thread numarasına göre belirlenecek.
            key = cv2.waitKey(1)

            if key == 27:
                break
            elif ord('r') == key:
                 zoom -= 0.1
                 fe.buildMap(zoom=zoom)     ## Gecikmeyi sağlayan arkadaş bu 

            elif ord('f') == key:
                zoom += 0.1
                fe.buildMap( zoom=zoom)     ## Gecikmeyi sağlayan arkadaş bu 

            elif ord('h') == key and beta <180 :
                beta += 30

                fe.buildMap(beta=beta)     ## Gecikmeyi sağlayan arkadaş bu 

            elif ord('y') == key and beta >-180:
                
                beta -= 30

                fe.buildMap(beta=beta)     ## Gecikmeyi sağlayan arkadaş bu 

            
            elif ord('s') == key:
                print("Ekran Goruntusu alindi.")
                cv2.imwrite('./Foto_Kayıt_Elektroland_ACROP.png', result_img)
            

        else:
            print("Kameraya Ulaşılamıyor.")

    cap.release()    
    cv2.destroyAllWindows()
    

if __name__ == '__main__':

        print (help_Text)  #terminale hangi button clickleri  ne yapar bunu yazdıralım . 
        main()   
