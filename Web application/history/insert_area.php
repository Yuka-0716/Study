<?php
// データベース接続設定
$host = 'localhost';
$dbname = 'phpmysql';
$username = 'root';
$password = '';

try {
    // POSTデータを受け取る
    $region = isset($_POST['region']) ? $_POST['region'] : null;
    $prefecture = isset($_POST['prefecture']) ? $_POST['prefecture'] : null;
    $areaCode = isset($_POST['areaCode']) ? $_POST['areaCode'] : null;

    // データベースに接続
    $dsn = "mysql:host=$host;dbname=$dbname;charset=utf8";
    $pdo = new PDO($dsn, $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // SQL 挿入クエリを準備
    $sql = "INSERT INTO weather (region, prefecture, areaCode) VALUES (:region, :prefecture, :areaCode)";

    // クエリを準備し、パラメータをバインド
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':region', $region);
    $stmt->bindParam(':prefecture', $prefecture);
    $stmt->bindParam(':areaCode', $areaCode);

    // クエリを実行してデータを挿入
    $stmt->execute();

    // データの挿入が成功したらリダイレクト
    header("Location: weather.html?areaCode=$areaCode");
    exit();

} catch (PDOException $e) {
    echo "エラー: " . $e->getMessage();
}
?>
