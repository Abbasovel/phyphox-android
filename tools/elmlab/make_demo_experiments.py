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
        <input axis="y">dp</input>
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
    <container size="0">amag</container>
  </data-containers>
  <input>
    <sensor type="accelerometer" rate="0">
      <output component="x">accX</output>
      <output component="y">accY</output>
      <output component="z">accZ</output>
      <output component="t">acc_time</output>
    </sensor>
  </input>
  <views>
    <view label="Ölçmə">
      <value label="Hiss olunan təcil |a|" size="3" precision="1" unit="m/s²">
        <input>amag</input>
      </value>
      <value label="Vəziyyət" size="2">
        <input>amag</input>
        <map max="2">ÇƏKİSİZLİK</map>
        <map>dayaq var</map>
      </value>
      <graph label="|a| zamandan asılı olaraq" timeOnX="true" labelX="t" unitX="s" labelY="|a|" unitY="m/s²" partialUpdate="true">
        <input axis="x">acc_time</input>
        <input axis="y">amag</input>
      </graph>
      <info label="9,8 m/s² = adi çəki (1 g). Atma anında |a| 9,8-dən böyük olur, uçuşda isə 0-a düşür. Telefonu yalnız yumşaq səthin üzərinə atın!"/>
    </view>
  </views>
  <analysis sleep="0.05">
    <formula formula="sqrt([1_]*[1_]+[2_]*[2_]+[3_]*[3_])">
      <input clear="false">accX</input>
      <input clear="false">accY</input>
      <input clear="false">accZ</input>
      <output>amag</output>
    </formula>
  </analysis>
  <export>
    <set name="Təcil">
      <data name="Vaxt (s)">acc_time</data>
      <data name="ax (m/s²)">accX</data>
      <data name="ay (m/s²)">accY</data>
      <data name="az (m/s²)">accZ</data>
      <data name="|a| (m/s²)">amag</data>
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
        <input axis="y">af</input>
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
        <input axis="y">vkmh</input>
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
      <edit label="Həssaslıq həddi" unit="" default="0.3" signed="false" min="0" max="1">
        <output>threshold</output>
      </edit>
      <edit label="Minimum fasilə" unit="s" default="0.1" signed="false">
        <output>mindelay</output>
      </edit>
      <info label="Zalda əks-səda saniyəölçəni vaxtından əvvəl dayandırırsa, həssaslıq həddini artırın. Əl çalmaları qısa və kəskin olsun."/>
    </view>
  </views>
  {analysis.group(1)}{analysis.group(2)}    <formula formula="sqrt((2*[1]/([2]-[3]))^2)">
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
OUT.mkdir(exist_ok=True)
for name, s in [("1_pressure.phyphox", pressure), ("2_weightless.phyphox", weightless), ("3_car.phyphox", car), ("4_sound.phyphox", sound)]:
    (OUT/name).write_text(s, encoding="utf-8")
print("ok")
