## showroom 網頁如何執行
> 在 showroom（最外層資料夾）底下安裝程式檔案內會使用到的套件，如：django、requests、pandas、json 等，基本上在 terminal 執行以下程式皆可成功

    pip install 套件名稱


> 因為程式內部目前主要控制普渡機器人，需開啟 server：PuduRobotOpenServer-win，綠色標誌的檔案，方可獲取普渡機器人資訊

>在 showroom（最外層資料夾）底下執行以下指令，無報錯便會出現網址，點擊即可開啟網頁

    python manage.py runserver

## 新增機器人
> 在網址後打 admin，即可進入後台，輸入以下資料，即可看到後台資料庫

    帳號：joylee
    密碼：10631206lee


> 目前尚未開發上傳機器人照片功能，因此需手動將照片存到 static/Image 資料夾底下，名稱需為 機器人的 name.png

## 網頁邏輯
>可參考 showroom_簡易控制機器網頁.pptx