<?php
//(1)アクションファイルの読み込み。LoginAction.php と InputparttimerAction.php の2つのアクションファイルを読み込む。
//これらのファイルには、各種アクション（関数）が含まれる。

require_once './actions/LoginAction.php';
require_once './actions/InputparttimerAction.php' ;

//(2)セッションの開始・再開
//session_start() 関数を使ってセッションを開始または再開。セッションを使用することで、ユーザのログイン状態などの情報を保持。
session_start();

//(3)ビューデータの準備
//$view という配列を初期化している。
//この配列は、ビュー（HTMLファイル）に渡すデータを格納する。
$view=array();

//(4)イベントの取得
//$_GET['event'] を通じて、URLパラメータからイベントを取得。
//もしevent パラメータがない場合は、showLoginPage イベントをデフォルトとして設定。
$event='showLoginPage';

if(isset($_GET['event'])){
  $event=$_GET['event'];
//  var_dump($event);
}

if((!isLoginned())&&($event != 'checkLogin')) $event='showLoginPage';

//(5)イベントに応じたアクションの選択・実行
//switch-case 文を使用して、取得したイベントに応じてアクションを実行する。

switch($event){
  case 'logout';//logout: ログアウト処理。
    logout();
  case 'showLoginPage' ;//ログインページを表示。
    require './views/login.phtml';
    break;
  case 'checkLogin';//ログイン情報のチェックを行う。
    $view=checkLogin($view);
  case 'showInputPage';// 入力ページを表示。
    $view=prepareInput($view);
    require './views/input.phtml';
    break;
  case 'receiveInput';//入力情報の受け取り処理を行う。
    $view=receiveInput($view);
    require './views/confirmInput.phtml';
    break;
  case 'fixInput';//入力情報の修正処理を行います。
    $view=fixInput($view);
    require './views/savedResult.phtml';
    break;
  default;//未定義のイベントが指定された場合はエラーメッセージを表示
    die("イベント($event)は未定義です。");
}
