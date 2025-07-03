from bs4 import BeautifulSoup

html = '''<select name="staffId" id="stylistId" class="w207"><option value="">すべてのスタッフ</option><option value="W001035204">宅万　明日香</option>
<option value="W001199864">八谷　実希</option>
<option value="W001165576">佐藤　恵子</option>
<option value="W001165577">小川　真里奈</option>
<option value="W001170136">浜野　遥香</option>
<option value="W001230763">松井　佑季</option>
<option value="W001165580">五嶋　優磨</option>
<option value="W001165582">佐藤　愛莉</option>
<option value="W001165585">山中　美玲</option>
<option value="W001183246">岡本　祥吾</option>
<option value="W000813709">大出　菜摘</option>
<option value="W000811178">川島　悠希</option>
<option value="W001230768">志田　愛佳</option></select>'''

soup = BeautifulSoup(html, 'html.parser')
options = soup.select('select#stylistId option')

for option in options:
    value = option.get('value').strip()
    name = option.get_text(strip=True)
    if value:  # skip "すべてのスタッフ"
        print(f"{value}\t{name}")
