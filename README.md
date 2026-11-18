# Compaz Finance 網站改版概念

UX CIRCLES 為 Compaz Finance（Lily Liu 創立的房貸與保障經紀，FCA 939072）製作的非官方改版概念網站。
網站頂部有「概念」標示，所有頁面皆設 `noindex`，`robots.txt` 禁止搜尋引擎收錄。

- 英文：`/`　簡體中文：`/sc/`（Lily 以英語及普通話服務，客戶評價亦有簡體中文名字，故採用簡體）
- 頁面：首頁（羅盤試算工具）、Mortgages & protection、About Lily、Contact、Privacy、404

## 如何修改

所有頁面由 `_build/pages.py` 產生，中英文並排寫在 `L(english, 中文)` 裡。

```bash
python3 _build/pages.py   # 重建所有頁面
python3 _build/fonts.py   # 修改中文字後，重新擷取 Noto Sans SC 子集字型
```

修改 CSS/JS 後，請把 `pages.py` 裡的 `V` 加一（快取更新）。

## 設計概念

- **招牌元素：羅盤。** Compaz 的商標本身就是一個橘色羅盤，Lily 的網站也自稱是「mortgage maze 裡的嚮導」。整個網站圍繞羅盤：首頁主視覺的指針、四個服務方位（000° 首套房、090° 轉貸、180° 出租房貸、270° 過橋貸款）、人壽保障放在羅盤中心、流程以航點呈現、favicon、404 頁「偏離航道」。
- **主視覺類型：`tool-first`**（作品集中尚未使用過）。客戶通常帶著問題而來，所以首屏直接是可用的試算：點選方位後，指針轉向，即時算出月供、印花稅、租金覆蓋率或過橋貸款總成本，再一鍵把試算結果帶進聯絡表格。
- **字型：** Red Hat Display（標題，與 Compaz 商標的字形幾乎一致：雙層 a、圓 C、緊密字距，讓標題和 logo 成為同一套字）、Onest（內文）、DM Mono（方位度數與數字，像儀表讀數）；中文 Noto Sans SC。作品集中皆未用過。
- **配色：** 商標的羅盤橘 `#f7931e`、商標字的墨黑 `#17150f`、白色與淺灰。刻意避開前幾個會計/金融網站常用的海軍藍＋米色。
- **標題：** EN「Find your bearing in the mortgage maze」（沿用 Lily 自己的 mortgage maze 說法）；中文「在英国贷款买房，先定方向」。
- **與作品集不同之處：** 不是左文右圖的 split，沒有拱形照片、浮動小卡、數字統計列，標題無斜體或彩色強調字。

## 內容來源

全部來自 compazfinance.co.uk（Index、About、Services 及三個服務細節頁、Contact、privacy），2026-11-17 擷取。
已修正原文的錯字（Mortaging、Indentify、ur），並刪除服務頁中誤貼的註腳數字（如「deal for you12」）。

印花稅計算依 GOV.UK「Residential property rates」（2025年4月1日起：首次購房者 30萬以下免稅、30–50萬 5%；額外房產 +5%；非英國居民 +2%），只適用於英格蘭及北愛爾蘭。

## 需要 Compaz Finance 確認

- 是否要公開電話：官網 Contact 頁把電話 07775 330483 放在 HTML 註解裡隱藏了，所以概念網站完全不顯示電話，只用電郵和留言
- 37 Hillcrest Road, Orpington 是否接待到訪客戶（目前寫「到訪前請先聯絡預約」）
- Lily 的中文名字（網站沒有提供，因此中文版只寫 Lily Liu）
- 「Remortgage」作為獨立服務是否合適（原網站寫在 Mortgaging 內）
- 試算工具中的示例利率（4.5%、5.2%、0.85%/月等）只是可修改的預設值，不是報價
- 隱私頁連到原網站的完整客戶隱私聲明 `/privacy`

沒有使用任何圖庫照片。
