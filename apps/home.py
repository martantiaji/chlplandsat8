import streamlit as st
import geemap

def app():
    st.title("ABOUT APP")
    st.markdown(
        """
        Pemerintah melalui Rencana Pembangunan Jangka Menengah Nasional (RPJMN) 2015-2019, menyebutkan bahwa ketahanan air, termasuk 
        eksistensi danau, adalah salah satu prioritas. Danau tidak lagi difungsikan sebagai penjaga keseimbangan ekologi, akan tetapi
        juga sebagai penyedia sumber air, protein, mineral, energi, dan bahkan penambahan fungsi sebagai pariwisata guna menyokong
        pertumbuhan ekonomi masyarakat. Dalam pengelolaan tersebut terdapat 15 danau yang menjadi prioritas yaitu Danau Rawapening,
        Rawa Danau di Banten, Danau Batur, Danau Toba, Danau Kerinci, Danau Maninjau, Danau Singkarak, Danau Poso, Danau Cascade 
        Mahakam-Semayang, Danau Melintang, Danau Tondano, Danau Tempe, Danau Matano, Danau Limboto, Danau Sentarum, Danau Jempang,
        dan Danau Sentani. (Marroli, 2017)
        
        Danau Matano dan Danau Towuti adalah danau yang terletak di Kabupaten Luwu Timur, Provinsi Sulawesi Selatan. Sejarahnya,
        kedua danau tersebut pada Surat Keputusan Menteri Pertanian No.45/KPTS/UM/1/1978 pada tanggal 25 Januari 1978 ditunjuk 
        sebagai kawasan hutan lindung. Kemudian pada tahun 1979 melalui Surat No.1243/Dj/I/1979 oleh Menteri Pertanian ditunjuk
        sebagai kawasan Taman Wisata Alam(Unit Pelaksana Teknis Kementerian Lingkungan Hidup dan Kehutanan, 2018)
        
        Kedua danau ini merupakan danau yang memiliki airnya yang bersih, jernih, dan tenang. Untuk menjaga kelestarian danau tersebut,
        diperlukan adanya penelitian mengenai parameter kondisi tingkat kesuburan perairan danau. Salah satu parameter tingkat kesuburan
        perairan tersebut adalah klorofil-a. Klorofil-a adalah salah satu pigmen fotosintesis yang paling penting bagi organisme yang ada di perairan
        
        Aplikasi web ini dibuat berdasarkan script [streamlit](https://github.com/martantiaji/chlplandsat8.git) dan script yang telah dibuat pada [Google Earth engine](https://code.earthengine.google.com/f833194f9a1d3a96663153fab24ee6e2)

    """
    )
    
