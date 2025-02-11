<?php
$servername = "localhost";  // サーバー名
$username = "root";    // ユーザー名
$password = "";    // パスワード
$dbname = "weawther";      // データベース名

// フォームからのデータを取得
$region = $_POST['region'];
$prefecture = $_POST['prefecture'];
$areaCode = $_POST['areaCode'];

// MySQLデータベースに接続
$conn = new mysqli($servername, $username, $password, $dbname);

// 接続をチェック
if ($conn->connect_error) {
    die("接続失敗: " . $conn->connect_error);
}

// SQL文を作成
$sql = "INSERT INTO regions (region, prefecture, areaCode) VALUES (?, ?, ?)";

// SQLステートメントを準備
$stmt = $conn->prepare($sql);
if ($stmt === false) {
    die("SQLステートメント準備エラー: " . $conn->error);
}

// パラメータをバインド
$stmt->bind_param("sss", $region, $prefecture, $areaCode);

// SQLステートメントを実行
if ($stmt->execute()) {
    echo "データが正常に保存されました";
} else {
    echo "エラー: " . $sql . "<br>" . $stmt->error;
}

// 接続を閉じる
$stmt->close();
$conn->close();

// weather.htmlにリダイレクト
header("Location: weather.html");
exit();

?>
