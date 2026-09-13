#!/usr/bin/env python
"""Build Kəsim's secondary static pages and discovery files."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASE = "https://twenion.github.io/manufacturing-site-demo/"


NAV = (
    ('imkanlar.html', 'İmkanlar'),
    ('materiallar.html', 'Materiallar'),
    ('keyfiyyet.html', 'Keyfiyyət'),
    ('haqqimizda.html', 'Haqqımızda'),
    ('elaqe.html', 'Əlaqə'),
)


PAGES = {
    'imkanlar.html': {
        'title': 'Metal emalı imkanları və texniki hədlər | Kəsim',
        'description': 'Lazer kəsim, CNC büküm, MIG/TIG qaynaq və toz boya üçün material, ölçü, qalınlıq və tolerans hədlərini müqayisə edin.',
        'code': 'Texniki imkanlar / 04 proses',
        'h1': 'Hansı detalı necə istehsal edə bilirik',
        'lead': 'Avadanlığın yalnız adını deyil, işlədiyimiz ölçünü, qalınlığı və qəbul həddini açıq göstəririk.',
        'body': '''
<section class="inner-section">
  <header><h2>Dörd proses, bir məsuliyyət xətti</h2><p>Detal proseslər arasında başqa podratçıya getmir. Ölçü nəzarəti eyni istehsal kartı ilə başlanır və bağlanır.</p></header>
  <div class="spec-grid">
    <article class="spec-card"><span class="process-code">LZR</span><div><h3><a href="lazer-kesim.html">Fiber lazer kəsim</a></h3><p>Vərəq metalda kontur, dəlik və işarələmə. DXF əsas formatdır.</p><ul class="spec-list"><li><strong>1500 × 3000 mm</strong>iş masası</li><li><strong>16 mm-dək</strong>qara polad</li><li><strong>8 mm-dək</strong>paslanmaz</li><li><strong>±0,20 mm</strong>başlanğıc tolerans</li></ul></div></article>
    <article class="spec-card"><span class="process-code">BKM</span><div><h3><a href="cnc-bukum.html">CNC büküm</a></h3><p>Proqramlaşdırılan ardıcıllıq və ilk detalda bucaq nəzarəti.</p><ul class="spec-list"><li><strong>2200 mm</strong>iş eni</li><li><strong>80 ton</strong>press gücü</li><li><strong>0,8–6 mm</strong>iş qalınlığı</li><li><strong>±0,5°</strong>bucaq həddi</li></ul></div></article>
    <article class="spec-card"><span class="process-code">QYN</span><div><h3><a href="qaynaq.html">MIG / TIG qaynaq</a></h3><p>Qara polad, paslanmaz və alüminium üçün ayrılmış iş sahələri.</p><ul class="spec-list"><li><strong>ISO 5817-C</strong>qəbul səviyyəsi</li><li><strong>160 A-dək</strong>TIG</li><li><strong>350 A-dək</strong>MIG/MAG</li><li><strong>100%</strong>vizual nəzarət</li></ul></div></article>
    <article class="spec-card"><span class="process-code">BYA</span><div><h3><a href="toz-boya.html">Toz boya</a></h3><p>Səth hazırlığı, rəngləmə və qalınlıq ölçümü bir xəttdə.</p><ul class="spec-list"><li><strong>2500 mm</strong>maksimum detal</li><li><strong>60–100 μm</strong>örtük</li><li><strong>RAL</strong>standart rənglər</li><li><strong>48 saat</strong>tipik müddət</li></ul></div></article>
  </div>
</section>
<section class="inner-section split"><div><h2>Fayl yoxlanışı nəyi əhatə edir</h2><p>Qiymət hesablamazdan əvvəl açıq kontur, üst-üstə düşən xətt, uyğun olmayan dəlik və büküm radiusu yoxlanır. Problem varsa istehsala vermədən göstəririk.</p></div><ol class="step-list"><li><div><h3>Geometriya</h3><p>Kontur bağlanması, ölçək və təkrarlanan xətt.</p></div></li><li><div><h3>İstehsal oluna bilmə</h3><p>Dəlik–qalınlıq nisbəti, kənar məsafəsi və radius.</p></div></li><li><div><h3>Yerləşdirmə</h3><p>Sac seçimi, istiqamət və qalan material.</p></div></li></ol></section>
<section class="callout"><div><h2>Prosesi seçmək lazım deyil</h2><p>Detalın son vəziyyətini və faylı göndərin. Kəsim, büküm və qaynaq ardıcıllığını texnoloq özü quracaq.</p></div><a class="primary-button" href="teklif.html">Faylı yoxlat</a></section>''',
    },
    'materiallar.html': {
        'title': 'Metal materialları, qalınlıq və başlanğıc qiymətlər | Kəsim',
        'description': 'Qara polad, paslanmaz polad və alüminium üçün stok qalınlıqları, vərəq ölçüləri, minimum sifariş və hesab qaydasına baxın.',
        'code': 'Material cədvəli / 03 qrup',
        'h1': 'Stokda olan metal və hesab qaydası',
        'lead': 'Materialın markası, real qalınlıq aralığı və qiymətə təsir edən dəyişənlər bir cədvəldə.',
        'body': '''
<section class="inner-section"><header><h2>Stok proqramı</h2><p>Cədvəldəki qiymətlər düzbucaqlı, deşiksiz detal üçün 1 m² xammalın başlanğıc hesabıdır; kəsim yolu və proses ayrıca hesablanır.</p></header>
<div class="table-shell" tabindex="0" role="region" aria-label="Material və qalınlıq cədvəli"><table class="data-table"><thead><tr><th>Material</th><th>Marka</th><th>Qalınlıq</th><th>Vərəq</th><th>Sıxlıq</th><th>Başlanğıc</th></tr></thead><tbody>
<tr><td>Qara polad</td><td>S235JR</td><td>0,8 / 1 / 1,5 / 2 / 3 / 4 / 5 / 6 / 8 / 10 / 12 / 16 mm</td><td>1500 × 3000 mm</td><td>7,85 g/sm³</td><td>2,15 ₼ / kg</td></tr>
<tr><td>Paslanmaz polad</td><td>AISI 304</td><td>0,8 / 1 / 1,5 / 2 / 3 / 4 / 5 / 6 / 8 mm</td><td>1500 × 3000 mm</td><td>7,90 g/sm³</td><td>4,80 ₼ / kg</td></tr>
<tr><td>Alüminium</td><td>EN AW-5754</td><td>1 / 1,5 / 2 / 3 / 4 / 5 / 6 mm</td><td>1500 × 3000 mm</td><td>2,70 g/sm³</td><td>5,10 ₼ / kg</td></tr>
</tbody></table></div><p class="table-note">Qiymətlər demo məlumatıdır, ƏDV daxil deyil və bazar təklifi sayılmır.</p></section>
<section class="inner-section split"><div><h2>Qiymət necə yaranır</h2><p>Eyni material və eyni sahə iki detal üçün eyni qiymət demək deyil. Lazer yolu, deşmə sayı, yerləşdirmə və sonrakı emal rəqəmi dəyişir.</p><p>Ana səhifədəki hesab sadə detal üçün aralıq verir. DXF yoxlanandan sonra təklifdə hər xərc ayrıca görünür.</p></div><dl class="metric-stack"><div><dt>Material</dt><dd>çəki × kg</dd></div><div><dt>Kəsim</dt><dd>metr + deşmə</dd></div><div><dt>Hazırlıq</dt><dd>sifariş üzrə</dd></div><div><dt>Sonrakı emal</dt><dd>əməliyyat üzrə</dd></div></dl></section>
<section class="notice"><h2>Material sertifikatı lazım olduqda</h2><p>Sifarişdə EN 10204 3.1 tələbini qeyd edin. Sertifikatlı material ayrıca partiyada saxlanır və sənəd detal nömrəsi ilə əlaqələndirilir.</p></section>''',
    },
    'keyfiyyet.html': {
        'title': 'Metal detal üçün ölçü nəzarəti və qəbul protokolu | Kəsim',
        'description': 'İlk detal yoxlanışı, partiya nəzarəti, istifadə edilən ölçü alətləri və nümunə qəbul protokolu ilə tanış olun.',
        'code': 'Nəzarət planı / QP-07',
        'h1': 'Ölçü protokolu detalın özündən ayrılmır',
        'lead': 'Nominal rəqəm, faktiki nəticə, alət və qərar eyni sətirdə. Qəbul və uyğunsuzluq görünən olmalıdır.',
        'body': '''
<section class="inner-section"><header><h2>Nümunə ilk detal protokolu</h2><p>Korpus paneli, S235JR, 2 mm, iş AZ-2609-014. Rəqəmlər xəyali demo məlumatıdır.</p></header>
<div class="table-shell" tabindex="0" role="region" aria-label="Nümunə ölçü protokolu"><table class="data-table"><thead><tr><th>Xüsusiyyət</th><th>Nominal</th><th>Tolerans</th><th>Faktiki</th><th>Alət</th><th>Qərar</th></tr></thead><tbody>
<tr><td>Ümumi en</td><td>320,00 mm</td><td>±0,20 mm</td><td>320,08 mm</td><td>Rəqəmsal ştangen</td><td>Qəbul</td></tr>
<tr><td>Ümumi uzunluq</td><td>180,00 mm</td><td>±0,20 mm</td><td>179,94 mm</td><td>Rəqəmsal ştangen</td><td>Qəbul</td></tr>
<tr><td>Dəlik diametri</td><td>Ø8,00 mm</td><td>+0,15 / 0 mm</td><td>8,06 mm</td><td>Kalibr tıxacı</td><td>Qəbul</td></tr>
<tr><td>Büküm bucağı</td><td>90,0°</td><td>±0,5°</td><td>89,8°</td><td>Rəqəmsal bucaqölçən</td><td>Qəbul</td></tr>
<tr><td>Örtük qalınlığı</td><td>80 μm</td><td>60–100 μm</td><td>84 μm</td><td>Qalınlıqölçən</td><td>Qəbul</td></tr>
</tbody></table></div></section>
<section class="inner-section split"><div><h2>Nə vaxt nə ölçülür</h2><p>İlk detal seriyanın qalanını buraxmaq üçün yoxlanır. Uzun partiyada hər 25 detalda kritik ölçülər təkrar edilir. Son detal partiyanın bağlanış nöqtəsidir.</p></div><ol class="step-list"><li><div><h3>Giriş</h3><p>Material markası, qalınlıq və səth vəziyyəti.</p></div></li><li><div><h3>İlk detal</h3><p>Çertyojdakı bütün kritik ölçülər.</p></div></li><li><div><h3>Partiya</h3><p>Hər 25 ədəddə seçilmiş nəzarət ölçüləri.</p></div></li><li><div><h3>Çıxış</h3><p>Say, vizual vəziyyət və son detal ölçüsü.</p></div></li></ol></section>
<section class="callout"><div><h2>Xüsusi nəzarət planınız varsa, təklifə əlavə edin</h2><p>Ölçü tezliyi və protokol formatı istehsaldan əvvəl razılaşdırılır.</p></div><a class="primary-button" href="teklif.html">Tələb əlavə et</a></section>''',
    },
    'teklif.html': {
        'title': 'Metal detal üçün texniki təklif sorğusu | Kəsim',
        'description': 'Detal faylını, materialı, sayı, sonrakı emalı və qəbul tələblərini bir sorğuda toplayın. Demo forma heç bir məlumat göndərmir.',
        'code': 'Təklif sorğusu / RFQ',
        'h1': 'İstehsal üçün lazım olan məlumatı bir dəfə göndərin',
        'lead': 'DXF, STEP və ya ölçülü PDF; material, say və son tarix. Natamam yer varsa texnoloq həmin sualı ayrıca qaytarır.',
        'body': '''
<section class="inner-section"><form class="form-panel" data-demo-form>
<fieldset><legend>Detal və material</legend><div class="form-grid">
<div><label for="rfq-material">Material</label><select id="rfq-material" name="material" required><option value="">Seçin</option><option>Qara polad S235</option><option>Paslanmaz polad AISI 304</option><option>Alüminium 5754</option><option>Texnoloq seçsin</option></select></div>
<div><label for="rfq-thickness">Qalınlıq</label><input id="rfq-thickness" name="thickness" placeholder="məs. 2 mm" required></div>
<div><label for="rfq-quantity">Ədəd</label><input id="rfq-quantity" name="quantity" type="number" min="1" max="10000" required></div>
<div><label for="rfq-date">İstənilən tarix</label><input id="rfq-date" name="date" type="date"></div>
<div class="span-2"><label for="rfq-file">İstehsal faylı</label><input id="rfq-file" name="drawing" type="file" accept=".dxf,.dwg,.step,.stp,.pdf" required><small>DXF, DWG, STEP və ya PDF · demo faylı yükləmir</small></div>
</div></fieldset>
<fieldset><legend>Emal və qəbul</legend><div class="form-grid">
<div><label for="rfq-process">Proses</label><select id="rfq-process" name="process"><option>Lazer kəsim</option><option>Lazer + büküm</option><option>Lazer + qaynaq</option><option>Tam istehsal</option></select></div>
<div><label for="rfq-finish">Səth</label><select id="rfq-finish" name="finish"><option>Emalsız</option><option>Kənar təmizləmə</option><option>Toz boya</option><option>Fırçalanmış paslanmaz</option></select></div>
<div class="span-2"><label for="rfq-notes">Kritik ölçü və qeydlər</label><textarea id="rfq-notes" name="notes" placeholder="Tolerans, görünən səth, qaynaq və qablaşdırma tələbi"></textarea></div>
</div></fieldset>
<fieldset><legend>Əlaqə</legend><div class="form-grid"><div><label for="rfq-name">Ad və şirkət</label><input id="rfq-name" name="name" autocomplete="organization" required></div><div><label for="rfq-email">E-poçt</label><input id="rfq-email" name="email" type="email" autocomplete="email" required></div></div></fieldset>
<div class="form-actions"><button class="primary-button" type="submit">Sorğunu yoxla</button><p>Bu demo məlumatı saxlamır və göndərmir.</p></div>
<div class="demo-status" data-demo-status tabindex="-1"><strong>Sorğu forması düzgündür.</strong> Bu demo olduğuna görə məlumat və fayl heç yerə göndərilmədi.</div>
</form></section>
<section class="notice"><h2>Cavabda nə gəlir</h2><p>Material və emal ayrı sətirlərdə, ədəd qiyməti, ümumi məbləğ, istehsal günü, təklifin etibarlılıq müddəti və texniki qeydlər.</p></section>''',
    },
    'haqqimizda.html': {
        'title': 'Kəsim haqqında — iş prinsipi və istehsal axını',
        'description': 'Kəsim demo metal emalı müəssisəsinin iş prinsipi: açıq texniki hədlər, ölçülə bilən təklif və partiya üzrə izlənən nəzarət.',
        'code': 'Şirkət / demo profil',
        'h1': 'Metal emalını sirli qiymət qutusundan çıxarırıq',
        'lead': 'Kəsim real şirkət deyil. Bu demo istehsalçı saytının müştəriyə hansı texniki məlumatı əvvəlcədən verməli olduğunu göstərir.',
        'body': '''
<section class="inner-section split"><div><h2>Saytın əsas fərziyyəsi</h2><p>Mühəndis təklif istəməzdən əvvəl üç şeyi bilmək istəyir: detal istehsal oluna bilərmi, hansı müddətdə və hansı qiymət aralığında. Bu məlumat gizlənəndə sorğu ya gecikir, ya da ümumiyyətlə göndərilmir.</p><p>Kəsim bunu texniki hədlər, açıq material cədvəli və canlı ilkin hesabla həll edən xəyali nümunədir.</p></div><dl class="metric-stack"><div><dt>İstehsal sahəsi</dt><dd>850 m²</dd></div><div><dt>Əsas proses</dt><dd>4</dd></div><div><dt>Tipik cavab</dt><dd>30 dəqiqə</dd></div><div><dt>Minimum sifariş</dt><dd>1 detal</dd></div></dl></section>
<section class="inner-section"><header><h2>İş qaydası</h2><p>Rəqəm yoxlanmadan söz verilmir; problem gizlədilmədən yazılır.</p></header><ol class="step-list"><li><div><h3>Fayl əvvəlcə texniki yoxlanır</h3><p>Açıq kontur, materiala uyğun olmayan detal və kritik ölçü sual kimi qaytarılır.</p></div></li><li><div><h3>Təklif hissələrə bölünür</h3><p>Material, kəsim, hazırlıq və sonrakı emal ayrıca göstərilir.</p></div></li><li><div><h3>İlk detal seriyanı açır</h3><p>Kritik ölçülər qəbul olunmadan partiyanın qalanı buraxılmır.</p></div></li><li><div><h3>Partiya protokolla bağlanır</h3><p>Say, vizual vəziyyət və son ölçü qeyd edilir.</p></div></li></ol></section>
<section class="callout"><div><h2>Bu, satış demosudur</h2><p>Marka, ünvan, rəqəmlər və istehsal nümunələri xəyalidir. Real şirkətin adına və məlumatına əsaslanmır.</p></div><a class="secondary-button" href="elaqe.html">Əlaqə səhifəsi</a></section>''',
    },
    'elaqe.html': {
        'title': 'Əlaqə və iş saatları | Kəsim',
        'description': 'Kəsim demo metal emalı müəssisəsinin xəyali telefon, e-poçt, ünvan və iş saatları. Forma məlumat göndərmir.',
        'code': 'Əlaqə / Sumqayıt',
        'h1': 'Texniki sualı birbaşa istehsala verin',
        'lead': 'Fayl olmadan da material, tolerans və proses barədə soruşa bilərsiniz. Buradakı əlaqə məlumatları qəsdən qeyri-real saxlanıb.',
        'body': '''
<section class="inner-section"><div class="contact-grid"><article><h2>Telefon</h2><p>B.e.–Ş. 08:00–18:00</p><a href="tel:+994180000000">+994 18 000 00 00</a></article><article><h2>E-poçt</h2><p>Texniki sorğu və fayl üçün</p><a href="mailto:istehsal@kesim.example">istehsal@kesim.example</a></article><article><h2>Ünvan</h2><p>Sumqayıt Sənaye Parkı<br>Demo korpus, AZ5000</p></article></div></section>
<section class="inner-section split"><div><h2>Qısa sual göndərin</h2><p>Qiymət üçün detal faylı lazımdır. Material və istehsal oluna bilmə sualını isə bu formadan yaza bilərsiniz.</p></div><form class="form-panel" data-demo-form><fieldset><legend>Mesaj</legend><div class="form-grid"><div><label for="contact-name">Ad</label><input id="contact-name" name="name" required></div><div><label for="contact-email">E-poçt</label><input id="contact-email" name="email" type="email" required></div><div class="span-2"><label for="contact-message">Sual</label><textarea id="contact-message" name="message" required></textarea></div></div></fieldset><div class="form-actions"><button class="primary-button" type="submit">Mesajı yoxla</button></div><div class="demo-status" data-demo-status tabindex="-1"><strong>Forma düzgündür.</strong> Demo olduğuna görə mesaj göndərilmədi.</div></form></section>''',
    },
    'mexfilik.html': {
        'title': 'Məxfilik qeydi | Kəsim demo saytı',
        'description': 'Kəsim demo saytında məlumatların emalı, local işləyən hesablayıcı və göndərilməyən formalar haqqında qısa məxfilik qeydi.',
        'code': 'Hüquqi qeyd / 12.09.2026',
        'h1': 'Bu demo məlumat toplamır',
        'lead': 'Saytda analitika, reklam pikseli, cookie, hesab və serverə göndərilən forma yoxdur.',
        'body': '''<article class="prose"><h2>Hesablayıcı</h2><p>Ana səhifədə ölçü, material və say əsasında aparılan hesab yalnız brauzerinizdə işləyir. Daxil etdiyiniz rəqəmlər saxlanmır və şəbəkə sorğusu yaratmır.</p><h2>Formalar</h2><p>Təklif və əlaqə formaları interfeys nümunəsidir. “Sorğunu yoxla” düyməsi sahələrin düzgün doldurulduğunu yoxlayır, lakin məlumatı və seçilmiş faylı heç yerə göndərmir.</p><h2>Cookie və üçüncü tərəf</h2><p>Sayt cookie yazmır, localStorage istifadə etmir, analitika və reklam kodu daşımır. Şrift, skript və üslub faylları repository daxilindən açılır; CDN sorğusu yoxdur.</p><h2>Demo statusu</h2><p>Kəsim xəyali markadır. Telefon sıfırlanıb, e-poçt isə real poçt qəbul etməyən <code>.example</code> domenindədir.</p><h2>Tarix</h2><p>Bu qeyd 12.09.2026 tarixində yenilənib.</p></article>''',
    },
}


SERVICES = {
    'lazer-kesim.html': ('LZR', 'Fiber lazer kəsim', 'Vərəq metalı ölçülə bilən kontura çevirən əsas proses.', [
        ('İş masası', '1500 × 3000 mm'), ('Qara polad', '0,8–16 mm'), ('Paslanmaz', '0,8–8 mm'), ('Alüminium', '1–6 mm'), ('Başlanğıc tolerans', '±0,20 mm'), ('Giriş faylı', 'DXF / DWG')]),
    'cnc-bukum.html': ('BKM', 'CNC büküm', 'Kəsilmiş detalı proqramlaşdırılan ardıcıllıqla formaya gətirən proses.', [
        ('İş eni', '2200 mm'), ('Press gücü', '80 ton'), ('Qalınlıq', '0,8–6 mm'), ('Bucaq həddi', '±0,5°'), ('Minimum daxili radius', 'materiala görə'), ('Nəzarət', 'ilk detal')]),
    'qaynaq.html': ('QYN', 'MIG və TIG qaynaq', 'Materiala uyğun ayrılmış sahədə yığım və ölçü nəzarətli birləşdirmə.', [
        ('Qara polad', 'MIG/MAG'), ('Paslanmaz', 'TIG'), ('Alüminium', 'AC TIG'), ('Qəbul səviyyəsi', 'ISO 5817-C'), ('Vizual nəzarət', '100%'), ('Protokol', 'tələb üzrə')]),
    'toz-boya.html': ('BYA', 'Toz boya', 'Hazırlıqdan örtük qalınlığının ölçülməsinə qədər idarə olunan səth prosesi.', [
        ('Maksimum detal', '2500 × 1200 × 900 mm'), ('Örtük', '60–100 μm'), ('Rəng', 'RAL kataloqu'), ('Parlaqlıq', 'mat / yarımat / parlaq'), ('Tipik müddət', '48 saat'), ('Nəzarət', 'qalınlıq + vizual')]),
}


def header(active: str) -> str:
    links = ''.join(
        f'<a href="{href}"{(" aria-current=\"page\"" if href == active else "")}>{label}</a>'
        for href, label in NAV
    )
    return f'''<a class="skip-link" href="#main">Əsas məzmuna keç</a>
<header class="site-header"><div class="header-inner"><a class="brand" href="index.html" aria-label="Kəsim ana səhifə"><img class="brand-mark" src="assets/img/brand-mark.svg" alt="" aria-hidden="true" width="40" height="40"><span class="brand-copy"><strong>Kəsim</strong><small>metal emalı</small></span></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav"><span class="sr-only">Menyunu aç</span><span></span><span></span></button><nav class="main-nav" id="main-nav" aria-label="Əsas menyu">{links}<a class="nav-cta" href="teklif.html">Təklif al</a></nav></div></header>'''


FOOTER = '''<footer class="site-footer"><div class="footer-main"><div><a class="brand brand-footer" href="index.html"><img class="brand-mark" src="assets/img/brand-mark.svg" alt="" aria-hidden="true" width="40" height="40"><span class="brand-copy"><strong>Kəsim</strong><small>metal emalı</small></span></a><p>Sumqayıtda xəyali metal emalı müəssisəsi.</p></div><div><h2>İstehsal</h2><a href="imkanlar.html">İmkanlar</a><a href="materiallar.html">Materiallar</a><a href="keyfiyyet.html">Keyfiyyət</a></div><div><h2>Şirkət</h2><a href="haqqimizda.html">Haqqımızda</a><a href="elaqe.html">Əlaqə</a><a href="mexfilik.html">Məxfilik</a></div><div><h2>Əlaqə</h2><a href="tel:+994180000000">+994 18 000 00 00</a><a href="mailto:istehsal@kesim.example">istehsal@kesim.example</a><span>B.e.–Ş. 08:00–18:00</span></div></div><div class="footer-note"><p>Bu sayt portfolio üçün hazırlanmış demodur. Kəsim real şirkət deyil; forma məlumat göndərmir.</p><p>© 2026 Kəsim</p></div></footer>'''


def schemas(filename: str, title: str, description: str) -> str:
    page_types = {
        'elaqe.html': 'ContactPage',
        'haqqimizda.html': 'AboutPage',
        'materiallar.html': 'CollectionPage',
    }
    data = [
        {
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Ana səhifə', 'item': BASE},
                {'@type': 'ListItem', 'position': 2, 'name': title, 'item': BASE + filename},
            ],
        },
        {
            '@context': 'https://schema.org',
            '@type': page_types.get(filename, 'WebPage'),
            '@id': BASE + filename + '#page',
            'url': BASE + filename,
            'name': title,
            'description': description,
            'inLanguage': 'az',
            'isPartOf': {'@type': 'WebSite', 'name': 'Kəsim', 'url': BASE},
        },
    ]
    if filename in SERVICES:
        data.append({
            '@context': 'https://schema.org',
            '@type': 'Service',
            '@id': BASE + filename + '#service',
            'name': title,
            'description': description,
            'areaServed': {'@type': 'Country', 'name': 'Azərbaycan'},
            'provider': {'@type': 'Organization', 'name': 'Kəsim Metal Emalı', 'url': BASE},
        })
    return ''.join(f'<script type="application/ld+json">{json.dumps(item, ensure_ascii=False)}</script>' for item in data)


def shell(filename: str, page: dict[str, str]) -> str:
    title = page['title']
    description = page['description']
    return f'''<!doctype html>
<html lang="az" class="no-js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><script>document.documentElement.classList.remove('no-js');</script><title>{html.escape(title)}</title><meta name="description" content="{html.escape(description, quote=True)}"><link rel="canonical" href="{BASE + filename}"><meta property="og:type" content="website"><meta property="og:locale" content="az_AZ"><meta property="og:title" content="{html.escape(title, quote=True)}"><meta property="og:description" content="{html.escape(description, quote=True)}"><meta property="og:url" content="{BASE + filename}"><meta property="og:site_name" content="Kəsim"><meta name="theme-color" content="#0a0d16"><link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg"><link rel="stylesheet" href="assets/css/style.css">{schemas(filename, page['h1'], description)}</head><body>{header(page.get('active', filename))}<nav class="breadcrumb" aria-label="Naviqasiya yolu"><ol><li><a href="index.html">Ana səhifə</a></li><li aria-current="page">{html.escape(page['h1'])}</li></ol></nav><main id="main"><header class="page-hero"><div><p class="job-code">{page['code']}</p><h1>{page['h1']}</h1></div><p>{page['lead']}</p></header><div class="inner-main">{page['body']}</div></main>{FOOTER}<script src="assets/js/site.js" defer></script></body></html>'''


def build_service(filename: str, service: tuple) -> None:
    code, name, lead, specs = service
    rows = ''.join(f'<div><dt>{html.escape(label)}</dt><dd>{html.escape(value)}</dd></div>' for label, value in specs)
    nav = ''.join(f'<a href="{href}"{(" aria-current=\"page\"" if href == filename else "")}>{data[1]}</a>' for href, data in SERVICES.items())
    page = {
        'title': f'{name} — ölçü, material və qəbul hədləri | Kəsim',
        'description': f'{name} üçün texniki imkanlar, material qalınlığı, ölçü həddi, tolerans və istehsal faylı tələbləri.',
        'code': f'Proses / {code}',
        'h1': name,
        'lead': lead,
        'active': 'imkanlar.html',
        'body': f'''<nav class="detail-nav" aria-label="İstehsal prosesləri">{nav}</nav><section class="inner-section split" style="margin-top:72px"><div><h2>Texniki çərçivə</h2><p>Bu rəqəmlər standart iş üçündür. Geometriya, materialın səthi və sonrakı emal bəzi hədləri dəyişə bilər; uyğunluq istehsal faylında təsdiqlənir.</p><a class="secondary-button" href="teklif.html">Faylı yoxlat</a></div><dl class="metric-stack">{rows}</dl></section><section class="inner-section"><header><h2>Prosesin üç nəzarət nöqtəsi</h2></header><ol class="step-list"><li><div><h3>Giriş yoxlanışı</h3><p>Fayl ölçəyi, material və kritik tələblər.</p></div></li><li><div><h3>İlk detal</h3><p>Əsas ölçülər və proses parametrləri.</p></div></li><li><div><h3>Partiya bağlanışı</h3><p>Say, səth və son detalın qəbul nəticəsi.</p></div></li></ol></section><section class="notice"><h2>Qiymət üçün nə göndərilməlidir</h2><p>DXF və ya STEP faylı, material, qalınlıq, ədəd, kritik tolerans və istənilən təhvil tarixi.</p></section>''',
    }
    (ROOT / filename).write_text(shell(filename, page), encoding='utf-8')


def build_404() -> None:
    page = '''<!doctype html><html lang="az"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Səhifə tapılmadı | Kəsim</title><meta name="description" content="Axtardığınız Kəsim demo səhifəsi mövcud deyil. Ana səhifəyə və ya texniki imkanlara qayıdın."><meta name="robots" content="noindex"><link rel="stylesheet" href="assets/css/style.css"></head><body>''' + header('') + '''<main id="main" class="error-page"><div><p class="error-code" aria-hidden="true">404</p><h1>Səhifə tapılmadı</h1><p>Ünvan dəyişib və ya link düzgün deyil.</p><a class="primary-button" href="index.html">Ana səhifəyə qayıt</a></div></main>''' + FOOTER + '''<script src="assets/js/site.js" defer></script></body></html>'''
    (ROOT / '404.html').write_text(page, encoding='utf-8')


def main() -> int:
    for filename, page in PAGES.items():
        (ROOT / filename).write_text(shell(filename, page), encoding='utf-8')
    for filename, service in SERVICES.items():
        build_service(filename, service)
    build_404()
    filenames = ['index.html', *PAGES.keys(), *SERVICES.keys()]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE if name == "index.html" else BASE + name}</loc></url>\n' for name in filenames) + '</urlset>\n'
    (ROOT / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n', encoding='utf-8')
    print(f'Built {len(filenames) + 1} HTML pages, sitemap.xml and robots.txt')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
