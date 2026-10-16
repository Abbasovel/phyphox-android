#!/usr/bin/env python3
"""Generates the 4 museum demo experiments (Azerbaijani) for the Elm Lab demo app.
Icons and the acoustic-stopwatch analysis are taken from the phyphox experiments (GPL-3.0).
Usage: python3 make_demo_experiments.py <path to phyphox-experiments checkout>"""
import re, sys, pathlib
SRC = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(__file__).parent / "demo_experiments"
def icon(name): return re.search(r'<icon[^>]*>.*?</icon>|<icon[^>]*/>', (SRC/name).read_text(encoding="utf-8"), re.S).group(0)
CAT = "Muzey nümayişi"
HEAD = '<phyphox version="1.20" locale="az">\n  <title>{t}</title>\n  <category>' + CAT + '</category>\n  {i}\n  <description>{d}</description>\n'

pressure = HEAD.format(t="Hava təzyiqi: baş və ayaq", i=icon("pressure.phyphox"), d="""Hava sütunu da çəkiyə malikdir: aşağıda təzyiq yuxarıdakından böyükdür. Boyunuz qədər (1,7 m) hündürlük fərqi təzyiqi təxminən 20 Pa (0,2 hPa) dəyişir: Δp = ρ·g·h = 1,2 · 9,81 · 1,7 ≈ 20 Pa.

Necə: telefonu yerə qoyun, ölçməni başladın, 20–30 s gözləyin (istənilən an «Sıfırla» düyməsi ilə indiki səviyyəni sıfır götürə bilərsiniz). Sonra telefonu başınız hündürlüyünə qaldırıb yenə 20–30 s tərpətməyin. Qrafikdə ~20 Pa-lıq pillə görünəcək.""") + """  <data-containers>
    <container size="0">pressure</container>
    <container size="0">p_time</container>
    <container size="1">p0</container>
    <container size="0">dp</container>
    <container size="0">dh</container>
  </data-containers>
  <input>
    <sensor type="pressure" rate="2" average="true">
      <output component="x">pressure</output>
      <output component="t">p_time</output>
    </sensor>
  </input>
  <views>
    <view label="Ölçmə">
      <value label="Təzyiq fərqi Δp" size="3" precision="1" unit="Pa">
        <input>dp</input>
      </value>
      <value label="Hündürlük fərqi Δh" size="2" precision="2" unit="m">
        <input>dh</input>
      </value>
      <button label="Sıfırla (bu səviyyə = 0)">
        <input type="empty"/>
        <output>pressure</output>
        <input type="empty"/>
        <output>p_time</output>
        <input type="empty"/>
        <output>dp</output>
        <input type="empty"/>
        <output>dh</output>
      </button>
      <graph label="Təzyiq fərqi (başlanğıca nəzərən)" timeOnX="true" labelX="t" unitX="s" labelY="Δp" unitY="Pa" partialUpdate="true">
        <input axis="x">p_time</input>
        <input axis="y" lineWidth="2">dp</input>
      </graph>
      <value label="Atmosfer təzyiqi" size="1" precision="2" unit="hPa">
        <input>pressure</input>
      </value>
      <info label="Telefonu yerdən başınızın hündürlüyünə qaldırın: Δp ≈ −20 Pa, Δh ≈ +1,7 m. Ölçmə zamanı telefonu tərpətməyin və qapıları açmayın."/>
    </view>
  </views>
  <analysis sleep="0.2">
    <first>
      <input clear="false">pressure</input>
      <output>p0</output>
    </first>
    <formula formula="([1_]-[2])*100">
      <input clear="false">pressure</input>
      <input clear="false">p0</input>
      <output>dp</output>
    </formula>
    <formula formula="[1_]*-0.0849473">
      <input clear="false">dp</input>
      <output>dh</output>
    </formula>
  </analysis>
  <export>
    <set name="Təzyiq">
      <data name="Vaxt (s)">p_time</data>
      <data name="Təzyiq (hPa)">pressure</data>
      <data name="Δp (Pa)">dp</data>
      <data name="Δh (m)">dh</data>
    </set>
  </export>
</phyphox>
"""

weightless = HEAD.format(t="Çəkisizlik", i=icon("accelerometer.phyphox"), d="""Cisim əldən çıxdığı andan yerə düşənə qədər çəkisizlik halındadır: həm qalxanda, həm ən yuxarı nöqtədə, həm də enəndə. Ona yalnız ağırlıq qüvvəsi təsir edir, dayaq yoxdur.

Akselerometr dayaq qüvvəsinin yaratdığı təcili ölçür. Telefon masada uzananda |a| ≈ 9,8 m/s² (1 g), sərbəst uçuşda isə |a| ≈ 0.

Necə: ölçməni başladın və telefonu yumşaq yatağın və ya döşəyin üzərinə 30–50 sm yuxarı atın. Qrafikdə bütün uçuş boyu |a| ≈ 0 olan "çuxur" görünəcək.""") + """  <data-containers>
    <container size="0">accX</container>
    <container size="0">accY</container>
    <container size="0">accZ</container>
    <container size="0">acc_time</container>
    <container size="0">elmlab_watch</container>
    <container>elmlab_threshold</container>
    <container>elmlab_delay</container>
    <container size="1">a_last</container>
    <container size="1" init="5">fl_threshold</container>
    <container size="1" init="0">fl_intensity</container>
    <container size="1" init="15">fl_frequency</container>
    <container size="1" init="0.5">fl_duty</container>
  </data-containers>
  <input>
    <sensor type="accelerometer" rate="0">
      <output component="x">accX</output>
      <output component="y">accY</output>
      <output component="z">accZ</output>
      <output component="t">acc_time</output>
    </sensor>
  </input>
  <output>
    <flashlight>
      <input parameter="intensity">fl_intensity</input>
      <input parameter="frequency">fl_frequency</input>
      <input parameter="dutycycle">fl_duty</input>
    </flashlight>
  </output>
  <views>
    <view label="Ölçmə">
      <value label="Hiss olunan təcil |a|" size="3" precision="1" unit="m/s²">
        <input>elmlab_watch</input>
      </value>
      <value label="Vəziyyət" size="2">
        <input>elmlab_watch</input>
        <map max="2">ÇƏKİSİZLİK</map>
        <map>dayaq var</map>
      </value>
      <graph label="|a| zamandan asılı olaraq" timeOnX="true" labelX="t" unitX="s" labelY="|a|" unitY="m/s²" partialUpdate="true">
        <input axis="x">acc_time</input>
        <input axis="y" lineWidth="2">elmlab_watch</input>
      </graph>
      <edit label="Fənər həddi (0 = söndür)" unit="m/s²" default="5" signed="false" decimal="true">
        <output>fl_threshold</output>
      </edit>
      <info label="|a| fənər həddindən aşağı olanda telefonun fənəri maksimal parlaqlıqla 15 Hz tezliklə yanıb-sönür."/>
      <edit label="Avto-pauza həddi (0 = söndür)" unit="m/s²" default="2" signed="false" decimal="true">
        <output>elmlab_threshold</output>
      </edit>
      <edit label="Pauzadan əvvəl gecikmə" unit="s" default="2" signed="false" decimal="true">
        <output>elmlab_delay</output>
      </edit>
      <info label="|a| avto-pauza həddinə düşəndən «gecikmə» qədər sonra ölçmə avtomatik dayanır və qrafik donur (fənər də sönür). Gecikmə 0 olsa, ölçmə dərhal dayanar və fənər yanmağa macal tapmaz. Davam etmək üçün ▶ düyməsinə basın."/>
      <info label="9,8 m/s² = adi çəki (1 g). Atma anında |a| 9,8-dən böyük olur, uçuşda isə 0-a düşür. Telefonu yalnız yumşaq səthin üzərinə atın!"/>
    </view>
  </views>
  <analysis sleep="0.05">
    <formula formula="sqrt([1_]*[1_]+[2_]*[2_]+[3_]*[3_])">
      <input clear="false">accX</input>
      <input clear="false">accY</input>
      <input clear="false">accZ</input>
      <output>elmlab_watch</output>
    </formula>
    <formula formula="sqrt([1_]*[1_]+[2_]*[2_]+[3_]*[3_])">
      <input clear="false">accX</input>
      <input clear="false">accY</input>
      <input clear="false">accZ</input>
      <output>a_last</output>
    </formula>
    <formula formula="heaviside([2]-[1])*heaviside([2]-0.000001)">
      <input keep="true">a_last</input>
      <input keep="true">fl_threshold</input>
      <output>fl_intensity</output>
    </formula>
  </analysis>
  <export>
    <set name="Təcil">
      <data name="Vaxt (s)">acc_time</data>
      <data name="ax (m/s²)">accX</data>
      <data name="ay (m/s²)">accY</data>
      <data name="az (m/s²)">accZ</data>
      <data name="|a| (m/s²)">elmlab_watch</data>
    </set>
  </export>
</phyphox>
"""

car = HEAD.format(t="Avtomobilin təcili", i=icon("linear_accelerometer.phyphox"), d="""Avtomobil sürətini artıranda telefon da onunla birlikdə təcil alır. Xətti akselerometr ağırlıq qüvvəsi çıxılmış təcili ölçür.

Necə: telefonu tutacaqda şaquli vəziyyətdə, ekranı sürücüyə tərəf bərkidin. Avtomobil dayanarkən ölçməni başladın, sonra təcillənin. "İrəli təcil" müsbət, əyləc mənfi göstəriləcək. Sürət GPS ilə ölçülür.

Yoxlama: 0–100 km/s vaxtı t olarsa, orta təcil = 27,8 / t m/s².

Təhlükəsizlik: telefonla sürücü yox, sərnişin məşğul olsun; ölçməni boş və bağlı ərazidə aparın.""") + """  <data-containers>
    <container size="0">ax</container>
    <container size="0">ay</container>
    <container size="0">az</container>
    <container size="0">a_time</container>
    <container size="0">af</container>
    <container size="1">afmax</container>
    <container size="0">v</container>
    <container size="0">vkmh</container>
    <container size="0">v_time</container>
    <container size="1">status</container>
  </data-containers>
  <input>
    <sensor type="linear_acceleration" rate="50" average="true">
      <output component="x">ax</output>
      <output component="y">ay</output>
      <output component="z">az</output>
      <output component="t">a_time</output>
    </sensor>
    <location>
      <output component="v">v</output>
      <output component="t">v_time</output>
      <output component="status">status</output>
    </location>
  </input>
  <views>
    <view label="Təcil">
      <value label="İrəli təcil" size="3" precision="2" unit="m/s²">
        <input>af</input>
      </value>
      <value label="İrəli təcil" size="2" precision="2" factor="0.1019716" unit="g">
        <input>af</input>
      </value>
      <value label="Maksimum təcil" size="2" precision="2" unit="m/s²">
        <input>afmax</input>
      </value>
      <graph label="İrəli təcil" timeOnX="true" labelX="t" unitX="s" labelY="a" unitY="m/s²" partialUpdate="true">
        <input axis="x">a_time</input>
        <input axis="y" lineWidth="2">af</input>
      </graph>
    </view>
    <view label="Sürət (GPS)">
      <value label="GPS">
        <input>status</input>
        <map max="-1">söndürülüb</map>
        <map min="0">aktivdir</map>
      </value>
      <value label="Sürət" size="3" precision="1" unit="km/s">
        <input>vkmh</input>
      </value>
      <graph label="Sürət" timeOnX="true" labelX="t" unitX="s" labelY="v" unitY="km/s" partialUpdate="true">
        <input axis="x">v_time</input>
        <input axis="y" lineWidth="2">vkmh</input>
      </graph>
    </view>
  </views>
  <analysis sleep="0.1">
    <formula formula="[1_]*-1">
      <input clear="false">az</input>
      <output>af</output>
    </formula>
    <max>
      <input as="y" clear="false">af</input>
      <output as="max">afmax</output>
    </max>
    <formula formula="[1_]*3.6">
      <input clear="false">v</input>
      <output>vkmh</output>
    </formula>
  </analysis>
  <export>
    <set name="Təcil">
      <data name="Vaxt (s)">a_time</data>
      <data name="İrəli təcil (m/s²)">af</data>
      <data name="ax (m/s²)">ax</data>
      <data name="ay (m/s²)">ay</data>
      <data name="az (m/s²)">az</data>
    </set>
    <set name="Sürət">
      <data name="Vaxt (s)">v_time</data>
      <data name="Sürət (km/s)">vkmh</data>
    </set>
  </export>
</phyphox>
"""

# 4. speed of sound: acoustic stopwatch analysis + two-phone formula
st = (SRC/"acoustic_stopwatch.phyphox").read_text(encoding="utf-8")
containers = re.search(r'<data-containers>(.*?)</data-containers>', st, re.S).group(1)
analysis = re.search(r'(<analysis[^>]*>)(.*?)</analysis>', st, re.S)
inp = re.search(r'<input>\s*<audio>.*?</input>', st, re.S).group(0)
sound = HEAD.format(t="Səsin sürəti", i=icon("acoustic_stopwatch.phyphox"), d="""İki telefon zalda bir-birindən d məsafədə (10–15 m) qoyulur, hər ikisində bu təcrübə işə salınır.
1) A telefonunun yanında bir nəfər əl çalır: hər iki saniyəölçən işə düşür, B-dəki bir az gec.
2) B telefonunun yanında ikinci nəfər əl çalır: hər iki saniyəölçən dayanır, A-dakı bir az gec.
Səs məsafəni iki dəfə qət etdiyindən: v = 2d / (t_A − t_B). Reaksiya vaxtı nəticəyə təsir etmir.

Telefonlardan birində d məsafəsini və digər telefonun göstərdiyi vaxtı daxil edin, səsin sürəti hesablanacaq. 20 °C-də gözlənilən: 343 m/s.""") + f"""  <data-containers>{containers}    <container clearGroup="Settings">d_m</container>
    <container clearGroup="Settings">t_other</container>
    <container clearGroup="Settings">temp_c</container>
    <container>v_sound</container>
    <container>v_theory</container>
  </data-containers>
  {inp}
  <views>
    <view label="Ölçmə">
      <value label="Bu telefonun vaxtı" size="3" precision="3" unit="s">
        <input>dt01</input>
      </value>
      <button label="Sıfırla">
        <input type="empty"/>
        <output>events</output>
        <input type="value">0</input>
        <output>i</output>
      </button>
      <separator height="1"/>
      <edit label="Telefonlar arası məsafə d" unit="m" default="10" signed="false">
        <output>d_m</output>
      </edit>
      <edit label="Digər telefonun vaxtı" unit="s" default="0" signed="false" decimal="true">
        <output>t_other</output>
      </edit>
      <value label="Səsin sürəti" size="3" precision="0" unit="m/s">
        <input>v_sound</input>
      </value>
      <separator height="1"/>
      <edit label="Havanın temperaturu" unit="°C" default="20" signed="true" decimal="true">
        <output>temp_c</output>
      </edit>
      <value label="Gözlənilən (nəzəri)" size="2" precision="0" unit="m/s">
        <input>v_theory</input>
      </value>
      <separator height="1"/>
      <edit label="Həssaslıq həddi" unit="" default="0.2" signed="false" min="0" max="1">
        <output>threshold</output>
      </edit>
      <edit label="Minimum fasilə" unit="s" default="0.1" signed="false">
        <output>mindelay</output>
      </edit>
      <info label="Zalda əks-səda saniyəölçəni vaxtından əvvəl dayandırırsa, həssaslıq həddini artırın. Əl çalmaları qısa və kəskin olsun."/>
    </view>
  </views>
  {analysis.group(1)}{analysis.group(2)}    <formula formula="sqrt((2*[1]/([2]-[3]))^2)*heaviside([3]-0.0000001)/heaviside([3]-0.0000001)">
      <input keep="true">d_m</input>
      <input clear="false">dt01</input>
      <input keep="true">t_other</input>
      <output>v_sound</output>
    </formula>
    <formula formula="331.3+0.606*[1]">
      <input keep="true">temp_c</input>
      <output>v_theory</output>
    </formula>
  </analysis>
</phyphox>
"""
from xml.sax.saxutils import escape as _e
TR = {
 "Hava təzyiqi: baş və ayaq": "Hava basıncı: baş ve ayak", "Ölçmə": "Ölçüm", "Təzyiq fərqi Δp": "Basınç farkı Δp",
 "Hündürlük fərqi Δh": "Yükseklik farkı Δh", "Sıfırla (bu səviyyə = 0)": "Sıfırla (bu seviye = 0)",
 "Təzyiq fərqi (başlanğıca nəzərən)": "Basınç farkı (başlangıca göre)", "Atmosfer təzyiqi": "Atmosfer basıncı",
 "Telefonu yerdən başınızın hündürlüyünə qaldırın: Δp ≈ −20 Pa, Δh ≈ +1,7 m. Ölçmə zamanı telefonu tərpətməyin və qapıları açmayın.":
   "Telefonu yerden başınızın yüksekliğine kaldırın: Δp ≈ −20 Pa, Δh ≈ +1,7 m. Ölçüm sırasında telefonu oynatmayın ve kapıları açmayın.",
 "Təzyiq": "Basınç", "Vaxt (s)": "Zaman (s)", "Təzyiq (hPa)": "Basınç (hPa)",
 "Çəkisizlik": "Ağırlıksızlık", "Hiss olunan təcil |a|": "Hissedilen ivme |a|", "Vəziyyət": "Durum",
 "ÇƏKİSİZLİK": "AĞIRLIKSIZLIK", "dayaq var": "destek var", "|a| zamandan asılı olaraq": "Zamana göre |a|",
 "Fənər həddi (0 = söndür)": "Fener eşiği (0 = kapalı)",
 "|a| fənər həddindən aşağı olanda telefonun fənəri maksimal parlaqlıqla 15 Hz tezliklə yanıb-sönür.":
   "|a| fener eşiğinin altına düştüğünde telefonun feneri en yüksek parlaklıkta 15 Hz frekansla yanıp söner.",
 "Avto-pauza həddi (0 = söndür)": "Otomatik duraklatma eşiği (0 = kapalı)", "Pauzadan əvvəl gecikmə": "Duraklatmadan önce gecikme",
 "|a| avto-pauza həddinə düşəndən «gecikmə» qədər sonra ölçmə avtomatik dayanır və qrafik donur (fənər də sönür). Gecikmə 0 olsa, ölçmə dərhal dayanar və fənər yanmağa macal tapmaz. Davam etmək üçün ▶ düyməsinə basın.":
   "|a| otomatik duraklatma eşiğine düştükten «gecikme» kadar sonra ölçüm otomatik olarak durur ve grafik donar (fener de söner). Gecikme 0 ise ölçüm hemen durur ve fener yanmaya fırsat bulamaz. Devam etmek için ▶ düğmesine basın.",
 "9,8 m/s² = adi çəki (1 g). Atma anında |a| 9,8-dən böyük olur, uçuşda isə 0-a düşür. Telefonu yalnız yumşaq səthin üzərinə atın!":
   "9,8 m/s² = normal ağırlık (1 g). Atış anında |a| 9,8'den büyüktür, uçuşta ise 0'a düşer. Telefonu yalnızca yumuşak bir yüzeyin üzerine atın!",
 "Təcil": "İvme", "Avtomobilin təcili": "Otomobilin ivmesi", "İrəli təcil": "İleri ivme", "Maksimum təcil": "Maksimum ivme",
 "Sürət (GPS)": "Hız (GPS)", "söndürülüb": "kapalı", "aktivdir": "etkin", "Sürət": "Hız",
 "İrəli təcil (m/s²)": "İleri ivme (m/s²)", "Sürət (km/s)": "Hız (km/sa)",
 "Səsin sürəti": "Sesin hızı", "Bu telefonun vaxtı": "Bu telefonun süresi", "Sıfırla": "Sıfırla",
 "Telefonlar arası məsafə d": "Telefonlar arası mesafe d", "Digər telefonun vaxtı": "Diğer telefonun süresi",
 "Havanın temperaturu": "Hava sıcaklığı", "Gözlənilən (nəzəri)": "Beklenen (teorik)", "Həssaslıq həddi": "Hassasiyet eşiği",
 "Minimum fasilə": "Minimum aralık",
 "Zalda əks-səda saniyəölçəni vaxtından əvvəl dayandırırsa, həssaslıq həddini artırın. Əl çalmaları qısa və kəskin olsun.":
   "Salondaki yankı kronometreyi erken durduruyorsa hassasiyet eşiğini artırın. El çırpmaları kısa ve keskin olsun.",
}
TR_DESC = {
 "1_pressure.phyphox": """Havanın da ağırlığı vardır: aşağıda basınç yukarıdakinden büyüktür. Boyunuz kadar (1,7 m) yükseklik farkı basıncı yaklaşık 20 Pa (0,2 hPa) değiştirir: Δp = ρ·g·h = 1,2 · 9,81 · 1,7 ≈ 20 Pa.

Nasıl: telefonu yere koyun, ölçümü başlatın, 20–30 s bekleyin (istediğiniz an «Sıfırla» düğmesiyle mevcut seviyeyi sıfır kabul edebilirsiniz). Sonra telefonu başınızın yüksekliğine kaldırıp yine 20–30 s oynatmayın. Grafikte ~20 Pa'lık bir basamak görünecek.""",
 "2_weightless.phyphox": """Cisim elden çıktığı andan yere düşene kadar ağırlıksızdır: yükselirken, en üst noktada ve inerken. Ona yalnızca yerçekimi etki eder, destek yoktur.

İvmeölçer, destek kuvvetinin oluşturduğu ivmeyi ölçer. Telefon masada dururken |a| ≈ 9,8 m/s² (1 g), serbest uçuşta ise |a| ≈ 0.

Nasıl: ölçümü başlatın ve telefonu yumuşak bir yatağın veya şiltenin üzerine 30–50 cm yukarı atın. Grafikte tüm uçuş boyunca |a| ≈ 0 olan bir «çukur» görünecek.""",
 "3_car.phyphox": """Otomobil hızlanırken telefon da onunla birlikte ivmelenir. Doğrusal ivmeölçer, yerçekimi çıkarılmış ivmeyi ölçer.

Nasıl: telefonu tutucuda dikey olarak, ekranı sürücüye dönük şekilde sabitleyin. Otomobil dururken ölçümü başlatın, sonra hızlanın. «İleri ivme» pozitif, fren negatif gösterilir. Hız GPS ile ölçülür.

Kontrol: 0–100 km/sa süresi t ise ortalama ivme = 27,8 / t m/s².

Güvenlik: telefonla sürücü değil yolcu ilgilensin; ölçümü boş ve kapalı bir alanda yapın.""",
 "4_sound.phyphox": """İki telefon salonda birbirinden d mesafede (10–15 m) konur, ikisinde de bu deney başlatılır.
1) A telefonunun yanında biri el çırpar: iki kronometre de başlar, B'deki biraz geç.
2) B telefonunun yanında ikinci kişi el çırpar: iki kronometre de durur, A'daki biraz geç.
Ses mesafeyi iki kez kat ettiği için: v = 2d / (t_A − t_B). Tepki süresi sonucu etkilemez.

Telefonlardan birinde d mesafesini ve diğer telefonun gösterdiği süreyi girin, sesin hızı hesaplanır. 20 °C'de beklenen: 343 m/s.""",
}
TR_TITLE = {"1_pressure.phyphox": "Hava basıncı: baş ve ayak", "2_weightless.phyphox": "Ağırlıksızlık", "3_car.phyphox": "Otomobilin ivmesi", "4_sound.phyphox": "Sesin hızı"}
import re as _re
RU = {
 "Hava təzyiqi: baş və ayaq": "Давление воздуха: голова и ноги", "Ölçmə": "Измерение", "Təzyiq fərqi Δp": "Разность давлений Δp",
 "Hündürlük fərqi Δh": "Разность высот Δh", "Sıfırla (bu səviyyə = 0)": "Сбросить (этот уровень = 0)",
 "Təzyiq fərqi (başlanğıca nəzərən)": "Разность давлений (относительно начала)", "Atmosfer təzyiqi": "Атмосферное давление",
 "Telefonu yerdən başınızın hündürlüyünə qaldırın: Δp ≈ −20 Pa, Δh ≈ +1,7 m. Ölçmə zamanı telefonu tərpətməyin və qapıları açmayın.":
   "Поднимите телефон с пола на высоту головы: Δp ≈ −20 Па, Δh ≈ +1,7 м. Во время измерения не двигайте телефон и не открывайте двери.",
 "Təzyiq": "Давление", "Vaxt (s)": "Время (с)", "Təzyiq (hPa)": "Давление (гПа)",
 "Çəkisizlik": "Невесомость", "Hiss olunan təcil |a|": "Ощущаемое ускорение |a|", "Vəziyyət": "Состояние",
 "ÇƏKİSİZLİK": "НЕВЕСОМОСТЬ", "dayaq var": "есть опора", "|a| zamandan asılı olaraq": "|a| в зависимости от времени",
 "Fənər həddi (0 = söndür)": "Порог фонарика (0 = выкл.)",
 "|a| fənər həddindən aşağı olanda telefonun fənəri maksimal parlaqlıqla 15 Hz tezliklə yanıb-sönür.":
   "Когда |a| ниже порога фонарика, фонарик телефона мигает на максимальной яркости с частотой 15 Гц.",
 "Avto-pauza həddi (0 = söndür)": "Порог автопаузы (0 = выкл.)", "Pauzadan əvvəl gecikmə": "Задержка перед паузой",
 "|a| avto-pauza həddinə düşəndən «gecikmə» qədər sonra ölçmə avtomatik dayanır və qrafik donur (fənər də sönür). Gecikmə 0 olsa, ölçmə dərhal dayanar və fənər yanmağa macal tapmaz. Davam etmək üçün ▶ düyməsinə basın.":
   "Через время «задержки» после того, как |a| опустится до порога автопаузы, измерение автоматически останавливается и график замирает (фонарик гаснет). При задержке 0 измерение остановится сразу, и фонарик не успеет загореться. Чтобы продолжить, нажмите ▶.",
 "9,8 m/s² = adi çəki (1 g). Atma anında |a| 9,8-dən böyük olur, uçuşda isə 0-a düşür. Telefonu yalnız yumşaq səthin üzərinə atın!":
   "9,8 м/с² = обычный вес (1 g). В момент броска |a| больше 9,8, а в полёте падает до 0. Бросайте телефон только на мягкую поверхность!",
 "Təcil": "Ускорение", "Avtomobilin təcili": "Ускорение автомобиля", "İrəli təcil": "Ускорение вперёд", "Maksimum təcil": "Максимальное ускорение",
 "Sürət (GPS)": "Скорость (GPS)", "söndürülüb": "выключен", "aktivdir": "активен", "Sürət": "Скорость",
 "İrəli təcil (m/s²)": "Ускорение вперёд (м/с²)", "Sürət (km/s)": "Скорость (км/ч)",
 "Səsin sürəti": "Скорость звука", "Bu telefonun vaxtı": "Время этого телефона", "Sıfırla": "Сбросить",
 "Telefonlar arası məsafə d": "Расстояние между телефонами d", "Digər telefonun vaxtı": "Время другого телефона",
 "Havanın temperaturu": "Температура воздуха", "Gözlənilən (nəzəri)": "Ожидаемое (теоретическое)", "Həssaslıq həddi": "Порог чувствительности",
 "Minimum fasilə": "Минимальный интервал",
 "Zalda əks-səda saniyəölçəni vaxtından əvvəl dayandırırsa, həssaslıq həddini artırın. Əl çalmaları qısa və kəskin olsun.":
   "Если эхо в зале останавливает секундомер раньше времени, увеличьте порог чувствительности. Хлопки должны быть короткими и резкими.",
}
RU_TITLE = {"1_pressure.phyphox": "Давление воздуха: голова и ноги", "2_weightless.phyphox": "Невесомость", "3_car.phyphox": "Ускорение автомобиля", "4_sound.phyphox": "Скорость звука"}
RU_DESC = {
 "1_pressure.phyphox": """Воздух тоже имеет вес: внизу давление больше, чем вверху. Разница высот, равная вашему росту (1,7 м), меняет давление примерно на 20 Па (0,2 гПа): Δp = ρ·g·h = 1,2 · 9,81 · 1,7 ≈ 20 Па.

Как: положите телефон на пол, запустите измерение, подождите 20–30 с (в любой момент кнопкой «Сбросить» можно принять текущий уровень за ноль). Затем поднимите телефон на высоту головы и снова не двигайте 20–30 с. На графике появится ступенька ~20 Па.""",
 "2_weightless.phyphox": """Тело невесомо с момента, когда оно покидает руку, и до падения: при подъёме, в верхней точке и при спуске. На него действует только сила тяжести, опоры нет.

Акселерометр измеряет ускорение, создаваемое силой опоры. Когда телефон лежит на столе, |a| ≈ 9,8 м/с² (1 g), а в свободном полёте |a| ≈ 0.

Как: запустите измерение и подбросьте телефон на 30–50 см над мягкой кроватью или матрасом. На графике весь полёт будет «ямой» с |a| ≈ 0.""",
 "3_car.phyphox": """Когда автомобиль разгоняется, телефон ускоряется вместе с ним. Линейный акселерометр измеряет ускорение без силы тяжести.

Как: закрепите телефон в держателе вертикально, экраном к водителю. Запустите измерение, пока автомобиль стоит, затем разгоняйтесь. «Ускорение вперёд» положительно, торможение отрицательно. Скорость измеряется по GPS.

Проверка: если время разгона 0–100 км/ч равно t, среднее ускорение = 27,8 / t м/с².

Безопасность: с телефоном работает пассажир, а не водитель; измеряйте на пустой закрытой площадке.""",
 "4_sound.phyphox": """Два телефона ставят в зале на расстоянии d (10–15 м) друг от друга, на обоих запускают этот эксперимент.
1) Рядом с телефоном A кто-то хлопает: оба секундомера запускаются, на B чуть позже.
2) Рядом с телефоном B второй человек хлопает: оба секундомера останавливаются, на A чуть позже.
Звук проходит расстояние дважды, поэтому: v = 2d / (t_A − t_B). Время реакции на результат не влияет.

Введите на одном из телефонов расстояние d и время, показанное другим телефоном, — скорость звука будет вычислена. При 20 °C ожидается 343 м/с.""",
}
EN = {
 "Hava təzyiqi: baş və ayaq": "Air pressure: head and feet", "Ölçmə": "Measurement", "Təzyiq fərqi Δp": "Pressure difference Δp",
 "Hündürlük fərqi Δh": "Height difference Δh", "Sıfırla (bu səviyyə = 0)": "Reset (this level = 0)",
 "Təzyiq fərqi (başlanğıca nəzərən)": "Pressure difference (relative to start)", "Atmosfer təzyiqi": "Atmospheric pressure",
 "Telefonu yerdən başınızın hündürlüyünə qaldırın: Δp ≈ −20 Pa, Δh ≈ +1,7 m. Ölçmə zamanı telefonu tərpətməyin və qapıları açmayın.":
   "Lift the phone from the floor to the height of your head: Δp ≈ −20 Pa, Δh ≈ +1.7 m. Do not move the phone or open doors during the measurement.",
 "Təzyiq": "Pressure", "Vaxt (s)": "Time (s)", "Təzyiq (hPa)": "Pressure (hPa)",
 "Çəkisizlik": "Weightlessness", "Hiss olunan təcil |a|": "Felt acceleration |a|", "Vəziyyət": "State",
 "ÇƏKİSİZLİK": "WEIGHTLESS", "dayaq var": "supported", "|a| zamandan asılı olaraq": "|a| over time",
 "Fənər həddi (0 = söndür)": "Flashlight threshold (0 = off)",
 "|a| fənər həddindən aşağı olanda telefonun fənəri maksimal parlaqlıqla 15 Hz tezliklə yanıb-sönür.":
   "While |a| is below the flashlight threshold, the phone's flashlight blinks at full brightness at 15 Hz.",
 "Avto-pauza həddi (0 = söndür)": "Auto-pause threshold (0 = off)", "Pauzadan əvvəl gecikmə": "Delay before pause",
 "|a| avto-pauza həddinə düşəndən «gecikmə» qədər sonra ölçmə avtomatik dayanır və qrafik donur (fənər də sönür). Gecikmə 0 olsa, ölçmə dərhal dayanar və fənər yanmağa macal tapmaz. Davam etmək üçün ▶ düyməsinə basın.":
   "The measurement stops automatically and the graph freezes (the flashlight turns off) one \"delay\" after |a| drops to the auto-pause threshold. With a delay of 0 it stops immediately and the flashlight has no time to light up. Press ▶ to continue.",
 "9,8 m/s² = adi çəki (1 g). Atma anında |a| 9,8-dən böyük olur, uçuşda isə 0-a düşür. Telefonu yalnız yumşaq səthin üzərinə atın!":
   "9.8 m/s² = normal weight (1 g). At the throw |a| is above 9.8, in flight it drops to 0. Only throw the phone onto a soft surface!",
 "Təcil": "Acceleration", "Avtomobilin təcili": "Car acceleration", "İrəli təcil": "Forward acceleration", "Maksimum təcil": "Maximum acceleration",
 "Sürət (GPS)": "Speed (GPS)", "söndürülüb": "off", "aktivdir": "active", "Sürət": "Speed",
 "İrəli təcil (m/s²)": "Forward acceleration (m/s²)", "Sürət (km/s)": "Speed (km/h)",
 "Səsin sürəti": "Speed of sound", "Bu telefonun vaxtı": "This phone's time", "Sıfırla": "Reset",
 "Telefonlar arası məsafə d": "Distance between phones d", "Digər telefonun vaxtı": "Other phone's time",
 "Havanın temperaturu": "Air temperature", "Gözlənilən (nəzəri)": "Expected (theoretical)", "Həssaslıq həddi": "Sensitivity threshold",
 "Minimum fasilə": "Minimum interval",
 "Zalda əks-səda saniyəölçəni vaxtından əvvəl dayandırırsa, həssaslıq həddini artırın. Əl çalmaları qısa və kəskin olsun.":
   "If the echo in the hall stops the stopwatch too early, raise the sensitivity threshold. Claps should be short and sharp.",
}
EN_TITLE = {"1_pressure.phyphox": "Air pressure: head and feet", "2_weightless.phyphox": "Weightlessness", "3_car.phyphox": "Car acceleration", "4_sound.phyphox": "Speed of sound"}
EN_DESC = {
 "1_pressure.phyphox": """Air has weight too: pressure is higher below than above. A height difference equal to your height (1.7 m) changes the pressure by about 20 Pa (0.2 hPa): Δp = ρ·g·h = 1.2 · 9.81 · 1.7 ≈ 20 Pa.

How: put the phone on the floor, start the measurement, wait 20–30 s (at any moment the «Reset» button takes the current level as zero). Then lift the phone to the height of your head and keep it still for another 20–30 s. The graph will show a step of ~20 Pa.""",
 "2_weightless.phyphox": """An object is weightless from the moment it leaves the hand until it lands: while rising, at the top and while falling. Only gravity acts on it, there is no support.

The accelerometer measures the acceleration caused by the supporting force. With the phone lying on a table |a| ≈ 9.8 m/s² (1 g), in free flight |a| ≈ 0.

How: start the measurement and toss the phone 30–50 cm up above a soft bed or mattress. The whole flight shows up as a «dip» with |a| ≈ 0.""",
 "3_car.phyphox": """When the car speeds up, the phone accelerates with it. The linear accelerometer measures acceleration without gravity.

How: fix the phone vertically in a holder, screen facing the driver. Start the measurement while the car is standing, then accelerate. «Forward acceleration» is positive, braking negative. Speed is measured by GPS.

Check: if the 0–100 km/h time is t, the average acceleration = 27.8 / t m/s².

Safety: the passenger, not the driver, handles the phone; measure on an empty, closed area.""",
 "4_sound.phyphox": """Two phones are placed in the hall at a distance d (10–15 m) from each other; this experiment is started on both.
1) Someone claps next to phone A: both stopwatches start, the one on B slightly later.
2) A second person claps next to phone B: both stopwatches stop, the one on A slightly later.
The sound travels the distance twice, so: v = 2d / (t_A − t_B). Reaction time does not affect the result.

On one phone enter the distance d and the time shown by the other phone, and the speed of sound is calculated. Expected at 20 °C: 343 m/s.""",
}

LANGS = [("tr", TR, TR_TITLE, TR_DESC, "Müze gösterisi"), ("ru", RU, RU_TITLE, RU_DESC, "Музейная демонстрация"), ("en", EN, EN_TITLE, EN_DESC, "Museum demonstration")]
def add_tr(name, xml):
    q = {chr(34): "&quot;"}
    used = set(_re.findall(r'(?:label|name)="([^"]*)"', xml)) | set(_re.findall(r'<map[^>]*>([^<]*)</map>', xml))
    missing = [u for u in used if u not in {_e(k, q) for k in TR} and not _re.fullmatch(r'[\w ()/²|.-]*', u)]
    if missing: print("untranslated in", name, missing)
    blocks = ""
    for loc, D, TT, DD, cat in LANGS:
        strings = "".join(f'      <string original="{_e(k, q)}">{_e(v)}</string>\n' for k, v in D.items() if _e(k, q) in used)
        blocks += (f'    <translation locale="{loc}">\n      <title>{_e(TT[name])}</title>\n      <category>{_e(cat)}</category>\n'
                   f'      <description>{_e(DD[name])}</description>\n{strings}    </translation>\n')
    i = xml.index("</description>") + len("</description>\n")
    return xml[:i] + "  <translations>\n" + blocks + "  </translations>\n" + xml[i:]
OUT.mkdir(exist_ok=True)
for name, s in [("1_pressure.phyphox", pressure), ("2_weightless.phyphox", weightless), ("3_car.phyphox", car), ("4_sound.phyphox", sound)]:
    (OUT/name).write_text(add_tr(name, s), encoding="utf-8")
print("ok")
