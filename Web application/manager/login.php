<?php
// セッションの開始・再開
session_start();

// ユーザ名とパスワードの設定
$userData = array('shiomi' => '0716');

// ユーザ名とパスワードの入力をチェックし、管理者用修正ページに遷移するかエラーメッセージを表示する
if (isset($_POST['username']) && isset($_POST['password'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];

    if (isset($userData[$username]) && $userData[$username] === $password) {
        $_SESSION['isLoginned'] = true;
        header("Location: manager.html");
        exit();
    } else {
        $errorMessage = "ユーザ名かパスワードが間違っています。";
    }
}
?>

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
        .nav .menu-group {
            list-style: none;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: flex-end;
        }
        .nav .menu-item {
            margin-left: 20px;
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
        .form-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .form-container div {
            margin: 10px 0;
        }
    </style>
    <title>管理者ログイン</title>
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
    <img src='webページテンプレート/images/headder6.png' alt="teruko" width="1500" height="200">
    <h1>管理者ログイン</h1>
    <form action="" method="post" class="form-container">
        <div>
            <label for="username">ユーザ名：</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="password">パスワード：</label>
            <input type="password" id="password" name="password" required><br>
        </div>
        <div>
            <input type="submit" value="ログイン"><br>
        </div>
    </form>
    <?php if (isset($errorMessage)) : ?>
        <p style="color: red;"><?php echo $errorMessage; ?></p>
    <?php endif; ?>
</body>
</html>
