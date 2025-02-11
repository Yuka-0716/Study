<?php
//(1)アクションファイルの読み込み
require_once './actions/LoginAction.php';
require_once './actions/InputparttimerAction.php' ;

//(2)セッションの開始・再開
session_start();

//(3)ビューデータの準備
$view=array();

//(4)イベントの取得
$event='showLoginPage';

if(isset($_GET['event'])){
  $event=$_GET['event'];
//  var_dump($event);
}

if((!isLoginned())&&($event != 'checkLogin')) $event='showLoginPage';

//(5)イベントに応じたアクションの選択・実行
switch($event){
  case 'logout';
    logout();
  case 'showLoginPage' ;
    require './views/login.phtml';
    break;
  case 'checkLogin';
    $view=checkLogin($view);
  case 'showInputPage';
    $view=prepareInput($view);
    require './views/input.phtml';
    break;
  case 'receiveInput';
    $view=receiveInput($view);
    require './views/confirmInput.phtml';
    break;
  case 'fixInput';
    $view=fixInput($view);
    require './views/savedResult.phtml';
    break;
  default;
    die("イベント($event)は未定義です。");
}
