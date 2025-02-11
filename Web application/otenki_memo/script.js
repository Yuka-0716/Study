$(document).ready(function() {
    // メモデータの配列
    const memos = [
        {
            title: 'お天気めも　 1.ご自愛ください',
            content: '最後に雲を眺めたのはいつですか。たまには空を見上げ、ひと休みしてください。',
            img: 'webページテンプレート/1.png'
        },
        {
            title: 'お天気めも　 2.年平均降水量',
            content: '世界の年平均降水量は約880mmです。日本はその約2倍、1718mmといわれています。日本は雨がたくさん降る国ですね。',
            img: 'webページテンプレート/5.png'
        },
        {
            title: 'お天気めも　 3.地球温暖化のこと、知ってますか',
            content: '地球温暖化により、この100年で地球の温度は100年あたり0.76℃の割合で上昇しています。わずかな量に感じますが、これにより異常気象が頻発し、生物資源が失われています。温室効果ガスの排出を減らし、温度上昇の割合を少しでも小さくしましょう。',
            img: 'webページテンプレート/6.png'
        },
        {
            title: 'お天気めも　　4.温室効果ガスを減らそう',
            content: '地球温暖化をもたらす効果をもつ気体を「温室効果ガス」といいます。代表的なのは二酸化炭素です。温室効果ガスの排出を減らすには、クリーンエネルギーを利用する等、世界規模で精力的に取り組む必要があります。',
            img: 'webページテンプレート/3.png'
        },
        {
            title: 'お天気めも 　5.ゲリラ豪雨に注意',
            content: 'ゲリラ豪雨という言葉は、実は専門用語ではありません。マスコミで使われたことをきたことを機に広まりました。これからの季節、急な大雨に気を付けていきましょう。',
            img: 'webページテンプレート/4.png'
        }
    ];

    // ページが読み込まれたときにメモを表示する
    function displayMemos() {
        $('#memos').empty();
        memos.forEach((memo, index) => {
            $('#memos').append(`
                <div class="memo">
                    <h2>${memo.title}</h2>
                    <p>${memo.content}</p>
                    <img src="${memo.img}" alt="${memo.title}">
                    <br>
                    <a href="confirm.html?index=${index}">内容を編集する</a>
                </div>
            `);
        });
        // ローカルストレージにメモデータを保存
        localStorage.setItem('memos', JSON.stringify(memos));
    }

    // メモの内容をローカルストレージから取得して更新する
    function updateMemoFromLocalStorage() {
        const confirmedMemo = JSON.parse(localStorage.getItem('confirmedMemo'));
        if (confirmedMemo) {
            const index = confirmedMemo.index;
            if (index !== undefined && index >= 0 && index < memos.length) {
                memos[index] = confirmedMemo;
            }
            localStorage.removeItem('confirmedMemo');
            displayMemos();
        }
    }

    // 初期表示
    displayMemos();
    updateMemoFromLocalStorage();
});
