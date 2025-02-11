<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="webページテンプレート/CSS/style.css">
    <link rel="stylesheet" type="text/css" href="webページテンプレート/CSS/keyframes.css">
    <link rel="stylesheet" type="text/css" href="webページテンプレート/CSS/slide.css">
    <link rel="shortcut icon" type="image/png" href="webページテンプレート/images/terukologo.jpg">
    <link rel="stylesheet" href="webページテンプレート/CSS/headerstyle.css">
    <style>
        body {
            /* 背景画像の設定 */
            background-image: url('webページテンプレート/images_photo/1.jpg');
            /* 画像を中央に配置し、背景サイズをカバー */
            background-position: center;
            background-size: cover;
            /* 背景のスクロールを固定 */
            background-attachment: fixed;
            /* コンテンツの中央揃え */
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: start;
            height: 100%;
            margin: 0;
        }
        header, nav {
            width: 100%;
            text-align: right;
        }
        .content {
            text-align: center;
            width: 80%;
            max-width: 1200px;
            margin: 20px auto;
            /* 背景を透過させる */
            background: rgba(255, 255, 255, 0.0);
            padding: 20px;
            border-radius: 8px;
        }
        table {
            margin: auto;
        }
    </style>
    <title>結果一覧</title>
</head>
<body>
    <header>
        <img src='webページテンプレート/images/terukologo.jpg' alt="teruko" width="50" height="50">
        <h1 class="title">Teruko</h1>
        <nav class="nav">
            <ul class="menu-group">
                <li class="menu-item"><a href="input.html">HOME</a></li>
                <li class="menu-item"><a href="showall.php">結果一覧</a></li>
                <li class="menu-item"><a href="introduce.html">アプリの紹介</a></li>
                <li class="menu-item"><a href="login.php">管理者ログイン</a></li>
            </ul>
        </nav>
    </header>
    <body>
    <img src='webページテンプレート/images/headder6.png' alt=”teruko” width="1500" height="200">
        <style>
            h2{
            clear: both;
	        margin-bottom: 50px;	/*下に空けるスペース*/
	        font-size: 1.5rem;		/*文字サイズ。冒頭で指定しているフォントサイズの2.25倍です。*/
	        text-align: center;		/*文字をセンタリング*/
	        letter-spacing: 0.1em;
            color: rgb(111, 20, 70); /* タイトルの色を赤色にする */
        }
        </style>
    <div class="content">
        <?php
        // データベース接続設定
        $host = 'localhost';
        $dbname = 'phpmysql';
        $username = 'root';
        $password = '';

        try {
            // PDO インスタンスを作成してデータベースに接続
            $dsn = "mysql:host=$host;dbname=$dbname;charset=utf8";
            $pdo = new PDO($dsn, $username, $password);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

            // SQL クエリを準備
            $sql = "SELECT prefecture, COUNT(*) AS count FROM weather GROUP BY prefecture";

            // クエリを実行
            $stmt = $pdo->query($sql);

            // 結果を取得
            $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

            if ($results) {
                echo "<h2>都道府県ごとの検索回数</h2>";
                echo "<canvas id='barChart' width='400' height='200'></canvas>";
                echo "<script src='https://cdn.jsdelivr.net/npm/chart.js'></script>";
                echo "<script>";
                echo "var ctx = document.getElementById('barChart').getContext('2d');";
                echo "var myChart = new Chart(ctx, {";
                echo "    type: 'bar',";
                echo "    data: {";
                echo "        labels: [";
                foreach ($results as $row) {
                    echo "'" . htmlspecialchars($row['prefecture']) . "',";
                }
                echo "        ],";
                echo "        datasets: [{";
                echo "            label: '検索回数',";
                echo "            data: [";
                foreach ($results as $row) {
                    echo $row['count'] . ",";
                }
                echo "            ],";
                echo "            backgroundColor: 'rgba(255, 99, 132, 0.2)',";
                echo "            borderColor: 'rgba(255, 99, 132, 1)',";
                echo "            borderWidth: 1";
                echo "        }]";
                echo "    },";
                echo "    options: {";
                echo "        scales: {";
                echo "            y: {";
                echo "                beginAtZero: true";
                echo "            }";
                echo "        }";
                echo "    }";
                echo "});";
                echo "</script>";

                // 詳細データを表示
                echo "<h2>詳細データ</h2>";
                echo "<table border='1'>";
                echo "<tr><th>地方</th><th>都道府県</th></tr>";
                $sql_detail = "SELECT region, prefecture FROM weather";
                $stmt_detail = $pdo->query($sql_detail);
                $results_detail = $stmt_detail->fetchAll(PDO::FETCH_ASSOC);
                foreach ($results_detail as $row_detail) {
                    echo "<tr>";
                    echo "<td>" . htmlspecialchars($row_detail['region']) . "</td>";
                    echo "<td>" . htmlspecialchars($row_detail['prefecture']) . "</td>";
                    echo "</tr>";
                }
                echo "</table>";
                
                // 入力画面に戻るボタン
                echo "<br>";
                echo "<form action='input.html'>";
                echo "<input type='submit' value='入力画面に戻る'>";
                echo "</form>";
                echo "<br>";

            } else {
                echo "データが見つかりません。";
            }

        } catch (PDOException $e) {
            echo "データベース接続エラー: " . $e->getMessage();
        }

        // 接続を閉じる
        $pdo = null;
        ?>
    </div>
</body>
</html>
